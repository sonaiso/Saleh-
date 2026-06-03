"""
Constitutional Document Safety Guard Tests

Purpose: Prevent regression of constitutionally unsafe formulations in docs.

Governing Law: لا وثيقة سلطوية بلا حارس (No authoritative document without a guard)

These tests enforce:
1. LCNV docs don't claim authoritative Candidate reconstruction
2. Required safe formulations are present
3. Future PR references are valid or marked speculative
4. Doc-code consistency (no non-existent APIs)

Authority: PR_1_49_AUTHORITY_AUDIT.md § 3.1 (Law 1: No Authoritative Document Without Guard)
"""

from pathlib import Path
import re


def test_lcnv_docs_do_not_claim_authoritative_candidate_reconstruction():
    """
    Guard against constitutionally unsafe LCNV formulations.

    Prevents PR #44 regression: `Unpack(Pack(x)) = x` violates Candidate primacy.

    FORBIDDEN formulations imply LCNV can reconstruct full Candidate independently,
    making LCNV source of truth instead of Candidate/Evidence/Trace stores.

    REQUIRED formulations enforce store-based reconstruction.

    Authority: INVERSE_EXTRACTION_AND_LOGARITHMIC_MEASUREMENT_LAW.md § 0.1, § 1.3
    """
    lcnv_doc_path = Path("docs/qiyas_core/LAYERED_COMPRESSED_NUMERIC_VALUE_ARCHITECTURE.md")
    assert lcnv_doc_path.exists(), f"LCNV doc not found at {lcnv_doc_path}"

    text = lcnv_doc_path.read_text()

    # FORBIDDEN: Formulations that violate Candidate primacy
    forbidden_patterns = [
        # Direct equality implies LCNV = Candidate authority
        "Unpack(Pack(x)) = x",
        "Unpack(LCNV(c)) = c",

        # Function signatures that return Candidate directly from LCNV
        "def unpack(lcnv: LCNV) -> Candidate",
        "unpack(lcnv: LCNV) -> Candidate",

        # Claims of full reconstruction without stores
        "reconstruct full Candidate",
        "Original candidate with full",

        # False PR reference (PR #45 is CTS tokenizer, not inverse law)
        "PR #45",  # Any mention should be removed or corrected
    ]

    violations = []
    for pattern in forbidden_patterns:
        if pattern in text:
            # Get context around violation for debugging
            idx = text.find(pattern)
            context_start = max(0, idx - 100)
            context_end = min(len(text), idx + 100)
            context = text[context_start:context_end]
            violations.append(f"FORBIDDEN pattern '{pattern}' found:\n{context}\n")

    assert not violations, (
        f"Constitutional violations found in LCNV doc:\n" + "\n".join(violations) +
        "\n\nThese formulations violate Candidate primacy (Candidate = source of truth, LCNV = encoding only).\n"
        "See INVERSE_EXTRACTION_AND_LOGARITHMIC_MEASUREMENT_LAW.md for correct formulations."
    )


def test_lcnv_docs_contain_required_safe_formulations():
    """
    Guard for required safe formulations in LCNV docs.

    REQUIRED formulations enforce:
    - Unpack returns EncodedCandidateStateProjection (not Candidate)
    - Full reconstruction requires stores (CandidateStore, EvidenceStore, TraceStore)
    - LCNV is encoding only, not source of truth

    Authority: INVERSE_EXTRACTION_AND_LOGARITHMIC_MEASUREMENT_LAW.md § 0.2, § 1.2
    """
    lcnv_doc_path = Path("docs/qiyas_core/LAYERED_COMPRESSED_NUMERIC_VALUE_ARCHITECTURE.md")
    assert lcnv_doc_path.exists(), f"LCNV doc not found at {lcnv_doc_path}"

    text = lcnv_doc_path.read_text()

    # REQUIRED: Safe formulations that preserve Candidate primacy
    required_patterns = [
        # Correct return type from Unpack
        "EncodedCandidateStateProjection",

        # Store requirements
        "CandidateStore",
        "EvidenceStore",
        "TraceStore",

        # Explicit statement of LCNV role
        "encoding of gate states",
        "NOT source of truth",

        # Reference to governing law
        "INVERSE_EXTRACTION_AND_LOGARITHMIC_MEASUREMENT_LAW",
    ]

    missing = []
    for pattern in required_patterns:
        if pattern not in text:
            missing.append(pattern)

    assert not missing, (
        f"Required safe formulations MISSING from LCNV doc:\n" + "\n".join(missing) +
        "\n\nThese formulations are MANDATORY to preserve Candidate primacy.\n"
        "See INVERSE_EXTRACTION_AND_LOGARITHMIC_MEASUREMENT_LAW.md for requirements."
    )


