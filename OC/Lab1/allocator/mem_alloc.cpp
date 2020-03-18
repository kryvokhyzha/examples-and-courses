//
// Created by Roman.Kryvokhyzha on 10.03.2020.
//

#include "mem_alloc.h"
#include <malloc.h>
#include <stdio.h>

#define FREE_STATE 0
#define BUSY_STATE 1

#define DEFAULT_FILLER 0

/*
* Структура, що визначає заголовок блоку.
* busyState - стан зайнятості.
* size - розмір блоку.
* prevSize - розмір попереднього блоку.
*/
typedef struct {
    char busyState;
    size_t size;
    size_t prevSize;
} Header;

/**
* Визначення типу вказівника на функцію пошуку блоку для виділення пам'яті.
*/
typedef Header* (*SearchAlgorithmFun)(size_t size);

/**
* Вказівник на початок пулу.
*/
el_t *firstBlock;

/**
* Кількість блоків в пулі.
*/
int blocksQuantity = 3;
/**
* Алгоритм пошуку блоку для виділення пам'яті.
*/
SearchAlgorithm sAlgorithm = FIRST_FOUND_ALGORITHM;
/**
* Специфікація функцій пошуку блоку для виділення пам'яті.
*/
Header *firstFoundSAlgorithm(size_t size);

/**
* Масив вказівників на функції пошуку блоку для виділення пам'яті.
*/
SearchAlgorithmFun sAlgFunArray[] = {
        firstFoundSAlgorithm
};

/**
* Розмір заголовку.
*/
size_t headerSize = sizeof(Header) / sizeof(el_t);

/**
* Заповнення полів заголовку визначеними значеннями.
* headerPtr - вказівник на заголовок.
* size - розмір блоку.
* prevSize - розмір попереднього блоку.
* busyState - стан зайнятості.
* returns Вказівник на заголовок.
*/
Header *fillHeader(Header *headerPtr, size_t size, size_t prevSize, char busyState) {
    headerPtr->busyState = busyState;
    headerPtr->size = size;
    headerPtr->prevSize = prevSize;

    return headerPtr;
}

/**
* Перехід на заголовок наступного блоку.
* lastHeaderPtr - вказівник на заголовок блоку.
* returns Вказівник на заголовок наступного блоку.
*/
Header *getNextHeader(Header *lastHeaderPtr) {
    return (Header*)((el_t*)lastHeaderPtr + headerSize + lastHeaderPtr->size);
}

/**
* Перехід на заголовок попереднього блоку.
* lastHeaderPtr - вказівник на заголовок блоку.
* returns Вказівник на заголовок попереднього блоку.
*/
Header *getPrevHeader(Header *lastHeaderPtr) {
    return (Header*)((el_t*)lastHeaderPtr - lastHeaderPtr->prevSize - headerSize);
}

/**
* Визначає, чи даний блок підходить для виділення пам'яті.
* size - об'єм пам'яті, що буде виділятися.
* returns 1 - якщо блок можна виділити, 0 - якщо не можна.
*/
int isAppropriateBlock(Header *headerPtr, size_t size) {
    return headerPtr->busyState == FREE_STATE && headerPtr->size >= size;
}

/**
* Ініціалізація пулу пам'яті.
*/
void poolInitialize() {
    firstBlock = (el_t*)malloc(POOL_SIZE * sizeof(el_t));

    for ( el_t *ptr = firstBlock, *lastPtr = ptr + POOL_SIZE - 1;
          ptr <= lastPtr; ptr++ ) {
        *ptr = DEFAULT_FILLER;
    }

    size_t freeSpace = POOL_SIZE - 3 * headerSize;

    el_t *ptr = firstBlock;
    // Визначення початкового нульового зайнятого блоку-бар'єру.
    fillHeader((Header*) ptr, 0, 0, BUSY_STATE);

    ptr += headerSize;
    // Визначення блоку вільного простору пам'яті
    fillHeader((Header*) ptr, freeSpace, 0, FREE_STATE);

    ptr += headerSize + freeSpace;
    // Визначення кінчевого нульового зайнятого блоку-бар'єру.
    fillHeader((Header*) ptr, 0, freeSpace, BUSY_STATE);
}

/**
* Звільнення пулу пам'яті.
*/
void poolFree() {
    free(firstBlock);
}

/**
* Пошук першого підходящого блоку для виділення пам'яті.
* size - розмір пам'яти, що має виділятися.
* returns Вказівник на знайдений блок або NULL, якщо блоку не знайдено.
*/
Header *firstFoundSAlgorithm(size_t size) {
    Header *headerPtr = (Header*)firstBlock + 1;

    for ( int i = 1, last = blocksQuantity - 2; i <= last; i++ ) {
        if ( isAppropriateBlock(headerPtr, size) ) {
            return headerPtr;
        }
        headerPtr = getNextHeader(headerPtr);
    }

    return NULL;
}

