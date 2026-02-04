#include <arpa/inet.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/time.h>

typedef struct {
    char ip[64];
    int port;
    size_t msg_size;
    int duration;
} arg_t;

void *worker(void *p) {
    arg_t *a = (arg_t *)p;

    int s = socket(AF_INET, SOCK_STREAM, 0);

    struct sockaddr_in addr = {0};
    addr.sin_family = AF_INET;
    addr.sin_port = htons(a->port);
    inet_pton(AF_INET, a->ip, &addr.sin_addr);

    connect(s, (struct sockaddr *)&addr, sizeof(addr));

    char *buf = malloc(a->msg_size);

    long bytes = 0;
    struct timeval start, now;
    gettimeofday(&start, NULL);

    while (1) {
        ssize_t r = recv(s, buf, a->msg_size, 0);
        if (r <= 0) break;

        bytes += r;

        gettimeofday(&now, NULL);
        if (now.tv_sec - start.tv_sec >= a->duration) break;
    }

    double time = (now.tv_sec - start.tv_sec) +
                  (now.tv_usec - start.tv_usec) / 1e6;

    double throughput = (bytes * 8.0) / (time * 1e9);
    double latency = (time * 1e6) / (bytes / a->msg_size);

    printf("RESULT %.6f %.6f\n", throughput, latency);
    fflush(stdout);

    close(s);
    free(buf);
    return NULL;
}

int main(int argc, char *argv[]) {
    char *ip = argv[1];
    int port = atoi(argv[2]);
    size_t size = atol(argv[3]);
    int threads = atoi(argv[4]);
    int duration = atoi(argv[5]);

    pthread_t t[threads];
    arg_t args[threads];

    for (int i = 0; i < threads; i++) {
        snprintf(args[i].ip, sizeof(args[i].ip), "%s", ip);
        args[i].port = port;
        args[i].msg_size = size;
        args[i].duration = duration;
        pthread_create(&t[i], NULL, worker, &args[i]);
    }

    for (int i = 0; i < threads; i++)
        pthread_join(t[i], NULL);
}
