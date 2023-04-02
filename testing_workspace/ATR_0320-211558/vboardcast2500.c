#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <signal.h>
#include <time.h>

int main(int argc, const char **argv) {
    int i;
    for (i = 0; i < 2500; i++){
        asm volatile(
          "vpbroadcastd %xmm0,%ymm0\n\t"
          "vpbroadcastd %xmm1,%ymm1\n\t"
          "vpbroadcastd %xmm2,%ymm2\n\t"
          "vpbroadcastd %xmm0,%ymm0\n\t"
          "vpbroadcastd %xmm1,%ymm1\n\t"
          "vpbroadcastd %xmm2,%ymm2\n\t"
        );
      }
}