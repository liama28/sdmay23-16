#include <stdio.h>
#include <stdlib.h>

int main() {
    int src = 1;

    int* x86_mem = (int*) malloc(1 * sizeof(int));  
    asm (
        //".intel_syntax noprefix\n\t"      // switch to Intel syntax
        "mov %0, %%rax\n\t"                 // Load address in rax
        "mov $2, %%ebx\n\t"                 // load 2 into ebx
        "mov $10000000, %%ecx\n"            // Number of loops. ecx is decremented in each loop
        "loop_start:\n\t"                   // Start of loop
          "movl $0, (%%rax)\n\t"            // Set x86_mem[0] back to 0
          ".rept 60;"                       // 60 is the max value
            "add %%ebx, (%%rax)\n\t"        // add 2 to x86_mem[0]
          ".endr;"                     
        "loop loop_start\n"
        //".att_syntax\n\t"             // switch back to AT&T syntax
        :                               // Outputs
        : "r" (x86_mem)                 // Inputs
        : "rax", "ebx", "eax", "ecx"    // clobbered registers
        );

    printf("%d\n", x86_mem[0]);

    return 0;
}