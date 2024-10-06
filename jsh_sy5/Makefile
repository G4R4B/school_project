CC = gcc
CFLAGS = -g -Wall -Wextra  #-fsanitize=address
LDLIBS = -lreadline

all:
	$(CC) $(CFLAGS) -o jsh main.c cd.c pwd.c $(LDLIBS)

clean:
	rm -f jsh