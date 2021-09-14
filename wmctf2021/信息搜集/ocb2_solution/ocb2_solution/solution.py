#!/usr/bin/env python3
from icecream import *
import os, json, socket, sys
from string import ascii_lowercase
from random import randint

nonces = set() # to contain i/o pairs of the blockcipher to be used as nonces/offsets
len_0n = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80' 

#This challenge requires you to implement two attacks against the OCB2 encryption scheme in order to recover the flag
# The first challenge requires forging a valid ciphertext that, when decrypted, gives a JSON object with the fields "user_id" and "permissions". 
# In order to obtain the flag, the value of "user_id" must be an element of the users set maintained by the challenger. The value of "permissions" must be "admin"
# Once the forgery is successful, the challenger will provide the attacker with the ciphertext of the flag, encrypted under a fresh nonce. The attacker then has to perform a plaintext recovery attack on the encrypted flag for the given nonce.


def controller(s, option, argumentslist):
    ''' A helper method to send and retrieve data from the challenge server'''

    # Send choice (1-4)
    s.send(str(option).encode('utf-8') + b'\n')
    if option == 1:
        # No arguments to send. Retrieve the encrypted credentials
        return eval(s.recv(4096).decode().split('\n')[0])

    # Receive and discard the prompt message
    s.recv(1024)

    # Send arguments separated by spaces
    m = b''
    for arg in argumentslist:
        m += arg.encode('utf-8') + b' '
    m += b'\n'
    s.send(m)

    # Get response data and return it as a python object
    response = s.recv(4096)
    print(response.decode())
    tmp = eval(response.decode().split('\n')[0])
    ic(tmp)
    return tmp



def block_xor(block1, block2):
    ''' Perform a bitwise XOR of two 16-byte blocks'''

    r = b''
    for a,b in zip(block1, block2):
        r += (a^b).to_bytes(1, 'big')
    return r


def two_times(block):
    ''' Perform x*block when interpreting block as an element of GF(2)[x]/(x^128+x^7+x^2+x+1) '''

    length = len(block)
    b = int(block.hex(), 16)
    carry = b >> 127
    b = (b << 1 & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF) ^ (carry * 0x87)
    return b.to_bytes(length, 'big')


def divide_by_two(block):
    ''' Inverse of two_times. 
    Perform (x^-1)*block when interpreting block as an element of GF(2^128)'''

    length = len(block)
    block = int(block.hex(), 16)
    under = block % 2 # check for x**0, as x**(-1) = x**127 + x**6 + x + 1
    block = (block ^ (under * 0x100000000000000000000000000000087))
    block >>= 1
    return block.to_bytes(length, 'big')


def three_times(block):
    ''' 3*block := (x+1) * block = two_times(block) XOR block'''

    return block_xor(block, two_times(block))


def sample_pairs(number):
    ''' Generates number-2 pairs of nonce, encrypted nonce, using a message of number bytes. These are then stored in the nonces set as byte strings.'''
    
    # Generate message for encryption oracle
    m = b''
    for i in range(16*(number-2)):
        m += b'\x00'
    m += len_0n
    for i in range(16):
        m += b'\x00'
    n = os.urandom(16)

    # Encrypt(n, m) = (n, c, t). Retrieve c
    c = controller(s, 3, [n.hex(), m.hex()])[1]
    
    # Forge a ciphertext to recover the encryption of the nonce
    c = bytes.fromhex(c)
    length = len(c)//16
    c_p = c[:(length-2)*16]
    c_mminus1 = block_xor(c[(length-2)*16:(length-1)*16],len_0n)
    c_p += c_mminus1
    t_p = c[(length-1)*16:]
   
    # Decrypt (n, c_p, t_p) = (n, m_p). Retrieve m_p
    m_p = controller(s, 4, [n.hex(), c_p.hex(), t_p.hex()])[1]
    
    # Find E_k(N)=L from decrypted forgery and use it to generate numblocks(m_prime)-1 pairs (X_i, Y_i) where Y_i = E_k(X_i)
    m_p = bytes.fromhex(m_p)
    if len(m_p) % 16 == 0:
        numblocks = len(m_p)//16
    else:
        # Shouldn't happen. Message should be divisible by the block length
        raise Exception('Wrong message length')
    m_last = m_p[-16:]
    # Recover L = x^(-numblocks)*(m_last XOR len(0^n))
    l = block_xor(m_last, len_0n)
    for i in range(numblocks):
        l = divide_by_two(l)

    # Recover numblocks-1 input-output pairs for E_k(.)
    for i in range(numblocks - 1):
        l = two_times(l)
        c_block = c_p[i*16:(i+1)*16]
        cipher_out = block_xor(c_block, l) # Output of the blockcipher for this block
        nonces.add((l, cipher_out))

