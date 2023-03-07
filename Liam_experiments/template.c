#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <signal.h>
#include <time.h>

// _____________________________________________________________

// TODO: Modify these values to match desired behavior.

// Number of loops for 'loop1'
/* Try keeping this value high enough, so the signature is noticeable
and you can collect good data but not so high the it takes more than
like 3 seconds to execute. */
#define LOOPS "375000"

// Number of times instructions are repeated
/* We want this value to be large so the number of instructions that
we want to test is significantly more than the instructions needed
to maintain the loop and register values. Although it cannot be too large
or it will take a long time to compile, and the out file will be very
large. */
#define REPEAT "300"

// Number of times that the function 'exe_x86' will be called
/* The more runs, the more data we can collect, but it will take
longer to run. That is really the only trade-off here.*/
#define RUNS 5

// How long the program will wait between each run of 'exe_x86' in milliseconds
/* It is a good idea to sleep between each run so we can visually
see where the instructions are executed, and so too many of them
are not executed back to back */
#define USLEEP 200000

// _____________________________________________________________

void exe_x86(void) {
    // TODO: Insert x86 instructions that you wish to test
    asm volatile(
        // ____ Pre Loop ____


        // Number of loops loaded into counting register 'ecx'
        "mov $"LOOPS", %%ecx\n\t"       // i = LOOPS;               
        
        // ____ Loop Start ____
        "loop1:\n\t"

            // ____ Pre Repeat ____


            // ____ Repeat Start ____
            ".rept "REPEAT"\n\t"

                // ____ Repeated Instructions ____
                
            
            ".endr;"

        // ____ Loop End ____
        "dec %%ecx\n\t"                 // i--;
        "jnz loop1\n\t"                 // i > 0


        :                               // Outputs
        :                               // Inputs
        // Any registers used
        : "ecx"                        // Clobbered registers or "memory"
    );
}

// _____________________________________________________________

int main(int argc, const char **argv) {

    if (argc < 2) {
        printf("Usage: %s <name>\n", argv[0]);
        exit(1);
    }

    // _________ Spawn child process for data collection ____________

    // Fork a child process
    pid_t pid = fork();

    if (pid == -1) { // Check for error
        perror("fork");
        exit(EXIT_FAILURE);
    }

    if (pid == 0) { // Child process
        char command[100];
        sprintf(command, "sudo /data_kill.sh %s", argv[1]);
        char *args[] = {"sh", "-c", command, NULL};
        execvp(args[0], args);
        perror("execvp");
        exit(EXIT_FAILURE);
    }

    // ____________________________________________________________

    clock_t start, end;
    double elapsed_time_ms;
    double sum_elapsed_time = 0;

    for (int i=0; i < RUNS; i++) {
        kill(pid, SIGUSR1);
        start = clock();
        exe_x86();
        end = clock();
        kill(pid, SIGUSR1);
        elapsed_time_ms = (double)(end - start) * 1000 / CLOCKS_PER_SEC;
        sum_elapsed_time += elapsed_time_ms;
        printf("%d: %lf milliseconds\n", i, elapsed_time_ms); 
        usleep(USLEEP);
    }

    printf("Average run time: %lf\n", (double)(sum_elapsed_time/RUNS));

    // ____________________________________________________________

    kill(pid, SIGINT);

    int status;
    waitpid(pid, &status, 0);

    if (WIFEXITED(status)) {
        printf("Child exited with status %d\n", WEXITSTATUS(status));
    } else if (WIFSIGNALED(status)) {
        printf("Child terminated by signal %d\n", WTERMSIG(status));
    }
    
    return (0);
}

