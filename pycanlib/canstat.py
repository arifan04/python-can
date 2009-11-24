import ctypes


class c_canStatus(ctypes.c_int):
    pass

canOK = 0
canERR_PARAM = -1
canERR_NOMSG = -2
canERR_NOTFOUND = -3
canERR_NOMEM = -4
canERR_NOCHANNELS = -5
canERR_RESERVED_3 = -6
canERR_TIMEOUT = -7
canERR_NOTINITIALIZED = -8
canERR_NOHANDLES = -9
canERR_INVHANDLE = -10
canERR_INIFILE = -11
canERR_DRIVER = -12
canERR_TXBUFOFL = -13
canERR_RESERVED_1 = -14
canERR_HARDWARE = -15
canERR_DYNALOAD = -16
canERR_DYNALIB = -17
canERR_DYNAINIT = -18
canERR_NOT_SUPPORTED = -19
canERR_RESERVED_5 = -20
canERR_RESERVED_6 = -21
canERR_RESERVED_2 = -22
canERR_DRIVERLOAD = -23
canERR_DRIVERFAILED = -24
canERR_NOCONFIGMGR = -25
canERR_NOCARD = -26
canERR_RESERVED_7 = -27
canERR_REGISTRY = -28
canERR_LICENSE = -29
canERR_INTERNAL = -30
canERR_NO_ACCESS = -31
canERR_NOT_IMPLEMENTED = -32
canERR__RESERVED = -33


def CANSTATUS_SUCCESS(status):
    return (status >= canOK)

canEVENT_RX = 32000
canEVENT_TX = 32001
canEVENT_ERROR = 32002
canEVENT_STATUS = 32003
canEVENT_ENVVAR = 32004

canNOTIFY_NONE = 0
canNOTIFY_RX = 0x0001
canNOTIFY_TX = 0x0002
canNOTIFY_ERROR = 0x0004
canNOTIFY_STATUS = 0x0008
canNOTIFY_ENVVAR = 0x0010

canSTAT_ERROR_PASSIVE = 0x00000001
canSTAT_BUS_OFF = 0x00000002
canSTAT_ERROR_WARNING = 0x00000004
canSTAT_ERROR_ACTIVE = 0x00000008
canSTAT_TX_PENDING = 0x00000010
canSTAT_RX_PENDING = 0x00000020
canSTAT_RESERVED_1 = 0x00000040
canSTAT_TXERR = 0x00000080
canSTAT_RXERR = 0x00000100
canSTAT_HW_OVERRUN = 0x00000200
canSTAT_SW_OVERRUN = 0x00000400
canSTAT_OVERRUN = (canSTAT_HW_OVERRUN | canSTAT_SW_OVERRUN)

canMSG_MASK = 0x00ff
canMSG_RTR = 0x0001
canMSG_STD = 0x0002
canMSG_EXT = 0x0004
canMSG_WAKEUP = 0x0008
canMSG_NERR = 0x0010
canMSG_ERROR_FRAME = 0x0020
canMSG_TXACK = 0x0040
canMSG_TXRQ = 0x0080

canMSGERR_MASK = 0xff00
canMSGERR_HW_OVERRUN = 0x0200
canMSGERR_SW_OVERRUN = 0x0400
canMSGERR_STUFF = 0x0800
canMSGERR_FORM = 0x1000
canMSGERR_CRC = 0x2000
canMSGERR_BIT0 = 0x4000
canMSGERR_BIT1 = 0x8000

canMSGERR_OVERRUN = 0x0600
canMSGERR_BIT = 0xC000
canMSGERR_BUSERR = 0xF800

canTRANSCEIVER_LINEMODE_NA = 0
canTRANSCEIVER_LINEMODE_SWC_SLEEP = 4
canTRANSCEIVER_LINEMODE_SWC_NORMAL = 5
canTRANSCEIVER_LINEMODE_SWC_FAST = 6
canTRANSCEIVER_LINEMODE_SWC_WAKEUP = 7
canTRANSCEIVER_LINEMODE_SLEEP = 8
canTRANSCEIVER_LINEMODE_NORMAL = 9
canTRANSCEIVER_LINEMODE_STDBY = 10
canTRANSCEIVER_LINEMODE_TT_CAN_H = 11
canTRANSCEIVER_LINEMODE_TT_CAN_L = 12
canTRANSCEIVER_LINEMODE_OEM1 = 13
canTRANSCEIVER_LINEMODE_OEM2 = 14
canTRANSCEIVER_LINEMODE_OEM3 = 15
canTRANSCEIVER_LINEMODE_OEM4 = 16
canTRANSCEIVER_RESNET_NA = 0
canTRANSCEIVER_RESNET_MASTER = 1
canTRANSCEIVER_RESNET_MASTER_STBY = 2
canTRANSCEIVER_RESNET_SLAVE = 3

canTRANSCEIVER_TYPE_UNKNOWN = 0
canTRANSCEIVER_TYPE_251 = 1
canTRANSCEIVER_TYPE_252 = 2
canTRANSCEIVER_TYPE_DNOPTO = 3
canTRANSCEIVER_TYPE_W210 = 4
canTRANSCEIVER_TYPE_SWC_PROTO = 5
canTRANSCEIVER_TYPE_SWC = 6
canTRANSCEIVER_TYPE_EVA = 7
canTRANSCEIVER_TYPE_FIBER = 8
canTRANSCEIVER_TYPE_K251 = 9
canTRANSCEIVER_TYPE_K = 10
canTRANSCEIVER_TYPE_1054_OPTO = 11
canTRANSCEIVER_TYPE_SWC_OPTO = 12
canTRANSCEIVER_TYPE_TT = 13
canTRANSCEIVER_TYPE_1050 = 14
canTRANSCEIVER_TYPE_1050_OPTO = 15
canTRANSCEIVER_TYPE_1041 = 16
canTRANSCEIVER_TYPE_1041_OPTO = 17
canTRANSCEIVER_TYPE_RS485 = 18
canTRANSCEIVER_TYPE_LIN = 19
canTRANSCEIVER_TYPE_KONE = 20
canTRANSCEIVER_TYPE_LINX_LIN = 64
canTRANSCEIVER_TYPE_LINX_J1708 = 66
canTRANSCEIVER_TYPE_LINX_K = 68
canTRANSCEIVER_TYPE_LINX_SWC = 70
canTRANSCEIVER_TYPE_LINX_LS = 72
