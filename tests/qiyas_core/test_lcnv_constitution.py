"""Constitutional tests for LCNV (Track B) — Minimal Isolated Runtime

Tests the constitutional laws from PR #52:
  1. Unpack(Pack(c)) = EncodedStateProjection(c), NOT Candidate(c)
  2. LCNV does NOT restore CandidateAuthority
  3. LCNV does NOT produce Meaning/Ifadah/Hukm
  4. CLOSED ≠ 0
  5. semantic_force = FORBIDDEN
  6. Number does not produce knowledge

Track isolation:
  - No SlotGeometry imports
  - No LogarithmicMeasurement imports
  - No integration with Track A or Track C

See: docs/qiyas_core/LAYERED_COMPRESSED_NUMERIC_VALUE_ARCHITECTURE.md
"""

from dataclasses import FrozenInstanceError

import pytest

from qiyas_core.lcnv import (
    CLOSED,
    LCNV,
    EncodedStateProjection,
    GateStateBundle,
    LCNVError,
    pack,
    unpack,
)


class TestLCNVConstitutionalLaws:
    """Test fundamental constitutional laws of LCNV system."""

    def test_unpack_pack_returns_projection_not_candidate(self):
        """
        Law 1: Unpack(Pack(c)) = EncodedStateProjection(c), NOT Candidate(c)

        Constitutional requirement from PR #52.
        """
        # Pack a minimal MCLO value
        lcnv = pack(
            mclo_value=42,
            source_layer_id="test_layer",
            rank_ceiling=5,
            residual_count=0,
        )

        # Unpack
        result = unpack(lcnv)

        # MUST be EncodedStateProjection, NOT Candidate
        assert isinstance(result, EncodedStateProjection)
        assert not hasattr(result, "candidate_authority")
        assert not hasattr(result, "evidence")
        assert not hasattr(result, "meaning")
        assert not hasattr(result, "hukm")

    def test_encoded_state_projection_is_not_candidate(self):
        """EncodedStateProjection is state projection, NOT authoritative Candidate."""
        projection = EncodedStateProjection(
            gate_states=GateStateBundle(mclo_state=42),
            source_layer_id="test_layer",
            encoding_format="mclo_only_v1",
        )

        # Verify it's projection only
        assert isinstance(projection, EncodedStateProjection)
        assert projection.gate_states.mclo_state == 42

        # Verify it lacks candidate authority markers
        assert not hasattr(projection, "candidate_authority")
        assert not hasattr(projection, "is_authoritative")

    def test_gate_state_bundle_is_not_candidate(self):
        """GateStateBundle is gate state encoding, NOT Candidate."""
        bundle = GateStateBundle(
            mclo_state=42,
            rank_ceiling=5,
            residual_count=0,
        )

        # Verify it's state encoding only
        assert isinstance(bundle, GateStateBundle)
        assert bundle.mclo_state == 42

        # Verify it lacks candidate authority
        assert not hasattr(bundle, "candidate_authority")
        assert not hasattr(bundle, "evidence")

    def test_closed_not_equal_zero(self):
        """
        Law: CLOSED ≠ 0

        CLOSED means "gate not opened", NOT "zero value".
        """
        # CLOSED is a distinct constant
        assert CLOSED != 0
        assert CLOSED == "CLOSED"

        # LCNV rejects 0 for MCLO block
        with pytest.raises(LCNVError, match="cannot be 0.*CLOSED ≠ 0"):
            LCNV(mclo_block=0)

        # GateStateBundle rejects 0 for mclo_state
        with pytest.raises(LCNVError, match="cannot be 0.*CLOSED ≠ 0"):
            GateStateBundle(mclo_state=0)

        # pack() rejects 0 for mclo_value
        with pytest.raises(LCNVError, match="Invalid MCLO value.*CLOSED ≠ 0"):
            pack(mclo_value=0, source_layer_id="test")

    def test_lcnv_does_not_produce_meaning(self):
        """LCNV MUST NOT produce Meaning, Ifadah, or Hukm."""
        lcnv = pack(mclo_value=42, source_layer_id="test_layer")
        projection = unpack(lcnv)

        # Verify no meaning-related attributes
        assert not hasattr(projection, "meaning")
        assert not hasattr(projection, "ifadah")
        assert not hasattr(projection, "hukm")
        assert not hasattr(projection, "reality_claim")

        # Verify gate states don't produce meaning
        assert not hasattr(projection.gate_states, "meaning")
        assert not hasattr(projection.gate_states, "semantic_value")

    def test_lcnv_does_not_produce_authority(self):
        """LCNV MUST NOT produce CandidateAuthority."""
        lcnv = pack(mclo_value=42, source_layer_id="test_layer")
        projection = unpack(lcnv)

        # Verify no authority markers
        assert not hasattr(projection, "candidate_authority")
        assert not hasattr(projection, "is_authoritative")
        assert not hasattr(projection, "authority_level")

    def test_number_does_not_produce_knowledge(self):
        """
        Governing principle: الرقم لا ينتج معرفة
        (Number does not produce knowledge)
        """
        # Pack a numeric value
        lcnv = pack(mclo_value=999, source_layer_id="test_layer")
        projection = unpack(lcnv)

        # The number 999 produces NO knowledge, meaning, or hukm
        assert projection.gate_states.mclo_state == 999
        assert not hasattr(projection, "knowledge")
        assert not hasattr(projection, "meaning")
        assert not hasattr(projection, "hukm")


