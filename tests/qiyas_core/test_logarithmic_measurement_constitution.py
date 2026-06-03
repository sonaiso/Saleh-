"""
Constitutional Guard: Licensed Logarithmic Measurement Law

This test prevents logarithmic operations from being applied to
Candidates, LCNV, Meanings, Hukm, or other non-quantitative objects.

Constitutional basis:
- docs/qiyas_core/LICENSED_LOGARITHMIC_MEASUREMENT_LAW.md
- Only LicensedMeasuredQuantity may enter logarithm
- Logarithm does not produce Candidate, Meaning, or Hukm
- Inverse returns quantity only, not Candidate

الكمية المرخّصة فقط تدخل اللوغاريتم.
واللوغاريتم لا ينتج مرشحًا ولا معنى ولا حكمًا.
"""

from pathlib import Path


def test_logarithm_law_forbids_non_quantities():
    """
    Guard against applying logarithm to non-quantitative objects.

    FORBIDDEN operations that violate quantitative domain restriction:
    - "log(Candidate)"
    - "log(LCNV)"
    - "log(Meaning)"
    - "log(Ifadah)"
    - "log(Hukm)"
    - "inverse_log → Candidate"
    - "inverse_log → Meaning"
    - "inverse_log → Hukm"
    - "logarithm produces meaning"
    - "logarithm derives semantic"
    - "every number can use logarithm"

    Constitutional principle:
    Logarithm operates ONLY on LicensedMeasuredQuantity,
    NOT on Candidate, Meaning, Hukm, or compressed values.
    """
    doc_path = Path(__file__).parent.parent.parent / "docs" / "qiyas_core" / "LICENSED_LOGARITHMIC_MEASUREMENT_LAW.md"

    assert doc_path.exists(), f"Logarithmic measurement law document not found: {doc_path}"

    text = doc_path.read_text(encoding="utf-8")

    # Forbidden formulations that violate quantitative domain restriction
    forbidden_patterns = [
        # Direct application to non-quantities without prohibition marker
        ("log(Candidate)", "Logarithm applied to Candidate"),
        ("log(LCNV)", "Logarithm applied to LCNV"),
        ("log(Meaning)", "Logarithm applied to Meaning"),
        ("log(Ifadah)", "Logarithm applied to Ifadah"),
        ("log(Hukm)", "Logarithm applied to Hukm"),

        # Inverse producing non-quantities without prohibition marker
        ("inverse_log → Candidate", "Inverse log producing Candidate"),
        ("inverse_log → Meaning", "Inverse log producing Meaning"),
        ("inverse_log → Hukm", "Inverse log producing Hukm"),

        # Semantic derivation claims
        ("logarithm produces meaning", "Logarithm producing meaning"),
        ("logarithm derives semantic", "Logarithm deriving semantics"),

        # Universal applicability claims
        ("every number can use logarithm", "Universal logarithm applicability"),
        ("all numbers may enter logarithm", "All numbers entering logarithm"),
    ]

    violations = []
    for phrase, description in forbidden_patterns:
        # Check if phrase appears WITHOUT the prohibition marker ⇏
        if phrase in text:
            # Find context around the phrase
            phrase_index = text.find(phrase)
            context_start = max(0, phrase_index - 50)
            context_end = min(len(text), phrase_index + len(phrase) + 50)
            context = text[context_start:context_end]

            # If the context does NOT contain ⇏ (prohibition marker), it's a violation
            if "⇏" not in context and "❌" not in context and "FORBIDDEN" not in context:
                violations.append((phrase, description, context))

    assert not violations, (
        f"Logarithmic measurement law regression detected. "
        f"Forbidden phrases found without prohibition markers: {[(p, d) for p, d, _ in violations]}\n\n"
        f"Constitutional violation: These formulations suggest logarithm can be applied "
        f"to non-quantitative objects (Candidate, Meaning, Hukm, etc.), violating the "
        f"principle that only LicensedMeasuredQuantity may enter logarithm.\n\n"
        f"Correct formulation:\n"
        f"  log : LicensedMeasuredQuantity → LogMeasuredQuantity\n"
        f"  inverse_log : LogMeasuredQuantity → LicensedMeasuredQuantity\n"
        f"  log(Candidate) ⇏ LogQuantity (explicitly forbidden)\n\n"
        f"الكمية المرخّصة فقط تدخل اللوغاريتم.\n"
        f"واللوغاريتم لا ينتج مرشحًا ولا معنى ولا حكمًا.\n"
        f"(Only LicensedMeasuredQuantity enters logarithm.\n"
        f" Logarithm does not produce Candidate, Meaning, or Hukm.)"
    )


