#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(){
    char ip[100];
    read(0,ip,100);
    printf(ip);
    printf("%s",ip);
    return 0;
}