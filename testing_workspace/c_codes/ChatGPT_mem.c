/* Write C code that inserts x86 assembly code using AT&T syntax that 
allocates memory stores a value in it, and multiply the value by 0xD*/

#include <stdlib.h>

int main() {
    int *ptr;

    // Allocate memory for an integer
    asm("movl $4, %eax"); // system call number for mmap
    asm("xorl %ebx, %ebx"); // address hint, zero for any address
    asm("movl $1, %ecx"); // PROT_READ
    asm("movl $2, %edx"); // PROT_WRITE
    asm("movl $32, %esi"); // length of memory region
    asm("xorl %edi, %edi"); // file descriptor
    asm("xorl %ebp, %ebp"); // offset
    asm("int $0x80"); // call mmap system call
    asm("movl %eax, %ebx"); // save returned address to ebx

    ptr = (int*) ebx; // cast address to int pointer

    // Store a value in the allocated memory
    *ptr = 0x7;

    // Multiply the value by 0xD
    asm("movl (%0), %%eax" : : "r" (ptr)); // load value from memory into eax
    asm("imull $0xD, %%eax" : : ); // multiply the value by 0xD
    asm("movl %%eax, (%0)" : : "r" (ptr)); // store the result back into memory

    // Free the allocated memory
    asm("movl $73, %eax"); // system call number for munmap
    asm("movl %0, %ebx" : : "r" (ptr)); // pass pointer address to ebx
    asm("movl $32, %ecx"); // length of memory region
    asm("int $0x80"); // call munmap system call

    return 0;
}