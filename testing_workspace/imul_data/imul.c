#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, const char * * argv) {
  for(int i = 0; i < 5; i++) {                
      __asm__ (
      //".intel_syntax noprefix\n\t"          // switch to Intel syntax
      "mov $401498, %%ecx\n\t"                 // Number of loops
      "loop1:\n\t"                            // Start of loop           
        ".rept 300\n\t"                           // 60 is the max value
          "mov $0x0000000003FCE23A,%%r8\n\t"
          "imul $0xD,%%r8,%%r8\n\t"
          "imul $0xD,%%r8,%%r8\n\t"
          "imul $0xD,%%r8,%%r8\n\t"
          "imul $0xD,%%r8,%%r8\n\t"
          "imul $0xD,%%r8,%%r8\n\t"
          "imul $0xD,%%r8,%%r8\n\t"
          "imul $0xD,%%r8,%%r8\n\t"
        ".endr;"
        "dec %%ecx\n\t"
        "jnz loop1\n\t"  
      //".att_syntax\n\t"             // switch back to AT&T syntax
      :                               // Outputs
      :                               // Inputs
      : "ecx", "r8"           // clobbered registers
    );
    usleep(200000); 
  }
  return (0);
}
