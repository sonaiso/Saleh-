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
