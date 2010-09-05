#include <stdio.h>
#include "a/test.h"

static int my_static_var = 10;

static void my_static_func(void) {
    printf("Hello A %d\n", my_static_var);
}

void dummy_a(void) {
    my_static_func();
}
