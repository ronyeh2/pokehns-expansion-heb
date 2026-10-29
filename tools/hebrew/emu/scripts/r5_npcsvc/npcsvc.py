#!/usr/bin/env python3
"""hns.py plus the ops the r5 field NPC service tours (tours/r5_npcsvc/*.txt) use: everything
scripts/r5_latin/r5lat.py registers (fieldwatch, pick, drive, monset, setmoney, approachnpc, partyinfo,
flags, vars, bagseek, bagpocket, ...).

Run:  npcsvc.py tour ROM OUT --tours <emu>/tours/r5_npcsvc [--clip] [--only RE] [--rtc SECONDS]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EMU = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, EMU)
sys.path.insert(0, os.path.join(EMU, "scripts", "r5_latin"))
import hns  # noqa: E402
import r5lat  # noqa: E402,F401  (registers the r2-r5 ops)

from hns import script_op, HnsError, _arg  # noqa: E402


if __name__ == "__main__":
    sys.argv[0] = hns.__file__
    sys.exit(hns.main())