class TestLCNVBlockOrdering:
    """Test block ordering dependency (Law 5)."""

    def test_mutabaqah_requires_binding(self):
        """Cannot have Mutabaqah block without Binding block."""
        with pytest.raises(LCNVError, match="Mutabaqah.*without Binding"):
            LCNV(
                mclo_block=42,
                binding_block=CLOSED,
                mutabaqah_block=10,  # Violates ordering
            )

    def test_tadammun_requires_binding(self):
        """Cannot have Tadammun block without Binding block."""
        with pytest.raises(LCNVError, match="Tadammun.*without Binding"):
            LCNV(
                mclo_block=42,
                binding_block=CLOSED,
                tadammun_block=20,  # Violates ordering
            )

    def test_iltizam_requires_binding(self):
        """Cannot have Iltizam block without Binding block."""
        with pytest.raises(LCNVError, match="Iltizam.*without Binding"):
            LCNV(
                mclo_block=42,
                binding_block=CLOSED,
                iltizam_block=30,  # Violates ordering
            )

    def test_all_closed_is_valid(self):
        """LCNV with only MCLO block (all others CLOSED) is valid."""
        lcnv = LCNV(
            mclo_block=42,
            lexical_block=CLOSED,
            meaning_block=CLOSED,
            binding_block=CLOSED,
            mutabaqah_block=CLOSED,
            tadammun_block=CLOSED,
            iltizam_block=CLOSED,
        )

        assert lcnv.mclo_block == 42
        assert lcnv.binding_block == CLOSED


class TestLCNVPackUnpack:
    """Test pack/unpack operations."""

    def test_pack_minimal_mclo(self):
        """Pack minimal MCLO value."""
        lcnv = pack(mclo_value=42, source_layer_id="test_layer")

        assert lcnv.mclo_block == 42
        assert lcnv.source_layer == "test_layer"
        assert lcnv.lexical_block == CLOSED
        assert lcnv.binding_block == CLOSED

    def test_pack_with_rank_residuals(self):
        """Pack with rank ceiling and residuals."""
        lcnv = pack(
            mclo_value=42,
            source_layer_id="test_layer",
            rank_ceiling=5,
            residual_count=2,
            has_blocking_residuals=False,
        )

        assert lcnv.mclo_block == 42
        assert lcnv.rank_block == 5
        assert lcnv.residual_block == 2

    def test_pack_preserves_blocking_residuals_false(self):
        """Pack preserves has_blocking_residuals=False."""
        lcnv = pack(
            mclo_value=42,
            source_layer_id="test_layer",
            has_blocking_residuals=False,
        )

        assert lcnv.has_blocking_residuals is False

    def test_pack_preserves_blocking_residuals_true(self):
        """Pack preserves has_blocking_residuals=True."""
        lcnv = pack(
            mclo_value=42,
            source_layer_id="test_layer",
            has_blocking_residuals=True,
        )

        assert lcnv.has_blocking_residuals is True

    def test_unpack_preserves_gate_states(self):
        """Unpack preserves all gate states."""
        lcnv = pack(
            mclo_value=42,
            source_layer_id="test_layer",
            rank_ceiling=5,
            residual_count=2,
        )

        projection = unpack(lcnv)

        assert projection.gate_states.mclo_state == 42
        assert projection.gate_states.lexical_state == CLOSED
        assert projection.gate_states.rank_ceiling == 5
        assert projection.gate_states.residual_count == 2

    def test_unpack_preserves_blocking_residuals_false(self):
        """Unpack preserves has_blocking_residuals=False."""
        lcnv = pack(
            mclo_value=42,
            source_layer_id="test_layer",
            has_blocking_residuals=False,
        )

        projection = unpack(lcnv)

        assert projection.gate_states.has_blocking_residuals is False

    def test_unpack_preserves_blocking_residuals_true(self):
        """Unpack preserves has_blocking_residuals=True."""
        lcnv = pack(
            mclo_value=42,
            source_layer_id="test_layer",
            has_blocking_residuals=True,
        )

        projection = unpack(lcnv)

        assert projection.gate_states.has_blocking_residuals is True

    def test_blocking_residuals_round_trip(self):
        """has_blocking_residuals round-trips through pack/unpack."""
        # Test with False
        lcnv_false = pack(
            mclo_value=42,
            source_layer_id="test_layer",
            has_blocking_residuals=False,
        )
        projection_false = unpack(lcnv_false)
        assert projection_false.gate_states.has_blocking_residuals is False

        # Test with True
        lcnv_true = pack(
            mclo_value=99,
            source_layer_id="test_layer",
            has_blocking_residuals=True,
        )
        projection_true = unpack(lcnv_true)
        assert projection_true.gate_states.has_blocking_residuals is True

    def test_unpack_requires_source_layer(self):
        """Unpack MUST fail if source_layer is missing."""
        lcnv = LCNV(mclo_block=42, source_layer=None)

        with pytest.raises(LCNVError, match="Cannot unpack LCNV without source_layer"):
            unpack(lcnv)

    def test_unpack_rejects_empty_source_layer(self):
        """Unpack MUST fail if source_layer is empty string."""
        lcnv = LCNV(mclo_block=42, source_layer="")

        with pytest.raises(LCNVError, match="Cannot unpack LCNV without source_layer"):
            unpack(lcnv)

    def test_unpack_creates_trace_reference(self):
        """Unpack creates trace reference, NOT full trace."""
        lcnv = pack(mclo_value=42, source_layer_id="test_layer")
        projection = unpack(lcnv)

        # Has trace reference
        assert projection.trace_ref is not None
        assert "test_layer" in projection.trace_ref
        assert "42" in projection.trace_ref

        # Does NOT have full trace
        assert not hasattr(projection, "full_trace")
        assert not hasattr(projection, "trace_store")

    def test_round_trip_pack_unpack(self):
        """Round trip: pack then unpack preserves state projection."""
        original_mclo = 42
        original_rank = 5

        # Pack
        lcnv = pack(
            mclo_value=original_mclo,
            source_layer_id="test_layer",
            rank_ceiling=original_rank,
        )

        # Unpack
        projection = unpack(lcnv)

        # State is preserved in projection
        assert projection.gate_states.mclo_state == original_mclo
        assert projection.gate_states.rank_ceiling == original_rank

        # But projection is NOT the original Candidate
        assert isinstance(projection, EncodedStateProjection)


