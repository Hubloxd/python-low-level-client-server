import asyncio
from asyncio import StreamReader, StreamWriter
from socket import socket
from utils import load_database, write_database, login_check_database, write_session_id

HOST = "localhost"
PORT = 50009
DATABASE = load_database()


async def handle_client(reader: StreamReader, writer: StreamWriter):
    async def register_user() -> None:
        writer.write("Username:".encode("utf8"))
        await writer.drain()
        user = await get_request()

        writer.write("Password:".encode("utf8"))
        await writer.drain()
        password = await get_request()

        writer.write("Confirm password:".encode("utf8"))
        await writer.drain()
        confirm_passwd = (await reader.read(2048)).strip()

        if password == confirm_passwd:
            write_database(user, password)
            writer.write("You are an registered user now!".encode("utf8"))
            await writer.drain()
        else:
            writer.write("Passwords do not match:".encode("utf8"))
            await writer.drain()

    async def get_request() -> str:
        try:
            d = (await reader.read(4096)).decode("utf8").strip()
            if not d:
                writer.close()
            return d
        except ConnectionError as exc:
            raise exc

    try:
        info: socket = writer.get_extra_info("socket")
        print(f"connection from {info.getpeername()}")
        while True:
            request = await get_request()
            print(request)

            match request.lower():
                case "_exit_":
                    response = "goodbye :)"
                    writer.write(response.encode("utf8"))
                    await writer.drain()
                    writer.close()
                case "_register_":
                    await register_user()
                    continue
                case "_login_":
                    try:
                        writer.write("Username:".encode("utf8"))
                        await writer.drain()
                        username = await get_request()

                        writer.write("Password:".encode("utf8"))
                        await writer.drain()
                        passwd = await get_request()
                    except ConnectionError as e:
                        print(e)
                        return
                    if login_check_database(username, passwd):
                        response = write_session_id(username)

                    else:
                        response = "_false_"

                case "_ping_":
                    response = "pong"
                case _:
                    response = request
            writer.write(response.encode("utf8"))
            await writer.drain()

    except ConnectionError as e:
        print(e)
    except KeyboardInterrupt:
        exit(0)


async def start_server():
    server = await asyncio.start_server(handle_client, host=HOST, port=PORT)
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(start_server(), debug=True)
