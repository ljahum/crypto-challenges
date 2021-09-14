
ocb.so: ocb.h ocb.c rijndael-alg-fst.h rijndael-alg-fst.c
	gcc -shared -fPIC *.c -o ocb.so

clean:
	rm -f ocb.so ocb.h ocb.c rijndael-alg-fst.h rijndael-alg-fst.c

ocb.h:
	wget http://web.cs.ucdavis.edu/~rogaway/ocb/ocb.h
ocb.c:
	wget http://web.cs.ucdavis.edu/~rogaway/ocb/ocb.c

rijndael-alg-fst.h:
	wget https://fastcrypto.org/front/misc/rijndael-alg-fst.h
rijndael-alg-fst.c:
	wget https://fastcrypto.org/front/misc/rijndael-alg-fst.c

