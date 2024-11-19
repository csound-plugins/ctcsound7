from __future__ import annotations

import sys
import numpy as np
import warnings
import ctypes as ct

from .common import *
from . import _util
from . import _dll

import typing as _t

libcsound, libcsoundpath = _dll.csoundDLL()
libcspt = libcsound


class CsoundParams(ct.Structure):
    _fields_ = [("debug_mode", ct.c_int32),         # debug mode, 0 or 1
                ("buffer_frames", ct.c_int32),      # number of frames in in/out buffers
                ("hardware_buffer_frames", ct.c_int32), # ibid. hardware
                ("displays", ct.c_int32),           # graph displays, 0 or 1
                ("ascii_graphs", ct.c_int32),       # use ASCII graphs, 0 or 1
                ("postscript_graphs", ct.c_int32),  # use postscript graphs, 0 or 1
                ("message_level", ct.c_int32),      # message printout control
                ("tempo", ct.c_int32),              # tempo ("sets Beatmode)
                ("ring_bell", ct.c_int32),          # bell, 0 or 1
                ("use_cscore", ct.c_int32),         # use cscore for processing
                ("terminate_on_midi", ct.c_int32),  # terminate performance at the end
                                                    #   of midifile, 0 or 1
                ("heartbeat", ct.c_int32),          # print heart beat, 0 or 1
                ("defer_gen01_load", ct.c_int32),   # defer GEN01 load, 0 or 1
                ("midi_key", ct.c_int32),           # pfield to map midi key no
                ("midi_key_cps", ct.c_int32),       # pfield to map midi key no as cps
                ("midi_key_oct", ct.c_int32),       # pfield to map midi key no as oct
                ("midi_key_pch", ct.c_int32),       # pfield to map midi key no as pch
                ("midi_velocity", ct.c_int32),      # pfield to map midi velocity
                ("midi_velocity_amp", ct.c_int32),  # pfield to map midi velocity as amplitude
                ("no_default_paths", ct.c_int32),   # disable relative paths from files, 0 or 1
                ("number_of_threads", ct.c_int32),  # number of threads for multicore performance
                ("syntax_check_only", ct.c_int32),  # do not compile, only check syntax
                ("csd_line_counts", ct.c_int32),    # csd line error reporting
                ("compute_weights", ct.c_int32),    # deprecated, kept for backwards comp.
                ("realtime_mode", ct.c_int32),      # use realtime priority mode, 0 or 1
                ("sample_accurate", ct.c_int32),    # use sample-level score event accuracy
                ("sample_rate_override", MYFLT),    # overriding sample rate
                ("control_rate_override", MYFLT),   # overriding control rate
                ("nchnls_override", ct.c_int32),    # overriding number of out channels
                ("nchnls_i_override", ct.c_int32),  # overriding number of in channels
                ("e0dbfs_override", MYFLT),         # overriding 0dbfs
                ("daemon", ct.c_int32),             # daemon mode
                ("ksmps_override", ct.c_int32),     # ksmps override
                ("FFT_library", ct.c_int32)]        # fft_lib


#
# PVSDAT window types
#
PVS_WIN_HAMMING = 0
PVS_WIN_HANN = 1
PVS_WIN_KAISER = 2
PVS_WIN_CUSTOM = 3
PVS_WIN_BLACKMAN = 4
PVS_WIN_BLACKMAN_EXACT = 5
PVS_WIN_NUTTALLC3 = 6
PVS_WIN_BHARRIS_3 = 7
PVS_WIN_BHARRIS_MIN = 8
PVS_WIN_RECT = 9

#
# PVSDAT formats
#
PVS_AMP_FREQ = 0   # phase vocoder
PVS_AMP_PHASE = 1  # polar DFT
PVS_COMPLEX = 2    # rectangular DFT
PVS_TRACKS = 3     # amp, freq, phase, ID tracks

#
# Constants used by the bus interface (csoundGetChannelPtr() etc.).
#
CSOUND_CONTROL_CHANNEL = 1
CSOUND_AUDIO_CHANNEL  = 2
CSOUND_STRING_CHANNEL = 3
CSOUND_PVS_CHANNEL = 4
CSOUND_VAR_CHANNEL = 5
CSOUND_ARRAY_CHANNEL = 6

CSOUND_CHANNEL_TYPE_MASK = 15

CSOUND_INPUT_CHANNEL = 16
CSOUND_OUTPUT_CHANNEL = 32

CSOUND_CONTROL_CHANNEL_NO_HINTS = 0
CSOUND_CONTROL_CHANNEL_INT = 1
CSOUND_CONTROL_CHANNEL_LIN = 2
CSOUND_CONTROL_CHANNEL_EXP = 3


#
# Event types
#
CS_INSTR_EVENT = 0
CS_TABLE_EVENT = 1
CS_END_EVENT = 2


# Instantiation
libcsound.csoundInitialize.restype = ct.c_int32
libcsound.csoundInitialize.argtypes = [ct.c_int32]
libcsound.csoundCreate.restype = CSOUND_p
libcsound.csoundCreate.argtypes = [ct.py_object, ct.c_char_p]
libcsound.csoundDestroy.argtypes = [CSOUND_p]

# Attributes
libcsound.csoundGetVersion.restype = ct.c_int32
libcsound.csoundGetSr.restype = MYFLT
libcsound.csoundGetSr.argtypes = [CSOUND_p]
libcsound.csoundGetKr.restype = MYFLT
libcsound.csoundGetKr.argtypes = [CSOUND_p]
libcsound.csoundGetKsmps.restype = ct.c_uint32
libcsound.csoundGetKsmps.argtypes = [CSOUND_p]
libcsound.csoundGetChannels.restype = ct.c_uint32
libcsound.csoundGetChannels.argtypes = [CSOUND_p, ct.c_int32]
libcsound.csoundGet0dBFS.restype = MYFLT
libcsound.csoundGet0dBFS.argtypes = [CSOUND_p]
libcsound.csoundGetA4.restype = MYFLT
libcsound.csoundGetA4.argtypes = [CSOUND_p]
libcsound.csoundGetCurrentTimeSamples.restype = ct.c_int64
libcsound.csoundGetCurrentTimeSamples.argtypes = [CSOUND_p]
libcsound.csoundGetSizeOfMYFLT.restype = ct.c_int32
libcsound.csoundGetHostData.restype = ct.py_object
libcsound.csoundGetHostData.argtypes = [CSOUND_p]
libcsound.csoundSetHostData.argtypes = [CSOUND_p, ct.py_object]
libcsound.csoundGetEnv.restype = ct.c_char_p
libcsound.csoundGetEnv.argtypes = [CSOUND_p, ct.c_char_p]
libcsound.csoundSetGlobalEnv.restype = ct.c_int32
libcsound.csoundSetGlobalEnv.argtypes = [ct.c_char_p, ct.c_char_p]
libcsound.csoundSetOption.restype = ct.c_int32
libcsound.csoundSetOption.argtypes = [CSOUND_p, ct.c_char_p]
libcsound.csoundGetParams.argtypes = [CSOUND_p, ct.POINTER(CsoundParams)]
libcsound.csoundGetDebug.restype = ct.c_int32
libcsound.csoundGetDebug.argtypes = [CSOUND_p]
libcsound.csoundSetDebug.argtypes = [CSOUND_p, ct.c_int32]
libcsound.csoundSystemSr.restype = MYFLT
libcsound.csoundSystemSr.argtypes = [CSOUND_p, MYFLT]
libcsound.csoundGetModule.restype = ct.c_int32
libcsound.csoundGetModule.argtypes = [CSOUND_p, ct.c_int,
                                        ct.POINTER(ct.c_char_p), ct.POINTER(ct.c_char_p)]
libcsound.csoundGetAudioDevList.restype = ct.c_int32
libcsound.csoundGetAudioDevList.argtypes = [CSOUND_p, ct.c_void_p, ct.c_int32]
libcsound.csoundGetMIDIDevList.restype = ct.c_int32
libcsound.csoundGetMIDIDevList.argtypes = [CSOUND_p, ct.c_void_p, ct.c_int32]
libcsound.csoundGetMessageLevel.restype = ct.c_int32
libcsound.csoundSetMessageLevel.argtypes = [CSOUND_p, ct.c_int32]

# Performance
libcsound.csoundCompile.restype = ct.c_int32
libcsound.csoundCompile.argtypes = [CSOUND_p, ct.c_int32, ct.POINTER(ct.c_char_p)]
libcsound.csoundCompileOrc.restype = ct.c_int32
libcsound.csoundCompileOrc.argtypes = [CSOUND_p, ct.c_char_p, ct.c_int32]
libcsound.csoundEvalCode.restype = MYFLT
libcsound.csoundEvalCode.argtypes = [CSOUND_p, ct.c_char_p]
libcsound.csoundCompileCSD.restype = ct.c_int32
libcsound.csoundCompileCSD.argtypes = [CSOUND_p, ct.c_char_p, ct.c_int32]
libcsound.csoundStart.restype = ct.c_int32
libcsound.csoundStart.argtypes = [CSOUND_p]
libcsound.csoundPerformKsmps.restype = ct.c_int32
libcsound.csoundPerformKsmps.argtypes = [CSOUND_p]
libcsound.csoundRunUtility.restype = ct.c_int32
libcsound.csoundRunUtility.argtypes = [CSOUND_p, ct.c_char_p, ct.c_int32, ct.POINTER(ct.c_char_p)]
libcsound.csoundReset.argtypes = [CSOUND_p]

# Realtime Audio I/O
libcsound.csoundSetHostAudioIO.argtypes = [CSOUND_p]
libcsound.csoundSetRTAudioModule.argtypes = [CSOUND_p, ct.c_char_p]
libcsound.csoundGetSpin.restype = ct.POINTER(MYFLT)
libcsound.csoundGetSpin.argtypes = [CSOUND_p]
libcsound.csoundGetSpout.restype = ct.POINTER(MYFLT)
libcsound.csoundGetSpout.argtypes = [CSOUND_p]

# Realtime MIDI I/O
libcsound.csoundSetHostMIDIIO.argtypes = [CSOUND_p]
libcsound.csoundSetMIDIModule.argtypes = [CSOUND_p, ct.c_char_p]
MIDIINOPENFUNC = ct.CFUNCTYPE(ct.c_int32, CSOUND_p, ct.POINTER(ct.c_void_p), ct.c_char_p)
MIDIREADFUNC = ct.CFUNCTYPE(ct.c_int32, CSOUND_p, ct.c_void_p, ct.c_char_p, ct.c_int32)
MIDIINCLOSEFUNC = ct.CFUNCTYPE(ct.c_int32, CSOUND_p, ct.c_void_p)
MIDIOUTOPENFUNC = ct.CFUNCTYPE(ct.c_int32, CSOUND_p, ct.POINTER(ct.c_void_p), ct.c_char_p)
MIDIWRITEFUNC = ct.CFUNCTYPE(ct.c_int32, CSOUND_p, ct.c_void_p, ct.c_char_p, ct.c_int32)
MIDIOUTCLOSEFUNC = ct.CFUNCTYPE(ct.c_int32, CSOUND_p, ct.c_void_p)
MIDIERRORFUNC = ct.CFUNCTYPE(ct.c_char_p, ct.c_int32)
MIDIDEVLISTFUNC = ct.CFUNCTYPE(ct.c_int32, CSOUND_p, ct.POINTER(CsoundMidiDevice), ct.c_int32)
libcsound.csoundSetExternalMidiInOpenCallback.argtypes = [CSOUND_p, MIDIINOPENFUNC]
libcsound.csoundSetExternalMidiReadCallback.argtypes = [CSOUND_p, MIDIREADFUNC]
libcsound.csoundSetExternalMidiInCloseCallback.argtypes = [CSOUND_p, MIDIINCLOSEFUNC]
libcsound.csoundSetExternalMidiOutOpenCallback.argtypes = [CSOUND_p, MIDIOUTOPENFUNC]
libcsound.csoundSetExternalMidiWriteCallback.argtypes = [CSOUND_p, MIDIWRITEFUNC]
libcsound.csoundSetExternalMidiOutCloseCallback.argtypes = [CSOUND_p, MIDIOUTCLOSEFUNC]
libcsound.csoundSetExternalMidiErrorStringCallback.argtypes = [CSOUND_p, MIDIERRORFUNC]
libcsound.csoundSetMIDIDeviceListCallback.argtypes = [CSOUND_p, MIDIDEVLISTFUNC]

