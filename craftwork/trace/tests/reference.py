"""The studio the kit's own tests run through: Productcraft, the first studio the kit served.

The kit holds no studio of its own (kit 0.9.0, #325), and the synthetic train in
`synth.py` is Productcraft-shaped (seven stages, two audit cycles, co-signs at 2
and 6), so the tests load Productcraft's profile from where it lives. It is read,
never copied. Engagements the tests build under `tmp_path` have no team folder
above them, so `$TRACEKIT_STUDIO` names this profile as the fallback, which the
CLI tests' subprocesses inherit too.
"""
import os
from pathlib import Path

from tracekit.studio import PROFILE_ENV, load_profile

REPO = Path(__file__).resolve().parents[3]
PROFILE = REPO / "productcraft" / "trace" / "studio.py"
os.environ.setdefault(PROFILE_ENV, str(PROFILE))
PRODUCTCRAFT = load_profile(PROFILE)
