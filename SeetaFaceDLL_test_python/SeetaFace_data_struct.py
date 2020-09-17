import ctypes


class SeetaImageData(ctypes.Structure):
    _fields_ = [
        ("width", ctypes.c_int32),
        ("height", ctypes.c_int32),
        ("channels", ctypes.c_int32),
        ("data", ctypes.POINTER(ctypes.c_uint8))
    ]


class SeetaRect(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_int),
        ("y", ctypes.c_int),
        ("width", ctypes.c_int),
        ("height", ctypes.c_int)
    ]


class SeetaFaceInfo(ctypes.Structure):
    _fields_ = [
        ("pos", SeetaRect),
        ("score", ctypes.c_float)
    ]


class SeetaFaceInfoArray(ctypes.Structure):
    _fields_ = [
        ("data", ctypes.POINTER(SeetaFaceInfo)),
        ("size", ctypes.c_int32)
    ]
