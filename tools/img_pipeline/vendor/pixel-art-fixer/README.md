# pixelfixer (Python)

The reference implementation of the [Pixel Art Fixer](../README.md): the
clearest version of the detector and reconstructor, and the easiest to read,
hack on, and extend.

## Install

Requires Python 3.9+.

```bash
pip install -r requirements.txt        # numpy, scipy, opencv-python, Pillow
```

Or install the package (adds a `pixelfixer` command):

```bash
pip install -e .
```

## Command line

```bash
python -m pixelfixer.cli input.png                    # print detection JSON
python -m pixelfixer.cli input.png --extract out.png  # write the fixed pixel art
python -m pixelfixer.cli input.png --overlay grid.png # write a grid overlay
python -m pixelfixer.cli folder/ --json results.json  # batch a folder
```

## Library

Detect the grid and reconstruct the true pixel art:

```python
import numpy as np
from PIL import Image
from pixelfixer import detect
from pixelfixer.reconstruct import reconstruct

rgba = np.array(Image.open("input.png").convert("RGBA"))
r = detect(rgba)                       # {step_x, step_y, cols, rows, consensus, ...}
out = reconstruct(rgba, r["step_x"], r["step_y"], r["cols"], r["rows"])
Image.fromarray(out).save("out.png")
```

Or the single-call server entry point (bytes in, PNG bytes out):

```python
from pixelfixer.api import process

result = process(image_bytes)               # full quality
result = process(image_bytes, mode="fast")  # bounded latency
result = process(image_bytes, low_memory=True)
# result: cols, rows, step_x, step_y, consensus, confidence, png (bytes), timings
```

## Package layout

| module            | role                                                       |
|-------------------|------------------------------------------------------------|
| `core.py`         | the consensus + arbitration orchestrator (`detect`)        |
| `autocorr.py`     | banded-autocorrelation detector (precision leader)         |
| `runlengths.py`   | boundary-distance comb detector (fastest)                  |
| `selfsim.py`      | shift self-similarity detector (drift-robust)              |
| `fusion.py`, `channels.py` | fused spectral / tile evidence for arbitration    |
| `varcontrast.py`  | within-cell variance "square packer"                       |
| `reconsearch.py`  | distillability score (the octave/harmonic arbiter)         |
| `reconstruct.py`  | grid to true-pixel image (phase solve, cuts, pooling)      |
| `quantize.py`, `colorspace.py` | color helpers (k-means, Oklab)                |
| `api.py`          | server entry point (`process`)                             |
| `cli.py`          | command-line interface                                     |

The algorithm is documented in full in
[`../docs/HOW_IT_WORKS.md`](../docs/HOW_IT_WORKS.md). For servers and batch jobs,
the [Rust core](../rust/) produces identical answers 11-24x faster.
