import ctypes
import logging
import nose
import random
import sys
import time
import types

sys.path.append("..")

from pycanlib import canlib, canstat, CAN


testLogger = logging.getLogger("pycanlib.test")


def setup():
    canlib.canInitializeLibrary()
    _numChannels = ctypes.c_int(0)
    canlib.canGetNumberOfChannels(ctypes.byref(_numChannels))
    numChannels = _numChannels.value
    #We need to verify that all of pycanlib's functions operate correctly
    #on both virtual and physical channels, so we need to find at least one
    #of each to test with
    physicalChannels = []
    virtualChannels = []
    for _channel in xrange(numChannels):
        _cardType = ctypes.c_int(0)
        canlib.canGetChannelData(_channel,
          canlib.canCHANNELDATA_CARD_TYPE, ctypes.byref(_cardType), 4)
        if _cardType.value == canlib.canHWTYPE_VIRTUAL:
            virtualChannels.append(_channel)
        elif _cardType.value != canlib.canHWTYPE_NONE:
            physicalChannels.append(_channel)
    testLogger.debug("numChannels = %d" % numChannels)
    testLogger.debug("virtualChannels = %s" % virtualChannels)
    testLogger.debug("physicalChannels = %s" % physicalChannels)
    if len(virtualChannels) == 0:
        raise Exception("No virtual channels available for testing")
    elif len(physicalChannels) == 0:
        raise Exception("No physical channels available for testing")


def testShallCreateInfoMessageObject():
    _msgObject = None
    _msgObject = CAN.InfoMessage()
    assert (_msgObject != None)
    assert ("timestamp" in _msgObject.__dict__.keys())
    assert ("info" in _msgObject.__dict__.keys())


def testShallNotAcceptInvalidTimestamps():
    for timestamp in ["foo", -5, -1.0, 0.0, 1, 1.0, 2.5, 10000, 10000.2]:
        yield isTimestampValid, timestamp


def isTimestampValid(timestamp):
    _msgObject = None
    try:
        _msgObject = CAN.InfoMessage(timestamp=timestamp)
    except Exception as e:
        testLogger.debug("Exception thrown by CAN.InfoMessage", exc_info=True)
        testLogger.debug(e.__str__())
    if isinstance(timestamp, (types.FloatType, types.IntType)) and (timestamp >= 0):
        assert (_msgObject != None)
    else:
        assert (_msgObject == None)


def testShallProvideStringRepresentationOfInfoMessage():
    timestamps = range(0, 10000, 503)
    infoStrings = ["info string 1", "info string 2", "not an info string",
                   "another string", None]
    for timestamp in timestamps:
        for infoString in infoStrings:
            yield checkInfoMsgStringRep, (float(timestamp) / 10), infoString


def checkInfoMsgStringRep(timestamp, infoString):
    _msgObject = None
    _msgObject = CAN.InfoMessage(timestamp=timestamp, info=infoString)
    assert (_msgObject != None)
    assert (_msgObject.timestamp == timestamp)
    assert (_msgObject.info == infoString)
    if infoString != None:
        assert (_msgObject.__str__() == "%.6f\t%s" % (timestamp, infoString))
    else:
        assert (_msgObject.__str__() == "%.6f" % timestamp)


def testShallCreateCANMessageObject():
    _msgObject = None
    _msgObject = CAN.Message()
    assert (_msgObject != None)
    assert ("timestamp" in _msgObject.__dict__.keys())
    assert ("device_id" in _msgObject.__dict__.keys())
    assert ("dlc" in _msgObject.__dict__.keys())
    assert ("payload" in _msgObject.__dict__.keys())
    assert ("flags" in _msgObject.__dict__.keys())


def testShallNotAcceptInvalidDeviceIDs():
    for device_id in ["foo", 0, 0.1, 10000, 0x0100, 2 ** 32]:
        yield isDeviceIDValid, device_id


