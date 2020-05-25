#include <cstdio>
#include <zconf.h>

void FirstFuction()
{
    for(int i = 0; i < 100; i++)
    {
        //process
        sleep(1);
    }
}

int main()
{
    printf("\n Inside main()\n");

    for(int i = 0;i<0xffffff;i++);

    FirstFuction();

    return 0;
}