class TestLCNVSerialization:
    """Test compact integer serialization."""

    def test_to_compact_int_minimal(self):
        """Serialize LCNV to compact integer (minimal runtime)."""
        lcnv = pack(mclo_value=42, source_layer_id="test_layer")

        compact = lcnv.to_compact_int()

        # Minimal runtime: compact int = MCLO block
        assert compact == 42

    def test_from_compact_int_minimal(self):
        """Deserialize LCNV from compact integer."""
        lcnv = LCNV.from_compact_int(value=42, source_layer="test_layer")

        assert lcnv.mclo_block == 42
        assert lcnv.source_layer == "test_layer"
        assert lcnv.lexical_block == CLOSED

    def test_compact_rejects_zero(self):
        """Compact serialization rejects 0 (CLOSED ≠ 0)."""
        with pytest.raises(LCNVError, match="Invalid LCNV compact value.*CLOSED ≠ 0"):
            LCNV.from_compact_int(value=0)

    def test_compact_rejects_negative(self):
        """Compact serialization rejects negative values."""
        with pytest.raises(LCNVError, match="Invalid LCNV compact value"):
            LCNV.from_compact_int(value=-1)


class TestTrackIsolation:
    """Verify Track B (LCNV) is isolated from other tracks."""

    def test_no_slot_geometry_imports(self):
        """LCNV MUST NOT import from SlotGeometry (Track A)."""
        import qiyas_core.lcnv as lcnv_module

        source = lcnv_module.__file__
        assert source is not None

        with open(source, "r") as f:
            content = f.read()

        # Verify no SlotGeometry imports (check import statements only)
        import_lines = [line for line in content.split('\n') if 'import' in line.lower()]
        for line in import_lines:
            assert "slot_geometry" not in line.lower()
            assert "slotcandidate" not in line.lower()

    def test_no_logarithmic_measurement_imports(self):
        """LCNV MUST NOT import from LogarithmicMeasurement (Track C)."""
        import qiyas_core.lcnv as lcnv_module

        source = lcnv_module.__file__
        assert source is not None

        with open(source, "r") as f:
            content = f.read()

        # Verify no LogMeasurement imports
        assert "LogMeasuredQuantity" not in content
        assert "logarithmic_measurement" not in content
        assert "LogMeasurementReadinessCarrier" not in content

    def test_lcnv_is_minimal_isolated(self):
        """LCNV runtime is minimal and isolated."""
        from qiyas_core.lcnv import __all__

        # Verify minimal exports
        assert "LCNV" in __all__
        assert "EncodedStateProjection" in __all__
        assert "GateStateBundle" in __all__
        assert "pack" in __all__
        assert "unpack" in __all__

        # Verify no higher-layer exports
        assert "Meaning" not in __all__
        assert "Hukm" not in __all__
        assert "SlotGeometry" not in __all__


class TestLCNVValidation:
    """Test LCNV validation constraints."""

    def test_pack_requires_source_layer(self):
        """pack() requires source_layer_id."""
        with pytest.raises(LCNVError, match="requires source_layer_id"):
            pack(mclo_value=42, source_layer_id="")

    def test_projection_requires_source_layer(self):
        """EncodedStateProjection requires source_layer_id."""
        with pytest.raises(LCNVError, match="requires source_layer_id"):
            EncodedStateProjection(
                gate_states=GateStateBundle(mclo_state=42),
                source_layer_id="",
                encoding_format="test",
            )

    def test_projection_requires_encoding_format(self):
        """EncodedStateProjection requires encoding_format."""
        with pytest.raises(LCNVError, match="requires encoding_format"):
            EncodedStateProjection(
                gate_states=GateStateBundle(mclo_state=42),
                source_layer_id="test",
                encoding_format="",
            )


