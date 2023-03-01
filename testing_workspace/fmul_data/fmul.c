#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, const char **argv)
{
  float f = 1.124343243;
  for (int i = 0; i < 5; i++)
  {
    __asm__( // 4 500 000 000        4.5 Billion
        //".intel_syntax noprefix\n\t"          // switch to Intel syntax
        "mov $6300, %%ecx\n\t" // Number of loops
        "mov %0, %%rax\n\t"
        "fld (%%rax)\n\t"
        "loop1:\n\t"              // Start of loop
        "fld (%%rax)\n\t"
          ".rept 300\n\t"          
            "fmul (%%rax)\n\t"
          ".endr;"
        "dec %%ecx\n\t"
        "jnz loop1\n\t"
        //".att_syntax\n\t"             // switch back to AT&T syntax
        :                     // Outputs
        : "r" (&f)                    // Inputs
        : "ecx", "eax", "ebx" // clobbered registers
    );
    usleep(200000);
  }
  return (0);
}
