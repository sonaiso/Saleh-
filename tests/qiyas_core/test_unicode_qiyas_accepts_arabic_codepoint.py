from qiyas_core.enums import CandidateStatus, EvidenceRank
from qiyas_core.evidence import Evidence, EvidenceSet
from qiyas_core.kernel import QiyasContext, QiyasKernel, QiyasRequest
from qiyas_core.node import QiyasNodeRef
from qiyas_core.rules.unicode_rules import UNICODE_ARABIC_MEMBERSHIP


def test_unicode_qiyas_accepts_arabic_codepoint():
    asl = QiyasNodeRef(
        node_id="اصل:arabic_unicode_block",
        node_type="ArabicUnicodeBlock",
        identity_ids=("identity:arabic_unicode_block",),
        trace_ids=("trace:asl",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
    )

    far = QiyasNodeRef(
        node_id="فرع:0628",
        node_type="InputCodepoint",
        identity_ids=("identity:codepoint:0628",),
        trace_ids=("trace:far",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
    )

    evidence = EvidenceSet(
        items=(
            Evidence(
                evidence_id="ev:unicode:0628",
                source_layer="UnicodeQiyas",
                proves=(
                    "اصل:established",
                    "فرع:determined",
                    "وصف:unicode_codepoint_in_arabic_range:evidenced",
                    "علة:belongs_to_arabic_script_domain:verified",
                    "وادي:cause:established",
                    "وادي:condition:satisfied",
                    "وادي:obstacle:absent",
                    "وادي:validity:valid",
                    "وادي:corruption:absent",
                    "وادي:nullity:absent",
                ),
                rank=EvidenceRank.FORMAL_STRUCTURE,
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
    assert result.accepted[0].rank == EvidenceRank.FORMAL_STRUCTURE
