"""
master_layer_registry.py — سجل الطبقات الرئيسي

هذا هو العمود الفقري لإدارة المشروع.
وظيفته أن يمنع أي طبقة أو PR خارج الخطة.

القانون:
    أي PR لا يذكر LayerSpec ID يُرفض.
    أي طبقة غير مسجلة لا يجوز تنفيذها.
    أي انتقال إلى طبقة في forbidden_direct_next يُحجب.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator

from .layer_spec import LayerSpec, LayerStatus


class RegistryViolation(Exception):
    """رُفع عند محاولة انتقال غير مرخص بين الطبقات."""
    pass


@dataclass
class MasterLayerRegistry:
    """
    سجل الطبقات الرئيسي.

    يحتوي على جميع LayerSpecs المسجلة ويُنفّذ:
        - منع الطبقات غير المسجلة
        - منع الانتقالات المحظورة (forbidden_direct_next)
        - التحقق من أن الـ origin موجود في السجل
        - إدارة حالة كل طبقة (planned → specified → implemented → audited → closed)
    """
    _layers: dict[str, LayerSpec] = field(default_factory=dict)

    def register(self, spec: LayerSpec) -> None:
        """تسجيل طبقة جديدة. يرفع RegistryViolation إذا كان الـ id مكررًا."""
        if spec.id in self._layers:
            raise RegistryViolation(
                f"Layer '{spec.id}' is already registered. "
                "لا يجوز تسجيل نفس الطبقة مرتين."
            )
        # تحقق من أن الـ origin مسجل (ما لم يكن ROOT)
        if spec.origin.layer_id != "ROOT" and spec.origin.layer_id not in self._layers:
            raise RegistryViolation(
                f"Layer '{spec.id}' references origin '{spec.origin.layer_id}' "
                "which is not yet registered. "
                "يجب تسجيل الأصل قبل الفرع — لا طبقة بلا أصل مسجل."
            )
        self._layers[spec.id] = spec

    def get(self, layer_id: str) -> LayerSpec:
        """جلب LayerSpec بمعرفه. يرفع KeyError إذا لم يُوجد."""
        if layer_id not in self._layers:
            raise RegistryViolation(
                f"Layer '{layer_id}' is not registered in MasterLayerRegistry. "
                "أي طبقة غير مسجلة لا يجوز تنفيذها."
            )
        return self._layers[layer_id]

    def assert_transition_allowed(self, from_layer_id: str, to_layer_id: str) -> None:
        """
        تحقق من أن الانتقال من from إلى to مسموح.

        يرفع RegistryViolation إذا:
            - to_layer_id في forbidden_direct_next للـ from
            - to_layer_id غير موجود في allowed_next_layer_ids (إذا محددة)
        """
        from_spec = self.get(from_layer_id)
        to_spec = self.get(to_layer_id)

        # فحص الانتقالات المحظورة صراحةً
        if to_layer_id in from_spec.forbidden_direct_next_layer_ids:
            raise RegistryViolation(
                f"Transition from '{from_layer_id}' to '{to_layer_id}' is FORBIDDEN. "
                f"Forbidden direct next: {from_spec.forbidden_direct_next_layer_ids}. "
                "هذا انتقال محظور مباشر — لا قفزة بلا تراخيص."
            )

        # فحص allowed_next (إذا محددة فهي ملزمة)
        if (
            from_spec.allowed_next_layer_ids
            and to_layer_id not in from_spec.allowed_next_layer_ids
        ):
            raise RegistryViolation(
                f"Transition from '{from_layer_id}' to '{to_layer_id}' is not in allowed_next. "
                f"Allowed next: {from_spec.allowed_next_layer_ids}."
            )

        # فحص allowed_previous في to (إذا محددة فهي ملزمة)
        if (
            to_spec.allowed_previous_layer_ids
            and from_layer_id not in to_spec.allowed_previous_layer_ids
        ):
            raise RegistryViolation(
                f"Layer '{to_layer_id}' does not accept '{from_layer_id}' as a previous layer. "
                f"Allowed previous: {to_spec.allowed_previous_layer_ids}."
            )

    def update_status(self, layer_id: str, new_status: LayerStatus) -> None:
        """تحديث حالة طبقة. يتحقق من الانتقال المنطقي."""
        spec = self.get(layer_id)
        _valid_transitions: dict[LayerStatus, tuple[LayerStatus, ...]] = {
            LayerStatus.PLANNED: (LayerStatus.SPECIFIED,),
            LayerStatus.SPECIFIED: (LayerStatus.IMPLEMENTED, LayerStatus.PLANNED),
            LayerStatus.IMPLEMENTED: (LayerStatus.AUDITED, LayerStatus.SPECIFIED),
            LayerStatus.AUDITED: (LayerStatus.CLOSED, LayerStatus.IMPLEMENTED),
            LayerStatus.CLOSED: (),
        }
        allowed_next_statuses = _valid_transitions.get(spec.status, ())
        if new_status not in allowed_next_statuses:
            raise RegistryViolation(
                f"Cannot transition layer '{layer_id}' from {spec.status} to {new_status}. "
                f"Allowed transitions: {allowed_next_statuses}."
            )
        # بوابة تبعية التنفيذ (implementation-dependency gate): لا تُنفَّذ طبقة
        # قبل تنفيذ أصلها. تُطبَّق فقط عند الانتقال إلى IMPLEMENTED.
        if new_status is LayerStatus.IMPLEMENTED:
            self._assert_origin_implemented(spec)
        # Python frozen dataclasses لا تُعدَّل — نُعيد التسجيل
        import dataclasses
        updated = dataclasses.replace(spec, status=new_status)
        self._layers[layer_id] = updated

    def _assert_origin_implemented(self, spec: LayerSpec) -> None:
        """
        بوابة تبعية التنفيذ (hybrid rule).

        لا يجوز نقل طبقة L إلى IMPLEMENTED إلا إذا كان أصلها O مُنفَّذًا:

            - O == ROOT                 → مسموح (لا أصل سابق).
            - O.phase == L.phase (INTRA) → يجب أن تكون طبقة الأصل O نفسها IMPLEMENTED.
            - O.phase != L.phase (CROSS) → يجب أن تكون كل طبقات O.phase IMPLEMENTED.
            - غير ذلك                    → RegistryViolation.

        يُفعّل القاعدة constitutional rule «لا قفزة بلا تراخيص» على مستوى الـ runtime:
        لا فرع مُنفَّذ بلا أصل مُنفَّذ. (companion downgrade rule مؤجَّل — راجع الملاحظة.)
        """
        origin_id = spec.origin.layer_id
        if origin_id == "ROOT":
            return
        origin = self.get(origin_id)
        if origin.phase == spec.phase:
            # INTRA edge: طبقة الأصل المحددة يجب أن تكون مُنفَّذة.
            if origin.status is not LayerStatus.IMPLEMENTED:
                raise RegistryViolation(
                    f"Cannot implement layer '{spec.id}': its origin layer "
                    f"'{origin_id}' (same phase {spec.phase}) is {origin.status}, "
                    f"not IMPLEMENTED. لا فرع مُنفَّذ بلا أصله المُنفَّذ."
                )
            return
        # CROSS edge: كل طبقات مرحلة الأصل يجب أن تكون مُنفَّذة.
        unimplemented = tuple(
            layer.id
            for layer in self._layers.values()
            if layer.phase == origin.phase and layer.status is not LayerStatus.IMPLEMENTED
        )
        if unimplemented:
            raise RegistryViolation(
                f"Cannot implement layer '{spec.id}': its origin phase "
                f"'{origin.phase}' is not fully IMPLEMENTED. "
                f"Pending layers: {unimplemented}. "
                "لا مرحلة لاحقة بلا اكتمال تنفيذ المرحلة الأصل."
            )

    def all_layers(self) -> Iterator[LayerSpec]:
        """إرجاع جميع الطبقات المسجلة."""
        return iter(self._layers.values())

    def layers_by_status(self, status: LayerStatus) -> tuple[LayerSpec, ...]:
        """إرجاع الطبقات بحالة محددة."""
        return tuple(s for s in self._layers.values() if s.status == status)

    def assert_layer_registered(self, layer_id: str) -> None:
        """تأكد أن الطبقة مسجلة. يُستخدم من PRs للتحقق قبل الكتابة."""
        self.get(layer_id)  # يرفع RegistryViolation إذا لم تُوجد

    def __len__(self) -> int:
        return len(self._layers)

    def __contains__(self, layer_id: str) -> bool:
        return layer_id in self._layers