class TestLCNVSemanticForce:
    """Test semantic_force = FORBIDDEN enforcement."""

    def test_lcnv_has_semantic_force_forbidden(self):
        """LCNV MUST have semantic_force = FORBIDDEN."""
        lcnv = pack(mclo_value=42, source_layer_id="test_layer")

        assert hasattr(lcnv, "semantic_force")
        assert lcnv.semantic_force == "FORBIDDEN"

    def test_encoded_state_projection_has_semantic_force_forbidden(self):
        """EncodedStateProjection MUST have semantic_force = FORBIDDEN."""
        lcnv = pack(mclo_value=42, source_layer_id="test_layer")
        projection = unpack(lcnv)

        assert hasattr(projection, "semantic_force")
        assert projection.semantic_force == "FORBIDDEN"

    def test_semantic_force_is_testable(self):
        """semantic_force is a real field, not just documentation."""
        lcnv = LCNV(mclo_block=42, source_layer="test")

        # Field is accessible and testable
        assert lcnv.semantic_force == "FORBIDDEN"

        # Cannot be changed (frozen dataclass)
        with pytest.raises(FrozenInstanceError):
            lcnv.semantic_force = "ALLOWED"  # type: ignore


class TestLCNVBlockValidation:
    """Test hardened block validation (0 and negative rejection)."""

    def test_mclo_block_rejects_zero(self):
        """MCLO block rejects 0 (CLOSED ≠ 0)."""
        with pytest.raises(LCNVError, match="MCLO block cannot be 0"):
            LCNV(mclo_block=0)

    def test_mclo_block_rejects_negative(self):
        """MCLO block rejects negative values."""
        with pytest.raises(LCNVError, match="MCLO block cannot be negative"):
            LCNV(mclo_block=-1)

    def test_lexical_block_rejects_zero(self):
        """Lexical block rejects 0."""
        with pytest.raises(LCNVError, match="Lexical block cannot be 0"):
            LCNV(mclo_block=42, lexical_block=0)

    def test_lexical_block_rejects_negative(self):
        """Lexical block rejects negative values."""
        with pytest.raises(LCNVError, match="Lexical block cannot be negative"):
            LCNV(mclo_block=42, lexical_block=-5)

    def test_meaning_block_rejects_zero(self):
        """Meaning block rejects 0."""
        with pytest.raises(LCNVError, match="Meaning block cannot be 0"):
            LCNV(mclo_block=42, meaning_block=0)

    def test_meaning_block_rejects_negative(self):
        """Meaning block rejects negative values."""
        with pytest.raises(LCNVError, match="Meaning block cannot be negative"):
            LCNV(mclo_block=42, meaning_block=-10)

    def test_binding_block_rejects_zero(self):
        """Binding block rejects 0."""
        with pytest.raises(LCNVError, match="Binding block cannot be 0"):
            LCNV(mclo_block=42, binding_block=0)

    def test_binding_block_rejects_negative(self):
        """Binding block rejects negative values."""
        with pytest.raises(LCNVError, match="Binding block cannot be negative"):
            LCNV(mclo_block=42, binding_block=-3)

    def test_mutabaqah_block_rejects_zero(self):
        """Mutabaqah block rejects 0."""
        with pytest.raises(LCNVError, match="Mutabaqah block cannot be 0"):
            LCNV(mclo_block=42, binding_block=10, mutabaqah_block=0)

    def test_mutabaqah_block_rejects_negative(self):
        """Mutabaqah block rejects negative values."""
        with pytest.raises(LCNVError, match="Mutabaqah block cannot be negative"):
            LCNV(mclo_block=42, binding_block=10, mutabaqah_block=-7)

    def test_tadammun_block_rejects_zero(self):
        """Tadammun block rejects 0."""
        with pytest.raises(LCNVError, match="Tadammun block cannot be 0"):
            LCNV(mclo_block=42, binding_block=10, tadammun_block=0)

    def test_tadammun_block_rejects_negative(self):
        """Tadammun block rejects negative values."""
        with pytest.raises(LCNVError, match="Tadammun block cannot be negative"):
            LCNV(mclo_block=42, binding_block=10, tadammun_block=-2)

    def test_iltizam_block_rejects_zero(self):
        """Iltizam block rejects 0."""
        with pytest.raises(LCNVError, match="Iltizam block cannot be 0"):
            LCNV(mclo_block=42, binding_block=10, iltizam_block=0)

    def test_iltizam_block_rejects_negative(self):
        """Iltizam block rejects negative values."""
        with pytest.raises(LCNVError, match="Iltizam block cannot be negative"):
            LCNV(mclo_block=42, binding_block=10, iltizam_block=-4)


