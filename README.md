# Ping-Pong Demonstration with gRPC and Protobuf

# What is gRPC?

gRPC is an Remote Procedure Call System. It is particularly useful for micro-services based
archietecture platforms. Suppose we have multiple micro services implemented in different languages
like C++, Python, NodeJS, and multiple clients implemented in Android-java, Ruby, React-Javascript. Then gRPC will ease the service-client communication by transfering messages through Google's ```language and platform neutral serialized data structure``` called Protobuf. Since gRPC uses protobuf to communicate between the client and services, it is also efficient in comparison with communication through JSON or XML because protobuf allows its data to be serialized and deserialized when needed.

# Project
This project will demonstrate 4 types of RPC called the Unary RPC, 
Server-streaming rpc, Client-streaming rpc, and Bidirectional streaming rpc.

These RPC calls have been designed to accomodate client-server communication 
through various design paradigms as listed below.

1.  Unary RPC: Client calls the server method through the stub object,
    and in my ```ping-client.py```, the stub method will be ```stub.GetPingPong```.
    Once stub method is called, the server will be notified of the function call from the client
    and the server will send a response.

2. Server-streaming rpc: A server-streaming RPC is similar to a unary RPC, except that the server returns a stream of messages in response to a client’s request. In our example, the client will
send a single ping, and th server will return return a stream of pongs.

3. A client-streaming RPC is similar to a unary RPC, except that the client sends a stream of messages to the server instead of a single message.  In our example, the client will
send a stream of pings, and the server will return return a pong after all pings have been recieved.
It doesn't have to be after all pings, but that decision is application-specific.

4. In a bidirectional streaming RPC, the call is initiated by the client sending a stream of pings
and the server responding with a stream of pongs. Since the streams are mutually exclusive, the order
of ping-pong will be application specific. For that reason, I created two methods to demonstrate 
bidirectional streaming rpc, where the first method ```bidirectional_all_ping_then_pong``` sends a bunch of pings first and then the server will respond with a bunch of pongs after all pings have been recieved by the server. However, in ```bidirectional_continues_ping_pong``` the client-server communicates continuesly meaning the server and client can play “ping-pong” – the server gets a request, then sends back a response, then the client sends another request based on the response, and so on.

# Things to TODO

1. Im currently doing the client-server communication insecurly. So I want to add the SSL Encryption
to the client and server streams. API Reference: https://grpc.io/docs/guides/auth/
2. I also want to implement a API Gateway that will perform protocol transcoding where a HTTPS 
communication protocal can be converted to a GRPC protocal. This will be particularly useful when using GRPC with REST API.


