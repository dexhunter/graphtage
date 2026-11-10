"""Time diffing two large JSON objects that share every key.

The documents are metrics snapshots: a few thousand scalar fields, a handful of
which changed. Key equality is decided by a linear scan, which is the bulk of
the runtime. Prints the diff cost so the result stays observable.
"""

import io
import json

from graphtage.json import build_tree
from graphtage.printer import Printer, set_default_printer

# Large enough that the key scan dominates process startup.
FIELDS = 3200


def snapshot(delta: int) -> dict[str, int]:
    """A flat JSON object of metric ids. ``delta`` bumps every seventh field."""
    return {
        f"metric.checkout.latency_ms.{i:05d}": i + (delta if i % 7 == 0 else 0)
        for i in range(FIELDS)
    }


def main() -> None:
    set_default_printer(Printer(out_stream=io.StringIO(), ansi_color=False, quiet=True))
    # Round-trip through the JSON parser so the strings are the ones a file load produces.
    before = build_tree(json.loads(json.dumps(snapshot(0))))
    after = build_tree(json.loads(json.dumps(snapshot(1))))
    diffed = before.diff(after)
    print(diffed.edited_cost())


if __name__ == "__main__":
    main()