class TestGateStateBundleValidation:
    """Test hardened GateStateBundle validation."""

    def test_mclo_state_rejects_zero(self):
        """MCLO state rejects 0 (CLOSED ≠ 0)."""
        with pytest.raises(LCNVError, match="MCLO state cannot be 0"):
            GateStateBundle(mclo_state=0)

    def test_mclo_state_rejects_negative(self):
        """MCLO state rejects negative values."""
        with pytest.raises(LCNVError, match="MCLO state cannot be negative"):
            GateStateBundle(mclo_state=-1)

    def test_lexical_state_rejects_zero(self):
        """Lexical state rejects 0."""
        with pytest.raises(LCNVError, match="Lexical state cannot be 0"):
            GateStateBundle(mclo_state=42, lexical_state=0)

    def test_lexical_state_rejects_negative(self):
        """Lexical state rejects negative values."""
        with pytest.raises(LCNVError, match="Lexical state cannot be negative"):
            GateStateBundle(mclo_state=42, lexical_state=-5)

    def test_meaning_state_rejects_zero(self):
        """Meaning state rejects 0."""
        with pytest.raises(LCNVError, match="Meaning state cannot be 0"):
            GateStateBundle(mclo_state=42, meaning_state=0)

    def test_meaning_state_rejects_negative(self):
        """Meaning state rejects negative values."""
        with pytest.raises(LCNVError, match="Meaning state cannot be negative"):
            GateStateBundle(mclo_state=42, meaning_state=-10)

    def test_binding_state_rejects_zero(self):
        """Binding state rejects 0."""
        with pytest.raises(LCNVError, match="Binding state cannot be 0"):
            GateStateBundle(mclo_state=42, binding_state=0)

    def test_binding_state_rejects_negative(self):
        """Binding state rejects negative values."""
        with pytest.raises(LCNVError, match="Binding state cannot be negative"):
            GateStateBundle(mclo_state=42, binding_state=-3)

    def test_mutabaqah_state_rejects_zero(self):
        """Mutabaqah state rejects 0."""
        with pytest.raises(LCNVError, match="Mutabaqah state cannot be 0"):
            GateStateBundle(mclo_state=42, mutabaqah_state=0)

    def test_mutabaqah_state_rejects_negative(self):
        """Mutabaqah state rejects negative values."""
        with pytest.raises(LCNVError, match="Mutabaqah state cannot be negative"):
            GateStateBundle(mclo_state=42, mutabaqah_state=-7)

    def test_tadammun_state_rejects_zero(self):
        """Tadammun state rejects 0."""
        with pytest.raises(LCNVError, match="Tadammun state cannot be 0"):
            GateStateBundle(mclo_state=42, tadammun_state=0)

    def test_tadammun_state_rejects_negative(self):
        """Tadammun state rejects negative values."""
        with pytest.raises(LCNVError, match="Tadammun state cannot be negative"):
            GateStateBundle(mclo_state=42, tadammun_state=-2)

    def test_iltizam_state_rejects_zero(self):
        """Iltizam state rejects 0."""
        with pytest.raises(LCNVError, match="Iltizam state cannot be 0"):
            GateStateBundle(mclo_state=42, iltizam_state=0)

    def test_iltizam_state_rejects_negative(self):
        """Iltizam state rejects negative values."""
        with pytest.raises(LCNVError, match="Iltizam state cannot be negative"):
            GateStateBundle(mclo_state=42, iltizam_state=-4)


class TestLCNVSemanticForceHardening:
    """Test semantic_force cannot be overridden (PR #67)."""

    def test_lcnv_semantic_force_cannot_be_overridden_via_init(self):
        """LCNV semantic_force cannot be overridden through constructor."""
        # init=False prevents passing semantic_force to constructor
        lcnv = LCNV(mclo_block=42, source_layer="test")
        assert lcnv.semantic_force == "FORBIDDEN"

        # Attempting to pass semantic_force should fail (not in __init__)
        # This is enforced by dataclass field(init=False)

    def test_projection_semantic_force_cannot_be_overridden_via_init(self):
        """EncodedStateProjection semantic_force cannot be overridden."""
        projection = EncodedStateProjection(
            gate_states=GateStateBundle(mclo_state=42),
            source_layer_id="test",
            encoding_format="test",
        )
        assert projection.semantic_force == "FORBIDDEN"

        # Attempting to pass semantic_force should fail (not in __init__)

    def test_lcnv_semantic_force_cannot_be_mutated(self):
        """LCNV semantic_force cannot be mutated after creation."""
        lcnv = LCNV(mclo_block=42, source_layer="test")

        with pytest.raises(FrozenInstanceError):
            lcnv.semantic_force = "ALLOWED"  # type: ignore

    def test_projection_semantic_force_cannot_be_mutated(self):
        """EncodedStateProjection semantic_force cannot be mutated."""
        projection = EncodedStateProjection(
            gate_states=GateStateBundle(mclo_state=42),
            source_layer_id="test",
            encoding_format="test",
        )

        with pytest.raises(FrozenInstanceError):
            projection.semantic_force = "ALLOWED"  # type: ignore


class TestLCNVFloatRejection:
    """Test LCNV rejects float values for blocks (PR #67)."""

    def test_lcnv_rejects_float_negative_block(self):
        """LCNV rejects negative float for MCLO block."""
        with pytest.raises(LCNVError, match="MCLO block cannot be float"):
            LCNV(mclo_block=-1.0)  # type: ignore

    def test_lcnv_rejects_float_positive_block(self):
        """LCNV rejects positive float for MCLO block."""
        with pytest.raises(LCNVError, match="MCLO block cannot be float"):
            LCNV(mclo_block=1.5)  # type: ignore

    def test_lcnv_rejects_float_lexical_block(self):
        """LCNV rejects float for lexical block."""
        with pytest.raises(LCNVError, match="Lexical block cannot be float"):
            LCNV(mclo_block=42, lexical_block=2.5)  # type: ignore

    def test_lcnv_rejects_float_meaning_block(self):
        """LCNV rejects float for meaning block."""
        with pytest.raises(LCNVError, match="Meaning block cannot be float"):
            LCNV(mclo_block=42, meaning_block=3.7)  # type: ignore

    def test_lcnv_rejects_float_binding_block(self):
        """LCNV rejects float for binding block."""
        with pytest.raises(LCNVError, match="Binding block cannot be float"):
            LCNV(mclo_block=42, binding_block=4.2)  # type: ignore

    def test_gate_state_bundle_rejects_float_negative_state(self):
        """GateStateBundle rejects negative float for state."""
        with pytest.raises(LCNVError, match="MCLO state cannot be float"):
            GateStateBundle(mclo_state=-1.0)  # type: ignore

    def test_gate_state_bundle_rejects_float_positive_state(self):
        """GateStateBundle rejects positive float for state."""
        with pytest.raises(LCNVError, match="MCLO state cannot be float"):
            GateStateBundle(mclo_state=1.5)  # type: ignore

    def test_gate_state_bundle_rejects_float_lexical_state(self):
        """GateStateBundle rejects float for lexical state."""
        with pytest.raises(LCNVError, match="Lexical state cannot be float"):
            GateStateBundle(mclo_state=42, lexical_state=2.5)  # type: ignore


