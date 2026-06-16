"""
test_repository_responsibility_matrix.py — اختبارات إنفاذ REC-1

REC-1: Repository Responsibility Matrix Enforcement.
تحويل حدود مصفوفة مسؤولية المستودعات من وثيقة كلامية إلى اختبارات
(maintainer instruction, 2026-06-10:
"لكن ليس كوثيقة كلامية فقط. يجب أن يحوّل الحدود إلى اختبارات").

Constitutional basis:
    docs/qiyas_core/PROJECT_RECOVERY_CANONICAL_MAP.md    §1, §2, §6, §7 (REC-1)
    docs/qiyas_core/CROSS_REPOSITORY_KNOWLEDGE_BRIDGE.md §3–§6
    docs/qiyas_core/REPOSITORY_RESPONSIBILITY_MATRIX.md  (REC-1 standalone doc)

أقسام الاختبارات:
    REC1-MAP-*      — الخريطة موجودة وتعلن التجميد وطابور التصحيح وشرط الرفع
    REC1-FREEZE-*   — بنود التجميد مفروضة في شجرة العمل لا في الوثيقة فقط
    REC1-BOUNDARY-* — Saleh- لا يحاول تعديل Binary- ولا يستضيفه ولا يعتمد عليه
    REC1-KTR-*      — أي معرفة عابرة للمستودعات تتطلب Knowledge Transfer Record
    REC1-MATRIX-*   — وثيقة المصفوفة قائمة ومربوطة ولا ترفع التجميد

Non-goals (هذه الاختبارات لا تنتج):
    No runtime implementation. No registry change. No rename. No YAML.
    No Binary- edits — Binary--side enforcement is REC-4, executed inside
    Binary- by the maintainer only (cross-write from Saleh- is FORBIDDEN).
"""
import re
from pathlib import Path

