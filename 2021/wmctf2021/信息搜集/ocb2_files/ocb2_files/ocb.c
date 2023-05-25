/*
 * ocb.c -- Implemented by Ted Krovetz (tdk@acm.org) -- Modified 2005.03.11
 *
 * This implementation is in the public domain. No warranty applies.
 *
 * This file needs an implementation of AES to work properly. It currently
 * uses "rijndael-alg-fst.c" by Barreto, Bosselaers and Rijmen, which should
 * be bundled with this implementation. (If not, search the Internet for
 * "rijndael-fst-3.0.zip", or substitute your preferred implementation.)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "rijndael-alg-fst.h"
#include "ocb.h"

#define BLOCKLEN 16                        /* AES block-length in bytes    */
typedef byte block[BLOCKLEN];              /* an AES block                 */
typedef unsigned ocb_aes_key[(MAXNR+1)*4]; /* an AES key                   */


/*************************************************************************** 
 * ocb_state structure definition - continued from ocb.h  
 ***************************************************************************/
struct _ocb_state {
    ocb_aes_key ekey;
    ocb_aes_key dkey;
    block headertag;
    unsigned taglen;
    unsigned noncelen;
    unsigned aes_rounds;
};

/*************************************************************************** 
 * xor_block  
 ***************************************************************************/
static void
xor_block(block dst, block src1, block src2)
{
    unsigned i;
    for (i = 0; i < sizeof(block); i++) {
        dst[i] = src1[i] ^ src2[i];
    }
}

/*************************************************************************** 
 * two_times, three_times
 *
 * These routines manipulate the offsets which are used for pre- and
 * post-whitening of blockcipher invocations. The offsets represent
 * polynomials, and these routines multiply the polynomials by other
 * constant polynomials. Note that as an optimization two consecutive
 * invocations of "three_times" can be efficiently replaced:
 *                     3(3(X)) == (2(2(X))) xor X
 *
 ***************************************************************************/
static void
two_times(block dst, block src)
/* 128-bit shift-left by 1 bit: src <<= 1. Xor 0x87 if carry out.          */
{
    unsigned i;
    unsigned char carry = src[0] >> 7;      /* set carry = high bit of src */
    for (i = 0; i < sizeof(block)-1; i++) {
        dst[i] = (src[i] << 1) | (src[i+1] >> 7);
    }
    dst[sizeof(block)-1] = (src[sizeof(block)-1] << 1) ^ (carry * 0x87);
}

static void
three_times(block dst, block src)
{
    block t;
    
    two_times(t,src);
    xor_block(dst, t, src);
}

/*************************************************************************** 
 * ocb_init - Allocate and initialize and OCB state structure
 ***************************************************************************/
ocb_state *
ocb_init(byte* Key, unsigned tlen, unsigned nlen, blockcipher E)
{
    unsigned keylen = 128;
    ocb_state *rval = (ocb_state *)malloc(sizeof(ocb_state));
    if (rval) {
        if (E == AES192) keylen = 192;
        if (E == AES256) keylen = 256;
        rijndaelKeySetupEnc((u32 *)(rval->ekey), Key, keylen);
        rijndaelKeySetupDec((u32 *)(rval->dkey), Key, keylen);
        memset(rval->headertag,0,sizeof(block));
        rval->taglen = tlen;
        rval->noncelen = nlen;
        rval->aes_rounds = (keylen/32)+6;
    }
    return rval;
}

/*************************************************************************** 
 * ocb_zeroize - zero and release memory  
 ***************************************************************************/
void
ocb_zeroize(ocb_state *K)
{
    memset(K,0,sizeof(ocb_state));
    free(K);
}

/*************************************************************************** 
 * pmac_function  
 ***************************************************************************/
