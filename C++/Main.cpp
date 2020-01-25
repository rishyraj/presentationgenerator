#include "mongoose.h"
#include <string>
#include <iostream>
#include <stdio.h>

// http struct
static struct mg_serve_http_opts s_http_server_opts;
static void ev_handler(struct mg_connection * connection, int e, void * p);
int InitServer(int port);

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

    for (;;) {
        mg_mgr_poll(&mgr, 1000);
    }

    // free all memory
    mg_mgr_free(&mgr);

    return 1;
}

// Event Handler
static void ev_handler(struct mg_connection * connection, int e, void * p) {
    if (e == MG_EV_HTTP_REQUEST) {
        mg_serve_http(connection, (struct http_message *) p, s_http_server_opts);
    }
}

