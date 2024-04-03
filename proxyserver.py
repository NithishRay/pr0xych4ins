import tkinter as tk
from tkinter import scrolledtext, messagebox
import socket
import threading
import webbrowser
import requests
import time

class ProxyChainTool:
    def __init__(self, master):
        self.master = master
        master.title("Proxy Chain Tool")

        # Variables
        self.proxies = tk.StringVar()
        self.proxy_list = []
        self.rotate_proxies = tk.BooleanVar()
        self.rotate_proxies.set(False)

        # GUI Elements
        self.label = tk.Label(master, text="Enter Proxies (host:port, host:port, ...)")
        self.label.pack()

        self.proxies_text = tk.Text(master, width=50, height=10)
        placeholder_text = "Example: 189.240.60.171:9090, 189.240.60.166:9090, 179.50.90.166:8515"
        self.proxies_text.insert(tk.END, placeholder_text)
        self.proxies_text.pack()

        self.rotate_check = tk.Checkbutton(master, text="Rotate Proxies", variable=self.rotate_proxies)
        self.rotate_check.pack()

        self.log_area = scrolledtext.ScrolledText(master, width=70, height=20)
        self.log_area.pack()

        self.start_button = tk.Button(master, text="Start Proxy Chain", command=self.start_proxy_chain)
        self.start_button.pack()

        self.send_request_button = tk.Button(master, text="Send Request", command=self.send_sample_request)
        self.send_request_button.pack()

    def start_proxy_chain(self):
        proxies_input = self.proxies_text.get("1.0", tk.END).strip()
        self.proxies.set(proxies_input)

        if not self.proxies.get():
            messagebox.showerror("Error", "Please enter proxies.")
            return

        self.proxy_list = [proxy.strip() for proxy in self.proxies.get().split(",")]

        self.log_area.insert(tk.END, "Proxy chain processing started.\n")
        threading.Thread(target=self.process_proxies).start()

    def process_proxies(self):
        proxy_index = 0
        rotate_proxies = self.rotate_proxies.get()

        while True:
            proxy = self.proxy_list[proxy_index]
            proxy_index = (proxy_index + 1) % len(self.proxy_list) if rotate_proxies else proxy_index

            try:
                host, port = proxy.split(":")
                proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                proxy_socket.connect((host, int(port)))

                self.log_area.insert(tk.END, f"Proxy: {proxy} - Connection Successful\n")

            except Exception as e:
                self.log_area.insert(tk.END, f'Error: {e}\n')

            finally:
                proxy_socket.close()

            # Sleep for demonstration purposes (replace with actual request interval)
            time.sleep(2)

    def send_sample_request(self):
        # Check if proxies are set
        if not self.proxy_list:
            messagebox.showerror("Error", "Please start the proxy chain first.")
            return

        # Send a sample request using the first proxy in the list
        proxy = self.proxy_list[0]
        try:
            # Use the requests library to send an HTTP GET request through the proxy
            response = requests.get('https://www.google.com', proxies={'http': f'http://{proxy}'})
            self.log_area.insert(tk.END, f"Request sent through Proxy: {proxy}\n")
            self.log_area.insert(tk.END, f"Response: {response.text}\n")
        except Exception as e:
            self.log_area.insert(tk.END, f'Error sending request through Proxy: {proxy} - {str(e)}\n')

if __name__ == '__main__':
    root = tk.Tk()
    app = ProxyChainTool(root)
    root.mainloop()
