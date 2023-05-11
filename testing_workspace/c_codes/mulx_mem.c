#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <signal.h>
#include <time.h>

#define STR(x) #x
#define XSTR(s) STR(s)

// _____________________________________________________________

// TODO: Modify these values to match desired behavior.

// Number of loops for 'loop1'
/* Try keeping this value high enough, so the signature is noticeable
and you can collect good data but not so high the it takes more than
like 3 seconds to execute. */
#define LOOPS 400000

// Number of times instructions are repeated
/* We want this value to be large so the number of instructions that
we want to test is significantly more than the instructions needed
to maintain the loop and register values. Although it cannot be too large
or it will take a long time to compile, and the out file will be very
large. */
#define REPEAT 300

/* The next two values are used to calculate the number of
instructions that are executed. */

// Number of repeated instructions
#define NUM_REPEAT 8

//Number of pre repeated instruction
#define NUM_PRE_REPEAT 0

// _____________________________________________________________

int main(int argc, const char **argv) {

    

    clock_t start, end;
    double elapsed_time_ms;

    start = clock();

    // _____________________________________________________________

    int* x86_mem = (int*) malloc(1 * sizeof(int)); 

    asm volatile(
        // ____ Pre Loop ____
        "mov %0, %%rax\n\t"                 // Load address in rax
        "mov $0xD, %%ebx\n\t"
        "mov %%ebx,(%%rax)\n\t"

        // Number of loops loaded into counting register 'ecx'
        "mov $"XSTR(LOOPS)", %%ecx\n\t"       // i = LOOPS;               
        
        // ____ Loop Start ____
        "loop1:\n\t"

            // ____ Pre Repeat ____


            // ____ Repeat Start ____
            ".rept "XSTR(REPEAT)"\n\t"

                // ____ Repeated Instructions ____
                "mov $0x0000000003FCE23A,%%ebx\n\t"
                "mulx (%%rax),%%ebx,%%ebx\n\t"
                "mulx (%%rax),%%ebx,%%ebx\n\t"
                "mulx (%%rax),%%ebx,%%ebx\n\t"
                "mulx (%%rax),%%ebx,%%ebx\n\t"
                "mulx (%%rax),%%ebx,%%ebx\n\t"
                "mulx (%%rax),%%ebx,%%ebx\n\t"
                "mulx (%%rax),%%ebx,%%ebx\n\t"
            
            ".endr;"

        // ____ Loop End ____
        "dec %%ecx\n\t"                 // i--;
        "jnz loop1\n\t"                 // i > 0


        :                               // Outputs
        : "r" (x86_mem)                               // Inputs
        // Any registers used
        : "ecx", "rax", "ebx", "memory"               // Clobbered registers or "memory"
    );

    // _____________________________________________________________
    
    end = clock();    
    elapsed_time_ms = (double)(end - start) * 1000 / CLOCKS_PER_SEC;
    unsigned long total_inst = (LOOPS*NUM_PRE_REPEAT)+((unsigned long)LOOPS*REPEAT*NUM_REPEAT)+(LOOPS*3);
    double total_inst_mil = total_inst / 1000000;
    printf("%lf %lf\n", total_inst_mil, elapsed_time_ms); 

    
    return (0);
}

