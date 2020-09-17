import ctypes


class Point(ctypes.Structure):
    _field_ = [("x", ctypes.c_int32), ("y", ctypes.c_int32)]


def main():
    p = Point(x=1, y=2)


if __name__ == "__main__":
    main()