def get_user_id():
    ''' Retrieve the user_id from a new user registration'''

    # Register a new user
    n, c, t = controller(s, 1, [])
    # Decrypt the response
    response = controller(s, 4, [n, c, t])[1]
    # Extract the user_id
    return json.loads(bytes.fromhex(response).decode())['user_id']


def gen_forged_auth(nonces):
    ''' Create a forged ciphertext with an existing user_id but with admin permissions.
    Submit this ciphertext to get an encrypted flag'''

    # Nonce used for the encryption query
    temp_nonce, temp_nonce_L = nonces.pop()
    # Nonce used for the decryption query (embedded in the query to the enc oracle)
    target_nonce, target_nonce_L = nonces.pop()

    user_id = get_user_id()
    
    # We'll generate forgery that decripts to something like the following:
    credentials = {'user_id': user_id, 'permissions': 'admin'}
    
    # Add bogus field to dict to make message length exactly 4 blocks. This simplifies things.
    credlength = len(str(credentials))
    ic(credlength)
    ic(credentials['user_id'])
    if credlength > 56:
        print("User_id is too long to conveniently forge a nice message. Get new user_id and try again")
        exit()
    lengthener = ''
    for i in range(64 - credlength - 7):
       lengthener += ascii_lowercase[randint(0,len(ascii_lowercase)-1)]
    credentials[lengthener] = 0
    cred = json.dumps(credentials).encode('utf-8')
    assert(len(cred) == 64)


    # Generate forged credentials message m as follows:
    # for block i 1<=i<=3: m[i] = cred[i] XOR x^i*target_nonce_L XOR x^i*temp_nonce_L
    # m[4] = len(0^n) XOR x^4*target_nonce_L XOR x^4*temp_nonce_L
    # m[5] = SIGMA (= XOR of cred[i]'s) XOR x^4*(x+1)*target_nonce_L XOR x^5*temp_nonce_L
    # m[6] = random block
    # 
    # Submit this to encryption oracle to obtain: 
    # c[1] = x*temp_nonce_L XOR E_k(cred[1] XOR x*target_nonce_L)
    # c[2] = x^2 * temp_nonce_L XOR E_k(cred[2] XOR x^2 * target_nonce_L)
    # c[3] = x^3 * temp_nonce_L XOR E_k(cred[3] XOR x^3 * target_nonce_L)
    # c[4] = x^4 * temp_nonce_L XOR E_k(len(0^n) XOR x^4 * target_nonce_L)
    # c[5] = x^5 * temp_nonce_L XOR E_k(SIGMA XOR x^4*(x+1) * target_nonce_L)
    # c[6] = who cares
    #
    # Create forged ciphertext as follows:
    # c'[i] = c[i] XOR x^i * target_nonce_L XOR x^i * temp_nonce_L = 
    #   x^i * target_nonce_L XOR E_k(cred[i] XOR x^i * target_nonce_L) for i, 1<=i<=3
    # c'[4] = c[4] XOR x^4 * temp_nonce_L XOR cred[4] = 
    #   cred[4] XOR E_k(len(0^n) XOR x^4 * target_nonce_L)
    # tag' = c[5] XOR x^5 * temp_nonce_L = E_k(SIGMA XOR x^4*(x+1)*target_nonce_L)
    # submit target_nonce, c', tag' to get flag
    
    
    m = b''
    temp_offset = temp_nonce_L
    targ_offset = target_nonce_L

    # Create m[1-3]
    for i in range(3):
        temp_offset = two_times(temp_offset)
        targ_offset = two_times(targ_offset)
        m += block_xor(block_xor(cred[i*16:(i+1)*16], temp_offset), targ_offset)
    
    # Create m[4]
    targ_offset = two_times(targ_offset)
    temp_offset = two_times(temp_offset)
    m += block_xor(block_xor(len_0n, targ_offset), temp_offset)

    # create m[5] this will eventually become the authentication tag
    targ_offset = three_times(targ_offset)
    temp_offset = two_times(temp_offset)
    m5 = bytes(16)
    for i in range(4):
        m5 = block_xor(m5, cred[i*16:(i+1)*16])

    m += block_xor(block_xor(m5, temp_offset), targ_offset)

    # create m[6]
    m += os.urandom(16)

    # Submit crafted message to obtain its ciphertext
    n, c, t = controller(s, 3, [temp_nonce.hex(), m.hex()])
    c = bytes.fromhex(c)
    t = bytes.fromhex(t)

    c_p = b''
    targ_offset = target_nonce_L
    temp_offset = temp_nonce_L
    
    # Create c'[1-3]
    for i in range(3):
        targ_offset = two_times(targ_offset)
        temp_offset = two_times(temp_offset)
        c_p += block_xor(block_xor(c[i*16:(i+1)*16], targ_offset), temp_offset)

    # Create c'[4]
    temp_offset = two_times(temp_offset)
    c_p += block_xor(block_xor(temp_offset, c[3*16:4*16]), cred[3*16:4*16])

    # Create tag'
    temp_offset = two_times(temp_offset)
    tag_p = block_xor(c[4*16:5*16], temp_offset)
    
    # Check: Print decrypted target_nonce, c_p, and tag_p and display the forged message
    print("Forged credentials:")
    print(bytes.fromhex(controller(s, 4, [target_nonce.hex(), c_p.hex(), tag_p.hex()])[1]))
    print(" ")

    # Decrypt target_nonce, c_p, tag_p and submit for encrypted flag
    # Obtain N* (new random nonce), Ek(Flag), Tag

    nonce, flag, flag_tag = controller(s, 2, [target_nonce.hex(), c_p.hex(), tag_p.hex()])
    return nonce, flag, flag_tag

