#include<stdio.h>
#include<stdlib.h>
// #include<Windows.h>
#include<math.h>
int main(){

    srand(0xDEADC0DE);
    for (int  j = 0; j < 32; ++j )
    {
        unsigned char a1 = A;
        unsigned char a2 = BYTE1(A);
        unsigned char a3 = BYTE2(A);
        unsigned char a4 = HIBYTE(A);
        
        unsigned char b1 = B;
        unsigned char b2 = BYTE1(B);
        unsigned char b3 = BYTE2(B);
        unsigned char b4 = HIBYTE(B);

        unsigned char c1 = C;
        unsigned char c2 = BYTE1(C);
        unsigned char c3 = BYTE2(C);
        unsigned char c4 = HIBYTE(C);
        for ( int i = 0; i < 4; ++i )
        {
            a1[i] = (23 * a1[i] + 66);
            b1[i] = (23 * b1[i] + 66);
            c1[i] = (23 * c1[i] + 66);
        }
        // 平接
        A = (a4 << 24) | (a3 << 16) | (a2 << 8) | a1;
        B = (b4 << 24) | (b3 << 16) | (b2 << 8) | b1;
        C = (c4 << 24) | (c3 << 16) | (c2 << 8) | c1;
        x1 = B >> 7;
        x2 = rand() + x1;
        x3 = (B >> 0xF) ^ (B << 10) | 3;
        A += x2 + (rand() ^ x3);

        x1 = C >> 7;
        x2 = rand() + x1;
        x3 = (C >> 15) ^ (C << 10) | 3;
        B += x2 + (rand() ^ x3);
        
        x1 = A >> 7;
        x2 = rand() + x1;
        x3 = (A >> 15) ^ (A << 10) | 3;
        C += x2 + (rand() ^ x3);
    }
    return 0;
//   *a1 = A;
//   a1[1] = B;
//   a1[2] = C;
//   return sub_7FF601D7132A(v4, &unk_7FF601D7ACC8);
}