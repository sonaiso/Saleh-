"""
Constitutional Guard: LCNV Inverse Law

This test prevents regression to the incorrect formulation that
Unpack(Pack(x)) = x, which would violate Candidate primacy.

Constitutional basis:
- docs/qiyas_core/LAYERED_COMPRESSED_NUMERIC_VALUE_ARCHITECTURE.md (Law 1, Law 7)
- Candidate is source of authority, LCNV is compressed trace
- Trace does not become origin, number does not produce knowledge

الأثر لا يصبح أصلًا.
والرقم لا ينتج معرفة.
"""

from pathlib import Path


def test_lcnv_inverse_law_does_not_claim_candidate_authority():
    """
    Guard against regression to incorrect LCNV inverse law.

    FORBIDDEN formulations that violate Candidate primacy:
    - "Unpack(Pack(x)) = x" (without qualification)
    - "Unpack(LCNV(c)) = c" (suggesting full Candidate restoration)
    - "reconstruct full Candidate" (from unpack alone)
    - "Unpack(LCNV) -> Candidate" (direct authority restoration)

    REQUIRED formulations:
    - "Unpack(Pack(c)) = EncodedStateProjection(c)"
    - "Unpack(Pack(c)) ≠ Candidate(c)"
    - "CandidateAuthority requires Validate + Stores"

    Constitutional principle:
    LCNV is reversible within projection bounds,
    NOT reversible within epistemological authority bounds.
    """
    doc_path = Path(__file__).parent.parent.parent / "docs" / "qiyas_core" / "LAYERED_COMPRESSED_NUMERIC_VALUE_ARCHITECTURE.md"

    assert doc_path.exists(), f"LCNV architecture document not found: {doc_path}"

    text = doc_path.read_text(encoding="utf-8")

    # Forbidden formulations that violate Candidate primacy
    forbidden_patterns = [
        # Simple reversibility without qualification
        ("Unpack(Pack(x)) = x", "Simple reversibility claim"),

        # Direct Candidate restoration without stores
        ("Unpack(LCNV(c)) = c", "Direct Candidate restoration"),

        # Claims of full reconstruction without validation
        ("reconstruct full Candidate", "Full reconstruction claim"),
        ("restore full Candidate", "Full restoration claim"),
        ("return full Candidate", "Full return claim"),

        # Equivalence claims that violate authority bounds
        ("Unpack = inverse of Pack", "Unqualified inverse claim"),
        ("lossless reversibility", "Lossless reversibility claim"),
    ]

    violations = []
    for phrase, description in forbidden_patterns:
        if phrase in text:
            violations.append((phrase, description))

    assert not violations, (
        f"LCNV inverse law regression detected. "
        f"Forbidden phrases found in document: {violations}\n\n"
        f"Constitutional violation: These formulations suggest LCNV can restore "
        f"full CandidateAuthority, violating the principle that Candidate is "
        f"source of truth and LCNV is compressed trace.\n\n"
        f"Correct formulation:\n"
        f"  Unpack(Pack(c)) = EncodedStateProjection(c), NOT Candidate(c)\n"
        f"  CandidateAuthority requires Validate(EncodedStateProjection + Stores)\n\n"
        f"الأثر لا يصبح أصلًا. والرقم لا ينتج معرفة.\n"
        f"(Trace does not become origin. Number does not produce knowledge.)"
    )


def test_lcnv_inverse_law_includes_required_formulations():
    """
    Verify the document contains the correct LCNV inverse law formulation.

    Required formulations established in PR #52:
    1. Unpack(Pack(c)) = EncodedStateProjection(c)
    2. Unpack(Pack(c)) ≠ Candidate(c)
    3. CandidateAuthority restoration formula with stores
    4. Forbidden derivations from Unpack(LCNV)
    5. Governing principle in Arabic and English
    """
    doc_path = Path(__file__).parent.parent.parent / "docs" / "qiyas_core" / "LAYERED_COMPRESSED_NUMERIC_VALUE_ARCHITECTURE.md"

    assert doc_path.exists(), f"LCNV architecture document not found: {doc_path}"

    text = doc_path.read_text(encoding="utf-8")

    # Required formulations
    required = [
        # Core inverse law
        "EncodedStateProjection",
        "Unpack(Pack(c)) ≠ Candidate(c)",

        # Authority restoration requirement
        "CandidateAuthority",
        "CandidateStore",
        "EvidenceStore",
        "TraceStore",
        "ResidualStore",
        "Validate",

        # Forbidden derivations
        "Unpack(LCNV) ⇏ CandidateAuthority",
        "Unpack(LCNV) ⇏ Meaning",
        "Unpack(LCNV) ⇏ Hukm",

        # Constitutional principle
        "reversible within projection bounds",
        "NOT reversible within epistemological authority bounds",

        # Governing principle in Arabic
        "Candidate هو مصدر السلطة",
        "LCNV أثر مضغوط",
        "الأثر لا يصبح أصلًا",
        "والرقم لا ينتج معرفة",
    ]

    missing = []
    for phrase in required:
        if phrase not in text:
            missing.append(phrase)

    assert not missing, (
        f"LCNV inverse law correction incomplete. "
        f"Required formulations missing: {missing}\n\n"
        f"The document must include the corrected inverse law established in PR #52.\n"
        f"See docs/qiyas_core/LAYERED_COMPRESSED_NUMERIC_VALUE_ARCHITECTURE.md Law 1 and Law 7."
    )


def test_lcnv_document_version_reflects_correction():
    """
    Verify document version was updated to reflect the inverse law correction.

    Version 1.0: Incorrect "Unpack(Pack(x)) = x"
    Version 2.0: Correct "Unpack(Pack(c)) = EncodedStateProjection(c)"
    """
    doc_path = Path(__file__).parent.parent.parent / "docs" / "qiyas_core" / "LAYERED_COMPRESSED_NUMERIC_VALUE_ARCHITECTURE.md"

    assert doc_path.exists(), f"LCNV architecture document not found: {doc_path}"

    text = doc_path.read_text(encoding="utf-8")

    # Version should be 2.0 or higher
    assert "**Document Version:** 2.0" in text or "**Document Version:** 2." in text, (
        "Document version must be 2.0 or higher to reflect LCNV inverse law correction."
    )

    # Should mention the correction
    assert "LCNV Inverse Law corrected" in text or "inverse law" in text.lower(), (
        "Document should mention the LCNV inverse law correction in its status or metadata."
    )


def test_lcnv_law_7_exists():
    """
    Verify Law 7 (Forbidden Derivations) exists in the document.

    Law 7 establishes explicit forbidden derivations from Unpack(LCNV),
    preventing numeric encoding from becoming source of authority.
    """
    doc_path = Path(__file__).parent.parent.parent / "docs" / "qiyas_core" / "LAYERED_COMPRESSED_NUMERIC_VALUE_ARCHITECTURE.md"

    assert doc_path.exists(), f"LCNV architecture document not found: {doc_path}"

    text = doc_path.read_text(encoding="utf-8")

    # Law 7 should exist
    assert "### Law 7:" in text or "Law 7:" in text, (
        "Law 7 (Forbidden Derivations from Unpack(LCNV)) must exist in the document."
    )

    # Should contain the forbidden derivations
    assert "Forbidden Derivations" in text, (
        "Law 7 must be titled with 'Forbidden Derivations'."
    )
