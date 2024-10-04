import grpc
from concurrent import futures

from sys import argv
from grpc_out import demo_pb2_grpc
from grpc_out import demo_pb2


fake_users_db = {
    1: ("cassidy", "company@gmail.com", "admin", "active"),
    2: ('bob', 'bob@gmail.com', 'user', 'active'),
    3: ('john', 'john@gmail.com', 'user', 'active'),
    4: ('petr', 'petr@gmail.com', 'user', 'active'),
    5: ('mary', 'mary@gmail.com', 'user', 'active'),
}


class UsersService(demo_pb2_grpc.UsersServicer):
    """Get users with variety of gRPC methods"""

    # Implement methods from proto file

    def GetNoneUnary(self, request, context):
        """Get none from client with unary-unary method"""

        print("\nGetNone method request: ", request)
        return demo_pb2.GetNone()

    def GetUserUnary(self, request, context):
        """Get user data from client ith unary-unary method"""

        print("\nGetUserUnary method request: ", request)

        # Create response by use response model from proto file
        response = demo_pb2.GetUserResponse(
            user_id=request.user_id,
            user_name=fake_users_db[request.user_id][0],
            user_email=fake_users_db[request.user_id][1],
            user_roles=fake_users_db[request.user_id][2],
            user_status=fake_users_db[request.user_id][3]
        )

        return response  # Return response to the service

    def GetUserClientStream(self, request_iterator, context):
        """Get user data from client with stream-unary method"""

        # Get requset iterator from client and print request data
        print('\n')
        for request in request_iterator:
            print("GetUserClientStream method request: ", request)

        # Create response by use response model from proto file
        response = demo_pb2.GetUserResponse(
            user_id=request.user_id,
            user_name=fake_users_db[request.user_id][0],
            user_email=fake_users_db[request.user_id][1],
            user_roles=fake_users_db[request.user_id][2],
            user_status=fake_users_db[request.user_id][3]
        )

        return response  # Return response to the service

    def GetUserServerStream(self, request, context):
        """Get user data from client with unary-stream method"""

        print("\nGetUserServerStream method request:: ", request)

        # Create generator for stream response
        def get_response():
            for i in range(1, len(fake_users_db)+1):
                response = demo_pb2.GetUserResponse(
                    user_id=i,
                    user_name=fake_users_db[i][0],
                    user_email=fake_users_db[i][1],
                    user_roles=fake_users_db[i][2],
                    user_status=fake_users_db[i][3]
                )

                yield response

        return get_response()  # Return response iterator to client

    def GetUserBidirectional(self, request_iterator, context):
        """Get users data from client with stream-stream method"""

        # Also, you can do simple like this (iterate over requests and yield response immediately):
        # for request in request_iterator:
        #     yield demo_pb2.GetUserResponse(
        #         user_id=request.user_id,
        #         user_name=fake_users_db[request.user_id][0],
        #         user_email=fake_users_db[request.user_id][1],
        #         user_roles=fake_users_db[request.user_id][2],
        #         user_status=fake_users_db[request.user_id][3]
        #     )

        # Method below is slower. Fist you received all request data and then prepare response

        # Get requset iterator from client and fill client_id list
        users_id = list()
        print('\n')
        for request in request_iterator:
            print("GetUserClientStream method request: ", request)
            users_id.append(request.user_id)

        # Create generator for stream response
        def get_response():
            for id in users_id:
                yield demo_pb2.GetUserResponse(
                    user_id=id,
                    user_name=fake_users_db[id][0],
                    user_email=fake_users_db[id][1],
                    user_roles=fake_users_db[id][2],
                    user_status=fake_users_db[id][3]
                )

        return get_response()  # Return response iterator to client


def start_insecure_server(server_addr: str):
    server = grpc.server(futures.ThreadPoolExecutor())
    demo_pb2_grpc.add_UsersServicer_to_server(UsersService(), server)
    server.add_insecure_port(server_addr)

    try:
        print(f"Server started on {server_addr} without encryption")
        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        pass


def start_secure_server(server_addr: str):
    server = grpc.server(futures.ThreadPoolExecutor())
    demo_pb2_grpc.add_UsersServicer_to_server(UsersService(), server)
    server.add_secure_port(server_addr, server_credentials=grpc.alts_server_credentials())

    try:
        print(f"Server started on {server_addr} with ALTS encryption")
        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    SERVER_HOST = 'localhost'
    SERVER_PORT = '23333'

    if len(argv) > 1 and argv[1] == '--alts':
        start_secure_server(SERVER_HOST + ':' + SERVER_PORT)
    else:
        start_insecure_server(SERVER_HOST + ':' + SERVER_PORT)
