#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
 //This doesn't work
int main(int argc, const char **argv)
{
  for (int i = 0; i < 10; i++)
  {
    __asm__( // 4 500 000 000        4.5 Billion
        //".intel_syntax noprefix\n\t"          // switch to Intel syntax
        "mov $7500000, %%ecx\n\t" // Number of loops
        "mov $0xFFFF,%%eax\n\t"
        "loop1:\n\t"              // Start of loop
          ".rept 300\n\t"          
            "push %%rax\n\t"
            "pop %%rax\n\t"
          ".endr;"
          "dec %%ecx\n\t"
        "jnz loop1\n\t"
        //".att_syntax\n\t"             // switch back to AT&T syntax
        :                     // Outputs
        :                     // Inputs
        : "ecx", "eax", "ebx" // clobbered registers
    );
    //usleep(100000);
  }
  return (0);
}
