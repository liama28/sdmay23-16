int main(int argc, const char * * argv) {
      __asm__ (
      //".intel_syntax noprefix\n\t"          // switch to Intel syntax
      "mov $60000000, %%ecx\n\t"                 // Number of loops
      "loop1:\n\t"                            // Start of loop           
        ".rept 25\n\t"                           // 60 is the max value
          "mov $0x0000000003FCE23A,%%r8\n\t"
          "imul $0xD,%%r8,%%r8\n\t"
          "imul $0xD,%%r8,%%r8\n\t"
          "imul $0xD,%%r8,%%r8\n\t"
          "imul $0xD,%%r8,%%r8\n\t"
          "imul $0xD,%%r8,%%r8\n\t"
          "imul $0xD,%%r8,%%r8\n\t"
          "imul $0xD,%%r8,%%r8\n\t"
        ".endr;"
        "dec %%ecx\n\t"
        "jnz loop1\n\t"  
      //".att_syntax\n\t"             // switch back to AT&T syntax
      :                               // Outputs
      :                               // Inputs
      : "ecx", "r8"           // clobbered registers
    );
  return (0);
}
