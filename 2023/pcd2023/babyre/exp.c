#include<stdio.h>
#include<stdlib.h>
// #include<Windows.h>
#include<math.h>



unsigned char encode_text[49] =
{
  0x48, 0x4D, 0x3B, 0xA0, 0x27, 0x31, 0x28, 0x54, 0x6D, 0xF1,
  0x21, 0x35, 0x18, 0x73, 0x6A, 0x4C, 0x71, 0x3B, 0xBD, 0x98,
  0xB6, 0x5A, 0x77, 0x2D, 0x0B, 0x2B, 0xCB, 0x9B, 0xE4, 0x8A,
  0x4C, 0xA9, 0x5C, 0x4F, 0x1B, 0xF1, 0x98, 0x3D, 0x30, 0x59,
  0x3F, 0x14, 0xFC, 0x7A, 0xF4, 0x64, 0x02, 0x2B, 0x00
};


// 先将种子填充好
// void Init_rand()
// {
// 	srand(0xDEADC0DE);
// 	for (int i = 0; i < 6 * 32; i++)
// 		random_arr[i] = rand();
// 	return;
// }

int inv(unsigned char a1)
{
    int tmp = a1-66;
    int ans = tmp*167 & 0xff;
    return ans;
}

void exp1(char * enc, int * key)
{
	int A[4] = { 0 };
	int B[4] = { 0 };
	int C[4] = { 0 };
	unsigned int c1, c2, c3;
	unsigned int x1, x2, x3;

	c1 = ((int*)enc)[0];
	c2 = ((int*)enc)[1];
	c3 = ((int*)enc)[2];
	for (int j = 31; j >= 0 ; j--)	
	{
		x1 = c1 >> 7;
		x2 = key[j * 6 + 4] + x1;
		x3 = (c1 >> 15) ^ (c1 << 10) | 3;
		c3 -= x2 + (key[j * 6 + 5] ^ x3);

		x1 = c3 >> 7;
		x2 = key[j * 6 + 2] + x1;
		x3 = (c3 >> 15) ^ (c3 << 10) | 3;
		c2 -= x2 + (key[j * 6 + 3] ^ x3);

		x1 = c2 >> 7;
		x2 = key[j * 6 + 0] + x1;                      
		x3 = (c2 >> 15) ^ (c2 << 10) | 3;
		c1 -= x2 + (key[j * 6 + 1] ^ x3);
			
		// 拆分
		A[0] = c1 & 0xff;
		A[1] = (c1 >> 8) & 0xff;
		A[2] = (c1 >> 16) & 0xff;
		A[3] = (c1 >> 24) & 0xff;
		B[0] = c2 & 0xff;
		B[1] = (c2 >> 8) & 0xff;
		B[2] = (c2 >> 16) & 0xff;
		B[3] = (c2 >> 24) & 0xff;
		C[0] = c3 & 0xff;
		C[1] = (c3 >> 8) & 0xff;
		C[2] = (c3 >> 16) & 0xff;
		C[3] = (c3 >> 24) & 0xff;
			
		for (int k = 0; k < 4; k++)
		{
			A[k] = inv((unsigned int)A[k]);
			B[k] = inv((unsigned int)B[k]);
			C[k] = inv((unsigned int)C[k]);
		}

		c1 = ((A[3]&0xff) << 24) | ((A[2]&0xff) << 16) | ((A[1]&0xff) << 8) | (A[0]&0xff);
		c2 = ((B[3]&0xff) << 24) | ((B[2]&0xff) << 16) | ((B[1]&0xff) << 8) | (B[0]&0xff);
		c3 = ((C[3]&0xff) << 24) | ((C[2]&0xff) << 16) | ((C[1]&0xff) << 8) | (C[0]&0xff);
	}
	for (int i = 0; i < 4; i++)
		printf("%c", ((char*)&c1)[i]);
	for (int i = 0; i < 4; i++)
		printf("%c", ((char*)&c2)[i]);
	for (int i = 0; i < 4; i++)
		printf("%c", ((char*)&c3)[i]);
}

int main(void)
{
	// Init_rand();
    int random_arr[6 * 32]={ 0 };
    srand(0xDEADC0DE);
	for (int i = 0; i < 6 * 32; i++)
		random_arr[i] = rand();

	exp1((char*)&encode_text[0], random_arr);
	exp1((char*)&encode_text[12], random_arr);
	exp1((char*)&encode_text[24], random_arr);
	exp1((char*)&encode_text[36], random_arr);

	return 0;
}