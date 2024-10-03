<h1 align="center">gRPC Tutorial Hell</h1>

<p align="center">
    <!-- <img src="https://img.shields.io/badge/%20Python-3.11.3-blue?style=for-the-badge&logo=Python" alt="Python">
    <img src="https://img.shields.io/badge/%20SQLAlchemy-2.0.35-brightgreen?style=for-the-badge" alt="SQLAlchemy">
    <img src="https://img.shields.io/badge/%20FastAPI-0.114.2-brightgreen?style=for-the-badge" alt="FastAPI">
    <img src="https://img.shields.io/badge/pytest-8.3.3-brightgreen?style=for-the-badge" alt="Pyetst">
    <img src="https://img.shields.io/badge/pytest_asyncio-0.24.0-brightgreen?style=for-the-badge" alt="pytest_asyncio"> -->
</p>

<p align="center">
    <img src="https://img.shields.io/github/downloads/peymone/grpc-hell/total?style=social&logo=github" alt="downloads">
    <img src="https://img.shields.io/github/watchers/peymone/grpc-hell" alt="watchers">
    <img src="https://img.shields.io/github/stars/peymone/grpc-hell" alt="stars">
</p>


<h1>Why do I need this gRPC?</h1>

**_Well, gRPC client can call server method directly from it. It's lightweight, support streaming, encryption and variety of authentications. And, many companies wants it, because cool. I think there are enough reasons._**

**_The examples of services presented here are completely meaningless, but are useful for understanding the protocol. So, we have:_**

- **_something (currently not imlemented)_**
- **_Unary RPC (client sends a single request and gets back a single response)_**


<h2>How to setup this gRPC thingy?</h2>

**_It's just common tutorial how to work with protocol_**

1. *_Install gRPC dependencies for protocol usage_*
    - _Install gRPC:_ ```pip install grpcio (gRPC)```
    - _Install proto buffer compiler:_ ```pip install grpcio-tools```
2. _Create .proto file somewhere and describe it (example below)_
    
```
syntax = "proto3"; // Version of syntax used py protocol
package demo; // Package name definition, which can be omitted in Python


// `message` is used to define the structure of the data to be transmitted

message Request {
    int64 client_id = 1;
    string request_data = 2;
}

message Response {
    int64 server_id = 1;
    string response_data = 2;
}

// `service` is used to define methods for gRPC services in a fixed format


service GRPCDemo {

    // unary-unary (In a single call, the client can only send request once, and the server can
    // only respond once.)

    rpc SimpleMethod (Request) returns (Response);

    // stream-unary (In a single call, the client can transfer data to the server several times,
    // but the server can only return a response once.)

    rpc ClientStreamingMethod (stream Request) returns (Response);

    // unary-stream (In a single call, the client can only transmit data to the server at one time,
    // but the server can return the response many times.)

    rpc ServerStreamingMethod (Request) returns (stream Response);

    // stream-stream (In a single call, both client and server can send and receive data
    // to each other multiple times.)
    
    rpc BidirectionalStreamingMethod (stream Request) returns (stream Response);
}

```
_You can find more information about .proto building here: <a href=https://protobuf.dev/programming-guides/proto>gRPC guide</a>_<br/>
_Or basic tutorial for python here: <a href=https://grpc.io/docs/languages/python/basics/>Basic Tutorial</a>_

3. _Next you need to generate the gRPC client and server interfaces_
    - Code: ```python -m grpc_tools.protoc --proto_path=./protos unary.proto --python_out=./grpc_out --grpc_python_out=./grpc_out```
    - _Oh, make a coffee_
4. _Cool, now, let's go implement your service and client_

**_P.S. the generated file `*_pb2_grpc.py` almost always has problems with importing `*_pb2.py` file._**


<h2>Where do I need to use this?</h2>

_Somewhere... Put something here_

