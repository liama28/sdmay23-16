#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#ifdef _MSC_VER
#include <intrin.h> /* for rdtscp and clflush */
#pragma optimize("gt",on)
#else
#include <x86intrin.h> /* for rdtscp and clflush */
#endif

int main(int argc,
  const char * * argv) {
    sleep(2);
    return (0);
}
