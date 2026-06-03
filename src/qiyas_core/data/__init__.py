"""qiyas_core.data — external data registries.

This subpackage holds external data registries (JSON, etc.) loaded by
sibling reader modules under `qiyas_core/`. The registries are
metadata only; they do not produce `Candidate` objects, do not use
`QiyasRule` or `QiyasKernel`, and do not license algebraic
transitions by themselves. See each registry's `constitutional_role`
field and the reader module's docstring.
"""