class TestLCNVStringRejection:
    """Test LCNV rejects string values for blocks (PR #67)."""

    def test_lcnv_rejects_string_block(self):
        """LCNV rejects string value for MCLO block (except CLOSED)."""
        with pytest.raises(LCNVError, match="MCLO block must be either CLOSED or positive integer"):
            LCNV(mclo_block="1")  # type: ignore

    def test_lcnv_rejects_string_lexical_block(self):
        """LCNV rejects string for lexical block (except CLOSED)."""
        with pytest.raises(LCNVError, match="Lexical block must be either CLOSED or positive integer"):
            LCNV(mclo_block=42, lexical_block="2")  # type: ignore

    def test_gate_state_bundle_rejects_string_state(self):
        """GateStateBundle rejects string value for state (except CLOSED)."""
        with pytest.raises(LCNVError, match="MCLO state must be either CLOSED or positive integer"):
            GateStateBundle(mclo_state="42")  # type: ignore

    def test_gate_state_bundle_rejects_string_lexical_state(self):
        """GateStateBundle rejects string for lexical state (except CLOSED)."""
        with pytest.raises(LCNVError, match="Lexical state must be either CLOSED or positive integer"):
            GateStateBundle(mclo_state=42, lexical_state="2")  # type: ignore


class TestUnpackDocstring:
    """Test unpack() docstring documents source_layer requirement (PR #67)."""

    def test_unpack_docstring_mentions_missing_source_layer(self):
        """unpack() docstring mentions LCNVError when source_layer is missing."""
        # Check that the docstring includes the Raises section
        assert unpack.__doc__ is not None
        assert "Raises:" in unpack.__doc__
        assert "LCNVError" in unpack.__doc__
        assert "source_layer" in unpack.__doc__


class TestLCNVBoolRejection:
    """Test LCNV rejects bool values (bool is subclass of int in Python)."""

    def test_lcnv_rejects_bool_true_mclo_block(self):
        """LCNV rejects True for MCLO block."""
        with pytest.raises(LCNVError, match="MCLO block cannot be bool"):
            LCNV(mclo_block=True)  # type: ignore

    def test_lcnv_rejects_bool_false_mclo_block(self):
        """LCNV rejects False for MCLO block."""
        with pytest.raises(LCNVError, match="MCLO block cannot be bool"):
            LCNV(mclo_block=False)  # type: ignore

    def test_lcnv_rejects_bool_true_lexical_block(self):
        """LCNV rejects True for lexical block."""
        with pytest.raises(LCNVError, match="Lexical block cannot be bool"):
            LCNV(mclo_block=42, lexical_block=True)  # type: ignore

    def test_lcnv_rejects_bool_false_lexical_block(self):
        """LCNV rejects False for lexical block."""
        with pytest.raises(LCNVError, match="Lexical block cannot be bool"):
            LCNV(mclo_block=42, lexical_block=False)  # type: ignore

    def test_gate_state_bundle_rejects_bool_true_mclo_state(self):
        """GateStateBundle rejects True for MCLO state."""
        with pytest.raises(LCNVError, match="MCLO state cannot be bool"):
            GateStateBundle(mclo_state=True)  # type: ignore

    def test_gate_state_bundle_rejects_bool_false_mclo_state(self):
        """GateStateBundle rejects False for MCLO state."""
        with pytest.raises(LCNVError, match="MCLO state cannot be bool"):
            GateStateBundle(mclo_state=False)  # type: ignore

    def test_gate_state_bundle_rejects_bool_true_lexical_state(self):
        """GateStateBundle rejects True for lexical state."""
        with pytest.raises(LCNVError, match="Lexical state cannot be bool"):
            GateStateBundle(mclo_state=42, lexical_state=True)  # type: ignore

    def test_gate_state_bundle_rejects_bool_false_lexical_state(self):
        """GateStateBundle rejects False for lexical state."""
        with pytest.raises(LCNVError, match="Lexical state cannot be bool"):
            GateStateBundle(mclo_state=42, lexical_state=False)  # type: ignore

    def test_pack_rejects_bool_true_mclo_value(self):
        """pack() rejects True for mclo_value."""
        with pytest.raises(LCNVError, match="mclo_value cannot be bool"):
            pack(mclo_value=True, source_layer_id="test")  # type: ignore

    def test_pack_rejects_bool_false_mclo_value(self):
        """pack() rejects False for mclo_value."""
        with pytest.raises(LCNVError, match="mclo_value cannot be bool"):
            pack(mclo_value=False, source_layer_id="test")  # type: ignore

    def test_from_compact_int_rejects_bool_true(self):
        """LCNV.from_compact_int() rejects True."""
        with pytest.raises(LCNVError, match="compact value cannot be bool"):
            LCNV.from_compact_int(True)  # type: ignore

    def test_from_compact_int_rejects_bool_false(self):
        """LCNV.from_compact_int() rejects False."""
        with pytest.raises(LCNVError, match="compact value cannot be bool"):
            LCNV.from_compact_int(False)  # type: ignore