static void
pmac_function(byte *M, unsigned mlen, block T, ocb_state *K)
{
    block Tmp,Checksum,Offset;
    block *mptr = (block *)M;
    
   /*
    * Initialize strings used for offsets and checksums
    */
    memset(Checksum,0,sizeof(block));
    rijndaelEncrypt((u32 *)(K->ekey), K->aes_rounds, Checksum, Offset);
    three_times(Offset,Offset);
    three_times(Offset,Offset);

   /*
    * Accumulate all but the last block
    */
    while (mlen > sizeof(block)) {
        two_times(Offset,Offset);
        xor_block(Tmp,Offset,*mptr);
        rijndaelEncrypt((u32 *)(K->ekey), K->aes_rounds, Tmp, Tmp);
        xor_block(Checksum,Tmp,Checksum);
        mlen = mlen - sizeof(block);
        mptr = mptr + 1;
    }

   /*
    * Accumulate the last block
    */
    two_times(Offset,Offset);
    if (mlen == sizeof(block)) {
        xor_block(Checksum,*mptr,Checksum);
        three_times(Offset,Offset);
    } else {
        memset(Tmp,0,sizeof(block));
        memcpy(Tmp,*mptr,mlen);
        Tmp[mlen] = 0x80;
        xor_block(Checksum,Tmp,Checksum);
        three_times(Offset,Offset);
        three_times(Offset,Offset);
    }

   /*
    * Compute result
    */
    xor_block(Tmp,Offset,Checksum);
    rijndaelEncrypt((u32 *)(K->ekey), K->aes_rounds, Tmp, T);
}

/*************************************************************************** 
 * ocb_provide_header  
 ***************************************************************************/
int
ocb_provide_header(ocb_state *K, byte *H, unsigned hlen)
{
    if (hlen == 0)
        memset(K->headertag,0,sizeof(block));
    else
        pmac_function(H, hlen, K->headertag, K);
	return 1;
}

/*************************************************************************** 
 * ocb_encrypt  
 ***************************************************************************/
int
ocb_encrypt(ocb_state *K, byte* N, byte* M, unsigned mlen, byte* C, byte* T)
{
    block Pad,Tmp,Checksum,Offset;
    block *mptr = (block *)M,
          *cptr = (block *)C;
    
   /*
    * Initialize strings used for offsets and checksums
    */
    memset(Checksum,0,sizeof(block));
    memset(Tmp,0,sizeof(block));
    memcpy(Tmp,N,K->noncelen);
    rijndaelEncrypt((u32 *)(K->ekey), K->aes_rounds, Tmp, Offset);

   /*
    * Encrypt and accumulate all but last block
    */
    while (mlen > sizeof(block)) {
        two_times(Offset,Offset);
        xor_block(Tmp,Offset,*mptr);
        rijndaelEncrypt((u32 *)(K->ekey), K->aes_rounds, Tmp, Tmp);
        xor_block(*cptr,Offset,Tmp);
        xor_block(Checksum,*mptr,Checksum);
        mlen = mlen - sizeof(block);
        cptr = cptr + 1;
        mptr = mptr + 1;
    }

   /*
    * Encrypt and accumulate last block
    */
    two_times(Offset,Offset);
    memset(Tmp,0,sizeof(block));
    Tmp[sizeof(block)-1] = mlen * 8;
    xor_block(Tmp,Offset,Tmp);
    rijndaelEncrypt((u32 *)(K->ekey), K->aes_rounds, Tmp, Pad);
    memcpy(Tmp,*mptr,mlen);
    memcpy((char *)Tmp+mlen,(char *)Pad+mlen,sizeof(block)-mlen);
    xor_block(Checksum,Tmp,Checksum);
    xor_block(Tmp,Pad,Tmp);
    memcpy(*cptr,Tmp,mlen);

   /*
    * Compute authentication tag
    */
    three_times(Offset,Offset);
    xor_block(Tmp,Offset,Checksum);
    rijndaelEncrypt((u32 *)(K->ekey), K->aes_rounds, Tmp, Tmp);
    xor_block(Tmp, K->headertag, Tmp);
    memcpy(T,Tmp,K->taglen);
    return 1;
}

/*************************************************************************** 
 * ocb_decrypt  
 ***************************************************************************/
