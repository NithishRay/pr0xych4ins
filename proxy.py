import tkinter as tk
from tkinter import scrolledtext
import socket
import threading
import webbrowser

def start_proxy_chain_gui():
    window = tk.Tk()
    window.title("Proxy Chain Tool")

    label = tk.Label(window, text="Enter Proxies (host:port, host:port, ...)")
    label.pack()

    proxies_text = tk.Text(window, width=50, height=10)
    placeholder_text = "Example: 189.240.60.171:9090, 189.240.60.166:9090, 179.50.90.166:8515"
    proxies_text.insert(tk.END, placeholder_text)
    proxies_text.pack()

    log_area = scrolledtext.ScrolledText(window, width=70, height=20)
    log_area.pack()

    start_button = tk.Button(window, text="Start Proxy Chain", command=lambda: start_proxy_chain_from_gui(proxies_text, log_area))
    start_button.pack()

    window.mainloop()

def start_proxy_chain_from_gui(proxies_text, log_area):
    proxies = proxies_text.get("1.0", "end-1c").strip()

    if proxies == "":
        log_area.insert(tk.END, "Please enter proxies.\n")
        return

    # Split the input proxies by comma and remove any leading/trailing spaces
    proxy_list = [proxy.strip() for proxy in proxies.split(",")]

    log_area.insert(tk.END, "Proxy chain processing started.\n")

    # Start the proxy chain process in a new thread
    proxy_thread = threading.Thread(target=process_proxies, args=(proxy_list, log_area))
    proxy_thread.start()

def process_proxies(proxy_list, log_area):
    # Initialize the proxy chain server
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind(('127.0.0.1', 8888))
    proxy_socket.listen(5)
    log_area.insert(tk.END, 'Proxy chain server is running on 127.0.0.1:8888\n')

    # Open a web browser when the proxy chain server starts
    webbrowser.open_new_tab('https://whatismyipaddress.com/')

    while True:
        client_socket, client_address = proxy_socket.accept()
        log_area.insert(tk.END, f'Accepted connection from {client_address}\n')
        proxy_thread = threading.Thread(target=handle_client, args=(client_socket, 0, proxy_list, log_area))
        proxy_thread.start()

def handle_client(client_socket, proxy_index, proxy_list, log_area):
    proxy = proxy_list[proxy_index]

    try:
        host, port = proxy.split(":")
        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_socket.connect((host, int(port)))

        request_data = client_socket.recv(4096)
        proxy_socket.sendall(request_data)

        response = b''
        while True:
            part = proxy_socket.recv(4096)
            if not part:
                break
            response += part

        client_socket.sendall(response)
        log_area.insert(tk.END, 'Request successfully proxied\n')

    except Exception as e:
        log_area.insert(tk.END, f'Error: {e}\n')

    finally:
        proxy_socket.close()
        client_socket.close()

if __name__ == '__main__':
    start_proxy_chain_gui()