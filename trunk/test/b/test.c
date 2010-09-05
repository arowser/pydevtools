#include <stdio.h>
#include "b/test.h"

static int my_static_var = 10;

static void my_static_func(void) {
    printf("Hello B: %d\n", my_static_var);
}

void dummy_b(void) {
    my_static_func();
}
