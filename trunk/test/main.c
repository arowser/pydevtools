#include <stdio.h>
#include "a/test.h"
#include "b/test.h"

typedef struct my_base_s {
    int a;
    char b;
} my_base_t;

typedef struct my_complex_e {
    my_base_t first;
    my_base_t second;
} my_complex_t;

my_complex_t temp;

static int f3(int a3) {
    int rc3;
    static int state = 0;
    
    
    rc3 = a3 + 1;
    state = rc3;
    
    return rc3;
}

static int f2(int a2) {
    int rc2;
    int b2;
    
    b2 = a2 + 1;
    
    rc2 = f3(b2);
    
    temp.second.a = rc2;
    
    return rc2;
}

int f1(int a1) {
    int rc1;
    int b1;
    
    b1 = a1 + 1;
    
    rc1 = f2(b1);
    
    temp.first.a = rc1;
    
    return rc1;
}

int main(void) {
    int rc0 = 0xFF;
    
    rc0 = f1(1);
    
    dummy_a();
    dummy_b();
    
    return rc0;
}
