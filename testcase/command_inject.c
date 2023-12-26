#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void excutor(char *cmd){
    char buffer[0x100];
    snprintf(buffer, 0x100, "ping %s;", cmd);
    system(buffer);
}

int main(){
    char ip[100];
    read(0,ip,100);
    if (!strcmp(ip,"echo\n"))
        excutor(ip);
    return 0;
}