def isDeviceIDValid(device_id):
    _msgObject = None
    try:
        _msgObject = CAN.Message(device_id=device_id)
    except Exception as e:
        testLogger.debug("Exception thrown by CAN.Message", exc_info=True)
        testLogger.debug(e.__str__())
    if isinstance(device_id, types.IntType) and (device_id in range(0, 2 ** 11)):
        assert (_msgObject != None)
    else:
        assert (_msgObject == None)


def testShallNotAcceptInvalidPayload():
    payloads = []
    payloads.append([])
    payloads.append([10000])
    payloads.append(["foo"])
    payloads.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    payloads.append([0, 100000])
    payloads.append([" ", 0])
    for payload in payloads:
        yield isPayloadValid, payload


def isPayloadValid(payload):
    _msgObject = None
    try:
        _msgObject = CAN.Message(payload=payload)
    except Exception as e:
        testLogger.debug("Exception thrown by CAN.Message", exc_info=True)
        testLogger.debug(e.__str__())
    payloadValid = True
    if len(payload) not in range(0, 9):
        payloadValid = False
    for item in payload:
        if not isinstance(item, types.IntType):
            payloadValid = False
        elif item not in range(0, 256):
            payloadValid = False
    if payloadValid:
        assert (_msgObject != None)
        assert (_msgObject.payload == payload)
    else:
        assert (_msgObject == None)


def testShallNotAcceptInvalidDLC():
    dlcs = ["foo", 0.25]
    for i in xrange(-2, 10):
        dlcs.append(i)
    for dlc in dlcs:
        yield isDLCValid, dlc


def isDLCValid(dlc):
    _msgObject = None
    try:
        _msgObject = CAN.Message(dlc=dlc)
    except Exception as e:
        testLogger.debug("Exception thrown by CAN.Message", exc_info=True)
        testLogger.debug(e.__str__())
    if dlc in range(0, 9):
        assert (_msgObject != None)
    else:
        assert (_msgObject == None)


def testShallNotAcceptInvalidFlags():
    flagsValues = ["foo", 0.25]
    for i in xrange(-2, 2):
        flagsValues.append(i)
    for i in xrange(2 ** 15 - 2, 2 ** 15 + 2):
        flagsValues.append(i)
    for i in xrange(2 ** 16 - 2, 2 ** 16 + 2):
        flagsValues.append(i)
    for flagsValue in flagsValues:
        yield areFlagsValid, flagsValue


def areFlagsValid(flags):
    _msgObject = None
    try:
        _msgObject = CAN.Message(flags=flags)
    except Exception as e:
        testLogger.debug("Exception thrown by CAN.Message", exc_info=True)
        testLogger.debug(e.__str__())
    if flags in range(0, 2 ** 16):
        assert (_msgObject != None)
    else:
        assert (_msgObject == None)


def testShallProvideStringRepresentationOfCANMessage():
    timestamps = [0.0, 1.23456, 9.9999999999, 1.06]
    dataArrays = [[1], [255], [0xb0, 0x81, 0x50]]
    dlcs = range(0, 9)
    flagsValues = [0, 1, 2 ** 15, 2 ** 16 - 1]
    deviceIDs = [0x0040, 0x0008, 0x0100]
    testData = []
    for timestamp in timestamps:
        for dataArray in dataArrays:
            for dlc in dlcs:
                for flags in flagsValues:
                    for device_id in deviceIDs:
                        yield (checkCANMessageStringRepr, timestamp,
                               dataArray, dlc, flags, device_id)


def checkCANMessageStringRepr(timestamp, dataArray, dlc, flags, device_id):
    _msgObject = None
    _msgObject = CAN.Message(device_id=device_id, timestamp=timestamp,
                             payload=dataArray, dlc=dlc, flags=flags)
    assert (_msgObject != None)
    dataString = ("%s" % ' '.join([("%.2x" % byte) for byte in dataArray]))
    expectedStringRep = "%.6f\t%.4x\t%.4x\t%d\t%s" % (timestamp, device_id,
                                                    flags, dlc, dataString)
    assert (_msgObject.__str__() == expectedStringRep)


