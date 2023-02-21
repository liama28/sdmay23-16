

int main(int argc, const char * * argv) {
  for(int i = 0; i < 120000000; i++) {
  __asm__(".rept 2;"
    "mov $$0x0000000003FCE23A,%r8;"
    "imul $$0xD,%r8,%r8;"
  ".endr");
    }
  return (0);
}
