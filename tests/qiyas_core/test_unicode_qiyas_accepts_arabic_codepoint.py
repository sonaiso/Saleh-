from qiyas_core.enums import CandidateStatus, EvidenceRank
from qiyas_core.evidence import Evidence, EvidenceSet
from qiyas_core.kernel import QiyasContext, QiyasKernel, QiyasRequest
from qiyas_core.node import QiyasNodeRef
from qiyas_core.rules.unicode_rules import UNICODE_ARABIC_MEMBERSHIP


def test_unicode_qiyas_accepts_arabic_codepoint():
    asl = QiyasNodeRef(
        node_id="asl:arabic_unicode_block",
        node_type="ArabicUnicodeBlock",
        identity_ids=("identity:arabic_unicode_block",),
        trace_ids=("trace:asl",),
        rank=EvidenceRank.FORM,
    )

    far = QiyasNodeRef(
        node_id="far:0628",
        node_type="InputCodepoint",
        identity_ids=("identity:codepoint:0628",),
        trace_ids=("trace:far",),
        rank=EvidenceRank.FORM,
    )

    evidence = EvidenceSet(
        items=(
            Evidence(
                evidence_id="ev:unicode:0628",
                source_layer="UnicodeQiyas",
                proves=(
                    "asl:established",
                    "far:determined",
                    "wasf:unicode_codepoint_in_arabic_range:evidenced",
                    "illah:belongs_to_arabic_script_domain:verified",
                    "wadi:sabab:established",
                    "wadi:shart:satisfied",
                    "wadi:mani:absent",
                    "wadi:sihha:valid",
                    "wadi:fasad:absent",
                    "wadi:butlan:absent",
                ),
                rank=EvidenceRank.FORM,
                trace_ids=("trace:ev",),
            ),
        )
    )

    request = QiyasRequest(
        rule=UNICODE_ARABIC_MEMBERSHIP,
        asl=asl,
        far=far,
        evidence=evidence,
        context=QiyasContext(layer="UnicodeQiyas"),
    )

    result = QiyasKernel().apply(request)

    assert len(result.accepted) == 1
    assert result.accepted[0].status == CandidateStatus.ACCEPTED
    assert result.accepted[0].candidate_type == "UnicodeCandidate"
    assert result.accepted[0].rank == EvidenceRank.FORM
