from __future__ import annotations

from dataclasses import dataclass
import uuid

from .audit import QiyasAudit
from .candidate import Candidate, CandidateSet
from .enums import CandidateStatus, EvidenceRank, ResidualEffect, ResidualSeverity
from .evidence import EvidenceSet
from .node import QiyasNodeRef
from .residual import Residual
from .rule import QiyasRule


@dataclass(frozen=True)
class QiyasContext:
    layer: str
    input_span: tuple[int, int] | None = None
    maqam: str | None = None
    available_slots: tuple[str, ...] = ()
    reference_stack: tuple[str, ...] = ()
    previous_candidate_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class QiyasRequest:
    rule: QiyasRule
    asl: QiyasNodeRef
    far: QiyasNodeRef
    evidence: EvidenceSet
    context: QiyasContext


def residual(
    request: QiyasRequest,
    residual_type: str,
    message: str,
    effect: ResidualEffect,
    trace_ids: tuple[str, ...],
    severity: ResidualSeverity | None = None,
) -> Residual:
    if severity is None:
        severity = (
            ResidualSeverity.BLOCKER
            if effect == ResidualEffect.BLOCK
            else ResidualSeverity.WARNING
        )

    return Residual(
        residual_type=residual_type,
        severity=severity,
        effect=effect,
        message=message,
        source_rule_id=request.rule.rule_id,
        layer=request.rule.layer,
        trace_ids=trace_ids,
    )


WADI_REQUIRED_CLAIMS = {
    "sabab": "wadi:sabab:established",
    "shart": "wadi:shart:satisfied",
    "mani": "wadi:mani:absent",
    "sihha": "wadi:sihha:valid",
    "fasad": "wadi:fasad:absent",
    "butlan": "wadi:butlan:absent",
}


