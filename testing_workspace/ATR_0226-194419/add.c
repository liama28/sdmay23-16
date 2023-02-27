#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
  for(int i = 0; i < 20; i++) {
  asm (
      //".intel_syntax noprefix\n\t"      // switch to Intel syntax
      "mov $2, %%ebx\n\t"                 // load 2 into ebx
      "mov $1500000, %%ecx\n"            // Number of loops
      "loop_start:\n\t"                   // Start of loop
        "movl $0, %%eax\n\t"            
        ".rept 60;"                       // 60 is the max value
          "add %%ebx, %%eax\n\t"        
        ".endr;"                     
      "loop loop_start\n"
      //".att_syntax\n\t"             // switch back to AT&T syntax
      :                               // Outputs
      :                               // Inputs
      : "ebx", "eax", "ecx"           // clobbered registers
    );
    usleep(25000);
  }


}