def testShallCreateBusObject():
    _bus1 = None
    _bus2 = None
    _bus1 = CAN.Bus()
    _bus2 = CAN.Bus()
    assert (_bus1 != None)
    assert (_bus2 != None)
    testLogger.debug("_bus1._write_handle.get_canlib_handle() = %d" %
                     _bus1._write_handle.get_canlib_handle())
    testLogger.debug("_bus2.writeHandle.get_canlib_handle() = %d" %
                     _bus2._write_handle.get_canlib_handle())
    assert (_bus1._write_handle.get_canlib_handle() == _bus2._write_handle.get_canlib_handle())
    assert (_bus1._read_handle.get_canlib_handle() == _bus2._read_handle.get_canlib_handle())


def testShallAcceptOnlyLegalChannelNumbers():
    _numChannels = ctypes.c_int(0)
    canlib.canGetNumberOfChannels(ctypes.byref(_numChannels))
    channelNumbers = ["foo", 0.25]
    for i in xrange(-3, _numChannels.value + 3):
        channelNumbers.append(i)
    for channelNumber in channelNumbers:
        yield checkChannelNumber, channelNumber, _numChannels.value


def checkChannelNumber(channelNumber, numChannels):
    _bus = None
    try:
        _bus = CAN.Bus(channel=channelNumber,
                       flags=canlib.canOPEN_ACCEPT_VIRTUAL)
    except:
        testLogger.debug("Exception thrown by CAN.Bus", exc_info=True)
    if channelNumber in range(0, numChannels):
        assert (_bus != None)
    else:
        testLogger.debug("numChannels = %d" % numChannels)
        assert (_bus == None)


#def testShallAcceptOnlyLegalSegmentLengths():
#    segmentLengths = ["foo", 0.25]
#    for i in xrange(-1, 10):
#        segmentLengths.append(i)
#    for tseg1 in segmentLengths:
#        for tseg2 in segmentLengths:
#            yield checkSegmentLengths, tseg1, tseg2


#def checkSegmentLengths(tseg1, tseg2):
#    _bus = None
#    try:
#        _bus = CAN.Bus(tseg1=tseg1, tseg2=tseg2)
#    except:
#        testLogger.debug("Exception thrown by CAN.Bus", exc_info=True)
#    if (isinstance(tseg1, types.IntType) and
#        isinstance(tseg2, types.IntType) and ((tseg1 + tseg2) < 16) and
#        (tseg1 >= 0) and (tseg2 >= 0)):
#        assert (_bus != None)
#    else:
#        assert (_bus == None)


def testShallNotAcceptInvalidBusFlags():
    _numChannels = ctypes.c_int(0)
    canlib.canGetNumberOfChannels(ctypes.byref(_numChannels))
    numChannels = _numChannels.value
    virtualChannels = []
    physicalChannels = []
    for _channel in xrange(numChannels):
        _cardType = ctypes.c_int(0)
        canlib.canGetChannelData(_channel,
          canlib.canCHANNELDATA_CARD_TYPE, ctypes.byref(_cardType), 4)
        if _cardType.value == canlib.canHWTYPE_VIRTUAL:
            virtualChannels.append(_channel)
        else:
            physicalChannels.append(_channel)
    testLogger.debug(virtualChannels)
    for _channel in virtualChannels:
        yield openVirtualChannelWithIncorrectFlags, _channel
    for _channel in virtualChannels:
        yield openChannelWithInvalidFlags, _channel
    for _channel in physicalChannels:
        yield openChannelWithInvalidFlags, _channel


def openVirtualChannelWithIncorrectFlags(channel):
    _bus = None
    try:
        _bus = CAN.Bus(channel=channel, flags=0)
    except CAN.InvalidBusParameterError as e:
        testLogger.debug("Exception thrown by CAN.Bus", exc_info=True)
        testLogger.debug(e)
#    except Exception as e:
#        print type(e)
#        raise e
    assert (_bus == None)


def openChannelWithInvalidFlags(channel):
    _bus = None
    try:
        _bus = CAN.Bus(channel=channel, flags=0xFFFF)
    except CAN.InvalidBusParameterError as e:
        testLogger.debug("Exception thrown by CAN.Bus", exc_info=True)
        testLogger.debug(e)
    assert (_bus == None)