# Messages
libcsound.csoundMessage.argtypes = [CSOUND_p, ct.c_char_p, ct.c_char_p]
libcsound.csoundMessageS.argtypes = [CSOUND_p, ct.c_int32, ct.c_char_p, ct.c_char_p]
MSGSTRFUNC = ct.CFUNCTYPE(None, CSOUND_p, ct.c_int32, ct.c_char_p)
libcsound.csoundSetMessageStringCallback.argtypes = [CSOUND_p, MSGSTRFUNC]
libcsound.csoundCreateMessageBuffer.argtypes = [CSOUND_p, ct.c_int32]
libcsound.csoundGetFirstMessage.restype = ct.c_char_p
libcsound.csoundGetFirstMessage.argtypes = [CSOUND_p]
libcsound.csoundGetFirstMessageAttr.restype = ct.c_int32
libcsound.csoundGetFirstMessageAttr.argtypes = [CSOUND_p]
libcsound.csoundPopFirstMessage.argtypes = [CSOUND_p]
libcsound.csoundGetMessageCnt.restype = ct.c_int32
libcsound.csoundGetMessageCnt.argtypes = [CSOUND_p]
libcsound.csoundDestroyMessageBuffer.argtypes = [CSOUND_p]

# Channels, Controls and Events
libcsound.csoundGetChannelPtr.restype = ct.c_int32
libcsound.csoundGetChannelPtr.argtypes = [CSOUND_p, ct.POINTER(ct.c_void_p),
                                            ct.c_char_p, ct.c_int32]
libcsound.csoundGetChannelVarTypeName.restype = ct.c_char_p
libcsound.csoundGetChannelVarTypeName.argtypes = [CSOUND_p, ct.c_char_p]
libcsound.csoundListChannels.restype = ct.c_int32
libcsound.csoundListChannels.argtypes = [CSOUND_p, ct.POINTER(ct.POINTER(ControlChannelInfo))]
libcsound.csoundDeleteChannelList.argtypes = [CSOUND_p, ct.POINTER(ControlChannelInfo)]
libcsound.csoundSetControlChannelHints.restype = ct.c_int32
libcsound.csoundSetControlChannelHints.argtypes = [CSOUND_p, ct.c_char_p, ControlChannelHints]
libcsound.csoundGetControlChannelHints.restype = ct.c_int32
libcsound.csoundGetControlChannelHints.argtypes = [CSOUND_p, ct.c_char_p,
                                                    ct.POINTER(ControlChannelHints)]
libcsound.csoundLockChannel.argtypes = [CSOUND_p, ct.c_char_p]
libcsound.csoundUnlockChannel.argtypes = [CSOUND_p, ct.c_char_p]
libcsound.csoundGetControlChannel.restype = MYFLT
libcsound.csoundGetControlChannel.argtypes = [CSOUND_p, ct.c_char_p, ct.POINTER(ct.c_int32)]
libcsound.csoundSetControlChannel.argtypes = [CSOUND_p, ct.c_char_p, MYFLT]
libcsound.csoundGetAudioChannel.argtypes = [CSOUND_p, ct.c_char_p, ct.POINTER(MYFLT)]
libcsound.csoundSetAudioChannel.argtypes = [CSOUND_p, ct.c_char_p, ct.POINTER(MYFLT)]
libcsound.csoundGetStringChannel.argtypes = [CSOUND_p, ct.c_char_p, ct.c_char_p]
libcsound.csoundSetStringChannel.argtypes = [CSOUND_p, ct.c_char_p, ct.c_char_p]

libcsound.csoundInitArrayChannel.restype = ARRAYDAT_p
libcsound.csoundInitArrayChannel.argtypes = [CSOUND_p, ct.c_char_p, ct.c_char_p,
                                                ct.c_int32, ct.POINTER(ct.c_int32)]
libcsound.csoundArrayDataType.restype = ct.c_char_p
libcsound.csoundArrayDataType.argtypes = [ARRAYDAT_p]
libcsound.csoundArrayDataDimensions.restype = ct.c_int32
libcsound.csoundArrayDataDimensions.argtypes = [ARRAYDAT_p]
libcsound.csoundArrayDataSizes.restype = ct.POINTER(ct.c_int32)
libcsound.csoundArrayDataSizes.argtypes = [ARRAYDAT_p]
libcsound.csoundSetArrayData.argtypes = [ARRAYDAT_p, ct.c_void_p]
libcsound.csoundGetArrayData.restype = ct.c_void_p
libcsound.csoundGetArrayData.argtypes = [ARRAYDAT_p]
libcsound.csoundGetStringData.restype = ct.c_char_p
libcsound.csoundGetStringData.argtypes = [CSOUND_p, STRINGDAT_p]
libcsound.csoundSetStringData.argtypes = [CSOUND_p, STRINGDAT_p, ct.c_char_p]
libcsound.csoundInitPvsChannel.restype = PVSDAT_p
libcsound.csoundInitPvsChannel.argtypes = [CSOUND_p, ct.c_char_p,
                                            ct.c_int32, ct.c_int32, ct.c_int32,
                                            ct.c_int32, ct.c_int32]
libcsound.csoundPvsDataFFTSize.restype = ct.c_int32
libcsound.csoundPvsDataFFTSize.argtypes = [PVSDAT_p]
libcsound.csoundPvsDataOverlap.restype = ct.c_int32
libcsound.csoundPvsDataOverlap.argtypes = [PVSDAT_p]
libcsound.csoundPvsDataWindowSize.restype = ct.c_int32
libcsound.csoundPvsDataWindowSize.argtypes = [PVSDAT_p]
libcsound.csoundPvsDataFormat.restype = ct.c_int32
libcsound.csoundPvsDataFormat.argtypes = [PVSDAT_p]
libcsound.csoundPvsDataFramecount.restype = ct.c_uint32
libcsound.csoundPvsDataFramecount.argtypes = [PVSDAT_p]
libcsound.csoundGetPvsData.restype = ct.POINTER(ct.c_float)
libcsound.csoundGetPvsData.argtypes = [PVSDAT_p]
libcsound.csoundSetPvsData.argtypes = [PVSDAT_p, ct.POINTER(ct.c_float)]
libcsound.csoundGetChannelDatasize.restype = ct.c_int32
libcsound.csoundGetChannelDatasize.argtypes = [CSOUND_p, ct.c_char_p]
CHANNELFUNC = ct.CFUNCTYPE(None, CSOUND_p, ct.c_char_p, ct.c_void_p, ct.c_void_p)
libcsound.csoundSetInputChannelCallback.argtypes = [CSOUND_p, CHANNELFUNC]
libcsound.csoundSetOutputChannelCallback.argtypes = [CSOUND_p, CHANNELFUNC]
libcsound.csoundEvent.argtypes = [CSOUND_p, ct.c_int32, ct.POINTER(MYFLT),
                                    ct.c_int32, ct.c_int32]
libcsound.csoundEventString.argtypes = [CSOUND_p, ct.c_char_p, ct.c_int32]
libcsound.csoundKeyPress.argtypes = [CSOUND_p, ct.c_char]
KEYBOARDFUNC = ct.CFUNCTYPE(ct.c_int32, ct.py_object, ct.c_void_p, ct.c_uint32)
libcsound.csoundRegisterKeyboardCallback.restype = ct.c_int32
libcsound.csoundRegisterKeyboardCallback.argtypes = [CSOUND_p, KEYBOARDFUNC,
                                                        ct.py_object, ct.c_uint32]
libcsound.csoundRemoveKeyboardCallback.argtypes = [CSOUND_p, KEYBOARDFUNC]

# Tables
libcsound.csoundTableLength.restype = ct.c_int32
libcsound.csoundTableLength.argtypes = [CSOUND_p, ct.c_int32]
libcsound.csoundGetTable.restype = ct.c_int32
libcsound.csoundGetTable.argtypes = [CSOUND_p, ct.POINTER(ct.POINTER(MYFLT)), ct.c_int32]
libcsound.csoundGetTableArgs.restype = ct.c_int32
libcsound.csoundGetTableArgs.argtypes = [CSOUND_p, ct.POINTER(ct.POINTER(MYFLT)), ct.c_int32]

# Score Handling
libcsound.csoundGetScoreTime.restype = ct.c_double
libcsound.csoundGetScoreTime.argtypes = [CSOUND_p]
libcsound.csoundIsScorePending.restype = ct.c_int32
libcsound.csoundIsScorePending.argtypes = [CSOUND_p]
libcsound.csoundSetScorePending.argtypes = [CSOUND_p, ct.c_int32]
libcsound.csoundGetScoreOffsetSeconds.restype = MYFLT
libcsound.csoundGetScoreOffsetSeconds.argtypes = [CSOUND_p]
libcsound.csoundSetScoreOffsetSeconds.argtypes = [CSOUND_p, MYFLT]
libcsound.csoundRewindScore.argtypes = [CSOUND_p]
libcsound.csoundSleep.argtypes = [ct.c_size_t]

# Opcodes
libcsound.csoundLoadPlugins.restype = ct.c_int32
libcsound.csoundLoadPlugins.argtypes = [CSOUND_p, ct.c_char_p]
OPCODEFUNC = ct.CFUNCTYPE(ct.c_int32, CSOUND_p, ct.c_void_p)
libcsound.csoundAppendOpcode.restype = ct.c_int32
libcsound.csoundAppendOpcode.argtypes = [CSOUND_p, ct.c_char_p, ct.c_int32,
    ct.c_int32, ct.c_char_p, ct.c_char_p,
    OPCODEFUNC, OPCODEFUNC, OPCODEFUNC]


# Symbols for Windat.polarity field
NOPOL = 0
NEGPOL = 1
POSPOL = 2
BIPOL = 3

# Table display (from graph_display.h)
libcsound.csoundSetIsGraphable.argtypes = [CSOUND_p, ct.c_int]


