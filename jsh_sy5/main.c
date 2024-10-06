#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>
#include <dirent.h>
#include <string.h>
#include <limits.h>
#include <stdbool.h>
#include <stdio.h>
#include <sys/wait.h>
#include <readline/readline.h>
#include <readline/history.h>
#include <signal.h>
#include <errno.h>

#include "cd.h"
#include "pwd.h"


static int jobs = 0;
static int error_num = 0;

char **cut(char* cmd, int * nbrArgu){
    
    char * cmd_copy = malloc(sizeof(char)*(strlen(cmd)+1));
    strcpy(cmd_copy, cmd);
    //count the number of arguments
    char * token = strtok(cmd_copy, " ");
    int i = 0;
    while (token != NULL){
        i++;
        token = strtok(NULL, " ");
    }
    free(cmd_copy);
    *nbrArgu = i;
    if (i == 0){
        return NULL;
    }
    //create the array of arguments
    char ** cmdSplit = malloc(sizeof(char*)*(i+1));
    token = strtok(cmd, " ");
    i = 0;
    while (token != NULL){
        cmdSplit[i] = malloc(sizeof(char)*(strlen(token)+1));
        strcpy(cmdSplit[i], token);
        token = strtok(NULL, " ");
        i++;
    }
    cmdSplit[i] = NULL;
    
    return cmdSplit;
}


void commande(char* cmd){
    // parser les cmd en fonction des espaces :
    int nbrArgu = 0;
    char ** cmdSplit = cut(cmd, &nbrArgu);
    if (cmdSplit == NULL){
        return;
    }
    if (strcmp(cmdSplit[0], "cd") == 0){
        if (nbrArgu == 1){
            error_num = cd(NULL);
        }else if (nbrArgu == 2){
            error_num = cd(cmdSplit[1]);
        }else{
            printf("%s : Erreur cette commande ne prend pas plus d'un argument \n", cmd) ;
        }
    }else if (strcmp(cmdSplit[0], "pwd") == 0){
        if (nbrArgu == 1){
            error_num = pwd();
        }else{
            printf("%s : Erreur cette commande ne prend pas d'argument \n", cmd) ;
        }
    }else if (strcmp(cmdSplit[0], "exit") == 0){
        if (nbrArgu == 1){
            for (int i = 0; i < nbrArgu; i++){
                free(*(cmdSplit+i));
            }
            free(cmdSplit);
            exit(error_num);
        }else if (nbrArgu == 2){
            int status = atoi(cmdSplit[1]);
            for (int i = 0; i < nbrArgu; i++){
                free(*(cmdSplit+i));
            }
            free(cmdSplit);
            exit(status);
        }else{
            printf("%s : Erreur cette commande ne prend qu'un argument \n", cmd) ;
        }
    }else if (strcmp(cmdSplit[0], "?") == 0){
        printf("%d\n", error_num);
        error_num = 0;
    }
    else {
    if(fork() == 0){
            if (execvp(cmdSplit[0], cmdSplit) == -1){
                fprintf(stderr,"bash: %s: %s\n",cmdSplit[0], strerror(errno));
                exit(errno);
            }
    }else {
            int status;
            wait(&status);
            error_num = WEXITSTATUS(status);
        }
}

    //free cmdSplit
    for (int i = 0; i < nbrArgu; i++){
        free(*(cmdSplit+i));
    }
    free(cmdSplit);
    
}


int main(void){
    char prompt[46]; // 30 + color of the prompt
    char * cwd = malloc(sizeof(char)*PATH_MAX);
    char * line_read = (char *)NULL;
    rl_outstream = stderr;
    while (1){
          if (line_read)
        {
                free (line_read);
                line_read = (char *)NULL;
        }
        getcwd(cwd,PATH_MAX);
        sprintf(prompt,"%d",jobs);
        if (strlen(prompt) + strlen(cwd) < 27){
            sprintf(prompt, "\033[00m[%d]\033[32m%s$\033[00m ", jobs, cwd);
        }else{
            sprintf(prompt, "\033[00m[%d]\033[32m...%s$\033[00m ", jobs, cwd + strlen(cwd) - 22);
        }
        line_read = readline(prompt); //lecture de la ligne de commande
        add_history(line_read);
        if (line_read == NULL){
            exit(error_num);
        }
        if (strcmp(line_read, "") != 0){
            commande(line_read);
        }
    }
    
}