"""Time rendering a JSON diff whose payload is long unchanged strings.

A catalog of a few hundred records. One integer field changes in a few records;
the long description strings are untouched, so they are printed a character at a
time. Prints a hash of the rendered diff so the bytes stay observable.
"""

import hashlib
import io
import json

from graphtage.json import JSONFormatter, build_tree
from graphtage.printer import Printer, set_default_printer

RECORDS = 280
# Long enough that per-character printing, not import or matching, is the runtime.
DESCRIPTION = "alpha-beta-gamma-delta " * 216


def catalog(bump: bool) -> dict[str, dict[str, object]]:
    """Product catalog. ``bump`` increments ``stock`` on every eleventh sku."""
    return {
        f"sku-{i:04d}": {
            "name": f"Widget {i:04d}",
            "description": DESCRIPTION + f"{i:04d}",
            "stock": i + (1 if bump and i % 11 == 0 else 0),
        }
        for i in range(RECORDS)
    }


def main() -> None:
    set_default_printer(Printer(out_stream=io.StringIO(), ansi_color=False, quiet=True))
    before = build_tree(json.loads(json.dumps(catalog(False))))
    after = build_tree(json.loads(json.dumps(catalog(True))))
    diffed = before.diff(after)
    buf = io.StringIO()
    printer = Printer(out_stream=buf, ansi_color=False, quiet=True)
    with printer:
        JSONFormatter.DEFAULT_INSTANCE.print(printer, diffed)
    rendered = buf.getvalue()
    digest = hashlib.sha256(rendered.encode()).hexdigest()
    print(f"{len(rendered)} {digest}")


if __name__ == "__main__":
    main()