MAKEGRAPHFUNC = ct.CFUNCTYPE(None, ct.c_void_p, ct.POINTER(Windat), ct.c_char_p)
libcsound.csoundSetMakeGraphCallback.argtypes = [CSOUND_p, MAKEGRAPHFUNC]
DRAWGRAPHFUNC = ct.CFUNCTYPE(None, ct.c_void_p, ct.POINTER(Windat))
libcsound.csoundSetDrawGraphCallback.argtypes = [CSOUND_p, DRAWGRAPHFUNC]
KILLGRAPHFUNC = ct.CFUNCTYPE(None, ct.c_void_p, ct.POINTER(Windat))
libcsound.csoundSetKillGraphCallback.argtypes = [CSOUND_p, KILLGRAPHFUNC]
EXITGRAPHFUNC = ct.CFUNCTYPE(ct.c_int32, ct.c_void_p)
libcsound.csoundSetExitGraphCallback.argtypes = [CSOUND_p, EXITGRAPHFUNC]

# Circular buffer functions (from circular_buffer.h)
libcsound.csoundCreateCircularBuffer.restype = ct.c_void_p
libcsound.csoundCreateCircularBuffer.argtypes = [CSOUND_p, ct.c_int32, ct.c_int32]
libcsound.csoundReadCircularBuffer.restype = ct.c_int32
libcsound.csoundReadCircularBuffer.argtypes = [CSOUND_p, ct.c_void_p, ct.c_void_p, ct.c_int32]
libcsound.csoundPeekCircularBuffer.restype = ct.c_int32
libcsound.csoundPeekCircularBuffer.argtypes = [CSOUND_p, ct.c_void_p, ct.c_void_p, ct.c_int32]
libcsound.csoundWriteCircularBuffer.restype = ct.c_int32
libcsound.csoundWriteCircularBuffer.argtypes = [CSOUND_p, ct.c_void_p, ct.c_void_p, ct.c_int32]
libcsound.csoundFlushCircularBuffer.argtypes = [CSOUND_p, ct.c_void_p]
libcsound.csoundDestroyCircularBuffer.argtypes = [CSOUND_p, ct.c_void_p]

OPENSOUNDFILEFUNC = ct.CFUNCTYPE(ct.c_void_p, CSOUND_p, ct.c_char_p, ct.c_int32, ct.c_void_p)
libcsound.csoundSetOpenSoundFileCallback.argtypes = [CSOUND_p, OPENSOUNDFILEFUNC]
OPENFILEFUNC = ct.CFUNCTYPE(ct.c_void_p, CSOUND_p, ct.c_char_p, ct.c_char_p)
libcsound.csoundSetOpenFileCallback.argtypes = [CSOUND_p, OPENFILEFUNC]

_scoreEventToTypenum = {
    'i': CS_INSTR_EVENT,
    'f': CS_TABLE_EVENT,
    'e': CS_END_EVENT
}


