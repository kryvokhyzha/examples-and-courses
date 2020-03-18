#pragma once 

struct LBlockDescriptor{
	size_t nextFreeBlock;//shift
};

struct PageDescriptor{
	size_t next; //list of pages with the same state	
	LBlockDescriptor* firstFree; //free block in state 1
	size_t bsize; // size of lBlock in state 1 or number of blocks in state 2
	char state; //0-free, 1-lblock, 2-mblock	
};

class Allocator {
public:	
	Allocator(const size_t ms, const size_t ps); 
	
	//return addr on begin of allocated block or NULL
	void* mem_alloc(size_t size);
	
	//return addr on begin of reallocated block or NULL
	void* mem_realloc(void *addr, size_t size);
	
	//free block by this address
	void mem_free(void *addr);
	
	//out blocks characteristic in table on console
	void mem_dump();
	
private:
	//begin of control information
	size_t* begin;
	//begin of pages in memory
	size_t* pagesBegin;
	size_t size;
	size_t pages;
	size_t pageSize;
	//array of all page descriptors
	PageDescriptor* pageDescriptors;
	//array of pages with state 1 
	size_t* lBlocks;

	size_t lBlocksLength;
	
	size_t firstFreePage;
	//define what type of state rigth for this size
	PageDescriptor defineCategory(size_t s);
	//round s to minimal need size power of 2
	size_t defineBlockSize(size_t s);

	//initial all pages as free
	void initPages();
	// return free block with size bs
	size_t* getFreeLBlock(size_t bs);
	//return index for lBlocks array
	size_t getIndex(size_t s);
	
	size_t createLBlockPage(size_t bs);
	//size_t getLBlockPage(size_t bs);
	//not use :/
	size_t getFreePage();
	//return page`s address from index of pages array 
	size_t* getAbsolutePageAddr(size_t index);
	//set all blocks in page to free state
	void setAllFree(PageDescriptor pd);
	//return big block with length ps*pageSize
	size_t* getFreeMBlock(size_t ps);
	//check is this block alst free in this page
	bool freeLBlockIsLast(PageDescriptor pd);
	//return number of page from her addr
	size_t findPageByAddress(size_t* addr);
	//return number of block from his addr
	size_t findBlockByAddress(size_t* addr, size_t bs);
	//copy data from old pos to new
	void copyData(size_t* from, size_t* to, size_t length);
};
