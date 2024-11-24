
Introduction
============

Quick Start
-----------

.. note:: *csound* should be installed before this bindings can be.


Render in real-time
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    import ctcsound7 as ct
    csound = ct.Csound()
    # Output to the default audio device
    csound.setOption('-odac')

    # Compile some csound code
    csound.compileOrc(r'''

    sr = 44100   ; Modify to fit your system
    ksmps = 64
    nchnls = 2
    0dbfs = 1

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

    # Start csound
    csound.start()

    # Creates a performance thread to be able to run csound without blocking
    # python's main thread.
    thread = csound.performanceThread()
    thread.play()

    # Schedule an instance of instr 1 for 10 seconds
    thread.scoreEvent(0, "i", [1, 0, 10])

    input("Press any key to stop...\n")
    thread.stop()


Render offline
^^^^^^^^^^^^^^


.. code-block:: python

    import ctcsound7 as ct
    csound = ct.Csound()

    # Send output to a soundfile 'outfile.wav'. Other formats are supported: flac
    # mp3, ogg, aiff
    csound.setOption('-ooutfile.wav')
    csound.compileOrc(r'''

    sr = 44100
    ksmps = 64
    nchnls = 2
    0dbfs = 1

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
    csound.start()

    # Schedule an instance of instr 1 for 10 seconds
    csound.scoreEvent("i", [1, 0, 10])

    # End rendering at 10 seconds. Without this the main
    # loop keeps rendering silence
    csound.setEndMarker(10)

    # Perform until the end of the score
    while not csound.performKsmps():
        pass



--------------------------


Compatibility
-------------

**csound7** supports both csound 6 and csound 7 and provides a compatibility layer
so that the same code can be used for any version of csound. In csound 7 some methods
have been removed: these are marked clearly in the documentation. Their corresponding
method has been kept in the csound 6 API with the indication that they need to be
replaced with compatible alternatives in order to write future-proof code

Some examples:


**setSpinSample**

.. code-block:: python

    csound = Csound()
    ...
    # csound 6
    csound.addSpinSample(frame, channel, sample)

    # csound 7
    spin = csound.spin()
    spin[nchnls * frame + channel] = sample


**spoutSample**

.. code-block:: python

    # Csound 6
    samp = csound.spoutSample(frame, channel)

    # Csound 7
    spout = csound.spout()
    samp = spout[nchnls * frame + channel]
