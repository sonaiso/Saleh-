"""Request factories for constitutional tests."""

from qiyas_core.enums import EvidenceRank
from qiyas_core.evidence import EvidenceSet
from qiyas_core.kernel import QiyasContext, QiyasRequest
from qiyas_core.node import QiyasNodeRef
from qiyas_core.rule import QiyasRule

from .nodes import make_unicode_node, make_haraka_node
from .evidence import make_evidence_set, make_valid_wadi_evidence
from .rules import make_minimal_rule


def make_qiyas_request(
    rule: QiyasRule | None = None,
    asl: QiyasNodeRef | None = None,
    far: QiyasNodeRef | None = None,
    evidence: EvidenceSet | None = None,
    *,
    layer: str | None = None,
) -> QiyasRequest:
    """Create a constitutionally valid QiyasRequest.

    Args:
        rule: QiyasRule to use (creates minimal rule if None)
        asl: Asl node (creates unicode node if None)
        far: Far node (creates haraka node if None)
        evidence: Evidence set (creates complete evidence if None)
        layer: Layer name (uses rule.layer if None)

    Returns:
        QiyasRequest ready for kernel execution
    """
    if rule is None:
        rule = make_minimal_rule()

    if asl is None:
        asl = make_unicode_node(
            node_id="اصل:test",
            identity_ids=("id:asl:test",),
        )

    if far is None:
        far = make_haraka_node(
            node_id="فرع:test",
            identity_ids=("id:far:test",),
        )

    if evidence is None:
        # Create complete evidence with all required claims
        evidence = make_evidence_set(
            "اصل:established",
            "فرع:determined",
            "وصف:test_wasf:evidenced",
            "علة:test_illah:verified",
            "وادي:cause:established",
            "وادي:condition:satisfied",
            "وادي:obstacle:absent",
            "وادي:validity:valid",
            "وادي:corruption:absent",
            "وادي:nullity:absent",
            evidence_id="ev:complete",
            source_layer=rule.layer,
        )

    context_layer = layer if layer is not None else rule.layer

    return QiyasRequest(
        rule=rule,
        asl=asl,
        far=far,
        evidence=evidence,
        context=QiyasContext(layer=context_layer),
    )


def make_request_with_evidence(
    *claims: str,
    evidence_id: str = "ev:custom",
    rule: QiyasRule | None = None,
    rank: EvidenceRank = EvidenceRank.ANALOGICAL,
) -> QiyasRequest:
    """Create a QiyasRequest with specific evidence claims.

    Args:
        *claims: Evidence claims to include
        evidence_id: Evidence identifier
        rule: QiyasRule to use (creates minimal rule if None)
        rank: Evidence rank

    Returns:
        QiyasRequest with the specified evidence claims
    """
    if rule is None:
        rule = make_minimal_rule()

    evidence = make_evidence_set(
        *claims,
        evidence_id=evidence_id,
        source_layer=rule.layer,
        rank=rank,
    )

    return make_qiyas_request(
        rule=rule,
        evidence=evidence,
    )
