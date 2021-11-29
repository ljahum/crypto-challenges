from Crypto.Util.number import *

def GCRT(mi, ai):
    """
    mi is modules
    ai is lefts
    return is msg ans big modules
    """
    assert (isinstance(mi, list) and isinstance(ai, list))
    curm, cura = mi[0], ai[0]
    for (m, a) in zip(mi[1:], ai[1:]):
        d = int(GCD(curm, m))
        c = a - cura
        assert (c % d == 0)
        K = c // d * inverse(curm // d, m // d)
        cura += curm * K
        curm = curm * m // d
        cura %= curm
    return cura % curm, curm


# secret = GCRT(primes, c)
