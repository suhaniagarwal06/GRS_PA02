# MT25046 - PA02 Makefile

CC = gcc
CFLAGS = -Wall -O2 -pthread
LDFLAGS = -pthread

TARGETS = \
	MT25046_Part_A1_Server MT25046_Part_A1_Client \
	MT25046_Part_A2_Server MT25046_Part_A2_Client \
	MT25046_Part_A3_Server MT25046_Part_A3_Client

all: $(TARGETS)

# ---------- Compilation rules ----------

MT25046_Part_A1_Server: MT25046_Part_A1_Server.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

MT25046_Part_A1_Client: MT25046_Part_A1_Client.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

MT25046_Part_A2_Server: MT25046_Part_A2_Server.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

MT25046_Part_A2_Client: MT25046_Part_A2_Client.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

MT25046_Part_A3_Server: MT25046_Part_A3_Server.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

MT25046_Part_A3_Client: MT25046_Part_A3_Client.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

# ---------- Clean rule (VERY IMPORTANT for PA02) ----------
clean:
	rm -f $(TARGETS) *.o
	rm -f MT25046_Part_C_Results.csv server.log
	rm -rf plots