class QiyasKernel:
    def __init__(self, *, fail_fast: bool = False) -> None:
        self.fail_fast = fail_fast

    def apply(self, request: QiyasRequest) -> CandidateSet:
        audit = QiyasAudit.empty()

        checks = (
            self._check_context_layer,
            self._check_node_types,
            self._check_asl_established,
            self._check_far_determined,
            self._check_effective_wasf,
            self._check_illah,
            self._check_wadi,
            self._check_fariq,
            self._check_identity,
            self._check_rank,
            self._check_forbidden_outputs_declared,
        )

        for check in checks:
            audit = check(request, audit)
            if audit.blocked and self.fail_fast:
                break

        if audit.blocked:
            return self._make_candidate_set(request, audit, CandidateStatus.BLOCKED)

        if audit.deferred:
            return self._make_candidate_set(request, audit, CandidateStatus.DEFERRED)

        return self._make_candidate_set(request, audit, CandidateStatus.ACCEPTED)

    def _check_context_layer(self, request: QiyasRequest, audit: QiyasAudit) -> QiyasAudit:
        if request.context.layer != request.rule.layer:
            return audit.add_residual(
                residual(
                    request,
                    "context_layer_mismatch",
                    "سياق الطلب لا يطابق طبقة القاعدة.",
                    ResidualEffect.BLOCK,
                    request.evidence.all_trace_ids(),
                )
            )
        return audit

    def _check_node_types(self, request: QiyasRequest, audit: QiyasAudit) -> QiyasAudit:
        if request.asl.node_type != request.rule.asl_type:
            audit = audit.add_residual(
                residual(
                    request,
                    "asl_type_mismatch",
                    "نوع الأصل لا يطابق نوع الأصل في القاعدة.",
                    ResidualEffect.BLOCK,
                    request.asl.trace_ids,
                )
            )

        if request.far.node_type != request.rule.far_type:
            audit = audit.add_residual(
                residual(
                    request,
                    "far_type_mismatch",
                    "نوع الفرع لا يطابق نوع الفرع في القاعدة.",
                    ResidualEffect.BLOCK,
                    request.far.trace_ids,
                )
            )

        return audit

    def _check_asl_established(self, request: QiyasRequest, audit: QiyasAudit) -> QiyasAudit:
        if not request.evidence.proves("asl:established"):
            return audit.add_residual(
                residual(
                    request,
                    "asl_not_established",
                    "الأصل غير ثابت بدليل.",
                    ResidualEffect.BLOCK,
                    request.asl.trace_ids,
                )
            )
        return audit

    def _check_far_determined(self, request: QiyasRequest, audit: QiyasAudit) -> QiyasAudit:
        if not request.evidence.proves("far:determined"):
            return audit.add_residual(
                residual(
                    request,
                    "far_not_determined",
                    "الفرع غير متعين.",
                    ResidualEffect.BLOCK,
                    request.far.trace_ids,
                )
            )
        return audit

    def _check_effective_wasf(self, request: QiyasRequest, audit: QiyasAudit) -> QiyasAudit:
        for wasf in request.rule.required_effective_wasf:
            claim = f"wasf:{wasf}:evidenced"
            if not request.evidence.proves(claim):
                audit = audit.add_residual(
                    residual(
                        request,
                        "effective_wasf_missing",
                        f"الوصف المؤثر غير مثبت: {wasf}",
                        ResidualEffect.BLOCK,
                        request.evidence.all_trace_ids(),
                    )
                )
        return audit

    def _check_illah(self, request: QiyasRequest, audit: QiyasAudit) -> QiyasAudit:
        for illah in request.rule.required_illah:
            claim = f"illah:{illah}:verified"
            if not request.evidence.proves(claim):
                audit = audit.add_residual(
                    residual(
                        request,
                        "shared_illah_missing",
                        f"العلة الجامعة غير متحققة: {illah}",
                        ResidualEffect.BLOCK,
                        request.evidence.all_trace_ids(),
                    )
                )
        return audit

    def _check_wadi(self, request: QiyasRequest, audit: QiyasAudit) -> QiyasAudit:
        for gate in request.rule.required_wadi_gates:
            claim = WADI_REQUIRED_CLAIMS[gate.value]
            if not request.evidence.proves(claim):
                audit = audit.add_residual(
                    residual(
                        request,
                        f"wadi_{gate.value}_failed",
                        f"حكم الوضع لم يمر: {gate.value}",
                        ResidualEffect.BLOCK,
                        request.evidence.all_trace_ids(),
                    )
                )
        return audit

    def _check_fariq(self, request: QiyasRequest, audit: QiyasAudit) -> QiyasAudit:
        for diff in request.rule.invalidating_differences:
            if request.evidence.proves(f"fariq:{diff}:present"):
                audit = audit.add_residual(
                    residual(
                        request,
                        "blocking_fariq_present",
                        f"وجد فارق قادح: {diff}",
                        ResidualEffect.BLOCK,
                        request.evidence.all_trace_ids(),
                    )
                )
        return audit

    def _check_identity(self, request: QiyasRequest, audit: QiyasAudit) -> QiyasAudit:
        identities = set(request.asl.identity_ids + request.far.identity_ids)
        traces = set(request.asl.trace_ids + request.far.trace_ids)

        if not identities:
            return audit.add_residual(
                residual(
                    request,
                    "identity_missing",
                    "لا توجد هوية محفوظة للأصل والفرع.",
                    ResidualEffect.BLOCK,
                    request.asl.trace_ids + request.far.trace_ids,
                )
            )

        if identities & traces:
            return audit.add_residual(
                residual(
                    request,
                    "identity_trace_conflict",
                    f"اختلاط identity مع trace: {sorted(identities & traces)}",
                    ResidualEffect.BLOCK,
                    request.asl.trace_ids + request.far.trace_ids,
                )
            )

        return audit

    def _check_rank(self, request: QiyasRequest, audit: QiyasAudit) -> QiyasAudit:
        ceiling = min(
            request.rule.rank_ceiling,
            request.asl.rank,
            request.far.rank,
            request.evidence.minimum_rank(),
            key=lambda r: r.value,
        )

        if ceiling == EvidenceRank.ZERO:
            return audit.add_residual(
                residual(
                    request,
                    "rank_zero",
                    "سقف الرتبة صفر.",
                    ResidualEffect.BLOCK,
                    request.evidence.all_trace_ids(),
                )
            )

        return audit.with_rank_ceiling(ceiling)

    def _check_forbidden_outputs_declared(
        self,
        request: QiyasRequest,
        audit: QiyasAudit,
    ) -> QiyasAudit:
        required = {"HukmCandidate", "RealityClaim", "FinalMeaning"}

        if not required.issubset(set(request.rule.forbidden_outputs)):
            return audit.add_residual(
                residual(
                    request,
                    "forbidden_outputs_incomplete",
                    "القاعدة لا تمنع الحكم أو الواقع أو المعنى النهائي صراحة.",
                    ResidualEffect.BLOCK,
                    request.evidence.all_trace_ids(),
                )
            )

        return audit

    def _make_candidate_set(
        self,
        request: QiyasRequest,
        audit: QiyasAudit,
        status: CandidateStatus,
    ) -> CandidateSet:
        rank = audit.rank_ceiling or EvidenceRank.ZERO

        if status != CandidateStatus.ACCEPTED:
            rank = EvidenceRank.ZERO

        candidate = Candidate(
            candidate_id=f"{status.value}:{request.rule.layer}:{uuid.uuid4().hex[:12]}",
            candidate_type=request.rule.output_candidate_type,
            status=status,
            layer=request.rule.layer,
            source_rule_id=request.rule.rule_id,
            asl_id=request.asl.node_id,
            far_id=request.far.node_id,
            identity_ids=request.asl.identity_ids + request.far.identity_ids,
            rank=rank,
            residuals=audit.residuals,
            trace_ids=request.asl.trace_ids
            + request.far.trace_ids
            + request.evidence.all_trace_ids()
            + audit.trace_ids,
            output_flags=frozenset({"CandidateOnly"}),
        )

        self._validate_output(request, candidate)

        return CandidateSet(
            set_id=f"set:{candidate.candidate_id}",
            layer=request.rule.layer,
            candidates=(candidate,),
            residuals=audit.residuals,
            trace_ids=candidate.trace_ids,
        )

    def _validate_output(self, request: QiyasRequest, candidate: Candidate) -> None:
        required_identity = set(request.asl.identity_ids + request.far.identity_ids)

        if not required_identity.issubset(set(candidate.identity_ids)):
            raise ValueError("Candidate lost source identities.")

        if candidate.output_flags & set(request.rule.forbidden_outputs):
            raise ValueError("Candidate produced forbidden output.")
