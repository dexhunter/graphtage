"""Peak traced memory of diffing two unordered JSON arrays of distinct ids.

The ids share no values, so every pair is a candidate. Pricing that cross product
builds several full copies of the pair list at once; that spike is the peak.
Prints ``peak_memory_bytes`` and the diff cost.
"""

import gc
import io
import tracemalloc

from graphtage import BuildOptions
from graphtage.json import build_tree
from graphtage.printer import Printer, set_default_printer

IDS = 300


def identifiers(prefix: str) -> list[str]:
    return [f"{prefix}-{i:04d}" for i in range(IDS)]


def main() -> None:
    set_default_printer(Printer(out_stream=io.StringIO(), ansi_color=False, quiet=True))
    options = BuildOptions(ignore_list_order=True)
    before = build_tree(identifiers("alpha"), options=options)
    after = build_tree(identifiers("beta"), options=options)
    gc.collect()
    tracemalloc.start()
    diffed = before.diff(after)
    _current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"peak_memory_bytes={peak}")
    print(diffed.edited_cost())


if __name__ == "__main__":
    main()
