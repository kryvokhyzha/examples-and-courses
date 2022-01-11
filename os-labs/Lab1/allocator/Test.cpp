#include <iostream>
#include "Allocator.h"

using namespace std;

void fillBlock(void *start, int size, int filler)
{
  for (int i = 0; i < size; i++)
  {
    *((int *)start + 1) = filler;
  }
}

void test()
{
  cout << "test() started! \n";
  const int n = 2000;
  const int calls = 15;
  const int bSize = 50;

  Allocator al = Allocator(n);

  void *curBlock;
  void *mas[calls]; // has all user blocks

  for (int i = 0; i < calls; i++)
  {
    curBlock = al.mem_alloc(bSize);
    mas[i] = curBlock;
    fillBlock(curBlock, 50, 170); //170(dec) = 1010 1010(bin)
  }

  cout << "alloc 15 blocks (length = 50) \n";
  al.mem_dump();
  cout << "min 3th el to 20\n";
  al.mem_realloc(mas[3], 20);
  al.mem_dump();
  cout << "max 3th el to 30\n";
  al.mem_realloc(mas[3], 30);
  al.mem_dump();
  cout << "max 3th el to 49\n";
  al.mem_realloc(mas[3], 49);
  al.mem_dump();
  cout << "free 2th and 4th els \n";
  al.mem_free(mas[2]);
  al.mem_free(mas[4]);
  al.mem_dump();
  cout << "...and max 3th el to 156 \n";
  al.mem_realloc(mas[3], 156);
  al.mem_dump();
  cout << "min 2th el to 53 \n";
  al.mem_realloc(mas[2], 53);
  al.mem_dump();
  cout << "test() finished! \n";
}

int main()
{
  test();
  getchar();
  return 0;
}
