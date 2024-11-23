import ctcsound7 as ct
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outfile', default='test.wav')
parser.add_argument('-d', '--dur', default=10, type=int)
args = parser.parse_args()

cs = ct.Csound()

cs.setOption(f"-o{args.outfile}")
ext = os.path.splitext(args.outfile)[1]
if ext == '.flac':
    cs.setOption("--format=flac")
elif ext == '.mp3':
    cs.setOption("--mpeg")
elif ext == '.ogg':
    cs.setOption("--format=ogg")
    cs.setOption("--format=vorbis")
else:
    assert ext == '.wav'

cs.compileOrc(r'''
0dbfs = 1
ksmps = 64
nchnls = 2

instr 1
  kchan init -1
  kchan = (kchan + metro:k(1)) % nchnls
  if changed:k(kchan) == 1 then
    println "Channel: %d", kchan + 1
  endif
  asig = pinker() * 0.2
  outch kchan + 1, asig
endin
''')

cs.scoreEvent('i', [1, 0, args.dur])
cs.scoreEvent('e', [0, args.dur])
cs.start()

while not cs.performKsmps():
    print(".", end='')
    pass
print("\nFinished...")
