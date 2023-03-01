#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, const char **argv)
{
     __asm__(
        //".intel_syntax noprefix\n\t"          // switch to Intel syntax
        "mov $0xD, %%eax\n\t"
        "mov $1875000, %%ecx\n\t" // Number of loops
        "loop1:\n\t"              // Start of loop
          ".rept 300\n\t"            // 60 is the max value
            "mov $0x0000000003FCE23A,%%ebx\n\t"
            "mulx %%eax,%%ebx,%%ebx\n\t"
            "mulx %%eax,%%ebx,%%ebx\n\t"
            "mulx %%eax,%%ebx,%%ebx\n\t"
            "mulx %%eax,%%ebx,%%ebx\n\t"
            "mulx %%eax,%%ebx,%%ebx\n\t"
            "mulx %%eax,%%ebx,%%ebx\n\t"
            "mulx %%eax,%%ebx,%%ebx\n\t"
          ".endr;"
        "dec %%ecx\n\t"
        "jnz loop1\n\t"
        //".att_syntax\n\t"             // switch back to AT&T syntax
        :                     // Outputs
        :                     // Inputs
        : "ecx", "eax", "ebx" // clobbered registers
    );
    //usleep(100000);
  return (0);
}
