#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

#define PATH_MAX 4096 /* # chars in a path name including nul */
int pwd(){
    char * cwd = malloc(sizeof(char)*PATH_MAX);
    getcwd(cwd,PATH_MAX);
    printf("%s\n",cwd);
    free(cwd);
    return 0;
}