def test_inverse_law_doc_forbids_logarithm_of_gates_and_encodings():
    """
    Guard for logarithmic measurement constraints.

    FORBIDDEN: log(gate), log(LCNV), log(CLOSED), log(BLOCK)
    PERMITTED: log(x) only when x > 0, x ∈ LicensedMeasuredQuantity, Gate(x) = OPEN

    Authority: INVERSE_EXTRACTION_AND_LOGARITHMIC_MEASUREMENT_LAW.md § 2.2
    """
    inverse_law_doc_path = Path("docs/qiyas_core/INVERSE_EXTRACTION_AND_LOGARITHMIC_MEASUREMENT_LAW.md")
    assert inverse_law_doc_path.exists(), f"Inverse law doc not found at {inverse_law_doc_path}"

    text = inverse_law_doc_path.read_text()

    # Required logarithmic constraints
    required_log_constraints = [
        "log(gate) is FORBIDDEN",
        "log(LCNV) is FORBIDDEN",
        "log(CLOSED)",
        "log(BLOCK)",
        "LicensedMeasuredQuantity",
        "Gate(x) = OPEN",
    ]

    missing = []
    for constraint in required_log_constraints:
        if constraint not in text:
            missing.append(constraint)

    assert not missing, (
        f"Required logarithmic constraints MISSING from inverse law doc:\n" + "\n".join(missing) +
        "\n\nThese constraints prevent log of gates, encodings, and blocked states."
    )


def test_pr_authority_audit_doc_exists_and_classifies_prs():
    """
    Guard for PR authority audit existence and completeness.

    Ensures PR #1-49 are classified to prevent authority mismatch.

    Authority: PR_1_49_AUTHORITY_AUDIT.md § 1.1, § 1.2
    """
    audit_doc_path = Path("docs/qiyas_core/PR_1_49_AUTHORITY_AUDIT.md")
    assert audit_doc_path.exists(), f"PR authority audit doc not found at {audit_doc_path}"

    text = audit_doc_path.read_text()

    # Critical PRs that MUST be classified
    critical_prs = [
        "PR #1",   # Kernel foundation
        "PR #16",  # 95% debt audit
        "PR #44",  # LCNV (needs correction)
        "PR #45",  # CTS tokenizer (NOT inverse law)
    ]

    missing = []
    for pr in critical_prs:
        if pr not in text:
            missing.append(pr)

    assert not missing, (
        f"Critical PRs MISSING from authority audit:\n" + "\n".join(missing) +
        "\n\nAll PRs #1-49 must be classified."
    )

    # Ensure PR #44 is marked as needs correction
    assert "MISMATCH/NEEDS CORRECTION" in text or "binding-but-needs-correction" in text, (
        "PR #44 must be classified as needing correction in authority audit"
    )

    # Ensure false PR #45 reference is corrected
    assert "CTS tokenizer" in text or "Z3" in text, (
        "PR #45 must be correctly identified as CTS tokenizer, not inverse law"
    )


