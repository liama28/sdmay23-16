#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
  int* x86_mem = (int*) malloc(1 * sizeof(int));  
  for(int i = 0; i < 5; i++) {
  asm (
      //".intel_syntax noprefix\n\t"      // switch to Intel syntax
      "mov %0, %%rax\n\t"                 // Load address in rax
      "mov $2, %%ebx\n\t"                 // load 2 into ebx
      "mov $565184, %%ecx\n"            // Number of loops
      "loop1:\n\t"              // Start of loop
        "movl $0, (%%rax)\n\t"            // Set x86_mem[0] back to 0
        ".rept 300;"                       // 60 is the max value
          "add %%ebx, (%%rax)\n\t"        // add 2 to x86_mem[0]
        ".endr;"                     
      "dec %%ecx\n\t"
      "jnz loop1\n\t"
      //".att_syntax\n\t"             // switch back to AT&T syntax
      :                               // Outputs
      : "r" (x86_mem)                 // Inputs
      : "rax", "ebx", "eax", "ecx"    // clobbered registers
    );
    usleep(200000);  // 0.1 s
  }

}
          