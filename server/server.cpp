#include "mongoose.h"
#include <string>
#include <iostream>
#include <stdio.h>

// http struct
static struct mg_serve_http_opts s_http_server_opts;
static void ev_handler(struct mg_connection * connection, int e, void * p);
int InitServer(int port);
static void broadcast(struct mg_connection *nc, const struct mg_str msg);
static void signal_handler(int sig_num);

int main(void) {
    int port = 0;

    // getting port, if failed port is 1000
    std::cout << "Select server port" << std::endl;
    std::cin >> port;
    if (std::cin.fail()) port = 1000;

    InitServer(port);

    return 0;
}

/* 0 for any failure
 */

int InitServer(int port) {

    // mongoose manager
    struct mg_mgr mgr;

    // mongoose connections
    struct mg_connection * connection;

    std::string portToChar = std::to_string(port);
    static const char * PORT = portToChar.c_str();

    mg_mgr_init(&mgr, NULL);
    std::cout << "Starting webserver on port " << PORT << std::endl;

    connection = mg_bind(&mgr, PORT, ev_handler);
    if (connection == NULL) {
        std::cout << "failed to create server" << std::endl;
        return 0;
    }

    mg_set_protocol_http_websocket(connection);

    // options
    s_http_server_opts.document_root = ".";
    s_http_server_opts.enable_directory_listing = "yes";

      signal(SIGTERM, signal_handler);
        signal(SIGINT, signal_handler);
  setvbuf(stdout, NULL, _IOLBF, 0);
  setvbuf(stderr, NULL, _IOLBF, 0);

    for (;;) {
        mg_mgr_poll(&mgr, 1000);
    }

    // free all memory
    mg_mgr_free(&mgr);

    return 1;
}

// // Event Handler
// static void ev_handler(struct mg_connection * connection, int e, void * p) {
//     printf("%d\n", e);
//     if (e == MG_EV_HTTP_REQUEST) {
//         mg_serve_http(connection, (struct http_message *) p, s_http_server_opts);
//     }
//     else if (e == MG_EV_WEBSOCKET_FRAME) {
//       struct websocket_message *wm = (struct websocket_message *) p;
//       /* New websocket message. Tell everybody. */
//       struct mg_str d = {(char *) wm->data, wm->size};
//       broadcast(connection, d);
//     } else if (e == MG_EV_WEBSOCKET_HANDSHAKE_DONE) {
//       /* New websocket connection. Tell everybody. */
//       broadcast(connection, mg_mk_str("++ joined"));
//     }
// }

static void ev_handler(struct mg_connection *nc, int ev, void *ev_data) {
  switch (ev) {
    case MG_EV_WEBSOCKET_HANDSHAKE_DONE: {
      /* New websocket connection. Tell everybody. */
      broadcast(nc, mg_mk_str("++ joined"));
      break;
    }
    case MG_EV_WEBSOCKET_FRAME: {
      struct websocket_message *wm = (struct websocket_message *) ev_data;
      /* New websocket message. Tell everybody. */
      struct mg_str d = {(char *) wm->data, wm->size};
      broadcast(nc, d);
      break;
    }
    case MG_EV_HTTP_REQUEST: {
      mg_serve_http(nc, (struct http_message *) ev_data, s_http_server_opts);
      break;
    }
    // case MG_EV_CLOSE: {
    //   /* Disconnect. Tell everybody. */
    //   if (is_websocket(nc)) {
    //     broadcast(nc, mg_mk_str("-- left"));
    //   }
    //   break;
    // }
  }
}

// broadcast message
static void broadcast(struct mg_connection *connection, const struct mg_str msg) {
  struct mg_connection *c;
  char buf[500];
  char addr[32];
  mg_sock_addr_to_str(&connection->sa, addr, sizeof(addr),
                      MG_SOCK_STRINGIFY_IP | MG_SOCK_STRINGIFY_PORT);

  snprintf(buf, sizeof(buf), "%s %.*s", addr, (int) msg.len, msg.p);
  printf("%s\n", buf); /* Local echo. */
  for (c = mg_next(connection->mgr, NULL); c != NULL; c = mg_next(connection->mgr, c)) {
    if (c == connection) continue; /* Don't send to the sender. */
    mg_send_websocket_frame(c, WEBSOCKET_OP_TEXT, buf, strlen(buf));
  }

}

  static void signal_handler(int sig_num) {
  signal(sig_num, signal_handler);  // Reinstantiate signal handler
}

