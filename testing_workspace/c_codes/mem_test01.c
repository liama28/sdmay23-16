#include <stdio.h>
#include <stdlib.h>

int main() {
    int src = 1;

    int* values = (int*) malloc(1 * sizeof(int));  

    asm (
        //".intel_syntax noprefix\n\t"    // switch to Intel syntax
        "mov %0, %%rax\n\t"
        "movl $1, (%%rax)\n\t"
        //".att_syntax\n\t"            // switch back to AT&T syntax
        :                               // Outputs
        : "r" (values), "r" (src)       // Inputs
        : "rax"                              // clobbered registers
        );

    printf("%d\n", values[0]);

    return 0;
}
