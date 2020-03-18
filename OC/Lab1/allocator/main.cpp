#include <stdio.h>
#include "mem_alloc.h"

#define ARRAY_SIZE 10

/**
* Виводить повідомлення, стан блоків пам'яті та виконує затримку.
*/
void infoAndWait(char message[]) {
    printf("%s\n", message);
    mem_dump();
    getchar();
}

/**
* Тестування функцій poolInitialize, poolFree, mem_alloc, mem_realloc, mem_free.
*/
void simpleMemoryTest() {
    printf("------------ Simple Memory Test ------------\n");

    char *blocksArray[ARRAY_SIZE];

    poolInitialize();
    infoAndWait("Initial pool:");

    for ( int i = 0; i < ARRAY_SIZE; i++ ) {
        blocksArray[i] = (char*)mem_alloc(50);
    }
    infoAndWait("After memory allocation:");

    mem_free(blocksArray[8]);
    infoAndWait("After blocksArray[8] memory free:");

    blocksArray[4] = (char*)mem_realloc(blocksArray[4], 20);
    infoAndWait("After blocksArray[4] memory reallocation to size 20:");

    mem_free(blocksArray[5]);
    infoAndWait("After blocksArray[5] memory free:");

    blocksArray[6] = (char*)mem_realloc(blocksArray[6], 200);
    infoAndWait("After blocksArray[6] memory reallocation to size 200:");

    blocksArray[4] = (char*)mem_realloc(blocksArray[4], 100);
    infoAndWait("After blocksArray[4] memory reallocation to 100:");

    blocksArray[5] = (char*)mem_alloc(70);
    infoAndWait("After blocksArray[5] memory allocation to 70:");

    for ( int i = 0; i <= 7; i++ ) {
        mem_free(blocksArray[i]);
    }
    mem_free(blocksArray[9]);
    infoAndWait("After all memory free:");

    poolFree();
    printf("Free pool\n");
    getchar();
}

int main() {
    simpleMemoryTest();

    return 0;
}
