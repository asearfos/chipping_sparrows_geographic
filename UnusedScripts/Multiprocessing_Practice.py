from multiprocessing import Pool, sharedctypes
import numpy as np
import warnings


def func(n):
    # ignore the PEP 3118 buffer warning
    # with warnings.catch_warnings():
    #     warnings.simplefilter('ignore', RuntimeWarning)

    v = np.ctypeslib.as_array(shared)

    print(n, v)
    return v.ctypes.data  # return the address


shared = None


def _init(a):
    global shared
    shared = a


if __name__ == '__main__':
    tmp = np.ctypeslib.as_ctypes(np.zeros((5,5)).flat)
    print(type(tmp))
    a = sharedctypes.Array(tmp._type_, tmp, lock=False)
    print(type(a))
    pool = Pool(processes=2, initializer=_init, initargs=a)

    a[0] = 1.0
    result = pool.map(func, range(3))
    print(result)