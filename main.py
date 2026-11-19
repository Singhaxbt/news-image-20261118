"""Copy the entry image to the output directory.

The entry is a front-page newspaper image (entry.png) held in this
repository; this program simply copies it to /output/entry.png, so the
run is deterministic: the same bytes go out every time.
"""

import os
import shutil
import sys
from pathlib import Path


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        print(f"error: entry image not found: {source}", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    # Copy through a temporary file and rename, so a partial write can
    # never land as the output, then verify the copy byte-for-byte size.
    tmp = target.with_name("entry.png.tmp")
    shutil.copyfile(source, tmp)
    if tmp.stat().st_size != source.stat().st_size:
        tmp.unlink(missing_ok=True)
        print("error: copied image size mismatch", file=sys.stderr)
        return 1
    os.replace(tmp, target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
