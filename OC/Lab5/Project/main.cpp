#include <cstdio>
#include <ctime>

int main() {
    clock_t begin = clock();

    int AM[2][2];
    int res = 0;

    for (int j = 500000000; j > 0; j--)
    {
        res += 2;
    }

    AM[0][0] += res;
    AM[1][1] =  AM[0][0];

    printf("%d\n", AM[0][0]);
    printf("Execution time: %f\n", (double)(clock() - begin) / CLOCKS_PER_SEC);
    return 0;
}