def test_logarithm_law_includes_required_formulations():
    """
    Verify the document contains the correct logarithmic measurement law formulation.

    Required formulations:
    1. LicensedMeasuredQuantity (input type)
    2. LogMeasuredQuantity (output type)
    3. log : LicensedMeasuredQuantity → LogMeasuredQuantity
    4. inverse_log : LogMeasuredQuantity → LicensedMeasuredQuantity
    5. Forbidden operations with prohibition markers
    6. Governing principles in Arabic and English
    """
    doc_path = Path(__file__).parent.parent.parent / "docs" / "qiyas_core" / "LICENSED_LOGARITHMIC_MEASUREMENT_LAW.md"

    assert doc_path.exists(), f"Logarithmic measurement law document not found: {doc_path}"

    text = doc_path.read_text(encoding="utf-8")

    # Required formulations
    required = [
        # Core types
        "LicensedMeasuredQuantity",
        "LogMeasuredQuantity",

        # Core operations
        "log : LicensedMeasuredQuantity → LogMeasuredQuantity",
        "inverse_log : LogMeasuredQuantity → LicensedMeasuredQuantity",

        # Forbidden operations (with prohibition marker)
        "log(Candidate) ⇏",
        "log(LCNV) ⇏",
        "log(Meaning) ⇏",
        "inverse_log(LogQuantity) ⇏ Candidate",

        # Identity preservation
        "Quantity is not identity",
        "Identity is preserved independent of trace",

        # Governing principle in Arabic
        "الكمية المرخّصة فقط تدخل اللوغاريتم",
        "واللوغاريتم لا ينتج مرشحًا ولا معنى ولا حكمًا",

        # Governing principle in English
        "Only a LicensedMeasuredQuantity may enter logarithm",
        "Logarithm does not produce Candidate",
        "Logarithm does not produce Meaning",
        "Logarithm does not produce Hukm",

        # Inverse law
        "inverse_log(log(Quantity)) = Quantity",
        "inverse_log(log(Candidate)) is FORBIDDEN",

        # Domain restriction
        "Logarithm does NOT operate on",
        "Logarithm ONLY operates on",
    ]

    missing = []
    for phrase in required:
        if phrase not in text:
            missing.append(phrase)

    assert not missing, (
        f"Logarithmic measurement law formulation incomplete. "
        f"Required formulations missing: {missing}\n\n"
        f"The document must establish the constitutional constraint that "
        f"logarithm operates ONLY on LicensedMeasuredQuantity, not on "
        f"Candidate, Meaning, Hukm, or other non-quantitative objects.\n"
        f"See docs/qiyas_core/LICENSED_LOGARITHMIC_MEASUREMENT_LAW.md"
    )


def test_logarithm_law_defines_wad_constraints():
    """
    Verify the document defines ahkam al-wad' (conditions of legal validity).

    Required ahkam al-wad':
    1. As-Sabab (The Cause)
    2. Ash-Shart (The Condition)
    3. Al-Mani' (The Blocking Factor)
    4. As-Sihhah (Correctness)
    5. Al-Fasad wa-l-Butlan (Corruption and Invalidity)
    """
    doc_path = Path(__file__).parent.parent.parent / "docs" / "qiyas_core" / "LICENSED_LOGARITHMIC_MEASUREMENT_LAW.md"

    assert doc_path.exists(), f"Logarithmic measurement law document not found: {doc_path}"

    text = doc_path.read_text(encoding="utf-8")

    # Required ahkam al-wad' sections
    required_wad = [
        "Ahkam Al-Wad'",
        "As-Sabab (The Cause)",
        "Ash-Shart (The Condition)",
        "Al-Mani' (The Blocking Factor)",
        "As-Sihhah (Correctness)",
        "Al-Fasad wa-l-Butlan",
    ]

    missing = []
    for section in required_wad:
        if section not in text:
            missing.append(section)

    assert not missing, (
        f"Logarithmic measurement law missing ahkam al-wad' sections: {missing}\n\n"
        f"The document must define the five conditions of legal validity "
        f"(sabab, shart, mani', sihhah, fasad/butlan) for logarithmic operations."
    )


