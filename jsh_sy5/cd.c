#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define PATH_MAX 4096 /* # chars in a path name including nul */

static char prev_dir[PATH_MAX];

int cd(char * path){
    int ret;
    if (path == NULL){
        getcwd(prev_dir,PATH_MAX);
       ret = chdir(getenv("HOME"));
    }
    else if (strcmp(path,"-") == 0){
        char * prev_prev_dir = malloc(sizeof(char)*PATH_MAX);
        getcwd(prev_prev_dir,PATH_MAX);
        ret = chdir(prev_dir);
        strcpy(prev_dir,prev_prev_dir);
        free(prev_prev_dir);
    }
    else{
    getcwd(prev_dir,PATH_MAX);
    ret = chdir(path);
    if(ret == -1){
        fprintf(stderr,"cd: %s: No such file or directory\n",path);
        return 1;
    }
    }
    return 0;
}