class Csound:
    """
    This class represents an instance of a csound process

    Args:
        hostData: any data, will be accessible within certain callbacks
        opcodeDir: the folder where to load opcodes from. If not given,
            default folders are used
        pointer: if given, the result of calling libcsound.csoundCreate(...),
            uses the given csound process instead of creating a new one

    Attributes:
        cs: a pointer to a csound process
        fromPointer: True if the csound process was given at creation, False
            if it was created by this instance itself

    """
    #
    # Instantiation
    #
    def __init__(self, hostData=None, opcodeDir='', pointer: ct.c_void_p = None):
        """Creates an instance of Csound.

        The hostData parameter can be None, or it can be any sort of data; these
        data can be accessed from the Csound instance that is passed to callback routines.
        If not None the opcodeDir parameter sets an override for the plugin module/opcode
        directory search.
        """
        if pointer:
            self.cs = pointer
            self.fromPointer = True
        else:
            opcdir = cstring(opcodeDir) if opcodeDir else ct.c_char_p()
            self.cs = libcsound.csoundCreate(ct.py_object(hostData), opcdir)
            self.fromPointer = False

        self._callbacks: dict[str, ct._FuncPointer] = {}
        """Holds any callback set"""

        self._perfthread: CsoundPerformanceThread | None = None
        """Holds the PerformanceThread attached to this csound instance, if any"""

    def __del__(self):
        """Destroys an instance of Csound."""
        if self._perfthread:
            self._perfthread = None  # This should destroy the performance thread

        if not self.fromPointer and libcsound:
            libcsound.csoundDestroy(self.cs)

    def csound(self) -> CSOUND_p:
        """
        Returns the opaque pointer to the underlying CSOUND struct.

        This pointer is needed to instantiate a CsoundPerformanceThread object.
        """
        return self.cs

    def performanceThread(self) -> CsoundPerformanceThread:
        """
        Returns a CsoundPerformanceThread attached to this csound instance

        Since there can be only one performance thread for each instance,
        calling this method repeatedly always returns the same thread as
        long as the thread has not been joint
        """
        if self._perfthread is None:
            self._perfthread = CsoundPerformanceThread(self.cs)
        return self._perfthread

    #
    # Attributes
    #
    def version(self) -> int:
        """Returns the version number times 1000 (5.00.0 = 5000)."""
        return libcsound.csoundGetVersion()

    def sr(self) -> float:
        """Returns the number of audio sample frames per second."""
        return libcsound.csoundGetSr(self.cs)

    def kr(self) -> float:
        """Returns the number of control samples per second."""
        return libcsound.csoundGetKr(self.cs)

    def ksmps(self) -> int:
        """Returns the number of audio sample frames per control sample."""
        return libcsound.csoundGetKsmps(self.cs)

    def nchnls(self) -> int:
        return libcsound.csoundGetChannels(self.cs, ct.c_int32(0))

    def nchnlsInput(self) -> int:
        return libcsound.csoundGetChannels(self.cs, ct.c_int32(1))

    def get0dBFS(self) -> float:
        """Returns the 0dBFS level of the spin/spout buffers."""
        return libcsound.csoundGet0dBFS(self.cs)

    def A4(self) -> float:
        """Returns the A4 frequency reference."""
        return libcsound.csoundGetA4(self.cs)

    def currentTimeSamples(self) -> int:
        """Returns the current performance time in samples."""
        return libcsound.csoundGetCurrentTimeSamples(self.cs)

    def sizeOfMYFLT(self) -> int:
        """Returns the size of MYFLT in bytes."""
        return libcsound.csoundGetSizeOfMYFLT()

    def hostData(self) -> ct.c_void_p:
        """Returns host data."""
        return libcsound.csoundGetHostData(self.cs)

    def setHostData(self, data) -> None:
        """
        Sets host data.

        Args:
            data: can be any data
        """
        libcsound.csoundSetHostData(self.cs, ct.py_object(data))

    def env(self, name: str) -> str | None:
        """Gets the value of environment variable name.

        Args:
            name: the environment variable

        Returns:
            the value or None if no such variable is found

        The searching order is: local environment of Csound,
        variables set with :meth:`Csound.setGlobalEnv`, and system environment variables.
        Should be called after compile_().
        Return value is None if the variable is not set.
        """
        ret = libcsound.csoundGetEnv(self.cs, cstring(name))
        if (ret):
            return pstring(ret)
        return None

    def setGlobalEnv(self, name: str, value: str | None) -> int:
        """Set the global value of environment variable name to value.

        Args:
            name: the name of the environment variable
            value: the value of the variable, or None to delete the variable

        Returns:
            0 if successfull, non-zero otherwise

        .. note::  It is not safe to call this function while any Csound instances
            are active.

        """
        return libcsound.csoundSetGlobalEnv(cstring(name), cstring(value) if value is not None else ct.c_char_p())

    def setOption(self, option: str):
        """Set csound option (flag).

        This needs to be called before any code is compiled.
        Multiple options are allowed in one string.
        Returns zero on success.
        """
        return libcsound.csoundSetOption(self.cs, cstring(option))

    def params(self, params: CsoundParams) -> None:
        """Gets the current set of parameters from a CSOUND instance.

        These parameters are in a CsoundParams structure.

        .. seealso:: :meth:`Csound.setParams`
        """
        libcsound.csoundGetParams(self.cs, ct.byref(params))

    def debug(self) -> bool:
        """Returns whether Csound is set to print debug messages.

        Those messages are sent through the DebugMsg() internal API
        function.
        """
        return libcsound.csoundGetDebug(self.cs) != 0

    def setDebug(self, debug: bool) -> None:
        """Sets whether Csound prints debug messages.

        The debug argument must have value True or False.
        Those messages come from the DebugMsg() internal API function.
        """
        libcsound.csoundSetDebug(self.cs, ct.c_int32(debug))

    def systemSr(self, val: int = 0) -> float:
        """If val > 0, sets the internal variable holding the system HW sr.

        Returns the stored value containing the system HW sr.
        """
        return libcsound.csoundSystemSr(self.cs, val)

    def module(self, number: int) -> tuple[str, str, int]:
        """Retrieves a module name and type given a number.

        Type is "audio" or "midi". Modules are added to list as csound loads
        them. Return CSOUND_SUCCESS on success and CSOUND_ERROR if module
        number was not found::

            n = 0
            while True:
                name, type_, err = cs.module(n)
                if err == ctcsound.CSOUND_ERROR:
                    break
                print("Module {}: {} ({})\n".format(n, name, type_))
                n += 1
        """
        name = ct.pointer(ct.c_char_p(cstring("dummy")))
        type_ = ct.pointer(ct.c_char_p(cstring("dummy")))
        err = libcsound.csoundGetModule(self.cs, ct.c_int32(number), name, type_)
        if err == CSOUND_ERROR:
            return '', '', err
        n = pstring(ct.string_at(name.contents))
        t = pstring(ct.string_at(type_.contents))
        return n, t, err

    def audioDevList(self, isOutput: bool) -> list[AudioDevice]:
        """Returns a list of available input and output audio devices.

        Each item in the list is a :class:`AudioDevice` with attributes
        ``deviceName``, ``deviceId``, ``rtModule``, ``masNchnls``,
        ``isOutput``

        Must be called after an orchestra has been compiled
        to get meaningful information.
        """
        n = libcsound.csoundGetAudioDevList(self.cs, None, ct.c_int32(isOutput))
        devs = (CsoundAudioDevice * n)()
        libcsound.csoundGetAudioDevList(self.cs, ct.byref(devs), ct.c_int32(isOutput))
        lst = []
        for dev in devs:
            d = AudioDevice(deviceName=pstring(dev.device_name),
                            deviceId=pstring(dev.device_id),
                            rtModule=pstring(dev.rt_module),
                            maxNchnls=dev.max_nchnls,
                            isOutput=dev.isOutput == 1)
            lst.append(d)
        return lst

    def midiDevList(self, isOutput=False) -> list[MidiDevice]:
        """Returns a list of available input or output midi devices.

        Each item in the list is a dictionnary representing a device. The
        dictionnary keys are device_name, interface_name, device_id,
        midi_module (value type string), isOutput (value type boolean).

        Must be called after an orchestra has been compiled
        to get meaningful information.
        """
        n = libcsound.csoundGetMIDIDevList(self.cs, None, ct.c_int32(isOutput))
        devs = (CsoundMidiDevice * n)()
        libcsound.csoundGetMIDIDevList(self.cs, ct.byref(devs), ct.c_int32(isOutput))
        return [MidiDevice(deviceName=pstring(dev.device_name),
                           interfaceName=pstring(dev.interface_name),
                           deviceId=pstring(dev.device_id),
                           midiModule=pstring(dev.midi_module),
                           isOutput=(dev.isOutput == 1))
                for dev in devs]

    def messageLevel(self) -> int:
        """Returns the Csound message level (from 0 to 231)."""
        return libcsound.csoundGetMessageLevel(self.cs)

    def setMessageLevel(self, messageLevel: int) -> None:
        """Sets the Csound message level (from 0 to 231)."""
        libcsound.csoundSetMessageLevel(self.cs, ct.c_int32(messageLevel))

    #
    # Performance
    #
    def compile_(self, *args):
        """Compiles Csound input files (such as an orchestra and score, or CSD).

        As directed by the supplied command-line arguments,
        but does not perform them. Returns a non-zero error code on failure.
        In this mode, the sequence of calls should be as follows::

            cs.compile_(args)
            while cs.perform_ksmps() == 0:
                pass
            cs.reset()
        """
        argc, argv = csoundArgList(args)
        return libcsound.csoundCompile(self.cs, argc, argv)

    def compileOrc(self, orc: str, block=True) -> int:
        """Parses, and compiles the given orchestra from an ASCII string.

        Also evaluating any global space code (i-time only)
        in synchronous or asynchronous (async_ = True) mode.

            orc = "instr 1 \n a1 rand 0dbfs/4 \n out a1 \n endin \n"
            cs.compile_orc(orc)
        """
        async_ = not block
        return libcsound.csoundCompileOrc(self.cs, cstring(orc), ct.c_int32(async_))

    def compileOrcAsync(self, orc: str) -> int:
        """Async version of :py:meth:`compileOrc()`.

        The code is parsed and compiled, then placed on a queue for
        asynchronous merge into the running engine, and evaluation.
        The function returns following parsing and compilation.
        """
        return self.compileOrc(orc, block=False)

    def evalCode(self, code: str) -> float:
        """Parses and compiles an orchestra given on an string, synchronously.

        Evaluating any global space code (i-time only).
        On SUCCESS it returns a value passed to the
        'return' opcode in global space:

            code = 'i1 = 2 + 2 \n return i1 \n'
            retval = cs.eval_code(code)
        """
        return libcsound.csoundEvalCode(self.cs, cstring(code))

    def compileCsd(self, path: str) -> int:
        """
        Compiles a Csound input file (.csd file) or a text string.

        Returns a non-zero error code on failure.

        If start is called before this method, the <CsOptions>
        element is ignored (but setOption can be called any number of
        times), the <CsScore> element is not pre-processed, but dispatched as
        real-time events; and performance continues indefinitely, or until
        ended by calling stop or some other logic. In this "real-time"
        mode, the sequence of calls should be:

            cs.setOption(...)
            cs.start()
            cs.compileCsd(path)
            while not cs.performKsmps():
                pass
            cs.reset()

        .. note::
            this function can be called repeatedly during performance to
            replace or add new instruments and events.

        But if this method is called before start, the <CsOptions>
        element is used, the <CsScore> section is pre-processed and dispatched
        normally, and performance terminates when the score terminates, or
        stop is called. In this "non-real-time" mode (which can still
        output real-time audio and handle real-time events), the sequence of
        calls should be:

            cs.compileCsd(path)
            cs.start()
            while not cs.performKsmps():
                pass
            cs.reset()
        """
        return libcsound.csoundCompileCSD(self.cs, cstring(path), ct.c_int32(0))

    def compileCsdText(self, code: str) -> int:
        """
        Compiles a Csound input file (.csd file) or a text string.

        Returns a non-zero error code on failure.

        If start is called before this method, the <CsOptions>
        element is ignored (but setOption can be called any number of
        times), the <CsScore> element is not pre-processed, but dispatched as
        real-time events; and performance continues indefinitely, or until
        ended by calling stop or some other logic. In this "real-time"
        mode, the sequence of calls should be:

            cs.setOption(...)
            cs.start()
            cs.compileCsdText(code)
            while not cs.performKsmps():
                pass
            cs.reset()

        .. note::
            this function can be called repeatedly during performance to
            replace or add new instruments and events.

        But if this method is called before start, the <CsOptions>
        element is used, the <CsScore> section is pre-processed and dispatched
        normally, and performance terminates when the score terminates, or
        stop is called. In this "non-real-time" mode (which can still
        output real-time audio and handle real-time events), the sequence of
        calls should be:

            cs.compileCsdText(code)
            cs.start()
            while not cs.performKsmps():
                pass
            cs.reset()
        """
        return libcsound.csoundCompileCSD(self.cs, cstring(code), ct.c_int32(1))

    def start(self):
        """Prepares Csound for performance.

        Normally called after compiling a csd file or an orc file, in which
        case score preprocessing is performed and performance terminates
        when the score terminates.

        However, if called before compiling a csd file or an orc file,
        score preprocessing is not performed and "i" statements are dispatched
        as real-time events, the <CsOptions> tag is ignored, and performance
        continues indefinitely or until ended using the API.
        """
        return libcsound.csoundStart(self.cs)

    def stop(self):
        """
        Only here for compatibility, not exposed in csound7
        """
        return

    def cleanup(self):
        """
        This is not needed in csound7, only here for compatibility
        """
        return

    def performKsmps(self):
        """Senses input events, and performs audio output.

        This is done for one control sample worth (ksmps) of audio output.
        start() must be called first.
        Returns False during performance, and True when
        performance is finished. If called until it returns True,
        it will perform an entire score.
        Enables external software to control the execution of Csound,
        and to synchronize performance with audio input and output.
        """
        return libcsound.csoundPerformKsmps(self.cs)

    def runUtility(self, name: str, args: list[str]) -> int:
        """Runs utility with the specified name and command line arguments.

        Should be called after loading utility plugins.
        Use reset() to clean up after calling this function.
        Returns zero if the utility was run successfully.
        """
        argc, argv = csoundArgList(args)
        return libcsound.csoundRunUtility(self.cs, cstring(name), argc, argv)

    def reset(self):
        """Resets all internal memory and state.

        In preparation for a new performance.
        Enable external software to run successive Csound performances
        without reloading Csound.
        """
        libcsound.csoundReset(self.cs)

    #
    # Realtime Audio I/O
    #
    def setHostAudioIO(self):
        """Disable all default handling of sound I/O.

        Calling this function after the creation of a Csound object
        and before the start of performance will disable all default
        handling of sound I/O by the Csound library via its audio
        backend module.
        Host application should in this case use the spin/spout
        buffers directly.
        """
        libcsound.csoundSetHostAudioIO(self.cs)

    def setHostImplementedAudioIO(self, state: bool, bufSize: int = 0):
        warnings.warn("This method is deprecated, use setHostAudioIO")
        self.setHostAudioIO()

    def setRTAudioModule(self, module: str) -> None:
        """Sets the current RT audio module."""
        libcsound.csoundSetRTAudioModule(self.cs, cstring(module))

    def spin(self) -> np.ndarray:
        """Returns the Csound audio input working buffer (spin) as an ndarray.

        Enables external software to write audio into Csound before
        calling perform_ksmps().
        """
        buf = libcsound.csoundGetSpin(self.cs)
        size = self.ksmps() * self.nchnlsInput()
        return _util.castarray(buf, shape=(size,))

    def spout(self) -> np.ndarray:
        """Returns the address of the Csound audio output working buffer (spout).

        Enables external software to read audio from Csound after
        calling perform_ksmps().
        """
        buf = libcsound.csoundGetSpout(self.cs)
        size = self.ksmps() * self.nchnls()
        return _util.castarray(buf, shape=(size,))

    #
    # Realtime MIDI I/O
    #
    def setHostMidiIO(self) -> None:
        """Disable all default handling of MIDI I/O.

        Call this function after csound_create()
        and before the start of performance to implement
        MIDI via the callbacks below.
        """
        libcsound.csoundSetHostMIDIIO(self.cs)

    def setHostImplementedMIDIIO(self, state: bool) -> None:
        """Called with *state* :code:`True` if the host is implementing via callbacks."""
        if state:
            self.setHostMidiIO()

    def setMidiModule(self, module: str) -> None:
        """Sets the current MIDI IO module."""
        libcsound.csoundSetMIDIModule(self.cs, cstring(module))

    def setExternalMidiInOpenCallback(self, function) -> None:
        """
        Sets a callback for opening real-time MIDI input.
        """
        self._callbacks['externalMidiInOpen'] = func = MIDIINOPENFUNC(function)
        libcsound.csoundSetExternalMidiInOpenCallback(self.cs, func)

    def setExternalMidiReadCallback(self, function) -> None:
        """Sets a callback for reading from real time MIDI input."""
        self._callbacks['externalMidiRead'] = func = MIDIREADFUNC(function)
        libcsound.csoundSetExternalMidiReadCallback(self.cs, func)

    def setExternalMidiInCloseCallback(self, function):
        """Sets a callback for closing real time MIDI input."""
        self._callbacks['externalMidiInClose'] = func = MIDIINCLOSEFUNC(function)
        libcsound.csoundSetExternalMidiInCloseCallback(self.cs, func)

    def setExternalMidiOutOpenCallback(self, function):
        """Sets a callback for opening real-time MIDI input."""
        self._callbacks['externalMidiOutOpen'] = func = MIDIOUTOPENFUNC(function)
        libcsound.csoundSetExternalMidiOutOpenCallback(self.cs, func)

    def setExternalMidiWriteCallback(self, function):
        """Sets a callback for reading from real time MIDI input."""
        self._callbacks['externalMidiWrite'] = func = MIDIWRITEFUNC(function)
        libcsound.csoundSetExternalMidiWriteCallback(self.cs, func)

    def setExternalMidiOutCloseCallback(self, function):
        """Sets a callback for closing real time MIDI input."""
        self._callbacks['externalMidiOutClose'] = func = MIDIOUTCLOSEFUNC(function)
        libcsound.csoundSetExternalMidiOutCloseCallback(self.cs, func)

    def setExternalMidiErrorStringCallback(self, function):
        """ Sets a callback for converting MIDI error codes to strings."""
        self._callbacks['externalMidiErrorString'] = f = MIDIERRORFUNC(function)
        libcsound.csoundSetExternalMidiErrorStringCallback(self.cs, f)

    def setMidiDeviceListCallback(self, function):
        """Sets a callback for obtaining a list of MIDI devices."""
        self._callbacks['setMidiDeviceList'] = f = MIDIDEVLISTFUNC(function)
        libcsound.csoundSetMIDIDeviceListCallback(self.cs, f)
    #
    # Csound Messages and Text
    #
    def message(self, fmt: str, *args):
        """Displays an informational message.

        This is a workaround because does not support variadic functions.
        The arguments are formatted in a string, using the python way, either
        old style or new style, and then this formatted string is passed to
        the Csound display message system.
        """
        if fmt[0] == '{':
            s = fmt.format(*args)
        else:
            s = fmt % args
        libcsound.csoundMessage(self.cs, cstring("%s"), cstring(s))

    def messageS(self, attr: int, fmt: str, *args) -> None:
        """Prints message with special attributes.

        (See msg_attr.h for the list of available attributes). With attr=0,
        message_S() is identical to message().
        This is a workaround because ctypes does not support variadic functions.
        The arguments are formatted in a string, using the python way, either
        old style or new style, and then this formatted string is passed to
        the csound display message system.
        """
        if fmt[0] == '{':
            s = fmt.format(*args)
        else:
            s = fmt % args
        libcsound.csoundMessageS(self.cs, ct.c_int32(attr), cstring("%s"), cstring(s))

    def setMessageStringCallback(self, attr: int, function):
        """Sets an alternative message print function.

        This function is to be called by Csound to print an
        informational message, using a less granular signature.
        This callback can be set for --realtime mode.
        This callback is cleared after reset.
        """
        self._messageStringCallback = MSGSTRFUNC(function)
        libcsound.csoundSetMessageStringCallback(self.cs, ct.c_int32(attr), self._messageStringCallback)

    def createMessageBuffer(self, echo=False) -> None:
        """
        Creates a buffer for storing messages printed by Csound.

        Should be called after creating a Csound instance.
        The buffer can be freed by calling :py:meth:`destroyMessageBuffer()`
        before deleting the Csound instance. You will generally want to call
        :py:meth:`cleanup()` to make sure the last messages are flushed to
        the message buffer before destroying Csound.

        Args:
            echo: if True, messages are also printed to stdout or stderr,
                depending on the type of the message, in addition to being
                stored in the buffer.

        Using the message buffer ties up the internal message callback, so
        :py:meth:`setMessageCallback()` should not be called after creating the
        message buffer.
        """
        libcsound.csoundCreateMessageBuffer(self.cs, ct.c_int32(echo))

    def firstMessage(self) -> str:
        """Returns the first message from the buffer."""
        s = libcsound.csoundGetFirstMessage(self.cs)
        return pstring(s)

    def firstMessageAttr(self) -> int:
        """Returns the attribute parameter of the first message in the buffer."""
        return libcsound.csoundGetFirstMessageAttr(self.cs)

    def popFirstMessage(self) -> None:
        """Removes the first message from the buffer."""
        libcsound.csoundPopFirstMessage(self.cs)

    def messageCnt(self) -> int:
        """Returns the number of pending messages in the buffer."""
        return libcsound.csoundGetMessageCnt(self.cs)

    def destroyMessageBuffer(self) -> None:
        """Releases all memory used by the message buffer."""
        libcsound.csoundDestroyMessageBuffer(self.cs)

    def readMessage(self) -> tuple[str, int]:
        """
        Reads a message from the message buffer and removes it from it

        Returns:
            a tuple (message: str, attribute: int). If there are no more
            messages, the message is an empty string and attribute is 0
        """
        cnt = self.messageCnt()
        if cnt <= 0:
            return '', 0
        msg = self.firstMessage()
        attr = self.firstMessageAttr()
        self.popFirstMessage()
        return msg, attr

    def iterMessages(self) -> _t.Iterator[tuple[str, int]]:
        """
        Iterate over the messages in the message buffer

        This operation empties the message buffer

        Returns:
            an iterator of tuple(message: str, attribute: int)
        """
        for i in range(self.messageCnt()):
            msg = self.firstMessage()
            attr = self.firstMessageAttr()
            yield msg, attr
            self.popFirstMessage()

    #
    # Channels, Controls and Events
    #
    def channelPtr(self, name: str, kind: str, output=True, input=False
                   ) -> tuple[np.ndarray | ct.c_char_p | ct.c_void_p | None, str]:
        """Get a pointer to the specified channel and an error message.

        Args:
            name: the name of the channel
            kind: one of 'control', 'audio', 'string', 'array', 'pvs'
            output: True if this is an output channel (from the perspective of csound).
                A channel can also be bidirectional (both output and input)
            input: True if this is an input channel (from the perspective of csound)
                A channel can also be bidirectional (both output and input)

        Returns:
            a tuple (channelptr, errmsg) where channelptr is a numpy array for control
            and audio channels, otherwise a void pointer
        The channel is created first if it does not exist yet.

        If the channel is a control or an audio channel, the pointer is
        translated to an ndarray of MYFLT. If the channel is a string channel,
        the pointer is casted to ct.c_char_p. The error message is either
        an empty string or a string describing the error that occured.

        If the channel already exists, it must match the data type
        (control, string, audio, pvs or array), however, the input/output bits
        are OR'd with the new value. Note that audio and string channels
        can only be created after calling compile_(), because the
        storage size is not known until then.
        """
        chantype = _util.packChannelType(kind=kind, output=output, input=input)
        return self._channelPtr(name, chantype)

    def channelInfo(self, name: str) -> tuple[str, int]:
        """
        Query info about a channel

        Args:
            name: the name of the channel

        Returns:
            a tuple (kind: str, mode: int). If the channel does not exist
            kind will be an empty string and mode will be 0
        """
        ptr = ct.c_void_p()
        ret = libcsound.csoundGetChannelPtr(self.cs, ct.byref(ptr), cstring(name), 0)
        assert ret != 0
        if ret == CSOUND_ERROR:
            return ('', 0)
        else:
            chantype = ret & CSOUND_CHANNEL_TYPE_MASK
            mode = ret - chantype
            kind = {
                CSOUND_CONTROL_CHANNEL: 'control',
                CSOUND_AUDIO_CHANNEL: 'audio',
                CSOUND_STRING_CHANNEL: 'string',
                CSOUND_PVS_CHANNEL: 'pvs',
                CSOUND_ARRAY_CHANNEL: 'array'
            }.get(chantype)
            if kind is None:
                raise RuntimeError(f"Got invalid channel kind: {chantype}")
            return kind, mode

    def _channelPtr(self, name: str, type_: int) -> tuple[np.ndarray | ct.c_char_p | ct.c_void_p | None, str]:
        """Get a pointer to the specified channel and an error message.

        The channel is created first if it does not exist yet.
        type_ must be the bitwise OR of exactly one of the following values,

        CSOUND_CONTROL_CHANNEL
            control data (one MYFLT value) - (MYFLT **) pp
        CSOUND_AUDIO_CHANNEL
            audio data (ksmps() MYFLT values) - (MYFLT **) pp
        CSOUND_STRING_CHANNEL
            string data as a STRINGDAT structure - (STRINGDAT **) pp
            (see string_data() and set_string_data())
        CSOUND_ARRAY_CHANNEL
            array data as an ARRAYDAT structure - (ARRAYDAT **) pp
            (see array_data(), set_array_data(), and init_array_channel())
        CSOUND_PVS_CHANNEL
            pvs data as a PVSDATEXT structure - (PVSDATEXT **) pp
            (see pvs_data(), set_pvs_data(), and init_pvs_channel())
        and at least one of these:

        CSOUND_INPUT_CHANNEL
        CSOUND_OUTPUT_CHANNEL

        If the channel is a control or an audio channel, the pointer is
        translated to an ndarray of MYFLT. If the channel is a string channel,
        the pointer is casted to ct.c_char_p. The error message is either
        an empty string or a string describing the error that occured.

        If the channel already exists, it must match the data type
        (control, string, audio, pvs or array), however, the input/output bits
        are OR'd with the new value. Note that audio and string channels
        can only be created after calling compile_(), because the
        storage size is not known until then.

        Return value is zero on success, or a negative error code,

        CSOUND_MEMORY
            there is not enough memory for allocating the channel
        CSOUND_ERROR
            the specified name or type is invalid

        or, if a channel with the same name but incompatible type
        already exists, the type of the existing channel. In the case
        of any non-zero return value, the pointer is set to None.
        Note: to find out the type of a channel without actually
        creating or changing it, set type_ to zero, so that the return
        value will be either the type of the channel, or CSOUND_ERROR
        if it does not exist.

        Operations on the pointer are not thread-safe by default. The host is
        required to take care of threadsafety by using lock_channel() and
        unlock_channel() to protect access to the pointer.

        See Top/threadsafe.c in the Csound library sources for
        examples. Optionally, use the channel get/set functions
        provided below, which are threadsafe by default.
        """
        length = 1  # default buf length for CSOUND_CONTROL_CHANNEL:
        ptr = ct.c_void_p()
        chan_type = type_ & CSOUND_CHANNEL_TYPE_MASK
        err = ''
        ret = libcsound.csoundGetChannelPtr(self.cs, ct.byref(ptr), cstring(name), type_)
        if ret == CSOUND_SUCCESS:
            if chan_type == CSOUND_STRING_CHANNEL:
                return ct.cast(ptr, STRINGDAT_p), err
            elif chan_type == CSOUND_ARRAY_CHANNEL:
                return ct.cast(ptr, ARRAYDAT_p), err
            elif chan_type == CSOUND_PVS_CHANNEL:
                return ct.cast(ptr, PVSDAT_p), err
            elif chan_type == CSOUND_AUDIO_CHANNEL:
                length = libcsound.csoundGetKsmps(self.cs)
            return _util.castarray(ptr, shape=(length,)), err

        if ret == CSOUND_MEMORY:
            err = 'Not enough memory for allocating channel'
        elif ret == CSOUND_ERROR:
            err = 'The specified channel name or type is not valid'
        elif ret == CSOUND_CONTROL_CHANNEL:
            err = 'A control channel named {} already exists'.format(name)
        elif ret == CSOUND_AUDIO_CHANNEL:
            err = 'An audio channel named {} already exists'.format(name)
        elif ret == CSOUND_STRING_CHANNEL:
            err = 'A string channel named {} already exists'.format(name)
        elif ret == CSOUND_ARRAY_CHANNEL:
            err = 'An array channel named {} already exists'.format(name)
        elif ret == CSOUND_PVS_CHANNEL:
            err = 'A PVS channel named {} already exists'.format(name)
        else:
            err = 'Unknown error'
        return None, err

    def channelVarTypeName(self, name: str) -> str:
        """Returns the var type for a channel name.

        Returns None if the channel was not found.
        Currently supported channel var types are 'control', 'audio',
        'string', 'pvs' and 'array'
        """
        ret = libcsound.csoundGetChannelVarTypeName(self.cs, cstring(name))
        if not ret:
            return ''
        return {
            'k': 'control',
            'a': 'audio',
            'S': 'string',
            'f': 'pvs',
            '[': 'array'
            }[ret]

    def allocatedChannels(self) -> list[dict]:
        chanlist, err = self.listChannels()
        if err:
            raise RuntimeError(f"Error while getting a list of channels: {err}")
        assert chanlist is not None
        n = len(chanlist)
        out = []
        for chaninfo in chanlist:
            assert isinstance(chaninfo, ControlChannelInfo)
            if chaninfo.hints:
                hints = {'min': chaninfo.hints.min,
                        'max': chaninfo.hints.max,
                        'width': chaninfo.hints.width,
                        'height': chaninfo.hints.height}
            else:
                hints = None
            kind, modeint = _util.unpackChannelType(chaninfo.type)
            out.append(ChannelInfo(name=chaninfo.name, kind=kind, mode=modeint, hints=hints))
            # out.append({'name': chaninfo.name, 'type': chaninfo.type, 'hints': hints})
        self.deleteChannelList(chanlist)
        return out

    def listChannels(self) -> tuple[ct.Array[ControlChannelInfo] | None, str]:
        """Returns a list of allocated channels and an error message.

        A ControlChannelInfo object contains the channel characteristics.
        The error message indicates if there is not enough
        memory for allocating the list or it is an empty string if there is no
        error. In the case of no channels or an error, the list is None.

        Notes: the caller is responsible for freeing the list returned by the
        C API with delete_channel_list(). The name pointers may become
        invalid after calling reset().
        """
        chn_infos = None
        err = ''
        ptr = ct.cast(ct.POINTER(ct.c_int)(), ct.POINTER(ControlChannelInfo))
        n = libcsound.csoundListChannels(self.cs, ct.byref(ptr))
        if n == CSOUND_MEMORY :
            err = 'There is not enough memory for allocating the list'
        if n > 0:
            chn_infos = ct.cast(ptr, ct.POINTER(ControlChannelInfo * n)).contents
        return chn_infos, err

    def deleteChannelList(self, lst: ct.Array[ControlChannelInfo]) -> None:
        """Releases a channel list previously returned by list_channels()."""
        ptr = ct.cast(lst, ct.POINTER(ControlChannelInfo))
        libcsound.csoundDeleteChannelList(self.cs, ptr)

    def setControlChannelHints(self, name: str, hints: ControlChannelHints):
        """Sets parameters hints for a control channel.

        These hints have no internal function but can be used by front ends to
        construct GUIs or to constrain values. See the ControlChannelHints
        structure for details.
        Returns zero on success, or a non-zero error code on failure:

        CSOUND_ERROR
            the channel does not exist, is not a control channel,
            or the specified parameters are invalid
        CSOUND_MEMORY
            could not allocate memory
        """
        return libcsound.csoundSetControlChannelHints(self.cs, cstring(name), hints)

    def controlChannelHints(self, name: str) -> tuple[ControlChannelHints | None, int]:
        """Returns special parameters (if any) of a control channel.

        Those parameters have been previously set with
        :meth:`Csound.setControlChannelHints` or the ``chnparams`` opcode.

        The return values are a ControlChannelHints structure and
        CSOUND_SUCCESS if the channel exists and is a control channel,
        otherwise, None and an error code are returned.
        """
        hints = ControlChannelHints()
        ret = libcsound.csoundGetControlChannelHints(self.cs, cstring(name),
            ct.byref(hints))
        if ret != CSOUND_SUCCESS:
            hints = None
        return hints, ret

    def lockChannel(self, channel):
        """Locks access to the channel.

        Access to data is allowed in a threadsafe manner.
        """
        libcsound.csoundLockChannel(self.cs, cstring(channel))

    def unlockChannel(self, channel):
        """Unlocks access to the channel.

        It allows access to data from elsewhere.
        """
        libcsound.csoundUnlockChannel(self.cs, cstring(channel))

    def controlChannel(self, name: str) -> tuple[float, int]:
        """Retrieves the value of control channel identified by *name*.

        Args:
            name: the name of the channel

        Returns:
            a tuple (value: float, returncode: int)

        """
        err = ct.c_int32(0)
        ret = libcsound.csoundGetControlChannel(self.cs, cstring(name), ct.byref(err))
        return ret, err.value

    def setControlChannel(self, name: str, val: float) -> None:
        """Sets the value of control channel identified by name."""
        libcsound.csoundSetControlChannel(self.cs, cstring(name), MYFLT(val))

    def audioChannel(self, name: str, samples: np.ndarray):
        """Copies the audio channel identified by name into ndarray samples.

        Args:
            name: name of the channel
            samples: a numpy array with space for at least ``ksmps`` samples

        """
        if len(samples.shape) > 1:
            raise ValueError(f"Only 1-dimensional arrays supported, got {samples}")
        if len(samples) < self.ksmps():
            raise ValueError(f"The given array is too small (ksmps: {self.ksmps()}, "
                             f"size of the given array: {len(samples)}")
        ptr = samples.ctypes.data_as(ct.POINTER(MYFLT))
        libcsound.csoundGetAudioChannel(self.cs, cstring(name), ptr)

    def setAudioChannel(self, name: str, samples: np.ndarray):
        """Sets the audio channel name with data from the ndarray samples.

        samples should contain at least ksmps() MYFLTs.
        """
        if len(samples.shape) > 1:
            raise ValueError(f"Only 1-dimensional arrays supported, got {samples}")
        if len(samples) < self.ksmps():
            raise ValueError(f"The given array is too small (ksmps: {self.ksmps()}, "
                             f"size of the given array: {len(samples)}")
        ptr = samples.ctypes.data_as(ct.POINTER(MYFLT))
        libcsound.csoundSetAudioChannel(self.cs, cstring(name), ptr)

    def stringChannel(self, name):
        """Return a string from the string channel identified by name."""
        n = libcsound.csoundGetChannelDatasize(self.cs, cstring(name))
        if n <= 0:
            return ""
        s = ct.create_string_buffer(n)
        libcsound.csoundGetStringChannel(self.cs, cstring(name),
            ct.cast(s, ct.POINTER(ct.c_char)))
        return pstring(ct.string_at(s))

    def setStringChannel(self, name: str, string: str) -> None:
        """Sets the string channel identified by name with string."""
        libcsound.csoundSetStringChannel(self.cs, cstring(name), cstring(string))

    def initArrayChannel(self, name: str, dtype: str, size: int | _t.Sequence[int]):
        """Create and initialise an array channel with a given array type.

        Args:
            name: name of the channel
            dtype: the data type of array, one of 'a' (audio), 'k' (control values),
                or 'S' (strings).
            size: the size of the array or the sizes of each dimension

        Returns:
            the ARRAYDAT_p for the requested channel or None on error

        .. note:: if the channel exists and has already been initialised,
            this function is a non-op.
        """
        if isinstance(size, int):
            sizes = (size, )
        else:
            sizes = size
        sz = np.array(sizes).astype(ct.c_int)
        sizeptr = sz.ctypes.data_as(ct.POINTER(ct.c_int))
        return libcsound.csoundInitArrayChannel(self.cs, cstring(name), cstring(dtype),
                                                sz.size, sizeptr)

    def arrayDataType(self, adat: ARRAYDAT_p) -> str:
        """Get the type of data the ARRAYDAT adat.

        Args:
            adata: the ARRAYDAT_p array

        Returns:
            the array datatype as a str, one of 'a' (audio), 'i' (init),
            'k' (control values) or 'S' (strings)

        """
        return pstring(libcsound.csoundArrayDataType(adat))

    def arrayDataDimensions(self, adat: ARRAYDAT_p) -> int:
        """Get the dimensions of the ARRAYDAT adat."""
        return libcsound.csoundArrayDataDimensions(adat)

    def arrayDataSizes(self, adat) -> tuple[int, ...]:
        """Get the sizes of each dimension of the ARRAYDAT adat.

        Args:
            adata: the array, a ARRAYDAT_p struct

        Returns:
            a list of sizes, where the size of the list is the number of
            dimensions of the array
        """
        sizes = libcsound.csoundArrayDataSizes(adat)
        dims = libcsound.csoundArrayDataDimensions(adat)
        return tuple(_util.castarray(sizes, shape=(dims,)))

    def setArrayData(self, adat: ARRAYDAT_p, data: np.ndarray) -> None:
        """Set the data in the ARRAYDAT adat."""
        # TODO: check data, get a void pointer to the data
        libcsound.csoundSetArrayData(adat, data)

    def arrayData(self, adat: ARRAYDAT_p) -> np.ndarray:
        """Get the data from the ARRAYDAT adat."""
        # TODO: construct a numpy array pointing to the returned data
        return libcsound.csoundGetArrayData(adat)

    # These two functions are using c void * for the data.
    # Not very useful in Python. To be refined.
    def stringData(self, sdata):
        """Get a null-terminated string from a STRINGDAT structure."""
        return pstring(libcsound.csoundGetStringData(self.cs, sdata))

    def setStringData(self, sdata, string: str):
        """Set a STRINGDAT structure with a null-terminated string."""
        libcsound.csoundSetStringData(self.cs, sdata, cstring(string))

    def initPvsChannel(self, name: str, fftsize: int, overlap: int,
                       winsize: int, wintype: int | str, format: int = 0
                       ) -> PVSDAT_p | None:
        """
        Create/initialise an Fsig channel.

        Args:
            name: name of the channel
            fftsize: FFT analysis size
            overlap: analysis overlap size in samples
            winsize: analysis window size in samples
            wintype: analysis window type. One of 'hamming', 'hann', 'kaiser',
                'blackman', 'blackman-exact', 'nuttallc3', 'bharris3',
                'bharrismin', 'rect' (see pvsdat types enumeration)
            format: analysis data format (see pvsdat format enumeration)

        Returns:
            the PVSDAT for the requested channel or None on error.

        .. note:: if the channel exists and has already been initialised,
            this function is a non-op.
        """
        if isinstance(wintype, str):
            wintypenum = PVS_WINDOWS.get(wintype)
            if wintypenum is None:
                raise ValueError(f"Window {wintype} not known. Possible windows: {PVS_WINDOWS.keys()}")
        else:
            wintypenum = wintype
        return libcsound.csoundInitPvsChannel(self.cs, cstring(name),
            fftsize, overlap, winsize, wintypenum, format)

    def pvsDataFftSize(self, pvsdat: PVSDAT_p) -> int:
        """Get the analysis FFT size used by the PVSDAT pvsdat."""
        return libcsound.csoundPvsDataFFTSize(pvsdat)

    def pvsDataOverlap(self, pvsdat: PVSDAT_p) -> int:
        """Get the analysis overlap size used by the PVSDAT pvsdat."""
        return libcsound.csoundPvsDataOverlap(pvsdat)

    def pvsDataWindowSize(self, pvsdat: PVSDAT_p) -> int:
        """Get the analysis window size used by the PVSDAT pvsdat."""
        return libcsound.csoundPvsDataWindowSize(pvsdat)

    def pvsDataFormat(self, pvsdat: PVSDAT_p) -> int:
        """Get the analysis data format used by the PVSDAT pvsdat."""
        return libcsound.csoundPvsDataFormat(pvsdat)

    def pvsDataFramecount(self, pvsdat: PVSDAT_p) -> int:
        """Get the current framecount from PVSDAT pvsdat."""
        return libcsound.csoundPvsDataFramecount(pvsdat)

    # These two functions are using c float * for the frame data.
    # Not very useful in Python. To be refined.
    def pvsData(self, pvsdat):
        """Get the analysis data frame from the PVSDAT pvsdat."""
        return libcsound.csoundGetPvsData(pvsdat)

    def setPvsData(self, pvsdat, frame):
        """Set the analysis data frame in the PVSDAT pvsdat."""
        libcsound.csoundSetPvsData(pvsdat, frame)

    def channelDatasize(self, name: str) -> int:
        """Returns the size of data stored in a channel."""
        return libcsound.csoundGetChannelDatasize(self.cs, cstring(name))

    def setInputChannelCallback(self, function: _t.Callable) -> None:
        """Sets the function to call whenever the invalue opcode is used."""
        self._intputChannelCallback = CHANNELFUNC(function)
        libcsound.csoundSetInputChannelCallback(self.cs, self._intputChannelCallback)

    def setOutputChannelCallback(self, function: _t.Callable) -> None:
        """Sets the function to call whenever the outvalue opcode is used."""
        self._outputChannelCallback = CHANNELFUNC(function)
        libcsound.csoundSetOutputChannelCallback(self.cs, self._outputChannelCallback)

    def event(self, kind: str, pfields: _t.Sequence[float] | np.ndarray, block=True):
        """
        Send a new event.

        Args:
            kind: the kind of event, one of 'i', 'f', 'e'
            params: pfields of the event, starting with p1
            block: if True, the operation is blocking. Otherwise it is
                performed asynchronously


        """
        eventtype = _scoreEventToTypenum.get(kind)
        if eventtype is None:
            raise ValueError(f"Invalid event kind, get {kind}, expected one of {_scoreEventToTypenum.keys()}")
        p = np.asarray(pfields, dtype=MYFLT)
        ptr = p.ctypes.data_as(ct.POINTER(MYFLT))
        n_fields = ct.c_int32(p.size)
        libcsound.csoundEvent(self.cs, ct.c_int32(eventtype), ptr, n_fields,
            ct.c_int32(not block))

    def scoreEvent(self, kind: str, pfields: _t.Sequence[float] | np.ndarray) -> int:
        """
        Send a new event

        This is an alias to event(..., block=True), here for compatibility
        with csound 6

        Args:
            kind: the kind of event, one of 'i', 'f', 'e'
            params: pfields of the event, starting with p1
        """
        self.event(kind=kind, pfields=pfields, block=True)
        return CSOUND_SUCCESS

    def scoreEventAsync(self, kind: str, pfields: _t.Sequence[float] | np.ndarray):
        """
        Send a new event, async

        This is an alias to event(..., block=True), here for compatibility
        with csound 6

        Args:
            kind: the kind of event, one of 'i', 'f', 'e'
            params: pfields of the event, starting with p1
        """
        return self.event(kind=kind, pfields=pfields, block=False)

    def inputMessage(self, s: str):
        """
        Similar to eventString, here for compatibility with csound6

        Args:
            s: a score line to send
        """
        return self.eventString(s, block=False)

    def eventString(self, message: str, block=True):
        """Send a new event as a string.

        Args:
            message: the message to send. Multiple events separated by newlines
                are possible. Score preprocessing (carry, etc.) is applied
            block: if true, the operation is run blocking

        """
        libcsound.csoundEventString(self.cs, cstring(message),
            ct.c_int32(not block))

    def keyPress(self, c: int | str):
        """Sets the ASCII code of the most recent key pressed.

        This value is used by the sensekey opcode if a callback for
        returning keyboard events is not set (see
        registerKeyboardCallback()).
        """
        if isinstance(c, str):
            c = ord(c[0])
        libcsound.csoundKeyPress(self.cs, cchar(c))

    def registerKeyboardCallback(self, function, userdata, typemask):
        """Registers general purpose callback functions for keyboard events.

        These callbacks will be called to query keyboard events. They
        are called on every control period by the sensekey opcode.

        The callback is preserved on reset(), and multiple
        callbacks may be set and will be called in reverse order of
        registration. If the same function is set again, it is only moved
        in the list of callbacks so that it will be called first, and the
        user data and type mask parameters are updated. type_mask can be the
        bitwise OR of callback types for which the function should be called,
        or zero for all types.

        Returns zero on success, CSOUND_ERROR if the specified function
        pointer or type mask is invalid, and CSOUND_MEMORY if there is not
        enough memory.

        The callback function takes the following arguments:

        user_data
            the "user data" pointer, as specified when setting the callback
        p
            data pointer, depending on the callback type
        type_
            callback type, can be one of the following (more may be added in
            future versions of Csound):

            CSOUND_CALLBACK_KBD_EVENT
            CSOUND_CALLBACK_KBD_TEXT
                called by the sensekey opcode to fetch key codes. The
                data pointer is a pointer to a single value of type int,
                for returning the key code, which can be in the range 1 to
                65535, or 0 if there is no keyboard event.
            For CSOUND_CALLBACK_KBD_EVENT, both key press and release
            events should be returned (with 65536 (0x10000) added to the
            key code in the latter case) as unshifted ASCII codes.
            CSOUND_CALLBACK_KBD_TEXT expects key press events only as the
            actual text that is typed.

        The return value should be zero on success, negative on error, and
        positive if the callback was ignored (for example because the type is
        not known).
        """
        if typemask == CSOUND_CALLBACK_KBD_EVENT:
            self.keyboard_cb_event_ref = KEYBOARDFUNC(function)
        else:
            self.keyboard_cb_text_ref = KEYBOARDFUNC(function)
        return libcsound.csoundRegisterKeyboardCallback(self.cs,
            KEYBOARDFUNC(function),
            ct.py_object(userdata), ct.c_uint(typemask))

    def removeKeyboardCallback(self, function):
        """Removes a callback previously set with register_keyboard_callback()."""
        libcsound.csoundRemoveKeyboardCallback(self.cs, KEYBOARDFUNC(function))

    #
    # Tables
    #
    def tableLength(self, table: int) -> int:
        """Returns the length of a function table.

        (Not including the guard point).
        If the table does not exist, returns -1.
        """
        return libcsound.csoundTableLength(self.cs, ct.c_int32(table))

    def table(self, tableNum) -> np.ndarray | None:
        """Returns a pointer to function table tableNum as an ndarray.

        The ndarray does not include the guard point. If the table does not
        exist, None is returned.
        """
        ptr = ct.POINTER(MYFLT)()
        size = libcsound.csoundGetTable(self.cs, ct.byref(ptr), tableNum)
        return _util.castarray(ptr, shape=(size,)) if size >= 0 else None

    def tableArgs(self, tableNum: int) -> np.ndarray | None:
        """Returns a pointer to the args used to generate a function table.

        The pointer is returned as an ndarray. If the table does not exist,
        None is returned.

        NB: the argument list starts with the GEN number and is followed by
        its parameters. eg. f 1 0 1024 10 1 0.5  yields the list
        {10.0, 1.0, 0.5}
        """
        ptr = ct.POINTER(MYFLT)()
        size = libcsound.csoundGetTableArgs(self.cs, ct.byref(ptr), tableNum)
        if size < 0:
            return None
        return _util.castarray(ptr, shape=(size,)) if size >= 0 else None

    #
    # Score Handling
    #
    def scoreTime(self) -> float:
        """Returns the current score time.

        The return value is the time in seconds since the beginning of
        performance.
        """
        return libcsound.csoundGetScoreTime(self.cs)

    def isScorePending(self) -> bool:
        """Tells whether Csound score events are performed or not.

        Independently of real-time MIDI events (see set_score_pending()).
        """
        return libcsound.csoundIsScorePending(self.cs) != 0

    def setScorePending(self, pending: bool) -> None:
        """Sets whether Csound score events are performed or not.

        Real-time events will continue to be performed. Can be used by external
        software, such as a VST host, to turn off performance of score events
        (while continuing to perform real-time events), for example to mute
        a Csound score while working on other tracks of a piece, or to play
        the Csound instruments live.
        """
        libcsound.csoundSetScorePending(self.cs, ct.c_int32(pending))

    def scoreOffsetSeconds(self) -> float:
        """Returns the score time beginning.

        At this time score events will actually immediately be performed
        (see :meth:`Csound.setScoreOffsetSeconds`).
        """
        return libcsound.csoundGetScoreOffsetSeconds(self.cs)

    def setScoreOffsetSeconds(self, time: float) -> None:
        """Csound score events prior to the specified time are not performed.

        Performance begins immediately at the specified time (real-time events
        will continue to be performed as they are received). Can be used by
        external software, such as a VST host, to begin score performance
        midway through a Csound score, for example to repeat a loop in a
        sequencer, or to synchronize other events with the Csound score.
        """
        libcsound.csoundSetScoreOffsetSeconds(self.cs, MYFLT(time))

    def rewindScore(self) -> None:
        """Rewinds a compiled Csound score.

        It is rewinded to the time specified with set_score_offset_seconds().
        """
        libcsound.csoundRewindScore(self.cs)

    def sleep(self, milliseconds: int) -> None:
        """Waits for at least the specified number of milliseconds.

        It yields the CPU to other threads.
        """
        libcsound.csoundSleep(ct.c_uint(milliseconds))

    #
    # Opcodes
    #
    def loadPlugins(self, directory: str) -> int:
        """Loads all plugins from a given directory.

        Generally called immediatly after csound_create() to make new
        opcodes/modules available for compilation and performance.
        """
        return libcsound.csoundLoadPlugins(self.cs, cstring(directory))

    def appendOpcode(self, opname: str, dsblksiz: int, flags: int,
                     outypes: str, intypes: str, initfunc: _t.Callable,
                     perffunc: _t.Callable, deinitfunc: _t.Callable = None):
        """Appends an opcode implemented by external software.

        This opcode is added to Csound's internal opcode list.
        The opcode list is extended by one slot, and the parameters are copied
        into the new slot.
        Returns zero on success.
        """
        deinit = deinitfunc if deinitfunc else OPCODEFUNC()
        return libcsound.csoundAppendOpcode(self.cs, cstring(opname), dsblksiz,
            flags, cstring(outypes), cstring(intypes),
            OPCODEFUNC(initfunc), OPCODEFUNC(perffunc), deinit)

    #
    # Table Display
    #
    def setIsGraphable(self, isGraphable: bool ) -> bool:
        """Tells Csound whether external graphic table display is supported.

        Return the previously set value (initially False).
        """
        ret = libcsound.csoundSetIsGraphable(self.cs, ct.c_int32(isGraphable))
        return (ret != 0)

    def setMakeGraphCallback(self, function) -> None:
        """Called by external software to set Csound's MakeGraph function."""
        self._callbacks['setMakeGraph'] = f = MAKEGRAPHFUNC(function)
        libcsound.csoundSetMakeGraphCallback(self.cs, f)

    def setDrawGraphCallback(self, function) -> None:
        """Called by external software to set Csound's DrawGraph function."""
        self._callbacks['drawGraph'] = f = DRAWGRAPHFUNC(function)
        libcsound.csoundSetDrawGraphCallback(self.cs, f)

    def setKillGraphCallback(self, function) -> None:
        """Called by external software to set Csound's KillGraph function."""
        self._callbacks['killGraph'] = func = KILLGRAPHFUNC(function)
        libcsound.csoundSetKillGraphCallback(self.cs, func)

    def setExitGraphCallback(self, function) -> None:
        """Called by external software to set Csound's ExitGraph function."""
        self._callbacks['exitGraph'] = f = EXITGRAPHFUNC(function)
        libcsound.csoundSetExitGraphCallback(self.cs, f)

    #
    # Circular Buffer Functions
    #
    def createCircularBuffer(self, numelem: int, elemsize: int) -> ct.c_void_p:
        """Creates a circular buffer with numelem number of elements.

        The element's size is set from elemsize. It should be used like::

            rb = cs.create_circular_buffer(1024, cs.size_of_MYFLT())
        """
        return libcsound.csoundCreateCircularBuffer(self.cs, numelem, elemsize)

    def readCircularBuffer(self, buffer: ct.c_void_p, out: np.ndarray, numitems: int) -> int:
        """Reads from circular buffer.

        Args:
            buffer: pointer to an existing circular buffer
            out: preallocated ndarray with at least items number of elements,
                where buffer contents will be read into
            items: number of samples to be read

        Returns the actual number of items read (0 <= n <= items).
        """
        if len(out) < numitems:
            return 0
        ptr = out.ctypes.data_as(ct.c_void_p)
        return libcsound.csoundReadCircularBuffer(self.cs, buffer, ptr, numitems)

    def peekCircularBuffer(self, buffer: ct.c_void_p, out: np.ndarray, numitems: int) -> int:
        """Reads from circular buffer without removing them from the buffer.

        Args:
            buffer: pointer to an existing circular buffer
            out: preallocated ndarray with at least items number of elements,
                where buffer contents will be read into
            numitems: number of samples to be read

        Returns:
            The actual number of items read (0 <= n <= items).
        """
        if len(out) < numitems:
            return 0
        ptr = out.ctypes.data_as(ct.c_void_p)
        return libcsound.csoundPeekCircularBuffer(self.cs, buffer, ptr, numitems)

    def writeCircularBuffer(self, buffer: ct.c_void_p, data: np.ndarray, numitems: int) -> int:
        """Writes to circular buffer.

        Args:
            buffer: pointer to an existing circular buffer
            data: ndarray with at least items number of elements to be written
                into circular buffer
            numitems: number of samples to write

        Returns:
            The actual number of items written (0 <= n <= items).
        """
        if len(data) < numitems:
            return 0
        ptr = data.ctypes.data_as(ct.c_void_p)
        return libcsound.csoundWriteCircularBuffer(self.cs, buffer, ptr, numitems)

    def flushCircularBuffer(self, buffer) -> None:
        """Empties circular buffer of any remaining data.

        This function should only be used if there is no reader actively
        getting data from the buffer.

        Args:
            buffer: pointer to an existing circular buffer

        """
        libcsound.csoundFlushCircularBuffer(self.cs, buffer)

    def destroyCircularBuffer(self, buffer) -> None:
        """Frees circular buffer."""
        libcsound.csoundDestroyCircularBuffer(self.cs, buffer)

    def setOpenSoundFileCallback(self, function) -> None:
        """Sets a callback for opening a sound file.

        The callback is made when a sound file is going to be opened.
        The following information is passed to the callback:

        string
            pathname of the file; either full or relative to current dir
        int
            access flags for the file.
        ptr
            sound file info of the file.

        Pass None to disable the callback.
        This callback is retained after a reset() call.
        """
        self._callbacks['openSoundFile'] = f = OPENSOUNDFILEFUNC(function)
        libcsound.csoundSetOpenSoundFileCallback(self.cs, f)

    def setOpenFileCallback(self, function) -> None:
        """Sets a callback for opening a file.

        The callback is made when a file is going to be opened.
        The following information is passed to the callback:

        string
            pathname of the file; either full or relative to current dir
        string
            access mode of the file.

        Pass None to disable the callback.
        This callback is retained after a reset() call.
        """
        self._callbacks['openFileCallback'] = f = OPENFILEFUNC(function)
        libcsound.csoundSetOpenFileCallback(self.cs, f)

    def getOpcodes(self) -> list[OpcodeDef]:
        return _getOpcodes()



