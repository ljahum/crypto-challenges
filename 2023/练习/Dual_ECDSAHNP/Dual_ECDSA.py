from sage.all import *
from hashlib import sha256
from Crypto.Util.number import long_to_bytes, bytes_to_long
from math import ceil
from random import randint

# safe curve parameters
# NIST P-256
NIST_256 = (
    NIST_256_P := 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff,
    NIST_256_K := GF(NIST_256_P),
    NIST_256_A := NIST_256_K(0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc),
    NIST_256_B := NIST_256_K(0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b),
    NIST_256_CURVE := EllipticCurve(NIST_256_K, (NIST_256_A, NIST_256_B)),
    NIST_256_GEN := NIST_256_CURVE(0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296, 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5),
    NIST_256_ORDER := 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551 * 0x1
)
NIST_256_CURVE.set_order(NIST_256_ORDER)

# NIST P-521
NIST_521 = (
    NIST_521_P := 0x01ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff,
    NIST_521_K := GF(NIST_521_P),
    NIST_521_A := NIST_521_K(0x01fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffc),
    NIST_521_B := NIST_521_K(0x0051953eb9618e1c9a1f929a21a0b68540eea2da725b99b315f3b8b489918ef109e156193951ec7e937b1652c0bd3bb1bf073573df883d2c34f1ef451fd46b503f00),
    NIST_521_CURVE := EllipticCurve(NIST_521_K, (NIST_521_A, NIST_521_B)),
    NIST_521_GEN := NIST_521_CURVE(0x00c6858e06b70404e9cd9e3ecb662395b4429c648139053fb521f828af606b4d3dbaa14b5e77efe75928fe1dc127a2ffa8de3348b3c1856a429bf97e7e31c2e5bd66, 0x011839296a789a3bc0045c8a5fb42c7d1bd998f54449579b446817afbd17273e662c97ee72995ef42640c550b9013fad0761353c7086a272c24088be94769fd16650),
    NIST_521_ORDER := 0x01fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa51868783bf2f966b7fcc0148f709a5d03bb5c9b8899c47aebb6fb71e91386409 * 0x1
)
NIST_521_CURVE.set_order(NIST_521_ORDER)

FLAG = open("./flag", "rb").read()
assert len(FLAG) == 64


class Dual_EC():

    def __init__(self, state=None, defaul_curve=True) -> None:
        if state == None:
            self.state = randint(1, 2**256)
        else:
            self.state = state
        if defaul_curve:
            self.init_curve(None)

    def init_curve(self, paras: tuple or list) -> None:
        if paras == None:
            self.Curve = NIST_256_CURVE
            # replace the generator
            self.g = NIST_256_GEN * self.state
            self.curve_order = NIST_256_ORDER
            self.P = randint(1, 2**20) * self.g
            self.Q = randint(1, 2**20) * self.g
        # customized curve
        else:
            Curve, P, Q = paras
            if not Curve.is_on_curve(P) or not Curve.is_on_curve(Q):
                raise ValueError("Points are not on the curve")
            self.Curve = Curve
            self.g = Curve.gen(0)
            self.P = P
            self.Q = Q

    def _update(self):
        self.state = int((self.state * self.P).xy()[0])

    def round(self) -> None:
        # extract the high 240 bits
        out = int((self.state * self.Q).xy()[0]) >> 16
        self._update()
        return out

    def random_bytes(self, n: int) -> int:
        rounds = ceil(n*8/240)
        out = 0
        for _ in range(rounds):
            out = (out << 240) + self.round()
        return long_to_bytes(out >> (rounds*240 - n*8), n)

    def random_bit_integer(self, n: int) -> int:
        rounds = ceil(n/240)
        out = 0
        for _ in range(rounds):
            out = (out << 240) + self.round()
        return out >> (rounds*240 - n)


class ECDSA():
 
    def __init__(self) -> None:
        self.prng = Dual_EC()
        self.hashfunc = sha256
        self.curve_bits = 521
        self.curve = NIST_521_CURVE
        self.generator = NIST_521_GEN
        self.order = NIST_521_ORDER
        self.pri_key = self.prng.random_bit_integer(self.curve_bits)
        self.pub_key = self.pri_key * self.generator

    def set_curve(self, curve: EllipticCurve) -> None:
        self.curve = curve
        self.generator = curve.gen(0)
        self.order = curve.order()
        self.curve_bits = self.order.nbits()

    def set_pri_key(self, d: int) -> None:
        self.pri_key = d
        self.pub_key = d * self.generator

    def sign(self, msg: bytes) -> tuple:
        k_bytes = self.prng.random_bytes(self.curve_bits//8)
        k = int(self.hashfunc(k_bytes).hexdigest(), 16)
        P = k * self.generator
        r = int(P.xy()[0])
        k_inv = int(inverse_mod(k, self.order))
        e = int(self.hashfunc(msg).hexdigest(), 16)
        s = (e + self.pri_key*r) * k_inv % self.order
        return (r, s)

    def verify(self, msg: bytes, signature: tuple) -> bool:
        r, s = signature
        if not (0 < r < self.order and 0 < s < self.order):
            return False
        e = int(self.hashfunc(msg).hexdigest(), 16)
        w = int(inverse_mod(s, self.order))
        u1 = e * w % self.order
        u2 = r * w % self.order
        P = u1 * self.generator + u2 * self.pub_key
        return int(r) == int(P.xy()[0])

    def embed_secret(self, msg: bytes) -> tuple:
        S = self.curve.lift_x(ZZ(bytes_to_long(msg)))
        K = self.prng.random_bit_integer(self.curve_bits)
        return K * S


if __name__ == "__main__":
    SIGNER = ECDSA()

    sig1 = SIGNER.sign(b"AN INFAMOUS PRNG NAMED DUAL_EC BACKDOORED BY NSA, FINALLY CONFIRMED BY SNOWDEN IN 2013.")
    sig2 = SIGNER.sign(b"NO ONE CAN EXTRACT THE BACKDOOR! UNLESS YOU CAN BREAK THE ECDSA SIGNATURE SCHEME / ECDLP!")
    emb_flag = SIGNER.embed_secret(FLAG)

    print(f"pub_key = {SIGNER.pub_key.xy() }")
    print(f"P = {SIGNER.prng.P.xy() }")
    print(f"Q = {SIGNER.prng.Q.xy() }")
    print(f"{sig1 = }")
    print(f"{sig2 = }")
    print(f"emb_flag = {emb_flag.xy() }")