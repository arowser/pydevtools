CC = gcc
CC_FLAGS = -gdwarf-2 -O0 -I.

TEST=test
OBJS = a/test.o b/test.o main.o

all: $(TEST)

%.o: %.c
	$(CC) $(CC_FLAGS) -o $@ -c $<

$(TEST): $(OBJS)
	$(CC) -o $@ $^

clean:
	rm -rf $(TEST) $(OBJS)