def test_logarithm_law_defines_farq_qadih():
    """
    Verify the document defines invalidating differences (al-farq al-qadih).

    The document must specify what constitutes an invalidating difference
    vs. a non-invalidating difference in logarithmic operations.
    """
    doc_path = Path(__file__).parent.parent.parent / "docs" / "qiyas_core" / "LICENSED_LOGARITHMIC_MEASUREMENT_LAW.md"

    assert doc_path.exists(), f"Logarithmic measurement law document not found: {doc_path}"

    text = doc_path.read_text(encoding="utf-8")

    # Required farq qadih sections
    required = [
        "Invalidating Difference",
        "Al-Farq Al-Qadih",
        "Examples of Invalidating Difference",
        "Examples of Non-Invalidating Difference",
    ]

    missing = []
    for section in required:
        if section not in text:
            missing.append(section)

    assert not missing, (
        f"Logarithmic measurement law missing farq qadih sections: {missing}\n\n"
        f"The document must define what constitutes an invalidating difference "
        f"in logarithmic operations (e.g., input is not a quantity, gate is closed)."
    )


def test_logarithm_law_preserves_algebraic_invariants():
    """
    Verify the document preserves the absolute algebraic invariants.

    Required invariants:
    1. Identity is not trace
    2. Trace is not identity
    3. Rank is computed by meet semantics
    4. Residuals must be preserved
    5. No layer produces next layer output without gate
    6. Potential candidates must not become final judgments
    """
    doc_path = Path(__file__).parent.parent.parent / "docs" / "qiyas_core" / "LICENSED_LOGARITHMIC_MEASUREMENT_LAW.md"

    assert doc_path.exists(), f"Logarithmic measurement law document not found: {doc_path}"

    text = doc_path.read_text(encoding="utf-8")

    # Required invariant mentions
    required_invariants = [
        # Identity/trace separation
        "Identity is preserved independent of trace",
        "Quantity is not identity",

        # Rank preservation
        "rank",
        "Rank",

        # Residual preservation
        "preserved_residuals",
        "Residuals are preserved",

        # No semantic derivation
        "does not produce Candidate",
        "does not produce Meaning",
        "does not produce Hukm",

        # Trace preservation
        "Trace is preserved",
        "trace",
    ]

    missing = []
    for invariant in required_invariants:
        if invariant not in text:
            missing.append(invariant)

    assert not missing, (
        f"Logarithmic measurement law does not preserve algebraic invariants: {missing}\n\n"
        f"The document must explicitly preserve the absolute invariants: "
        f"identity/trace separation, rank preservation, residual preservation, "
        f"and prohibition of semantic derivation."
    )


def test_logarithm_law_no_runtime_implementation():
    """
    Verify the document explicitly states NO runtime implementation yet.

    This is a constitutional constraint document only.
    Runtime implementation must come later in a separate PR.
    """
    doc_path = Path(__file__).parent.parent.parent / "docs" / "qiyas_core" / "LICENSED_LOGARITHMIC_MEASUREMENT_LAW.md"

    assert doc_path.exists(), f"Logarithmic measurement law document not found: {doc_path}"

    text = doc_path.read_text(encoding="utf-8")

    # Must state no runtime implementation
    assert "no runtime implementation yet" in text.lower() or "No runtime implementation yet" in text, (
        "Document must explicitly state that no runtime implementation exists yet. "
        "This is a constitutional constraint document only."
    )

    # Must have implementation status section
    assert "Implementation Status" in text, (
        "Document must have an 'Implementation Status' section."
    )

    # Must state it's constitutional constraint only
    assert "Constitutional constraint" in text or "constitutional constraint" in text, (
        "Document must identify itself as a constitutional constraint document."
    )


def test_logarithm_law_relationship_to_lcnv():
    """
    Verify the document clarifies the relationship between logarithm and LCNV.

    Logarithm and LCNV are different operations with shared constraints.
    The document must make this distinction clear.
    """
    doc_path = Path(__file__).parent.parent.parent / "docs" / "qiyas_core" / "LICENSED_LOGARITHMIC_MEASUREMENT_LAW.md"

    assert doc_path.exists(), f"Logarithmic measurement law document not found: {doc_path}"

    text = doc_path.read_text(encoding="utf-8")

    # Must clarify relationship to LCNV
    required = [
        "Relationship to LCNV",
        "Logarithm ≠ LCNV",
        "LCNV compresses qiyas layer state",
        "Logarithm compresses quantitative ranges",
    ]

    missing = []
    for phrase in required:
        if phrase not in text:
            missing.append(phrase)

    assert not missing, (
        f"Logarithmic measurement law does not clarify relationship to LCNV: {missing}\n\n"
        f"The document must distinguish logarithm (quantitative range compression) "
        f"from LCNV (layer state compression) while noting their shared constraints."
    )
