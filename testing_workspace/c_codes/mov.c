#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, const char **argv)
{
  for (int i = 0; i < 5; i++)
  {
    __asm__( // 4 500 000 000        4.5 Billion
        //".intel_syntax noprefix\n\t"          // switch to Intel syntax
        "mov $3000000, %%ecx\n\t" // Number of loops
        "loop1:\n\t"              // Start of loop
          ".rept 300\n\t"          
            "mov $0xF3F3F3F3F3FCE23A,%%rax\n\t"
            "mov %%rax, %%rbx\n\t"
            "mov %%rbx, %%rax\n\t"
          ".endr;"
          "dec %%ecx\n\t"
        "jnz loop1\n\t"
        //".att_syntax\n\t"             // switch back to AT&T syntax
        :                     // Outputs
        :                     // Inputs
        : "ecx", "eax", "ebx" // clobbered registers
    );
    usleep(200000);
  }
  return (0);
}
