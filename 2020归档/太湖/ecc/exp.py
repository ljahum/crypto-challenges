import collections*
import random
from Crypto.Util.number import *

EllipticCurve = collections.namedtuple('EllipticCurve', 'name p a b')

curve = EllipticCurve(
	'secp256k1',
	p=0x00fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffeffffffff0000000000000000ffffffff,
	a=0x00fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffeffffffff0000000000000000fffffffc,

	b =0x00b3312fa7e23ee7e4988e056be3f82d19181d9c6efe8141120314088f5013875ac656398d8a2ed19d2a85c8edd3ec2aef,

)


# Modular arithmetic ##########################################################

def inverse_mod(k, p):
   """Returns the inverse of k modulo p.
  This function returns the only integer x such that (x * k) % p == 1.
  k must be non-zero and p must be a prime.
  """
   if k == 0:
	   raise ZeroDivisionError('division by zero')

   if k < 0:
	   # k ** -1 = p - (-k) ** -1 (mod p)
	   return p - inverse_mod(-k, p)

   # Extended Euclidean algorithm.
   s, old_s = 0, 1
   t, old_t = 1, 0
   r, old_r = p, k

   while r != 0:
	   quotient = old_r // r
	   old_r, r = r, old_r - quotient * r
	   old_s, s = s, old_s - quotient * s
	   old_t, t = t, old_t - quotient * t

   gcd, x, y = old_r, old_s, old_t

   
   

   return x % p


# Functions that work on curve points #########################################

def is_on_curve(point):
   """Returns True if the given point lies on the elliptic curve."""
   if point is None:
	   # None represents the point at infinity.
	   return True

   x, y = point

   return (y * y - x * x * x - curve.a * x - curve.b) % curve.p == 0


def point_neg(point):
   """Returns -point."""
   

   if point is None:
	   # -0 = 0
	   return None

   x, y = point
   result = (x, -y % curve.p)

   

   return result


def point_add(point1, point2):
   """Returns the result of point1 + point2 according to the group law."""
   
   

   if point1 is None:
	   # 0 + point2 = point2
	   return point2
   if point2 is None:
	   # point1 + 0 = point1
	   return point1

   x1, y1 = point1
   x2, y2 = point2

   if x1 == x2 and y1 != y2:
	   # point1 + (-point1) = 0
	   return None

   if x1 == x2:
	   # This is the case point1 == point2.
	   m = (3 * x1 * x1 + curve.a) * inverse_mod(2 * y1, curve.p)
   else:
	   # This is the case point1 != point2.
	   m = (y1 - y2) * inverse_mod(x1 - x2, curve.p)

   x3 = m * m - x1 - x2
   y3 = y1 + m * (x3 - x1)
   result = (x3 % curve.p,
			 -y3 % curve.p)

   

   return result


def scalar_mult(k, point):
   """Returns k * point computed using the double and point_add algorithm."""
   

   if k < 0:
	   # k * point = -k * (-point)
	   return scalar_mult(-k, point_neg(point))

   result = None
   addend = point

   while k:
	   if k & 1:
		   # Add.
		   result = point_add(result, addend)

	   # Double.
	   addend = point_add(addend, addend)

	   k >>= 1

   

   return result


# Keypair generation and ECDHE ################################################

def main():
	G = (0xaa87ca22be8b05378eb1c71ef320ad746e1d3b628ba79b9859f741e082542a385502f25dbf55296c3a545e3872760ab7,
		 0x3617de4a96262c6f5d9e98bf9292dc29f8f41dbd289a147ce9da3113b5f0b8c00a60b1ce1d7e819d7a431d7c90ea0e5f)
	pri = 0xe05b05a4d6c336fba9346a64932f145a4c89d641a07a4cdda185daeda7943fa0dcc2428820cc7ff7644d817917ebcace
	pub = (0x8625db50578051603a33679ddc3a47258f38553f22840d7076a2f8e20296da56886a7e2e240fcf0b5775f474ca0b0690,
			0xb041c446ffef03ae4b3e622f5b99649a264172e7dfa85b5ce87468ac436e679f31a792ae8830414e81515ddc61dbc708)


	c1 = (24003781112879348220058803836033945042865485305464905467674393176615089477541954401077778512524464973048661625611766,
	28206975141069863747440019357792832391407275600645008495572799929028656654635919809015500539951381128059791451723260)

	c2 = (25972577012057310998482368542830747788006175098189596510234023630951675635795121449793787044812379072009990261128415,
	  26404574880338157355180649551087036452335866504634102098567238931093015093862341056668365880979208280931190589546641)
	
	p = 0x00fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffeffffffff0000000000000000ffffffff

	
	rpub = scalar_mult(pri,c2)
	print(rpub[0])
	m1= c1[0]*invert(rpub[0],p)%p
	m2= c1[1]*invert(rpub[1],p)%p
	print(long_to_bytes(m1)+long_to_bytes(m2))

	
if __name__ == '__main__':
	main()

	# flag{3CC_I3_Use7f1_HaHA}
	
