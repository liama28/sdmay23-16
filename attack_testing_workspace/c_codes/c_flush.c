#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <sys/time.h>
#ifdef _MSC_VER
#include <intrin.h> /* for rdtscp and clflush */
#pragma optimize("gt",on)
#else
#include <x86intrin.h> /* for rdtscp and clflush */
#endif

uint8_t temp = 0;

int main(int argc, const char * * argv) {
  unsigned int array1_size = 16;
  uint8_t array1[160] = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16};
  uint8_t array2[256 * 512]; // = 131072 = 4096 * 32
  int i, j, mix_i, junk = 0;
  volatile uint8_t * addr;

  int len = 40;

  for (i = 0; i < sizeof(array2); i++)
    array2[i] = 1; /* write to array2 so in RAM not copy-on-write zero pages */

  while (--len >= 0) {
    for (i = 999; i > 0; i--) {
      for (j = 0; j < 256; j++) _mm_clflush( & array2[j * 512]); /* intrinsic for clflush instruction */
      for (j = 0; j < 256; j++) {
        mix_i = ((j * 167) + 13) & 255;
        addr = & array2[mix_i * 512];
        junk = * addr; /* MEMORY ACCESS TO TIME */
      }
    }
  }
  return (0);
}
