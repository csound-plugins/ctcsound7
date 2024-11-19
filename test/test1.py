import ctcsound7 as ct
import ctcsound7._util as util
import sys

sr, rtmodule = ct.getSystemSr(module='')
print(":::::::::: System sr: ", sr)
if not (0 < sr <= 96000):
    print("Invalid samplerate")
    sys.exit(1)
util.testCsound(module=rtmodule, sr=sr)
