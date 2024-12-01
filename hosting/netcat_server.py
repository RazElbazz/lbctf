import socket
import subprocess
import threading
import os
import random
import string


def handle_client(client_socket, executable, flag):
    try:
        # Start the executable as a subprocess, capturing both stdout and stderr
        process = subprocess.Popen(executable, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Read the output of the executable and send it to the client
        def send_output():
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output == 'win\n':
                    print(flag)
                    client_socket.sendall(flag.encode('utf-8'))
                    client_socket.close()
                    break
                if output:
                    try:
                        client_socket.sendall(output.encode('utf-8'))
                    except BrokenPipeError:
                        print("Client disconnected while sending output.")
                        break

        # Read the error output and send it to the client (if any)
        def send_error_output():
            while True:
                error_output = process.stderr.readline()
                if error_output == '' and process.poll() is not None:
                    break
                if error_output:
                    try:
                        client_socket.sendall(error_output.encode('utf-8'))
                    except BrokenPipeError:
                        print("Client disconnected while sending error output.")
                        break

        # Start the threads for sending output and error output
        threading.Thread(target=send_output, daemon=True).start()
        threading.Thread(target=send_error_output, daemon=True).start()

        # Now, wait for the client's input and send it to the executable
        while True:
            client_input = client_socket.recv(1024).decode('utf-8')
            if client_input == 'exit' or not client_input:
                break
            try:
                process.stdin.write(client_input)  # Send input to the executable
                process.stdin.flush()  # Ensure it's sent immediately
            except BrokenPipeError:
                print("The executable process has terminated unexpectedly.")
                break

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()



def start_server(challenge, host='0.0.0.0', port=5000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        # Start a new thread to handle the client's interaction with the executable
        threading.Thread(target=handle_client, args=(client_socket, challenge + "prog.exe", open(challenge + "flag").read().replace('^', random.choice(string.ascii_letters)) + "\n"), daemon=True).start()

if __name__ == "__main__":

    challenge_id = 1

    # Replace 'your_executable.exe' with the path to the executable you want to run
    start_server(challenge=f'../levels/binary_exploitation/{challenge_id}/')