int
ocb_decrypt(ocb_state *K, byte* N, byte* C, unsigned clen,  byte* T, byte* P)
{
    block Pad,Tmp,Checksum,Offset;
    block *mptr = (block *)P,
          *cptr = (block *)C;
    
   /*
    * Initialize strings used for offsets and checksums
    */
    memset(Checksum,0,sizeof(block));
    memset(Tmp,0,sizeof(block));
    memcpy(Tmp,N,K->noncelen);
    rijndaelEncrypt((u32 *)(K->ekey), K->aes_rounds, Tmp, Offset);

   /*
    * Decrypt and accumulate all but last block
    */
    while (clen > sizeof(block)) {
        two_times(Offset,Offset);
        xor_block(Tmp,Offset,*cptr);
        rijndaelDecrypt((u32 *)(K->dkey), K->aes_rounds, Tmp, Tmp);
        xor_block(*mptr,Offset,Tmp);
        xor_block(Checksum,*mptr,Checksum);
        clen = clen - sizeof(block);
        cptr = cptr + 1;
        mptr = mptr + 1;
    }

   /*
    * Decrypt and accumulate last block
    */
    two_times(Offset,Offset);
    memset(Tmp,0,sizeof(block));
    Tmp[sizeof(block)-1] = clen * 8;
    xor_block(Tmp,Offset,Tmp);
    rijndaelEncrypt((u32 *)(K->ekey), K->aes_rounds, Tmp, Pad);
    memset(Tmp,0,sizeof(block));
    memcpy(Tmp,*cptr,clen);
    xor_block(Tmp,Pad,Tmp);
    xor_block(Checksum,Tmp,Checksum);
    memcpy(*mptr,Tmp,clen);

   /*
    * Compute result
    */
    three_times(Offset,Offset);
    xor_block(Tmp,Offset,Checksum);
    rijndaelEncrypt((u32 *)(K->ekey), K->aes_rounds, Tmp, Tmp);
    xor_block(Tmp,K->headertag,Tmp);
    return (memcmp(T,Tmp,K->taglen)?0:1);
}

/*************************************************************************** 
 * main - simple test
 ***************************************************************************/
static void pbuf(void *buf, int n, char *s)
{
    int i;
    unsigned char *cp = (unsigned char *)buf;
    
    if (n < 0 || n > 64)
        n = 64;
    
    if (s)
        printf("%s: ", s);
        
    for (i = 0; i < n; i++)
        printf("%02X", (unsigned char)cp[i]);
    printf("\n");
}

#define maxsize 128

static void
produce_vector(byte *M, int mlen, byte *N, byte *H, int hlen, byte *K)
{
	ocb_state *state;
	byte C[maxsize];
    block T;

	state = ocb_init(K,16,16,AES128);
	ocb_provide_header(state,H,hlen);
	ocb_encrypt(state,N,M,mlen,C,T);
	ocb_zeroize(state);
	
	pbuf(H, hlen, "  H "); 
	pbuf(M, mlen, "  M "); 
	pbuf(C, mlen, "  C "); 
	pbuf(T, 16,   "  T ");
	printf("\n");
}

int
main(void)
{
    byte S[128];
    byte M[maxsize] = {0};
    byte P[maxsize] = {0};
    byte C[maxsize] = {0};
    byte H[maxsize] = {0};
    block N = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15};
    block K = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15};
    block T;
    int res;
    ocb_state *state;
    
    for (res = 0; res < 128; res++) S[res] = (byte)res;
    
    produce_vector(S, 0, N, S, 0, K);
    produce_vector(S, 8, N, S, 0, K);
    produce_vector(S, 16, N, S, 0, K);
    produce_vector(S, 24, N, S, 0, K);
    produce_vector(S, 32, N, S, 0, K);
    produce_vector(S, 40, N, S, 0, K);
    
    produce_vector(S, 8, N, S, 8, K);
    produce_vector(S, 16, N, S, 16, K);
    produce_vector(S, 24, N, S, 24, K);
    produce_vector(S, 32, N, S, 32, K);
    produce_vector(S, 40, N, S, 40, K);
    
    state = ocb_init((byte *)"abcdefghijklmnop",sizeof(T),sizeof(N),AES128);
    ocb_provide_header(state,H,sizeof(H));
    ocb_encrypt(state,N,M,sizeof(M),C,T);
    pbuf(T, 16, "Tag       ");
    pbuf(C, 16, "Ciphertext");    
    res = ocb_decrypt(state,N,C,sizeof(M),T,P);
    ocb_zeroize(state);
    printf("Tags match: %i.\n", res);
    printf("Message in equals out: %i.\n", (memcmp(M,P,sizeof(M))==0?1:0));
    return 0;
}