CSOUNDPERFTHREAD_p = ct.c_void_p
PROCESSFUNC = ct.CFUNCTYPE(None, ct.c_void_p)

libcspt = libcsound
libcspt.csoundCreatePerformanceThread.restype = CSOUNDPERFTHREAD_p
libcspt.csoundCreatePerformanceThread.argtypes = [CSOUND_p]
libcspt.csoundDestroyPerformanceThread.argtypes = [CSOUNDPERFTHREAD_p]
libcspt.csoundPerformanceThreadIsRunning.restype = ct.c_int32
libcspt.csoundPerformanceThreadIsRunning.argtypes = [CSOUNDPERFTHREAD_p]
libcspt.csoundPerformanceThreadGetProcessCB.restype = ct.c_void_p
libcspt.csoundPerformanceThreadGetProcessCB.argtypes = [CSOUNDPERFTHREAD_p]
libcspt.csoundPerformanceThreadSetProcessCB.argtypes = [CSOUNDPERFTHREAD_p, PROCESSFUNC, ct.c_void_p]
libcspt.csoundPerformanceThreadGetCsound.restype = CSOUND_p
libcspt.csoundPerformanceThreadGetCsound.argtypes = [CSOUNDPERFTHREAD_p]
libcspt.csoundPerformanceThreadGetStatus.restype = ct.c_int32
libcspt.csoundPerformanceThreadGetStatus.argtypes = [CSOUNDPERFTHREAD_p]
libcspt.csoundPerformanceThreadPlay.argtypes = [CSOUNDPERFTHREAD_p]
libcspt.csoundPerformanceThreadPause.argtypes = [CSOUNDPERFTHREAD_p]
libcspt.csoundPerformanceThreadTogglePause.argtypes = [CSOUNDPERFTHREAD_p]
libcspt.csoundPerformanceThreadStop.argtypes = [CSOUNDPERFTHREAD_p]
libcspt.csoundPerformanceThreadRecord.argtypes = [CSOUNDPERFTHREAD_p, ct.c_char_p, ct.c_int32, ct.c_int32]
libcspt.csoundPerformanceThreadStopRecord.argtypes = [CSOUNDPERFTHREAD_p]
libcspt.csoundPerformanceThreadScoreEvent.argtypes = [CSOUNDPERFTHREAD_p, ct.c_int32, ct.c_char, ct.c_int32, ct.POINTER(MYFLT)]
libcspt.csoundPerformanceThreadInputMessage.argtypes = [CSOUNDPERFTHREAD_p, ct.c_char_p]
libcspt.csoundPerformanceThreadSetScoreOffsetSeconds.argtypes = [CSOUNDPERFTHREAD_p, ct.c_double]
libcspt.csoundPerformanceThreadJoin.restype = ct.c_int32
libcspt.csoundPerformanceThreadJoin.argtypes = [CSOUNDPERFTHREAD_p]
libcspt.csoundPerformanceThreadFlushMessageQueue.argtypes = [CSOUNDPERFTHREAD_p]


