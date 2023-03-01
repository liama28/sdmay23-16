#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, const char **argv)
{
  int* x86_mem = (int*) malloc(1 * sizeof(int));
   __asm__( // 4 500 000 000        4.5 Billion
        //".intel_syntax noprefix\n\t"          // switch to Intel syntax
        "mov %0, %%rax\n\t"    
        "mov $5000000, %%ecx\n\t" // Number of loops
        "loop1:\n\t"              // Start of loop
          ".rept 300\n\t"          
            "movl $0xFCE23A,(%%rax)\n\t"
            "mov (%%rax), %%rbx\n\t"
            "mov %%rbx, (%%rax)\n\t"
          ".endr;"
          "dec %%ecx\n\t"
        "jnz loop1\n\t"
        //".att_syntax\n\t"             // switch back to AT&T syntax
        :                     // Outputs
        : "r" (x86_mem)       // Inputs
        : "ecx", "eax", "ebx" // clobbered registers
    );
    //usleep(100000);
  return (0);
}
