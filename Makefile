# MT25XXX - PA02 Makefile
# Uses -O2 for realistic profiling and -pthread for multithreading.

CC = gcc
CFLAGS = -Wall -O2 -pthread
LDFLAGS = -pthread

TARGETS = \
	MT25XXX_Part_A1_Server MT25XXX_Part_A1_Client \
	MT25XXX_Part_A2_Server MT25XXX_Part_A2_Client \
	MT25XXX_Part_A3_Server MT25XXX_Part_A3_Client

all: $(TARGETS)

# ---------- Compilation rules ----------

MT25XXX_Part_A1_Server: MT25XXX_Part_A1_Server.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

MT25XXX_Part_A1_Client: MT25XXX_Part_A1_Client.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

MT25XXX_Part_A2_Server: MT25XXX_Part_A2_Server.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

MT25XXX_Part_A2_Client: MT25XXX_Part_A2_Client.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

MT25XXX_Part_A3_Server: MT25XXX_Part_A3_Server.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

MT25XXX_Part_A3_Client: MT25XXX_Part_A3_Client.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

# ---------- Clean rule (VERY IMPORTANT for PA02) ----------
clean:
	rm -f $(TARGETS) *.o
	rm -f MT25XXX_Part_C_Results.csv server.log
	rm -rf plots
