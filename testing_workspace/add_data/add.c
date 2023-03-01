#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
  for(int i = 0; i < 5; i++) {
  asm (
      //".intel_syntax noprefix\n\t"      // switch to Intel syntax
      "mov $2, %%ebx\n\t"                 // load 2 into ebx
      "mov $3267973, %%ecx\n"            // Number of loops
      "loop1:\n\t"                   // Start of loop
        "movl $0, %%eax\n\t"            
        ".rept 300;"                       // 60 is the max value
          "add %%ebx, %%eax\n\t"        
        ".endr;"                     
      "dec %%ecx\n\t"
      "jnz loop1\n\t"
      //".att_syntax\n\t"             // switch back to AT&T syntax
      :                               // Outputs
      :                               // Inputs
      : "ebx", "eax", "ecx"           // clobbered registers
    );
    usleep(200000);                   // 0.1 s                  
  }


}
