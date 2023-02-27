#include <stdio.h>
#include <stdlib.h>

int main() {
    int* values;
    int size = 5;
    int sum;

    // allocate dynamic memory
    values = (int*) malloc(size * sizeof(int));

    // initialize values
    for (int i = 0; i < size; i++) {
        values[i] = i * 2;
    }

    // use inline assembly to access values
    asm (
        "movl %0, %%eax\n\t"   // move the pointer to the allocated memory into eax
        "movl (%%eax), %%ebx\n\t" // load the first value into ebx
        "addl $4, %%eax\n\t"   // move the pointer to the second value
        "movl (%%eax), %%ecx\n\t" // load the second value into ecx
        "addl %%ecx, %%ebx\n\t"  // add the second value to the first value
        "movl %%ebx, %1\n\t"   // move the result into variable sum
        :                       // output operands: none
        : "r" (values), "r" (sum) // input operands: values is the pointer to the allocated memory, sum is a variable to store the result
        : "eax", "ebx", "ecx"   // clobbered registers: we use eax, ebx, and ecx, so we need to tell the compiler
    );

    printf("The sum of the first two values in the allocated memory is %d\n", sum);

    // free dynamic memory
    free(values);

    return 0;
}
