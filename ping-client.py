import grpc
import ping_pong_pb2_grpc
import ping_pong_pb2
import logging


def generate_ping(number: int, ping_string: str):
    return ping_pong_pb2.Ping(number=number, ping_string=ping_string)


def multi_ping():
    """
    Finite generator that yields an instance of Ping
    """
    messages = [
        generate_ping(number=1, ping_string="Ping-1"),
        generate_ping(number=3, ping_string="Ping-2"),
        generate_ping(number=3, ping_string="Ping-3"),
        generate_ping(number=4, ping_string="Ping-4"),
    ]
    for message in messages:
        logging.info(
            f"Sending: number {message.number} and message {message.ping_string}"
        )
        yield message


def infinite_ping():
    while True:
        ping_obj = generate_ping(number=1, ping_string="Client plays ping")
        logging.info(f"Sending: {ping_obj.ping_string}")
        yield ping_obj


def single_ping():
    ping_obj = generate_ping(number=1, ping_string="Client plays single ping")
    return ping_obj


def unary_ping_pong(stub: ping_pong_pb2_grpc.PingPongGuideStub):
    """
    Send a single ping and recieve a single pong
    """
    ping_obj = generate_ping(number=10, ping_string="ping")
    response = stub.GetPingPong(ping_obj)
    logging.info("Receiving: " + response.pong_string)


def server_stream_ping_pong(stub: ping_pong_pb2_grpc.PingPongGuideStub):
    """
        Send a single ping, then server will send multipe pongs.
    """
    single_ping_req = single_ping()
    response_generator = stub.ServerStreamPingPong(
        single_ping_req
    )  # Recieves back a generator as a response from server
    for response in response_generator:
        logging.info(
            response.pong_string
        )  # Server will yield two strings: "Client plays ping!" and "Server plays pong!"


def client_stream_ping_pong(stub: ping_pong_pb2_grpc.PingPongGuideStub):
    """
    Send all pings to the client first, then server will send a single success message of all pongs recieved.
    """
    multi_ping_pong = multi_ping()
    single_response = stub.ClientStreamPingPong(multi_ping_pong)
    logging.info(single_response.pong_string)


def bidirectional_all_ping_then_pong(stub: ping_pong_pb2_grpc.PingPongGuideStub):
    """
    Send all pings from client first, then server will send all of its pongs.
    """
    multi_ping_obj = multi_ping()
    response_generator = stub.BiDirectionalAllPingsThenPong(multi_ping_obj)

    for responses in response_generator:
        logging.info(f"Receiving: {responses.pong_string}")


def bidirectional_continues_ping_pong(stub: ping_pong_pb2_grpc.PingPongGuideStub):
    """
    Client and Server play Ping-Pong Simultaneuously
    """
    request_ping_pong_generator_obj = (
        infinite_ping()
    )  # This is a generator that will be sent as a request to server with the message "Client plays ping!"
    responses = stub.BiDirectionalGetContinuesPingPong(
        request_ping_pong_generator_obj
    )  # The request will be a generator that will generate infinite pings

    for response in responses:
        logging.info(response.pong_string)  # Play all server messages


def run():
    logging.info("Starting client...")
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = ping_pong_pb2_grpc.PingPongGuideStub(channel)
        # unary_ping_pong(stub)
        # client_stream_ping_pong(stub)
        # server_stream_ping_pong(stub)
        # bidirectional_all_ping_then_pong(stub)
        # bidirectional_continues_ping_pong(stub)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run()