/**
* Виділення пам'яті в знайденому потрібному блоці.
* headerPtr - вказівник на заголовок блоку.
* size - розмір пам'яті, що буде виділятися.
* returns Вказівник на початок блоку.
*/
void *freeBlockAlloc(Header *headerPtr, size_t size) {
    size_t restSpace = headerPtr->size - size;

    // За необхідності розбиваємо блок на 2 частини
    if ( restSpace > headerSize ) {
        Header *newHeaderPtr = (Header*)((el_t*)headerPtr + headerSize + size);
        fillHeader(newHeaderPtr, restSpace - headerSize, size, FREE_STATE);

        getNextHeader(newHeaderPtr)->prevSize = newHeaderPtr->size;

        headerPtr->size = size;

        blocksQuantity++;
    }
    headerPtr->busyState = BUSY_STATE;

    return (void*)(headerPtr + 1);
}

/**
* Виділення пам'яті заданого розміру.
* size - розмір пам'яті, що буде виділятися.
* returns Вказівник на виділену область пам'яті або NULL, якщо виділення не вдалося.
*/
void *mem_alloc(size_t size) {
    Header *headerPtr = (*sAlgFunArray[sAlgorithm])(size);

    if ( headerPtr == NULL ) {
        return NULL;
    }

    return freeBlockAlloc(headerPtr, size);
}

/**
* Перевиділення пам'яті.
* addr - вказівник на область пам'яті, що буде перевиділятися.
* size - новий розмір області.
* returns Вказівник на перевиділену область пам'яті або NULL, якщо перевиділення не вдалося.
*/
void *mem_realloc(void *addr, size_t size) {
    if ( addr == NULL ) {
        return mem_alloc(size);
    }

    Header *headerPtr = (Header*)addr - 1;
    size_t freeSpace = headerPtr->size;

    // Якщо даного блоку достатньо для виділення місця, то використовуємо тільки його
    if ( freeSpace > size ) {
        return freeBlockAlloc(headerPtr, size);
    }

    // Якщо даного блоку не достатньо, то при можливості використовуємо наступний блок
    Header *nextHeaderPtr = getNextHeader(headerPtr);
    if ( nextHeaderPtr->busyState == FREE_STATE ) {
        freeSpace += nextHeaderPtr->size + headerSize;

        if ( freeSpace > size ) {
            headerPtr->size = freeSpace;
            blocksQuantity--;

            return freeBlockAlloc(headerPtr, size);
        }
    }

    // Надалі доведеться переміщати дані
    el_t *oldPtr = (el_t*)addr;
    el_t *newPtr;

    // При можливості використовуємо попередній блок
    Header *prevHeaderPtr = getPrevHeader(headerPtr);
    if ( prevHeaderPtr->busyState == FREE_STATE ) {
        freeSpace += prevHeaderPtr->size + headerSize;

        if ( freeSpace > size) {
            prevHeaderPtr->size = freeSpace;
            blocksQuantity--;

            // Переміщення даних
            newPtr = (el_t*)(prevHeaderPtr + 1);
            for ( size_t i = 0; i < headerPtr->size; i++ ) {
                newPtr[i] = oldPtr[i];
            }

            return freeBlockAlloc(prevHeaderPtr, size);
        }
    }

    // Якщо не вдалося перевиділити місце з допомогою суміжніх блоків
    newPtr = (el_t*)mem_alloc(size);
    if ( newPtr == NULL ) {
        return NULL;
    }

    // Переміщення даних
    for ( size_t i = 0; i < headerPtr->size; i++ ) {
        newPtr[i] = oldPtr[i];
    }

    mem_free((void*)oldPtr);
    return newPtr;
}

/**
* Звільнення пам'яті.
* addr - вказівник на область пам'яті, що буде звільнюватися.
*/
void mem_free(void *addr) {
    Header *headerPtr = (Header*)addr - 1;
    Header *nextHeaderPtr = getNextHeader(headerPtr);
    Header *prevHeaderPtr = getPrevHeader(headerPtr);

    headerPtr->busyState = FREE_STATE;

    if ( nextHeaderPtr->busyState == FREE_STATE ) {
        headerPtr->size += nextHeaderPtr->size + headerSize;
        getNextHeader(headerPtr)->prevSize = headerPtr->size;
        blocksQuantity--;
    }

    if ( prevHeaderPtr->busyState == FREE_STATE ) {
        prevHeaderPtr->size += headerPtr->size + headerSize;
        getNextHeader(prevHeaderPtr)->prevSize = prevHeaderPtr->size;
        blocksQuantity--;
    }
}

/**
* Виведення стану блоків пам'яті.
*/
void mem_dump() {
    Header *headerPtr = (Header*) firstBlock;

    printf("Blocks quantity: %d\n", blocksQuantity);

    for ( int i = 0; i < blocksQuantity; i++ ) {
        printf("Block %d:\n", i);
        printf("\tBusy state: %s\n", headerPtr->busyState == BUSY_STATE ? "busy" : "free");
        printf("\tBlock size: %u\n", headerPtr->size);
        printf("\tPrevious block size: %d\n", headerPtr->prevSize);

        headerPtr = getNextHeader(headerPtr);
    }
    printf("----------------------------------------\n");
}
