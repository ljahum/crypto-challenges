#include <vector>
#include <string>
#include <random>
#include <sstream>
#include <iostream>
#include <algorithm>

// #include "homomorphic_system.cpp"
// #include "pallisade"
#define HIGH 9
#define LOW 0
using namespace std;

int VecToNum(vector<int64_t> vec)
{
    std::vector<int> values(begin(vec), end(vec));

    int res = std::accumulate(values.begin(), values.end(), 0, [](int acc, int val)
                              { return 10 * acc + val; });

    return res;
}
int Genrand(int lr, int hr)
{
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> distr(lr, hr);

    int rnum = distr(gen);
    return rnum;
}

vector<int> slice(const vector<int> &v, int start = 0, int end = -1)
{
    int olen = v.size();
    int nlen;

    if (end == -1 or end >= olen)
    {
        nlen = olen - start;
    }
    else
    {
        nlen = end - start;
    }

    vector<int> nv(nlen);

    for (int i = 0; i < nlen; i++)
    {
        nv[i] = v[start + i];
    }

    return nv;
}
int main()
{
    int MAT_SIZE = 5;
    vector<int64_t> p;
    vector<int64_t> msgvector;

    vector<vector<int64_t>> m1(5, vector<int64_t>(5));
    vector<int> row = {0, 1, 2, 3, 4};
    int tmp;
    for (int x = 0; x < 5; x++)
    {
        for (int y = 0; y < 5; y++)
        {
            // m1[x][y] = x*5+y ;
            // cout<<m1[x][y]<<endl;
            // if ((x == row[0]) || (x == row[1]))
            //     m1[x][y] = 0;
            // else 
            tmp = Genrand(LOW, HIGH);
            m1[x][y] = Genrand(LOW, HIGH); //0~9随机
        }
    }
    long int userInp;
    msgvector = m1[row[2]];

    // FheEncrypt(msgvector);
    // EncryptedOperations();

    // p = FheDecrypt();
    cout<<msgvector.size()<<endl;
    p = vector<int64_t>(msgvector.begin(), msgvector.begin()+5+1);
    
    cout<<p.size()<<endl;

    userInp = VecToNum(p);
    printf("%ld\n",userInp);
    for(int i=0;i<p.size();i++)
    {
        cout<<p[i]<<" ";
    }
    cout<<endl;
        
    

    
    return 0;
}
