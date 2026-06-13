"""Layer 4 LicensedSyllableCandidate terminal demo.

Run:
    PYTHONPATH=src:. python3 tools/qiyas_licensed_syllable_demo.py "بِ ضَ وَ يَ ضَرَبَ"

Authorization:
    Narrow Layer 4 authorization (2026-06-13) — potential-only runtime
    slice. Not a global REC freeze release; no Layer 5; no semantic
    runtime; no meaning / hukm / i'rab / dalalah / reality claim.

The tool calls the canonical runtime at
src/qiyas_core/licensed_syllable.py. It does not query GitHub, does not
call any external service, does not access any file or external data
source. The full output is whatever the canonical runtime returns.
"""

from __future__ import annotations

import sys

from qiyas_core.licensed_syllable import (
    analyze_licensed_syllables,
    render_licensed_syllable_analysis,
)


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print(
            "usage: python3 tools/qiyas_licensed_syllable_demo.py <vocalized-text>"
        )
        return 2
    text = args[0]
    analysis = analyze_licensed_syllables(text)
    print(render_licensed_syllable_analysis(analysis))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
