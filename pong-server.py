from ping_pong_pb2_grpc import (
    PingPongGuideServicer,
    add_PingPongGuideServicer_to_server,
)
import ping_pong_pb2
import grpc
from concurrent.futures import ThreadPoolExecutor
import logging


class PongServer(PingPongGuideServicer):
    def generate_pong(self, number: int, pong_string: str):
        return ping_pong_pb2.Pong(number=number, pong_string=pong_string)

    def GetPingPong(self, request, context):
        """
        Recieves: Ping
        Sends: Pong
        """
        generate_pong_obj = self.generate_pong(
            number=10, pong_string=f"{request.ping_string}-pong"
        )
        return generate_pong_obj

    def ServerStreamPingPong(self, request, context):
        """
        Recieves: Ping
        Sends: Pong, Pong, Pong....
        """
        logging.info(f"Recieved: {request.ping_string}")
        while True:
            pong = self.generate_pong(number=2, pong_string="Server plays pong")
            yield pong


    def ClientStreamPingPong(self, request_iterator, context):
        """
        Recieves: Ping, Ping, Ping, Ping
        Sends: Pong
        """
        count = 0
        for request in request_iterator:
            logging.info(f"Recived request {count} with message {request.ping_string}")
            count += 1

        generate_pong_obj = self.generate_pong(
            number=10, pong_string=f"All pings recieved successfully!"
        )
        return generate_pong_obj

    def BiDirectionalAllPingsThenPong(self, request_iterator, context):
        """
        Recieves: (Ping-1, 1), (Ping-2, 3), (Ping-3, 3), (Ping-4, 4)
        Sends: Ping-2, Ping-3 because 3=3. 
        """
        prev_pings = []
        for ping_object in request_iterator:
            ping_object_number, ping_object_string = (
                ping_object.number,
                ping_object.ping_string,
            )
            for prev_ping in prev_pings:
                prev_ping_object_number, prev_ping_object_string = (
                    prev_ping.number,
                    prev_ping.ping_string,
                )
                if prev_ping_object_number == ping_object_number:
                    generate_pong_obj = self.generate_pong(
                        number=200,
                        pong_string=f"{prev_ping_object_string} and {ping_object_string} have the same numbers!",
                    )
                    yield generate_pong_obj
            prev_pings.append(ping_object)

    def BiDirectionalGetContinuesPingPong(self, request_iterator, context):
        """
        Recieves: Ping, Ping, Ping...
        Sends: Pong, Pong, Pong...
        """
        while True:
            request_object = next(request_iterator)
            pong = self.generate_pong(
                number=2,
                pong_string=f"{request_object.ping_string} <-> Server plays pong",
            )
            yield pong


def serve(address: str) -> None:
    server = grpc.server(ThreadPoolExecutor())
    add_PingPongGuideServicer_to_server(PongServer(), server)
    server.add_insecure_port(address)
    server.start()
    logging.info("Server serving at %s", address)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve("localhost:50051")
