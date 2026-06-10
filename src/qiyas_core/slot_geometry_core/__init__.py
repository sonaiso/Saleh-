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
from .master_registry_seed import build_master_registry_seed
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
    "gamma",
]
