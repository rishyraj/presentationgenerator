#include "mongoose.h"

static const char *url = "ws://127.0.0.1:1000";
static int exit_flag = 0;

static void ev_handler(struct mg_connection *c, int ev, void *p) {
  if (ev == MG_EV_HTTP_REPLY) {
    struct http_message *hm = (struct http_message *)p;
    c->flags |= MG_F_CLOSE_IMMEDIATELY;
    fwrite(hm->message.p, 1, (int)hm->message.len, stdout);
    putchar('\n');
    exit_flag = 1;
  } else  if (ev == MG_EV_CONNECT) {
    if ((*(int *) p) != 0) {
        fprintf(stderr, "connection err\n");
    }
  } else if (ev == MG_EV_CLOSE) {
    exit_flag = 1;
    printf("Closing connection");
  } else if (ev == MG_EV_POLL) {
    char msg[500];
    int n = 0;
    fd_set read_set, write_set, err_set;
    struct timeval timeout = {0, 0};
    FD_ZERO(&read_set);
    FD_ZERO(&write_set);
    FD_ZERO(&err_set);
    FD_SET(0 /* stdin */, &read_set);
    if (select(1, &read_set, &write_set, &err_set, &timeout) == 1) {
      n = read(0, msg, sizeof(msg));
    }
    if (n <= 0) return;
    while (msg[n - 1] == '\r' || msg[n - 1] == '\n') n--;
    mg_send_websocket_frame(c, WEBSOCKET_OP_TEXT, msg, n);
  } else if (ev == MG_EV_WEBSOCKET_FRAME) {
    struct websocket_message *wm = (struct websocket_message *) p;
    printf("%.*s\n", (int) wm->size, wm->data);
  } 
}

int main(void) {
  struct mg_mgr mgr;

  mg_mgr_init(&mgr, NULL);
  mg_connect_ws(&mgr, ev_handler, url, NULL, NULL);

  while (exit_flag == 0) {
    mg_mgr_poll(&mgr, 1000);
  }
  mg_mgr_free(&mgr);

  return 0;
}
