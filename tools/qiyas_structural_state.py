"""qiyas_structural_state — terminal-visible unified structural verification.

Thin, read-only renderer over qiyas_core.qiyas_structural_verification. It is
potential-only and makes no semantic/hukm/i'rab/dalalah/meaning claim.

Run:
    PYTHONPATH=src:. python3 tools/qiyas_structural_state.py "شَاذّ عَدَّ بَيت ضَرَبَ"
"""

from __future__ import annotations

import sys

from qiyas_core.qiyas_structural_verification import (
    render_structural_verification,
    verify_text,
)


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print("usage: python3 tools/qiyas_structural_state.py <text>")
        return 2
    for v in verify_text(args[0]):
        print(render_structural_verification(v))
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
