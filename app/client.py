import grpc

from grpc_out import demo_pb2
from grpc_out import demo_pb2_grpc


# Implement methods from proto file

def get_none_unary(stub):
    """Get none from servise with unary-unary method"""

    response = stub.GetNoneUnary(demo_pb2.GetNone())
    print("\nGetNone method response: ", response)


def get_user_unary(stub):
    """Get user data from service with unary-unary method"""

    # Create request by use request model from proto file
    id = input("\nEnter user id for request (fake db have only 5 users): ")
    request = demo_pb2.GetUserRequest(user_id=int(id))

    # Get response from service by use method from proto file
    response = stub.GetUserUnary(request)

    # Print response
    print("\nGetUserUnary method response:\n")
    print(f'user id: {response.user_id}')
    print(f'user name: {response.user_name}')
    print(f'user email: {response.user_email}')
    print(f'user roles: {response.user_roles}')
    print(f'user status: {response.user_status}')
    print('\n')


def get_user_client_stream(stub):
    """Get user data from service with stream-unary method"""

    # Create generator for stream request
    def get_request():
        for i in range(1, 6):  # fake db have only 5 users
            request = demo_pb2.GetUserRequest(user_id=i)
            yield request

    # Get response from service with unary format
    response = stub.GetUserClientStream(get_request())

    print("\nGetUserClientStream method response:\n")
    print(f'user id: {response.user_id}')
    print(f'user name: {response.user_name}')
    print(f'user email: {response.user_email}')
    print(f'user roles: {response.user_roles}')
    print(f'user status: {response.user_status}')

    print("\nAs you can see, by sending 5 user IDs, we only received data for the last one.")


def get_user_server_stream(stub):
    """Get users data from service with unary-stream method"""

    # Create request by use request model from proto file
    id = input("\nEnter user id for request (fake db have only 5 users): ")
    request = demo_pb2.GetUserRequest(user_id=int(id))

    # Get response iterator from service
    response_iterator = stub.GetUserServerStream(request)

    # Print response data by itrate over response iterator
    print("\nGetUserServerStream method response:\n")
    for response in response_iterator:
        print(f'user id: {response.user_id}')
        print(f'user name: {response.user_name}')
        print(f'user email: {response.user_email}')
        print(f'user roles: {response.user_roles}')
        print(f'user status: {response.user_status}')
        print('\n')

    print("As you can see, by sending 1 user ID, we received all users data")


def get_user_bidirectional(stub):
    """Get users data from service with stream-stream method"""

    # Create generator for stream request
    def get_request():
        for i in range(1, 6):  # fake db have only 5 users
            request = demo_pb2.GetUserRequest(user_id=i)
            yield request

    # Get response iterator from service
    response_iterator = stub.GetUserBidirectional(get_request())

    # Print response data by itrate over response iterator
    print("\nGetUserBidirectional method response:\n")
    for response in response_iterator:
        print(f'user id: {response.user_id}')
        print(f'user name: {response.user_name}')
        print(f'user email: {response.user_email}')
        print(f'user roles: {response.user_roles}')
        print(f'user status: {response.user_status}')
        print('\n')

    print("As you can see, by sending 5 user ids, we received all users data")


def main():
    # Create connection with service
    with grpc.insecure_channel("localhost:23333") as channel:
        stub = demo_pb2_grpc.UsersStub(channel)

        get_none_unary(stub)
        get_user_unary(stub)
        get_user_client_stream(stub)
        get_user_server_stream(stub)
        get_user_bidirectional(stub)


if __name__ == "__main__":
    main()