def recover_flag_L(nonce, ciphertext, tag):
    ''' Given N*, C*, T*, first recover L*:
        Pick N',L' from nonces. 
        Create M' = M[1]||M[2] with M[1] = N* XOR x*L'
        Encrypt to get N', C', T'
        Recover L* = C'[1] XOR x*L'
    '''

    temp_nonce, temp_nonce_L = nonces.pop()
    m = block_xor(bytes.fromhex(nonce), two_times(temp_nonce_L)) + os.urandom(16)
    # Encrypt temp_nonce.hex(), m.hex()
    # Receive C'
    c = bytes.fromhex(controller(s, 3, [temp_nonce.hex(), m.hex()])[1])

    # Return L*
    return block_xor(c[:16], two_times(temp_nonce_L))

def recover_flag(nonce, nonce_L, ciphertext, tag):
    ''' This takes the target nonce N*, its encryption under K L*,
        the flag ciphertext, and the flag tag, and returns the plaintext of the flag'''

    c = bytes.fromhex(ciphertext)

    # Given N, L, C = C[1]||C[2]||...||C[m], T, create
    # C$ = C[2] XOR x^2*L XOR x*L||C[1] XOR x^2*L XOR X*L || C[3] || ... ||C[m]
    # Submit (N,C$,T) to decryption oracle to receive (M$)
    # Flag = M$[2] XOR x^2*L XOR x*L || M$[1] XOR x^2*L XOR x*L || M$[3] ||...||M$[m]
    
    
    # Build C$ as described above
    c_p = b''
    for i in range(1, -1, -1):
        c_p += block_xor(block_xor(c[i*16:(i+1)*16], two_times(nonce_L)), two_times(two_times(nonce_L)))
    c_p += c[32:]


    # Decrypt nonce.hex(), c_p.hex(), tag
    # Receive m_p = M$
    m_p = bytes.fromhex(controller(s, 4, [nonce.hex(), c_p.hex(), tag])[1])
 
    flag = b''
    for i in range(1,-1,-1):
        flag += block_xor(block_xor(m_p[i*16:(i+1)*16], two_times(nonce_L)), two_times(two_times(nonce_L)))
    flag += m_p[32:]
    return flag


if __name__ == '__main__':
    try:
        host = '0.0.0.0'
        port = 20000
    except:
        exit()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(port)))
    s.recv(1024)

    # Generate some nonce, encrypted_nonce pairs. This is more than enough
    sample_pairs(10)
    print("Recovered N,L Pairs:")
    for a,b in nonces:
        print(a.hex(), b.hex())
    print(" ")

    # Forge authorization to obtain the encrypted flag
    nonce, encflag, flag_tag = gen_forged_auth(nonces)
    print("Encrypted flag")
    print('Nonce: %s\nFlag ciphertext: %s\nFlag tag: %s\n' % (nonce, encflag, flag_tag))
    
    # Recover the encryption of the flag nonce
    nonce_L = recover_flag_L(nonce, encflag, flag_tag)
    print('Nonce_L: %s\n' % (nonce_L.hex()))
    input()
    # Recover the flag plaintext
    flag = recover_flag(bytes.fromhex(nonce), nonce_L, encflag, flag_tag)
    print('Flag: %s' % flag.decode())

