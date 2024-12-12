import ctcsound7
import time
import ctypes

assert ctcsound7.VERSION >= 7000

cs = ctcsound7.Csound()
cs.setOption('-odac')
cs.compileOrc(r'''

sr = 48000
0dbfs = 1
nchnls = 2

instr 1
  prints "init instr 1"
  if metro(10) == 1 then
    println "perf instr 1"
  endif
endin
''')


def proc(data):
    print("----", data)
    

cs.start()
thread = cs.performanceThread()
print(thread.processCallback())
data = ctcsound7.CsoundParams()
param = ctypes.c_void_p()
thread.setProcessCallback(proc, param)
thread.play()

thread.scoreEvent(0, "i", [1, 0, 10])


time.sleep(2)
thread.stop()
