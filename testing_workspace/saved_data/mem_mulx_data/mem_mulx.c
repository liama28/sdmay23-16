#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, const char * * argv) {
  int* x86_mem = (int*) malloc(1 * sizeof(int));  
  for(int i = 0; i < 5; i++) {                
      __asm__ (
      //".intel_syntax noprefix\n\t"          // switch to Intel syntax
      "mov %0, %%rax\n\t"                 // Load address in rax
      "mov $0xD, %%ebx\n\t"
      "mov %%ebx,(%%rax)\n\t"
      "mov $395152, %%ecx\n\t"                 // Number of loops
      "loop1:\n\t"                            // Start of loop           
        ".rept 300\n\t"                           // 60 is the max value
          "mov $0x0000000003FCE23A,%%ebx\n\t"
          "mulx (%%rax),%%ebx,%%ebx\n\t"
          "mulx (%%rax),%%ebx,%%ebx\n\t"
          "mulx (%%rax),%%ebx,%%ebx\n\t"
          "mulx (%%rax),%%ebx,%%ebx\n\t"
          "mulx (%%rax),%%ebx,%%ebx\n\t"
          "mulx (%%rax),%%ebx,%%ebx\n\t"
          "mulx (%%rax),%%ebx,%%ebx\n\t"
        ".endr;"
        "dec %%ecx\n\t"
        "jnz loop1\n\t"  
      //".att_syntax\n\t"             // switch back to AT&T syntax
      :                               // Outputs
      : "r" (x86_mem)                               // Inputs
      : "ecx", "rax", "ebx"           // clobbered registers
    );
    usleep(200000); 
  }
  return (0);
}
