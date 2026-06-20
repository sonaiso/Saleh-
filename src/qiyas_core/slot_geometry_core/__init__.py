# slot_geometry_core — PR-CORE-0
#
# هذه الحزمة لا تعرف العربية مباشرة.
# هي تحوّل الدستور الوثائقي إلى عقود برمجية قابلة للاختبار.
#
# القانون:
#   لا طبقة بلا أصل.
#   لا أصل بلا فرع مرخص.
#   لا فرع بلا مقايسة.
#   لا مقايسة بلا حد.
#   لا حد بلا اكتمال أدنى.
#   لا اكتمال بلا هوية موروثة.
#   لا هوية بلا أثر.
#   لا قائمة بلا منع الحكم.
#   لا Gamma بلا TargetBoundary.
#   لا PR بلا سجل أصل وفرع.

from .gamma import GammaResult, GammaStatus, gamma
from .identity_inheritance import IdentityInheritance, IdentityInheritanceViolation
from .layer_spec import BranchSpec, LayerSpec, LayerStatus, OriginSpec
from .master_layer_registry import MasterLayerRegistry, RegistryViolation
from .master_registry_seed import build_master_registry_seed, build_p0_implemented_registry, build_p1_specified_registry, build_p1_atomic_carriers_implemented_registry, build_p1_sequence_position_implemented_registry, build_p1_slot_implemented_registry, build_p2_implemented_registry, build_p3_implemented_registry, build_p4_implemented_registry, build_p5_implemented_registry, build_p6_implemented_registry, build_p7_implemented_registry, build_p8_implemented_registry, build_p9_implemented_registry, build_p10_implemented_registry, build_p2_specified_registry, build_p3_specified_registry, build_p4_specified_registry, build_p5_specified_registry, build_p6_specified_registry, build_p7_specified_registry, build_p8_specified_registry, build_p9_specified_registry, build_p10_specified_registry, build_p11_specified_registry, build_p12_specified_registry
from .minimum_completion import MinimumCompletionSpec, MinimumCompletionViolation
from .registry_entry import RegistryEntry, RegistryEntryViolation
from .target_boundary import TargetBoundary

__all__ = [
    "BranchSpec",
    "GammaResult",
    "GammaStatus",
    "IdentityInheritance",
    "IdentityInheritanceViolation",
    "LayerSpec",
    "LayerStatus",
    "MasterLayerRegistry",
    "MinimumCompletionSpec",
    "MinimumCompletionViolation",
    "OriginSpec",
    "RegistryEntry",
    "RegistryEntryViolation",
    "RegistryViolation",
    "TargetBoundary",
    "build_master_registry_seed",
    "build_p0_implemented_registry",
    "build_p1_specified_registry",
    "build_p1_atomic_carriers_implemented_registry",
    "build_p1_sequence_position_implemented_registry",
    "build_p1_slot_implemented_registry",
    "build_p2_implemented_registry",
    "build_p3_implemented_registry",
    "build_p4_implemented_registry",
    "build_p5_implemented_registry",
    "build_p6_implemented_registry",
    "build_p7_implemented_registry",
    "build_p8_implemented_registry",
    "build_p9_implemented_registry",
    "build_p10_implemented_registry",
    "build_p2_specified_registry",
    "build_p3_specified_registry",
    "build_p4_specified_registry",
    "build_p5_specified_registry",
    "build_p6_specified_registry",
    "build_p7_specified_registry",
    "build_p8_specified_registry",
    "build_p9_specified_registry",
    "build_p10_specified_registry",
    "build_p11_specified_registry",
    "build_p12_specified_registry",
    "gamma",
]