from qiyas_core.slot_geometry_core import LayerStatus
from qiyas_core.slot_geometry_core import master_registry_seed
from qiyas_core.slot_geometry_core.master_registry_seed import (
    LAYER_ID_P1_HARAKA_FUNCTION_CARRIER,
    _P1_LAYER_IDS,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC = REPO_ROOT / "src"
TESTS = REPO_ROOT / "tests"
DOCS = REPO_ROOT / "docs" / "qiyas_core"

RECOVERY_MAP = DOCS / "PROJECT_RECOVERY_CANONICAL_MAP.md"
BRIDGE = DOCS / "CROSS_REPOSITORY_KNOWLEDGE_BRIDGE.md"
MATRIX = DOCS / "REPOSITORY_RESPONSIBILITY_MATRIX.md"
CONTROL_FRAME = DOCS / "CANONICAL_ARCHITECTURE_CONTROL_FRAME.md"
LAYER_REGISTRY_DOC = DOCS / "LAYER_REGISTRY.md"

THIS_FILE = Path(__file__).resolve()

# Import statements only — a string literal mentioning binary_core (such as
# this constant) does not match, because the pattern is anchored to the
# from/import keyword at the start of a line.
BINARY_IMPORT = re.compile(r"^\s*(?:from|import)\s+binary_core\b", re.MULTILINE)

# Path markers that would indicate Saleh- code reaching into a sibling
# Binary- working tree.
SIBLING_TREE_MARKERS = ("../Binary-", "/Binary-/")

# Dependency declaration surfaces that must never name the other repository.
DEPENDENCY_FILES = (
    "requirements.txt",
    "requirements-dev.txt",
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _normalized(path: Path) -> str:
    """نص مُوحَّد البياض — يسمح بمطابقة الجمل الملتفّة على عدة أسطر."""
    return " ".join(_read(path).split())


def _python_sources(*roots: Path):
    for root in roots:
        for path in sorted(root.rglob("*.py")):
            yield path


# ─────────────────────────────────────────────────────────────────────────────
# REC1-MAP — الخريطة موجودة وتعلن التجميد
# ─────────────────────────────────────────────────────────────────────────────

class TestRec1MapExistsAndDeclaresFreeze:
    """REC1-MAP — خريطة الاسترداد موجودة وتعلن التجميد وطابور التصحيح."""

    def test_REC1_MAP_01_recovery_map_exists(self):
        """REC1-MAP-01: ملف الخريطة موجود في المسار القانوني."""
        assert RECOVERY_MAP.is_file(), (
            "docs/qiyas_core/PROJECT_RECOVERY_CANONICAL_MAP.md must exist"
        )

    def test_REC1_MAP_02_declares_project_freeze_in_effect(self):
        """REC1-MAP-02: الخريطة تعلن أن التجميد ساري المفعول."""
        assert "PROJECT FREEZE is in effect" in _read(RECOVERY_MAP)

    def test_REC1_MAP_03_freeze_forbids_all_seven_items(self):
        """REC1-MAP-03: بنود التجميد السبعة منصوصة حرفيًا."""
        text = _read(RECOVERY_MAP)
        for forbidden_line in (
            "لا PR-D جديد.",
            "لا P1 runtime.",
            "لا YAML implementation.",
            "لا Lambert W.",
            "لا metrics.",
            "لا HarakaFunction.",
            "لا LetterIdentity runtime.",
        ):
            assert forbidden_line in text, f"freeze line missing: {forbidden_line}"

    def test_REC1_MAP_04_freeze_release_requires_maintainer_after_rec1_to_rec4(self):
        """REC1-MAP-04: شرط رفع التجميد = تعليمات صريحة بعد اندماج REC-1 … REC-4."""
        normalized = _normalized(RECOVERY_MAP)
        assert (
            "the freeze lifts only by explicit maintainer instruction"
            in normalized
        )
        assert "REC-1 … REC-4" in normalized

    def test_REC1_MAP_05_corrective_queue_lists_rec0_to_rec6(self):
        """REC1-MAP-05: طابور التصحيح يضم REC-0 إلى REC-6."""
        text = _read(RECOVERY_MAP)
        for item in ("REC-0", "REC-1", "REC-2", "REC-3", "REC-4", "REC-5", "REC-6"):
            assert item in text, f"queue item missing: {item}"

    def test_REC1_MAP_06_out_of_queue_prs_are_rejected(self):
        """REC1-MAP-06: قانون الرفض — أي PR خارج الطابور أو خارج الترتيب مرفوض."""
        assert (
            "A PR not in this queue, or out of this order, is rejected while "
            "the freeze holds." in _normalized(RECOVERY_MAP)
        )

    def test_REC1_MAP_07_responsibility_matrix_names_three_repositories(self):
        """REC1-MAP-07: مصفوفة المسؤولية تسمي المستودعات الثلاثة وحدودها."""
        normalized = _normalized(RECOVERY_MAP)
        assert "Repository Responsibility Matrix" in normalized
        assert "`Binary-`" in normalized
        assert "`Saleh-`" in normalized
        assert "Arabic (future package/repo" in normalized
        assert (
            "Encoding / Unicode / WrittenSurface / SyllableBridgeExport"
            in normalized
        )

    def test_REC1_MAP_08_haraka_function_carrier_recorded_as_suspended(self):
        """REC1-MAP-08: تعليق HarakaFunctionCarrier مسجَّل مع الاسم التصحيحي."""
        normalized = _normalized(RECOVERY_MAP)
        assert "HarakaFunctionCarrier" in normalized
        assert "suspended" in normalized
        assert "HarakaMarkIdentityCarrier" in normalized


# ─────────────────────────────────────────────────────────────────────────────
# REC1-FREEZE — بنود التجميد مفروضة في شجرة العمل
# (file evidence + test enforcement — لا PASS داخل Markdown فقط)
# ─────────────────────────────────────────────────────────────────────────────

class TestRec1FreezeEnforcedInWorkingTree:
    """REC1-FREEZE — التجميد مفروض اختباريًا على الشجرة، لا وثائقيًا فقط."""

    def test_REC1_FREEZE_01_only_rec5_schema_surface_admitted(self):
        """REC1-FREEZE-01 (REC-5 narrow lift): لا حزمة YAML runtime — لا
        slot_geometry_yaml ولا examples. REC-5 admits ONLY schemas/slot_geometry/
        as the validated LayerSpec source (YAML files only); no other schemas/*
        subtree and no runtime package may appear."""
        # Still fully frozen — REC-5 did not touch these:
        assert not (SRC / "qiyas_core" / "slot_geometry_yaml").exists()
        assert not (REPO_ROOT / "examples").exists()
        # REC-5 narrow lift: schemas/ may exist, but ONLY with the slot_geometry
        # subtree, and that subtree may contain YAML source/schema files only.
        schemas_root = REPO_ROOT / "schemas"
        if schemas_root.exists():
            children = sorted(
                p.name for p in schemas_root.iterdir() if not p.name.startswith(".")
            )
            assert children == ["slot_geometry"], children
            for path in (schemas_root / "slot_geometry").rglob("*"):
                if path.is_file():
                    assert path.suffix in {".yaml", ".yml"}, path.name

    def test_REC1_FREEZE_02_no_lambert_w_machinery_in_src(self):
        """REC1-FREEZE-02: لا آلات Lambert W في src/ — لا اسم ملف ولا محتوى."""
        offenders = [
            path
            for path in _python_sources(SRC)
            if "lambert" in path.name.lower()
            or "lambert" in _read(path).lower()
        ]
        assert offenders == [], (
            f"Lambert W machinery is frozen; found in: {offenders}"
        )

    def test_REC1_FREEZE_03_no_metrics_package_beyond_logarithmic_measurement(self):
        """REC1-FREEZE-03: لا حزمة metrics جديدة تحت src/qiyas_core/."""
        assert not (SRC / "qiyas_core" / "metrics").exists()
        assert not (SRC / "qiyas_core" / "metrics.py").exists()

    def test_REC1_FREEZE_04_no_registry_builder_advances_p1_beyond_specified(self):
        """REC1-FREEZE-04: لا بانٍ في السجل يرفع أي طبقة P1 فوق SPECIFIED،
        إلا الاستثناء المُصرَّح به في SCG-P1 PR-1: الباني
        ``build_p1_atomic_carriers_implemented_registry`` يرفع **فقط** الطبقتين
        الذريتين LetterIdentityCarrier و HarakaMarkIdentityCarrier إلى
        IMPLEMENTED؛ تبقى ConditionedTypedSequence و PositionCarrier و
        SlotCandidate ≤ SPECIFIED، ويبقى المنع ساريًا لكل باقي البناة."""
        allowed = {LayerStatus.PLANNED, LayerStatus.SPECIFIED}
        # Narrow PR-1 carve-out (2026-06-17): exactly the two atomic carriers.
        pr1_builder = "build_p1_atomic_carriers_implemented_registry"
        atomic_carriers = {
            master_registry_seed.LAYER_ID_P1_LETTER_IDENTITY_CARRIER,
            master_registry_seed.LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER,
        }
        builders = [
            (name, value)
            for name, value in vars(master_registry_seed).items()
            if name.startswith("build_") and callable(value)
        ]
        assert builders, "registry builders must exist in master_registry_seed"
        for name, builder in builders:
            # Freeze fails closed: a builder that no longer takes zero
            # arguments is itself a queue change that must surface here.
            registry = builder()
            for layer_id in _P1_LAYER_IDS:
                status = registry.get(layer_id).status
                if name == pr1_builder and layer_id in atomic_carriers:
                    # Authorized PR-1 advancement of the two atomic carriers only.
                    assert status is LayerStatus.IMPLEMENTED, (
                        f"{name} must advance {layer_id} to IMPLEMENTED (PR-1)"
                    )
                    continue
                assert status in allowed, (
                    f"{name} advances {layer_id} to {status}; "
                    "P1 runtime is frozen except the PR-1 atomic carriers "
                    "(لا P1 runtime عدا الطبقتين الذريتين المُصرَّح بهما)"
                )

    def test_REC1_FREEZE_05_no_p1_implemented_builder_exists(self):
        """REC1-FREEZE-05: لا يوجد build_p1_implemented_registry — P1 مجمّدة."""
        assert not hasattr(master_registry_seed, "build_p1_implemented_registry")

    def test_REC1_FREEZE_06_suspended_haraka_function_layer_not_advanced(self):
        """REC1-FREEZE-06: الطبقة المعلَّقة HarakaFunctionCarrier باقية على SPECIFIED."""
        registry = master_registry_seed.build_p1_specified_registry()
        spec = registry.get(LAYER_ID_P1_HARAKA_FUNCTION_CARRIER)
        assert spec.status == LayerStatus.SPECIFIED


# ─────────────────────────────────────────────────────────────────────────────
# REC1-BOUNDARY — Saleh- لا يحاول تعديل Binary-
# ─────────────────────────────────────────────────────────────────────────────

class TestRec1SalehDoesNotTouchBinary:
    """REC1-BOUNDARY — لا استيراد، لا استضافة، لا مسار، لا اعتماد على Binary-."""

    def test_REC1_BOUNDARY_01_no_binary_core_import_in_src_or_tests(self):
        """REC1-BOUNDARY-01: لا استيراد لـ binary_core في src/ أو tests/ (FORBIDDEN-05)."""
        offenders = [
            path
            for path in _python_sources(SRC, TESTS)
            if BINARY_IMPORT.search(_read(path))
        ]
        assert offenders == [], (
            f"runtime dependency on Binary- is forbidden; found in: {offenders}"
        )

    def test_REC1_BOUNDARY_02_saleh_does_not_host_binary_core_package(self):
        """REC1-BOUNDARY-02: لا حزمة src/binary_core/ داخل Saleh- — الترميز حد Binary-."""
        assert not (SRC / "binary_core").exists()

    def test_REC1_BOUNDARY_03_no_sibling_binary_working_tree_paths(self):
        """REC1-BOUNDARY-03: لا مسارات إلى شجرة عمل Binary- مجاورة."""
        offenders = []
        for path in _python_sources(SRC, TESTS):
            if path == THIS_FILE:
                # This enforcement file names the forbidden markers in order
                # to forbid them; it is the single licensed exception.
                continue
            text = _read(path)
            if any(marker in text for marker in SIBLING_TREE_MARKERS):
                offenders.append(path)
        assert offenders == [], (
            f"cross-repo working-tree paths are forbidden; found in: {offenders}"
        )

    def test_REC1_BOUNDARY_04_no_dependency_declaration_on_binary(self):
        """REC1-BOUNDARY-04: ملفات الاعتمادات لا تسمّي Binary- أو binary_core."""
        for name in DEPENDENCY_FILES:
            path = REPO_ROOT / name
            if not path.exists():
                continue
            text = _read(path)
            assert "binary_core" not in text, f"{name} must not depend on binary_core"
            assert "Binary-" not in text, f"{name} must not depend on Binary-"


# ─────────────────────────────────────────────────────────────────────────────
# REC1-KTR — المعرفة العابرة للمستودعات تتطلب Knowledge Transfer Record
# ─────────────────────────────────────────────────────────────────────────────

class TestRec1KnowledgeTransferRecordRequired:
    """REC1-KTR — الجسر القرائي قائم، والكتابة المتبادلة ممنوعة، والنقل بسجل فقط."""

    def test_REC1_KTR_01_bridge_document_exists(self):
        """REC1-KTR-01: وثيقة الجسر موجودة في المسار القانوني."""
        assert BRIDGE.is_file(), (
            "docs/qiyas_core/CROSS_REPOSITORY_KNOWLEDGE_BRIDGE.md must exist"
        )

    def test_REC1_KTR_02_cross_read_allowed_cross_write_forbidden(self):
        """REC1-KTR-02: القراءة مسموحة، الكتابة ممنوعة، الاستيراد لا يُرخَّص إلا بسجل."""
        text = _read(BRIDGE)
        assert "Cross-read is allowed." in text
        assert "Cross-write is forbidden." in text
        assert (
            "Cross-import is forbidden unless licensed by a Knowledge "
            "Transfer Record." in _normalized(BRIDGE)
        )

    def test_REC1_KTR_03_bridge_enumerates_forbidden_01_to_08(self):
        """REC1-KTR-03: المحظورات الثمانية FORBIDDEN-01 … FORBIDDEN-08 منصوصة."""
        text = _read(BRIDGE)
        for index in range(1, 9):
            assert f"FORBIDDEN-0{index}" in text, f"FORBIDDEN-0{index} missing"

    def test_REC1_KTR_04_bridge_forbids_runtime_dependency_and_sharing(self):
        """REC1-KTR-04: لا اعتماد تشغيلي، لا نواة مشتركة، لا dataclass مشتركة."""
        normalized = _normalized(BRIDGE)
        assert "neither repository imports from the other at runtime" in normalized
        assert "no shared QiyasKernel or BinaryKernel" in normalized
        assert "no dataclass definition shared between repositories" in normalized

    def test_REC1_KTR_05_transfer_record_required_with_all_fields(self):
        """REC1-KTR-05: كل نقل معرفة يتطلب سجلًا بحقوله الثمانية."""
        normalized = _normalized(BRIDGE)
        assert (
            "Every time a discovery in one repository is applied to the "
            "other, a Knowledge Transfer Record must be filed" in normalized
        )
        text = _read(BRIDGE)
        for field in (
            "source_repository:",
            "target_repository:",
            "discovery:",
            "source_context:",
            "target_application:",
            "transfer_type:",
            "forbidden_in_this_transfer:",
            "result:",
        ):
            assert field in text, f"KTR field missing: {field}"

    def test_REC1_KTR_06_recovery_map_binds_to_bridge_and_ktr(self):
        """REC1-KTR-06: الخريطة تُلزِم بالجسر وبسجل نقل المعرفة."""
        normalized = _normalized(RECOVERY_MAP)
        assert "CROSS_REPOSITORY_KNOWLEDGE_BRIDGE.md" in normalized
        assert "Knowledge Transfer Record" in normalized


# ─────────────────────────────────────────────────────────────────────────────
# REC1-MATRIX — وثيقة المصفوفة المستقلة قائمة ومربوطة ولا ترفع التجميد
# ─────────────────────────────────────────────────────────────────────────────

class TestRec1MatrixDocumentStandsAndIsLinked:
    """REC1-MATRIX — ترقية §2 إلى وثيقة مستقلة مربوطة من وثيقتي الحوكمة."""

    def test_REC1_MATRIX_01_matrix_document_exists(self):
        """REC1-MATRIX-01: وثيقة المصفوفة موجودة في المسار القانوني."""
        assert MATRIX.is_file(), (
            "docs/qiyas_core/REPOSITORY_RESPONSIBILITY_MATRIX.md must exist"
        )

    def test_REC1_MATRIX_02_declares_three_repository_boundaries(self):
        """REC1-MATRIX-02: المصفوفة تطابق حدود الخريطة §2 للمستودعات الثلاثة."""
        normalized = _normalized(MATRIX)
        assert (
            "Encoding / Unicode / WrittenSurface / SyllableBridgeExport"
            in normalized
        )
        assert "qiyas_core" in normalized
        assert "slot_geometry_core" in normalized
        assert "Arabic (future package/repo" in normalized

    def test_REC1_MATRIX_03_declares_cross_write_forbidden_and_ktr(self):
        """REC1-MATRIX-03: المصفوفة تعلن منع الكتابة المتبادلة واشتراط السجل."""
        normalized = _normalized(MATRIX)
        assert "الكتابة المتبادلة ممنوعة" in normalized
        assert "Knowledge Transfer Record" in normalized

    def test_REC1_MATRIX_04_cross_linked_from_control_frame(self):
        """REC1-MATRIX-04: مربوطة من CANONICAL_ARCHITECTURE_CONTROL_FRAME.md."""
        assert "REPOSITORY_RESPONSIBILITY_MATRIX.md" in _read(CONTROL_FRAME)

    def test_REC1_MATRIX_05_cross_linked_from_layer_registry(self):
        """REC1-MATRIX-05: مربوطة من LAYER_REGISTRY.md."""
        assert "REPOSITORY_RESPONSIBILITY_MATRIX.md" in _read(LAYER_REGISTRY_DOC)

    def test_REC1_MATRIX_06_matrix_does_not_lift_the_freeze(self):
        """REC1-MATRIX-06: المصفوفة تنص على أنها لا ترفع التجميد."""
        normalized = _normalized(MATRIX)
        assert "does not lift the freeze" in normalized
        assert "REC-4" in normalized

    def test_REC1_MATRIX_07_matrix_cites_its_enforcement_tests(self):
        """REC1-MATRIX-07: المصفوفة تستشهد بملف اختبارات الإنفاذ (doc–code alignment)."""
        assert (
            "tests/qiyas_core/test_repository_responsibility_matrix.py"
            in _read(MATRIX)
        )

    def test_REC1_MATRIX_08_binary_side_enforcement_is_rec4_maintainer_only(self):
        """REC1-MATRIX-08: إنفاذ جهة Binary- مؤجَّل إلى REC-4 بيد الـ maintainer فقط."""
        normalized = _normalized(MATRIX)
        assert "REC-4" in normalized
        assert "maintainer only" in normalized
        assert "FORBIDDEN" in normalized