def test_governing_laws_prevent_recurrence():
    """
    Guard for governing laws that prevent pattern recurrence.

    Ensures audit doc establishes laws preventing:
    1. Authoritative docs without guards
    2. Future PR references without verification
    3. Doc-authority mismatch

    Authority: PR_1_49_AUTHORITY_AUDIT.md § 3
    """
    audit_doc_path = Path("docs/qiyas_core/PR_1_49_AUTHORITY_AUDIT.md")
    assert audit_doc_path.exists(), f"PR authority audit doc not found at {audit_doc_path}"

    text = audit_doc_path.read_text()

    # Required governing laws
    required_laws = [
        "No Authoritative Document Without Guard",
        "No Future PR Reference Without Verification",
        "Separate Encoding Authority from Candidate Authority",
        "لا وثيقة سلطوية بلا حارس",  # Arabic principle
    ]

    missing = []
    for law in required_laws:
        if law not in text:
            missing.append(law)

    assert not missing, (
        f"Required governing laws MISSING from authority audit:\n" + "\n".join(missing) +
        "\n\nThese laws prevent recurrence of PR #44 pattern."
    )


def test_block_constraints_are_defined():
    """
    Guard for block-specific constitutional constraints.

    Ensures:
    - LexicalOnly = LafziSignifiedOnly (NOT semantic meaning)
    - MeaningOnly = SingularLexicalMadlulCandidate (POTENTIAL_ONLY)
    - MCLO = SignifierOnlyValue (broader than Abjad)

    Authority: INVERSE_EXTRACTION_AND_LOGARITHMIC_MEASUREMENT_LAW.md § 3
    """
    inverse_law_doc_path = Path("docs/qiyas_core/INVERSE_EXTRACTION_AND_LOGARITHMIC_MEASUREMENT_LAW.md")
    assert inverse_law_doc_path.exists(), f"Inverse law doc not found at {inverse_law_doc_path}"

    text = inverse_law_doc_path.read_text()

    # Required block constraints
    required_block_constraints = [
        "LexicalOnly = LafziSignifiedOnly",
        "MeaningOnly = SingularLexicalMadlulCandidate",
        "MCLO = SignifierOnlyValue",
        "PTI_force = POTENTIAL_ONLY",
        "PTI_computed = FORBIDDEN",
    ]

    missing = []
    for constraint in required_block_constraints:
        if constraint not in text:
            missing.append(constraint)

    assert not missing, (
        f"Required block constraints MISSING from inverse law doc:\n" + "\n".join(missing) +
        "\n\nThese constraints prevent semantic overreach in LCNV blocks."
    )


def test_no_direct_meaning_from_lcnv():
    """
    Guard against LCNV producing meaning/hukm/reality claims.

    LCNV must not claim to produce:
    - FinalMeaning
    - AuthoritativeMeaning
    - Hukm
    - RealityClaim
    - Semantic content

    Authority: INVERSE_EXTRACTION_AND_LOGARITHMIC_MEASUREMENT_LAW.md § 1.3, § 3
    """
    inverse_law_doc_path = Path("docs/qiyas_core/INVERSE_EXTRACTION_AND_LOGARITHMIC_MEASUREMENT_LAW.md")
    assert inverse_law_doc_path.exists(), f"Inverse law doc not found at {inverse_law_doc_path}"

    text = inverse_law_doc_path.read_text()

    # Required prohibitions
    required_prohibitions = [
        "GateStateBundle ≠ Meaning",
        "GateStateBundle ≠ Hukm",
        "has_semantic_authority() = False",
        "is_source_of_truth() = False",
    ]

    missing = []
    for prohibition in required_prohibitions:
        if prohibition not in text:
            missing.append(prohibition)

    assert not missing, (
        f"Required prohibitions MISSING from inverse law doc:\n" + "\n".join(missing) +
        "\n\nThese prohibitions prevent LCNV from claiming semantic authority."
    )


# Run all tests when executed directly
if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