class CsoundPerformanceThread:
    """Runs Csound in a separate thread.

    The playback (which is paused by default) is stopped by calling
    stop(), or if an error occurs.
    The constructor takes a Csound instance pointer as argument; it assumes
    that ctcsound.compile_() was called successfully before creating
    the performance thread. Once the playback is stopped for one of the above
    mentioned reasons, the performance thread returns.
    """
    def __init__(self, csp: ct.c_void_p):
        self.cpt = libcspt.csoundCreatePerformanceThread(csp)

    def __del__(self):
        libcspt.csoundDestroyPerformanceThread(self.cpt)

    def isRunning(self) -> bool:
        """Returns True if the performance thread is running, False otherwise."""
        return libcspt.csoundPerformanceThreadIsRunning(self.cpt) != 0

    def processCallback(self) -> ct._FuncPointer:
        """Returns the process callback."""
        return PROCESSFUNC(libcspt.csoundPerformanceThreadGetProcessCB(self.cpt))

    def setProcessCallback(self, function: _t.Callable[[ct.c_void_p, _t.Any], None], data):
        """Sets the process callback.
        Args:
            function: a function of the form ``(csound: void, data: Any) -> None``
            data: can be anything
        """
        libcspt.csoundPerformanceThreadSetProcessCB(self.cpt, PROCESSFUNC(function), ct.byref(data))

    def csound(self) -> ct.c_void_p:
        """Returns the Csound instance pointer."""
        return libcspt.csoundPerformanceThreadGetCsound(self.cpt)

    def status(self) -> int:
        """Returns the current status.

        Zero if still playing, positive if the end of score was reached or
        performance was stopped, and negative if an error occured.
        """
        return libcspt.csoundPerformanceThreadGetStatus(self.cpt)

    def play(self):
        """Continues performance if it was paused."""
        libcspt.csoundPerformanceThreadPlay(self.cpt)

    def pause(self) -> None:
        """Pauses performance (can be continued by calling play())."""
        libcspt.csoundPerformanceThreadPause(self.cpt)

    def togglePause(self) -> None:
        """Pauses or continues performance, depending on current state."""
        libcspt.csoundPerformanceThreadtogglePause(self.cpt)

    def stop(self) -> None:
        """Stops performance (cannot be continued)."""
        libcspt.csoundPerformanceThreadStop(self.cpt)

    def record(self, filename: str, samplebits: int, numbufs: int):
        """Starts recording the output from Csound.

        The sample rate and number of channels are taken directly from the
        running Csound instance.
        """
        libcspt.csoundPerformanceThreadRecord(self.cpt, cstring(filename), samplebits, numbufs)

    def stopRecord(self):
        """Stops recording and closes audio file."""
        libcspt.csoundPerformanceThreadStopRecord(self.cpt)

    def scoreEvent(self, absp2mode: int, kind: str, pfields: _t.Sequence[float] | np.ndarray):
        """Sends a score event.

        The event has type *kind* (e.g. 'i' for a note event).

        Args:
            absp2mode: if non-zero, the start time of the event is measured
                from the beginning of performance, instead of the default of
                relative to the current time
            kind: the event kind, one of 'i', 'f', 'e', ...
            pfields: a tuple, a list, or an ndarray of MYFLTs with all the pfields
        """
        p = np.array(pfields).astype(MYFLT)
        ptr = p.ctypes.data_as(ct.POINTER(MYFLT))
        numFields = p.size
        libcspt.csoundPerformanceThreadScoreEvent(self.cpt, ct.c_int32(absp2mode), cchar(kind), numFields, ptr)

    def inputMessage(self, s: str):
        """Sends a score event as a string, similarly to line events (-L)."""
        libcspt.csoundPerformanceThreadInputMessage(self.cpt, cstring(s))

    def setScoreOffsetSeconds(self, time: float):
        """Sets the playback time pointer to the specified value (in seconds)."""
        libcspt.csoundPerformanceThreadSetScoreOffsetSeconds(self.cpt, ct.c_double(time))

    def join(self):
        """Waits until the performance is finished or fails.

        Returns a positive value if the end of score was reached or
        stop() was called, and a negative value if an error occured.
        Also releases any resources associated with the performance thread
        object.
        """
        return libcspt.csoundPerformanceThreadJoin(self.cpt)

    def flushMessageQueue(self):
        """Waits until all pending messages are actually received.

        (pause, send score event, etc.)
        """
        libcspt.csoundPerformanceThreadFlushMessageQueue(self.cpt)


