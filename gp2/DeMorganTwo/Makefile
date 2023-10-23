OBJECTS = $(patsubst lexer.o,,$(patsubst %.c,%.o,$(wildcard *.c)))
CC = gcc

CFLAGS = -L/usr/lib -L/usr/lib/x86_64-linux-gnu -lJudy -Wall -Wno-unused-but-set-variable -DNDEBUG -O3 -flto -fuse-linker-plugin

default:	$(OBJECTS)
		$(CC) $(OBJECTS) $(CFLAGS) -o gp2run

%.o:		%.c
		$(CC) -c $(CFLAGS) -o $@ $<

clean:	
		rm *