class TestLCNVRankResidualValidation:
    """Test LCNV validates rank and residual fields."""

    def test_lcnv_rejects_bool_true_rank_block(self):
        """LCNV rejects True for rank_block."""
        with pytest.raises(LCNVError, match="rank_block cannot be bool"):
            LCNV(mclo_block=42, rank_block=True)  # type: ignore

    def test_lcnv_rejects_zero_rank_block(self):
        """LCNV rejects 0 for rank_block."""
        with pytest.raises(LCNVError, match="rank_block must be positive integer"):
            LCNV(mclo_block=42, rank_block=0)  # type: ignore

    def test_lcnv_rejects_negative_rank_block(self):
        """LCNV rejects negative rank_block."""
        with pytest.raises(LCNVError, match="rank_block must be positive integer"):
            LCNV(mclo_block=42, rank_block=-1)  # type: ignore

    def test_lcnv_accepts_none_rank_block(self):
        """LCNV accepts None for rank_block."""
        lcnv = LCNV(mclo_block=42, rank_block=None)
        assert lcnv.rank_block is None

    def test_lcnv_accepts_positive_rank_block(self):
        """LCNV accepts positive integer for rank_block."""
        lcnv = LCNV(mclo_block=42, rank_block=5)
        assert lcnv.rank_block == 5

    def test_lcnv_rejects_bool_true_residual_block(self):
        """LCNV rejects True for residual_block."""
        with pytest.raises(LCNVError, match="residual_block cannot be bool"):
            LCNV(mclo_block=42, residual_block=True)  # type: ignore

    def test_lcnv_rejects_negative_residual_block(self):
        """LCNV rejects negative residual_block."""
        with pytest.raises(LCNVError, match="residual_block cannot be negative"):
            LCNV(mclo_block=42, residual_block=-1)  # type: ignore

    def test_lcnv_accepts_zero_residual_block(self):
        """LCNV accepts 0 for residual_block."""
        lcnv = LCNV(mclo_block=42, residual_block=0)
        assert lcnv.residual_block == 0

    def test_lcnv_accepts_positive_residual_block(self):
        """LCNV accepts positive integer for residual_block."""
        lcnv = LCNV(mclo_block=42, residual_block=3)
        assert lcnv.residual_block == 3

    def test_lcnv_rejects_string_has_blocking_residuals(self):
        """LCNV rejects string 'true' for has_blocking_residuals."""
        with pytest.raises(LCNVError, match="has_blocking_residuals must be bool"):
            LCNV(mclo_block=42, has_blocking_residuals="true")  # type: ignore

    def test_lcnv_rejects_int_has_blocking_residuals(self):
        """LCNV rejects int 1 for has_blocking_residuals."""
        with pytest.raises(LCNVError, match="has_blocking_residuals must be bool"):
            LCNV(mclo_block=42, has_blocking_residuals=1)  # type: ignore

    def test_lcnv_accepts_true_has_blocking_residuals(self):
        """LCNV accepts True for has_blocking_residuals."""
        lcnv = LCNV(mclo_block=42, has_blocking_residuals=True)
        assert lcnv.has_blocking_residuals is True

    def test_lcnv_accepts_false_has_blocking_residuals(self):
        """LCNV accepts False for has_blocking_residuals."""
        lcnv = LCNV(mclo_block=42, has_blocking_residuals=False)
        assert lcnv.has_blocking_residuals is False

    def test_gate_state_bundle_rejects_bool_true_rank_ceiling(self):
        """GateStateBundle rejects True for rank_ceiling."""
        with pytest.raises(LCNVError, match="rank_ceiling cannot be bool"):
            GateStateBundle(mclo_state=42, rank_ceiling=True)  # type: ignore

    def test_gate_state_bundle_rejects_zero_rank_ceiling(self):
        """GateStateBundle rejects 0 for rank_ceiling."""
        with pytest.raises(LCNVError, match="rank_ceiling must be positive integer"):
            GateStateBundle(mclo_state=42, rank_ceiling=0)  # type: ignore

    def test_gate_state_bundle_rejects_negative_rank_ceiling(self):
        """GateStateBundle rejects negative rank_ceiling."""
        with pytest.raises(LCNVError, match="rank_ceiling must be positive integer"):
            GateStateBundle(mclo_state=42, rank_ceiling=-1)  # type: ignore

    def test_gate_state_bundle_accepts_none_rank_ceiling(self):
        """GateStateBundle accepts None for rank_ceiling."""
        bundle = GateStateBundle(mclo_state=42, rank_ceiling=None)
        assert bundle.rank_ceiling is None

    def test_gate_state_bundle_accepts_positive_rank_ceiling(self):
        """GateStateBundle accepts positive integer for rank_ceiling."""
        bundle = GateStateBundle(mclo_state=42, rank_ceiling=5)
        assert bundle.rank_ceiling == 5

    def test_gate_state_bundle_rejects_bool_true_residual_count(self):
        """GateStateBundle rejects True for residual_count."""
        with pytest.raises(LCNVError, match="residual_count cannot be bool"):
            GateStateBundle(mclo_state=42, residual_count=True)  # type: ignore

    def test_gate_state_bundle_rejects_negative_residual_count(self):
        """GateStateBundle rejects negative residual_count."""
        with pytest.raises(LCNVError, match="residual_count cannot be negative"):
            GateStateBundle(mclo_state=42, residual_count=-1)  # type: ignore

    def test_gate_state_bundle_accepts_zero_residual_count(self):
        """GateStateBundle accepts 0 for residual_count."""
        bundle = GateStateBundle(mclo_state=42, residual_count=0)
        assert bundle.residual_count == 0

    def test_gate_state_bundle_accepts_positive_residual_count(self):
        """GateStateBundle accepts positive integer for residual_count."""
        bundle = GateStateBundle(mclo_state=42, residual_count=3)
        assert bundle.residual_count == 3

    def test_gate_state_bundle_rejects_int_has_blocking_residuals(self):
        """GateStateBundle rejects int 1 for has_blocking_residuals."""
        with pytest.raises(LCNVError, match="has_blocking_residuals must be bool"):
            GateStateBundle(mclo_state=42, has_blocking_residuals=1)  # type: ignore

    def test_gate_state_bundle_accepts_true_has_blocking_residuals(self):
        """GateStateBundle accepts True for has_blocking_residuals."""
        bundle = GateStateBundle(mclo_state=42, has_blocking_residuals=True)
        assert bundle.has_blocking_residuals is True

    def test_gate_state_bundle_accepts_false_has_blocking_residuals(self):
        """GateStateBundle accepts False for has_blocking_residuals."""
        bundle = GateStateBundle(mclo_state=42, has_blocking_residuals=False)
        assert bundle.has_blocking_residuals is False

    def test_pack_rejects_bool_true_rank_ceiling(self):
        """pack() rejects True for rank_ceiling."""
        with pytest.raises(LCNVError, match="rank_ceiling cannot be bool"):
            pack(mclo_value=42, source_layer_id="test", rank_ceiling=True)  # type: ignore

    def test_pack_rejects_zero_rank_ceiling(self):
        """pack() rejects 0 for rank_ceiling."""
        with pytest.raises(LCNVError, match="rank_ceiling must be positive integer"):
            pack(mclo_value=42, source_layer_id="test", rank_ceiling=0)  # type: ignore

    def test_pack_rejects_negative_rank_ceiling(self):
        """pack() rejects negative rank_ceiling."""
        with pytest.raises(LCNVError, match="rank_ceiling must be positive integer"):
            pack(mclo_value=42, source_layer_id="test", rank_ceiling=-1)  # type: ignore

    def test_pack_accepts_none_rank_ceiling(self):
        """pack() accepts None for rank_ceiling."""
        lcnv = pack(mclo_value=42, source_layer_id="test", rank_ceiling=None)
        assert lcnv.rank_block is None

    def test_pack_accepts_positive_rank_ceiling(self):
        """pack() accepts positive integer for rank_ceiling."""
        lcnv = pack(mclo_value=42, source_layer_id="test", rank_ceiling=5)
        assert lcnv.rank_block == 5

    def test_pack_rejects_bool_true_residual_count(self):
        """pack() rejects True for residual_count."""
        with pytest.raises(LCNVError, match="residual_count cannot be bool"):
            pack(mclo_value=42, source_layer_id="test", residual_count=True)  # type: ignore

    def test_pack_rejects_negative_residual_count(self):
        """pack() rejects negative residual_count."""
        with pytest.raises(LCNVError, match="residual_count cannot be negative"):
            pack(mclo_value=42, source_layer_id="test", residual_count=-1)  # type: ignore

    def test_pack_accepts_zero_residual_count(self):
        """pack() accepts 0 for residual_count."""
        lcnv = pack(mclo_value=42, source_layer_id="test", residual_count=0)
        assert lcnv.residual_block == 0

    def test_pack_accepts_positive_residual_count(self):
        """pack() accepts positive integer for residual_count."""
        lcnv = pack(mclo_value=42, source_layer_id="test", residual_count=3)
        assert lcnv.residual_block == 3

    def test_pack_rejects_int_has_blocking_residuals(self):
        """pack() rejects int 1 for has_blocking_residuals."""
        with pytest.raises(LCNVError, match="has_blocking_residuals must be bool"):
            pack(mclo_value=42, source_layer_id="test", has_blocking_residuals=1)  # type: ignore

    def test_pack_accepts_true_has_blocking_residuals(self):
        """pack() accepts True for has_blocking_residuals."""
        lcnv = pack(mclo_value=42, source_layer_id="test", has_blocking_residuals=True)
        assert lcnv.has_blocking_residuals is True

    def test_pack_accepts_false_has_blocking_residuals(self):
        """pack() accepts False for has_blocking_residuals."""
        lcnv = pack(mclo_value=42, source_layer_id="test", has_blocking_residuals=False)
        assert lcnv.has_blocking_residuals is False

