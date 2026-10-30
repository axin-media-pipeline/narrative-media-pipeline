"""Run inside an existing RVC Python environment. Not a bundled RVC implementation."""
import os
from pathlib import Path
import sys

root, source, model, output = map(Path, sys.argv[1:])
os.chdir(root)
sys.path.insert(0, str(root))
os.environ.update(weight_root=str(model.parent), rmvpe_root=str(root / "assets" / "rmvpe"),
                  RVC_CUDA_GRAPH="0", RVC_OFFLINE_CUDA_GRAPH="0",
                  PATH=str(root) + os.pathsep + os.environ.get("PATH", ""))
sys.argv = [sys.argv[0], "--noautoopen"]
import numpy as np
import soundfile as sf
from scipy.signal import resample_poly
from math import gcd
from configs.config import Config
from infer.vc.modules import VC

input_data, input_rate = sf.read(source, dtype="float32")
if input_data.ndim != 1 or input_rate != 48000:
    raise ValueError("Expected mono 48000 Hz input")
vc = VC(Config())
vc.get_vc(model.name)
status, result = vc.vc_single(0, str(source), 0, "rmvpe", "", 0, 0, .6, .33)
if result is None or result[1] is None:
    raise RuntimeError(str(status))
rate, converted = result
converted = np.asarray(converted, dtype=np.float32)
if converted.ndim != 1 or not len(converted) or not np.isfinite(converted).all():
    raise ValueError("Invalid RVC output")
if rate != input_rate:
    factor = gcd(int(rate), input_rate)
    converted = resample_poly(converted, input_rate // factor, int(rate) // factor)
difference = len(converted) - len(input_data)
if abs(difference) > round(input_rate * .1):
    raise ValueError(f"RVC duration differs by {difference / input_rate:.3f}s")
if difference < 0:
    converted = np.pad(converted, (0, -difference))
else:
    converted = converted[:len(input_data)]
sf.write(output, converted, input_rate, subtype="PCM_16")
print(f"RVC conversion complete; adjusted {difference} samples")
