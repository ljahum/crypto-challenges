from hashlib import md5
from z3 import *
from random import Random
from itertools import count
from time import time
import logging

logging.basicConfig(format='STT> %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

SYMBOLIC_COUNTER = count()

class Untwister:
    def __init__(self):
        name = next(SYMBOLIC_COUNTER)
        self.MT = [BitVec(f'MT_{i}_{name}', 32) for i in range(624)]
        self.index = 0
        self.solver = Solver()

    #This particular method was adapted from https://www.schutzwerk.com/en/43/posts/attacking_a_random_number_generator/
    def symbolic_untamper(self, solver, y):
        name = next(SYMBOLIC_COUNTER)

        y1 = BitVec(f'y1_{name}', 32)
        y2 = BitVec(f'y2_{name}' , 32)
        y3 = BitVec(f'y3_{name}', 32)
        y4 = BitVec(f'y4_{name}', 32)

        equations = [
            y2 == y1 ^ (LShR(y1, 11)),
            y3 == y2 ^ ((y2 << 7) & 0x9D2C5680),
            y4 == y3 ^ ((y3 << 15) & 0xEFC60000),
            y == y4 ^ (LShR(y4, 18))
        ]

        solver.add(equations)
        return y1

    def symbolic_twist(self, MT, n=624, upper_mask=0x80000000, lower_mask=0x7FFFFFFF, a=0x9908B0DF, m=397):
        '''
            This method models MT19937 function as a Z3 program
        '''
        MT = [i for i in MT] #Just a shallow copy of the state

        for i in range(n):
            x = (MT[i] & upper_mask) + (MT[(i+1) % n] & lower_mask)
            xA = LShR(x, 1)
            xB = If(x & 1 == 0, xA, xA ^ a) #Possible Z3 optimization here by declaring auxiliary symbolic variables
            MT[i] = MT[(i + m) % n] ^ xB

        return MT

    def get_symbolic(self, guess):
        name = next(SYMBOLIC_COUNTER)
        ERROR = 'Must pass a string like "?1100???1001000??0?100?10??10010" where ? represents an unknown bit'

        assert type(guess) == str, ERROR
        assert all(map(lambda x: x in '01?', guess)), ERROR
        assert len(guess) <= 32, "One 32-bit number at a time please"
        guess = guess.zfill(32)

        self.symbolic_guess = BitVec(f'symbolic_guess_{name}', 32)
        guess = guess[::-1]

        for i, bit in enumerate(guess):
            if bit != '?':
                self.solver.add(Extract(i, i, self.symbolic_guess) == bit)

        return self.symbolic_guess


    def submit(self, guess):
        '''
            You need 624 numbers to completely clone the state.
                You can input less than that though and this will give you the best guess for the state
        '''
        if self.index >= 624:
            name = next(SYMBOLIC_COUNTER)
            next_mt = self.symbolic_twist(self.MT)
            self.MT = [BitVec(f'MT_{i}_{name}', 32) for i in range(624)]
            for i in range(624):
                self.solver.add(self.MT[i] == next_mt[i])
            self.index = 0

        symbolic_guess = self.get_symbolic(guess)
        symbolic_guess = self.symbolic_untamper(self.solver, symbolic_guess)
        self.solver.add(self.MT[self.index] == symbolic_guess)
        self.index += 1

    def get_random(self):
        '''
            This will give you a random.Random() instance with the cloned state.
        '''
        logger.debug('Solving...')
        start = time()
        self.solver.check()
        model = self.solver.model()
        end = time()
        logger.debug(f'Solved! (in {round(end-start,3)}s)')

        #Compute best guess for state
        state = list(map(lambda x: model[x].as_long(), self.MT))
        result_state = (3, tuple(state+[self.index]), None)
        r = Random()
        r.setstate(result_state)
        return r

leak = [47945, 50431, 10861, 5794, 26338, 2641, 58647, 52422, 35384, 50426, 58144, 2744, 7864, 25333, 3500, 59273, 38075, 38630, 18760, 19660, 54418, 53538, 20251, 25758, 4500, 14384, 40765, 43841, 62662, 64548, 6468, 8997, 20572, 9920, 64146, 49443, 32054, 56082, 21773, 38390, 14905, 47230, 43126, 37449, 1016, 23685, 48461, 13070, 58381, 51813, 48909, 10953, 31195, 1703, 33439, 54463, 63977, 29188, 44901, 53588, 32843, 9923, 2188, 42503, 53555, 44818, 55094, 40544, 25787, 34965, 65151, 37069, 6342, 36889, 51214, 58386, 34925, 9558, 33552, 29554, 30350, 20166, 4221, 61353, 50656, 7337, 1001, 18279, 27268, 49581, 37870, 54591, 12438, 13649, 42007, 33542, 18118, 48407, 34338, 12147, 19178, 8925, 31109, 12296, 52419, 392, 9296, 16055, 64775, 46394, 58494, 24157, 62237, 16211, 23935, 10368, 48440, 60061, 47813, 49032, 50836, 18404, 30552, 7142, 44142, 44549, 36078, 63112, 28345, 39821, 10004, 32221, 16021, 32152, 53113, 13857, 49328, 11817, 27777, 43088, 43453, 29962, 16338, 44353, 27974, 25145, 56050, 34129, 39236, 46167, 64639, 54581, 33004, 35652, 16294, 11109, 19396, 51476, 30332, 24701, 43628, 44507, 27688, 37172, 61339, 9893, 45217, 7969, 33523, 2495, 15578, 55444, 48564, 5055, 16048, 8512, 1819, 19702, 13388, 41099, 30256, 10592, 46063, 30881, 8338, 41214, 55255, 50060, 65028, 9114, 8417, 43767, 62760, 49830, 50660, 19358, 22142, 53025, 37930, 49155, 2150, 56194, 36251, 49654, 32395, 33677, 48743, 12627, 30575, 64001, 60220, 26908, 44207, 23532, 18430, 45511, 33553, 62631, 55155, 58715, 59152, 20864, 14790, 32774, 48679, 24325, 54109, 2747, 17046, 19083, 60413, 11773, 42188, 17011, 13361, 2105, 23067, 45439, 1122, 54117, 31435, 49692, 59556, 51893, 24342, 11073, 52326, 23237, 22930, 12691, 38125, 36714, 54043, 34880, 53599, 18609, 36631, 24367, 49135, 26821, 64486, 12154, 37534, 14100, 33744, 37183, 7652, 26403, 42166, 12290, 32315, 19153, 55490, 4558, 60768, 44149, 26258, 38676, 31228, 43610, 39357, 36475, 29434, 41437, 64762, 5251, 33641, 43819, 29769, 38136, 8348, 33123, 17571, 18343, 50569, 55502, 7371, 14515, 41553, 12979, 1276, 45454, 56057, 51518, 30382, 30678, 60443, 58274, 50882, 64918, 34569, 58195, 34410, 47490, 13676, 37502, 61987, 7616, 11528, 13577, 51098, 5435, 51972, 63061, 55995, 21627, 2439, 47554, 6891, 53790, 62563, 38921, 30600, 49498, 49671, 38844, 42840, 49982, 16503, 13854, 63825, 25195, 41078, 36872, 36288, 63461, 29293, 28630, 23547, 57332, 43051, 49205, 14579, 23897, 944, 47223, 6819, 61851, 57886, 10858, 14380, 35796, 4509, 52576, 47112, 44349, 56553, 45075, 31505, 2779, 17216, 47395, 15024, 26498, 25299, 26548, 39954, 33242, 65187, 33291, 38861, 6956, 4371, 11762, 41126, 54447, 56384, 34835, 595, 52198, 13324, 38653, 21103, 34301, 20781, 64650, 17773, 1921, 46490, 37683, 27720, 7812, 49737, 20423, 16452, 52475, 27896, 49613, 60121, 54986, 30680, 37740, 8407, 30833, 29431, 62841, 27957, 57755, 59153, 44802, 42423, 28202, 54075, 3879, 25261, 57958, 53266, 22806, 64334, 34962, 57708, 20653, 17925, 59244, 38640, 31264, 7962, 5234, 16995, 35712, 39263, 33764, 9168, 59263, 6297, 28879, 54753, 31041, 42448, 57238, 52395, 61412, 29370, 52297, 21906, 36837, 62511, 13185, 53251, 47459, 47320, 24874, 5152, 63178, 20614, 808, 6789, 37043, 9713, 31692, 18319, 60295, 9628, 1053, 54874, 26808, 28046, 27964, 7534, 43316, 51573, 51143, 41954, 16366, 19618, 23676, 63245, 28329, 25170, 55118, 49376, 22296, 41638, 42595, 49291, 51001, 21173, 17098, 11956, 33292, 28909, 63160, 63480, 32649, 49809, 24112, 59503, 38840, 22914, 17473, 51978, 25420, 64060, 58894, 35793, 57163, 59038, 58787, 64067, 55780, 61906, 1696, 156, 25499, 57706, 47842, 47243, 14668, 17052, 57195, 53288, 49178, 2557, 31221, 17492, 11560, 23012, 9147, 44260, 22094, 53197, 40404, 21209, 30940, 18586, 48011, 60631, 8838, 13044, 5480, 19584, 20231, 15078, 58154, 8305, 55680, 49974, 2861, 58626, 61041, 47937, 42776, 35207, 39418, 12989, 1507, 5082, 23278, 26969, 10328, 18480, 34160, 55965, 59869, 197, 38066, 17097, 49306, 12749, 21846, 9946, 12323, 39813, 19141, 14950, 15987, 33630, 14715, 52499, 15978, 24078, 60217, 32262, 11645, 1649, 50062, 21979, 30545, 1450, 48657, 41697, 23357, 17880, 27613, 38277, 54988, 11074, 57591, 183, 62803, 8532, 61133, 26944, 63400, 53095, 8663, 59702, 19325, 24726, 51297, 21286, 2373, 38774, 20677, 29443, 24693, 20621, 14031, 45485, 34645, 9926, 12620, 1406, 41462, 50338, 25841, 61724, 41722, 11520, 48377, 34111, 50805, 23351, 64363, 50091, 35487, 49978, 41001, 37117, 17133, 54868, 58918, 17295, 16857, 45165, 5732, 46277, 54359, 64982, 2336, 61929, 40501, 18901, 39938, 949, 45839, 7519, 36935, 55287, 21096, 44443, 12240, 16160, 28355, 42275, 27747, 13398, 12395, 33973, 17137, 60697, 37064, 27782, 45671, 22264, 505, 20989, 57585, 4283, 43110, 28497, 25900, 16383, 13961, 24192, 29296, 34776, 36286, 18398, 55882, 28748, 54021, 673, 22723, 23699, 48463, 17316, 55309, 54229, 28342, 11147, 16132, 24344, 53367, 45597, 42843, 27078, 4034, 16975, 18534, 29674, 36962, 60773, 8030, 17118, 7392, 41627, 44768, 51104, 10876, 16293, 54589, 65082, 62573, 2679, 23869, 61905, 52526, 51584, 57063, 27294, 51821, 9070, 30961, 38741, 36309, 57422, 58231, 32775, 57469, 2306, 43632, 6110, 17478, 3399, 60718, 23947, 21488, 41712, 43552, 34154, 35374, 17522, 16603, 53459, 52136, 49823, 21443, 35049, 4854, 25769, 63782, 21355, 11189, 17330, 41173, 6620, 24475, 40910, 26100, 34752, 10491, 39327, 561, 24612, 36253, 41875, 1589, 44536, 64133, 37260, 24719, 21955, 40847, 8529, 12294, 22158, 31784, 32185, 18438, 9983, 9362, 46554, 8294, 11447, 38253, 32008, 44252, 14392, 36259, 40422, 53018, 41387, 61549, 43601, 24082, 64942, 50817, 18470, 52024, 19769, 38618, 54451, 44579, 48552, 52967, 3546, 13047, 19986, 752, 25560, 33608, 55220, 35170, 17378, 3632, 7932, 12764, 28016, 51153, 42067, 22380, 11170, 35549, 14546, 6725, 50718, 40157, 54482, 45086, 50180, 44396, 19469, 48734, 9003, 32234, 4973, 19031, 32744, 15216, 11167, 31666, 50585, 28017, 56213, 23276, 62789, 19240, 52247, 51360, 23933, 2117, 23909, 20136, 11108, 55792, 10848, 42772, 52949, 20973, 49997, 20027, 26803, 34251, 18768, 1273, 21372, 57638, 43004, 27339, 51671, 4505, 7193, 64268, 15856, 9038, 63520, 62076, 41936, 27929, 23469, 55533, 25007, 31555, 15349, 11603, 51345, 44304, 49007, 35765, 50361, 48434, 41407, 41415, 27322, 45767, 56009, 17808, 36797, 55785, 18842, 27904, 55984, 54213, 25742, 30451, 13819, 37675, 23224, 18337, 63137, 40370, 39116, 53931, 7352, 5724, 14040, 13609, 34023, 39058, 59660, 20699, 5752, 594, 53440, 58700, 58977, 11902, 11358, 54271, 52581, 63883, 4496, 65446, 8092, 32955, 1788, 7547, 30827, 42738, 51248, 13433, 52570, 45277, 4811, 59546, 17021, 32981, 6168, 45440, 41446, 43907, 44327, 22960, 48214, 53682, 39618, 65392, 31131, 36083, 31230, 15227, 1530, 21222, 11049, 27763, 5251, 56978, 12249, 55352, 54216, 24824, 65111, 21374, 42945, 57027, 3920, 32541, 65155, 12251, 19929, 19866, 58236, 22788, 54575, 53449, 16521, 55829, 14990, 8653, 55846, 6198, 24332, 28673, 50260, 60726, 55293, 35325, 4142, 28883, 19302, 31711, 10833, 62836, 27199, 14853, 21172, 61281, 43290, 23364, 62192, 58280, 64481, 40708, 17966, 54004, 1651, 1008, 12674, 54156, 48976, 60163, 47799, 14781, 37556, 58786, 14677, 16666, 22398, 41273, 22312, 49859, 4327, 54222, 52527, 35043, 35462, 33939, 30396, 17371, 10883, 42056, 31285, 7486, 33758, 62824, 58144, 19003, 17210, 28590, 39138, 20818, 58339, 7397, 30592, 54635, 33004, 6524, 54578, 21592, 33877, 37330, 51484, 18861, 26317, 426, 6365, 34363, 21922, 33037, 22209, 63283, 6463, 22503, 32397, 54053, 8538, 37449, 39658, 34111, 49684, 27364, 55762, 2892, 64875, 17558, 45202, 37747, 61781, 39006, 5, 55444, 4965, 65360, 45810, 23739, 51172, 37274, 39909, 58863, 28111, 449, 14406, 62190, 13688, 57145, 23653, 56791, 4065, 13079, 59309, 57940, 59317, 17968, 28037, 27233, 53242, 30901, 10758, 57188, 9100, 51760, 16566, 20555, 50514, 35271, 59680, 24646, 14768, 13335, 30246, 39364, 51795, 5031, 38107, 32158, 443, 10384, 6774, 47929, 15499, 50368, 51827, 54022, 18908, 2157, 9827, 14658, 16901, 40891, 5884, 51302, 10387, 10960, 16761, 26793, 55085, 35673, 35137, 13497, 28211, 60579, 60497, 47403, 9106, 59526, 10327, 8063, 41945, 5754, 57621, 26709, 22739, 25547, 24703, 20746, 3895, 44111, 51320, 42212, 59781, 29064, 44610, 16431, 39515, 18156, 14210, 27507, 47206, 41530, 44123, 29499, 47242, 50363, 3339, 57490, 36566, 48636, 49784, 10942, 64447, 26791, 52829, 53204, 55163, 32261, 32157, 58261, 41129, 60614, 30034, 55489, 55576, 25052, 4263, 32514, 1419, 22605, 56589, 48192, 44655, 61295, 8855, 42987, 26448, 33214, 46651, 56194, 28472, 12965]


ut = Untwister()
for i in leak:
    ut.submit(bin(i)[2:] + '?'*16)

rng = ut.get_random()


m = rng.getrandbits(64)

flag = "flag{"+str(m)+"}"
print(m)
print(flag)

flag_md5 = md5(flag.encode()).hexdigest()
print(flag_md5)