def testCheckStatus():
    for _handle in xrange(-100, 100):
        if (_handle not in CAN.READ_HANDLE_REGISTRY.keys()) and \
          (_handle not in CAN.WRITE_HANDLE_REGISTRY.keys()):
            yield operateOnInvalidHandle, _handle


def operateOnInvalidHandle(handle):
    try:
        device_id = ctypes.c_long(0)
        data = ctypes.create_string_buffer(8)
        dlc = ctypes.c_uint(0)
        flags = ctypes.c_uint(0)
        flags = ctypes.c_uint(0)
        timestamp = ctypes.c_long(0)
        canlib.canRead(handle, ctypes.byref(device_id),
          ctypes.byref(data), ctypes.byref(dlc), ctypes.byref(flags),
          ctypes.byref(timestamp))
    except canlib.CANLIBError as e:
        testLogger.debug("canRead throws exception", exc_info=True)
        assert (e.error_code == canstat.canERR_INVHANDLE)
        expected = "function canRead failed -"
        expected += " Handle is invalid (code -10)"
        actual = e.__str__()[:len(expected)]
        assert (expected == actual)


def testReadWrite():
    _numChannels = ctypes.c_int(0)
    canlib.canGetNumberOfChannels(ctypes.byref(_numChannels))
    numChannels = _numChannels.value
    virtualChannels = []
    physicalChannels = []
    for _channel in xrange(numChannels):
        _cardType = ctypes.c_int(0)
        canlib.canGetChannelData(_channel,
          canlib.canCHANNELDATA_CARD_TYPE, ctypes.byref(_cardType), 4)
        if _cardType.value == canlib.canHWTYPE_VIRTUAL:
            virtualChannels.append(_channel)
        else:
            physicalChannels.append(_channel)
    testLogger.debug(virtualChannels)
    for _channel in physicalChannels:
        yield writeAndReadBack, _channel
    for _channel in virtualChannels:
        yield writeAndReadBack, _channel, canlib.canOPEN_ACCEPT_VIRTUAL


def writeAndReadBack(busChannel, flags=0):
    _bus1 = CAN.Bus(channel=busChannel, speed=105263, tseg1=10, tseg2=8,
                    sjw=4, no_samp=1, flags=flags, name="_bus1")
    _bus2 = CAN.Bus(channel=busChannel, speed=105263, tseg1=10, tseg2=8,
                    sjw=4, no_samp=1, flags=flags, name="_bus2")
    _startTime = _bus1.read_timer()
    _msg1 = CAN.Message(device_id=0x0010, payload=[1, 2, 3], dlc=3, flags=0x02)
    _bus1.write(_msg1)
    rxMsg = None
    testFailed = True
    while _bus1.read_timer() < (_startTime + 5):
        tmp = _bus2.read()
        if tmp != None:
            testLogger.debug(tmp)
            rxMsg = tmp
            if ((_msg1.device_id == rxMsg.device_id) and
                (_msg1.payload == rxMsg.payload) and
                (_msg1.dlc == rxMsg.dlc) and
                (_msg1.flags == rxMsg.flags)):
                testLogger.debug("rxMsg matches _msg1")
                testLogger.debug(rxMsg)
                testLogger.debug(_msg1)
                testFailed = False
                break
    assert not testFailed
    _startTime = _bus1.read_timer()
    _bus2.write(_msg1)
    rxMsg = None
    testFailed = True
    while _bus1.read_timer() < (_startTime + 5):
        tmp = _bus1.read()
        if tmp != None:
            rxMsg = tmp
            if ((_msg1.device_id == rxMsg.device_id) and
                (_msg1.payload == rxMsg.payload) and
                (_msg1.dlc == rxMsg.dlc) and
                (_msg1.flags == rxMsg.flags)):
                testLogger.debug("rxMsg matches _msg1")
                testLogger.debug(rxMsg)
                testLogger.debug(_msg1)
                testFailed = False
                break
    assert not testFailed
