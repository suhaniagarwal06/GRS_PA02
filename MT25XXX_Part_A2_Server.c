#include <arpa/inet.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>

#define FIELDS 8

typedef struct {
    int sock;
    size_t msg_size;
} client_arg;

void *client_thread(void *arg) {
    client_arg *c = (client_arg *)arg;

    size_t field_size = c->msg_size / FIELDS;

    char *fields[FIELDS];
    struct iovec iov[FIELDS];

    for (int i = 0; i < FIELDS; i++) {
        fields[i] = malloc(field_size);
        memset(fields[i], 'A' + i, field_size);
        iov[i].iov_base = fields[i];
        iov[i].iov_len = field_size;
    }

    struct msghdr msg = {0};
    msg.msg_iov = iov;
    msg.msg_iovlen = FIELDS;

    while (sendmsg(c->sock, &msg, 0) > 0);

    for (int i = 0; i < FIELDS; i++) free(fields[i]);
    close(c->sock);
    free(c);
    return NULL;
}

int main(int argc, char *argv[]) {
    int port = atoi(argv[1]);
    size_t msg_size = atol(argv[2]);

    int s = socket(AF_INET, SOCK_STREAM, 0);

    struct sockaddr_in addr = {0};
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    addr.sin_addr.s_addr = INADDR_ANY;

    bind(s, (struct sockaddr *)&addr, sizeof(addr));
    listen(s, 128);

    printf("READY\n"); fflush(stdout);

    while (1) {
        int c = accept(s, NULL, NULL);

        client_arg *arg = malloc(sizeof(client_arg));
        arg->sock = c;
        arg->msg_size = msg_size;

        pthread_t t;
        pthread_create(&t, NULL, client_thread, arg);
        pthread_detach(t);
    }
}
