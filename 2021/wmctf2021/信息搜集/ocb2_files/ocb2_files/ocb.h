/*
 * ocb.h -- Implemented by Ted Krovetz (tdk@acm.org) -- Modified 2005.03.04
 */
#ifndef HEADER_OCB_H
#define HEADER_OCB_H

#ifdef  __cplusplus
extern "C" {
#endif

typedef enum {AES128,AES192,AES256} blockcipher;  /* "standard" ciphers */
typedef unsigned char byte;
typedef struct _ocb_state ocb_state;            /* OCB context - opaque */

/*
 * ocb_init
 *
 * Allocate and setup an OCB context data structure for a session.
 * Returns NULL if an error occurs.
 */
ocb_state *
ocb_init(
    byte* Key,         /* The key, as a string, for this session.       */
    unsigned tlen,     /* The tag length, in bytes, in this session.    */
    unsigned nlen,     /* The nonce length, in bytes, in this session.  */
    blockcipher bc     /* Enumerated that indicates what cipher to use. */
);

/*
 * ocb_provide_header
 *
 * Supply a message header. The message header remains active for all
 * subsequent ocb_encrypt() and ocb_decrypt() calls unless the header
 * is cancelled by supplying a zero-length header, or replaced.
 * Returns 0 if an error occurs.
 */
int
ocb_provide_header(
    ocb_state *K,     /* The OCB context.                               */
    byte *H,          /* The header (associated data)                   */    
    unsigned hlen     /* having hlen bytes                              */
);

/*
 * ocb_zeroize
 *
 * Session is over; zero and deallocate OCB structure.
 */
void
ocb_zeroize(
    ocb_state *K /* The OCB context to remove                           */
);

/*
 * ocb_encrypt
 *
 * Encrypt the given message with the given key, nonce and header.
 * Specify the header (if nonempty) with ocb_provide_header().
 * Returns 0 if an error occurs.
 */
int
ocb_encrypt(
    ocb_state *K,      /* The caller provides the OCB context,          */
    byte* N,           /* the nonce (length K->nlen) and                */
    byte* M,           /* the plaintext and                             */
    unsigned mlen,     /* its length (in bytes).                        */
    byte* C,           /* The mlen-byte ciphertext                      */
    byte* T            /* and tag T (length K->tlen) are returned.      */
);

/*
 * ocb_decrypt()
 *
 * Decrypt the given ciphertext with the given key, nonce and header.
 * Specify the header (if nonempty) with ocb_provide_header().
 * Returns 1 for a valid ciphertext/nonce/header/key combination,
 * Returns 0 if an error occurs.
 */
int
ocb_decrypt(
    ocb_state *K,   /* The caller provides the OCB context,             */
    byte* N,        /* the nonce (length K->nlen)                       */
    byte* C,        /* the ciphertext                                   */
    unsigned clen,  /* its length (in bytes), and                       */
    byte* T,        /* tag (length K->tlen).                            */
    byte* P         /* return the clen-byte plaintext.                  */
);

#ifdef  __cplusplus
}
#endif

#endif /* !HEADER_OCB_H */
