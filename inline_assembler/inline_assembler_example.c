#include<stdio.h>

int main()
{
    int intel_src = 1;
    int intel_dst;

    /*
     * Taken from
     * https://gcc.gnu.org/onlinedocs/gcc/Extended-Asm.html#Extended-Asm
     *
     * Also, see:
     * https://gcc.gnu.org/onlinedocs/gcc/Extended-Asm.html#OutputOperands
     *
     * This assembly copies src to dst and add 1 to dst
     *
     * */
    asm ("mov %1, %0\n\t"
         "add $1, %0"
         : "=r" (intel_dst)
         : "r" (intel_src));

    int at_src = 5;
    int at_dst;
    asm ("movl %1, %0\n\t"
         "addl $1, %0"
         : "=r" (at_dst)
         : "r" (at_src));

    printf("%d\n", intel_dst);
    printf("%d\n", at_dst);
    return 0;
}
