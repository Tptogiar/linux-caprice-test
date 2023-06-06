#include <stdio.h>
#include <string.h>

struct key_t {
    char c[80];
};




int main() {
    struct key_t key = {"Hello World"};
    printf("pointer key = %p \n",key);
    printf("pointer &key = %p \n",&key);
    printf("pointer key.c = %p \n",key.c);
    printf("pointer &key.c = %p \n",&key.c);


    char str[] = "   Hello    World   !";
    printf("pointer str = %p \n",str);
    printf("pointer &str = %p \n",&str);



    
    int length = strlen((char*)str);
    printf("The length of the string is %d\n", length);
    return 0;
}