def getSystemSr(module: str = '') -> tuple[float, str]:
    """
    Get the system samplerate reported by csound

    Not all modules report a system samplerate. Modules
    which do report it are 'jack' and 'auhal' (coreaudio). Portaudio
    will normally report a default samplerate of 44100, but this may
    vary for each platform. T obtain a list of available modules see
    :meth:`Csound.modules`

    Args:
        module: the module to use, or a default for each platform

    Returns:
        a tuple (samplerate: float, module: str), where samplerate
        is the reported samplerate and module is the module used
        (which is only of interest if no module was given)
    """
    if not module:
        module = _util.defaultRealtimeModule()
    csound = Csound()
    csound.createMessageBuffer(echo=False)
    csound.setOption(f'-+rtaudio={module}')
    csound.setOption(f'-odac')
    csound.setOption('--get-system-sr')
    sr = 0.
    for msg, attr in csound.iterMessages():
        if msg.startswith("system sr:"):
            sr = float(msg.split(":")[1].strip())
            break
    csound.destroyMessageBuffer()
    return sr, module


def _getOpcodes() -> list[OpcodeDef]:
    cs = Csound()
    cs.createMessageBuffer(echo=False)
    cs.setOption('-z1')
    msgcnt = cs.messageCnt()
    opcodes = []
    parts = []
    _ = _util.asciistr
    for i in range(cs.messageCnt()):
        msg = cs.firstMessage()
        cs.popFirstMessage()
        msgstripped = msg.strip()
        if msgstripped:
            parts.append(msgstripped)
        if msg.endswith('\n'):
            if not parts:
                break
            name = parts[0]
            if len(parts) == 3:
                outsig = parts[1].strip()
                insig = parts[2].strip()
            else:
                continue
            if outsig == '(null)':
                outsig = ''
            if insig == '(null)':
                insig = ''
            opcodes.append(OpcodeDef(name=_(name), outtypes=_(outsig), intypes=_(insig), flags=0))
            parts.clear()
    return opcodes
