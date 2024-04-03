import tkinter as tk
from tkinter import scrolledtext
import socket
import threading
import webbrowser
import netifaces

def start_proxy_chain_gui():
    window = tk.Tk()
    window.title("Proxy Chain Tool")

    label = tk.Label(window, text="Enter Proxies (host:port, host:port, ...)")
    label.pack()

    proxies_text = tk.Text(window, width=50, height=10)
    placeholder_text = "Example: 189.240.60.171:9090, 189.240.60.166:9090, 179.50.90.166:8515"
    proxies_text.insert(tk.END, placeholder_text)
    proxies_text.pack()

    urls_label = tk.Label(window, text="Enter URLs (one per line)")
    urls_label.pack()

    urls_text = tk.Text(window, width=50, height=10)
    urls_text.pack()

    log_area = scrolledtext.ScrolledText(window, width=70, height=20)
    log_area.pack()

    start_button = tk.Button(window, text="Start Proxy Chain", command=lambda: start_proxy_chain_from_gui(proxies_text, urls_text, log_area))
    start_button.pack()

    window.mainloop()

def start_proxy_chain_from_gui(proxies_text, urls_text, log_area):
    proxies = proxies_text.get("1.0", "end-1c").strip()

    if proxies == "":
        log_area.insert(tk.END, "Please enter proxies.\n")
        return

    urls = urls_text.get("1.0", "end-1c").strip().splitlines()
    if not urls:
        log_area.insert(tk.END, "Please enter URLs.\n")
        return

    # Split the input proxies by comma and remove any leading/trailing spaces
    proxy_list = [proxy.strip() for proxy in proxies.split(",")]

    log_area.insert(tk.END, "Proxy chain processing started.\n")

    # Start the proxy chain process in a new thread for each URL
    for url in urls:
        proxy_thread = threading.Thread(target=process_proxy_chain_request, args=(url, proxy_list, log_area))
        proxy_thread.start()

def process_proxy_chain_request(url, proxy_list, log_area):
    try:
        # Open a web browser for each URL
        webbrowser.open_new_tab(url)

        # Simulate sending a request through the proxy chain (replace with actual request code)
        log_area.insert(tk.END, f"Sending request to {url} through proxy chain...\n")
        # You can add your request logic here using the proxy_list

    except Exception as e:
        log_area.insert(tk.END, f'Error: {e}\n')


def change_ip_addresses(interface_name, new_ipv4=None, new_ipv6=None):
    interfaces = netifaces.interfaces()
    if interface_name not in interfaces:
        print(f"Error: Interface '{interface_name}' not found.")
        return

    # Get the addresses currently assigned to the interface
    addresses = netifaces.ifaddresses(interface_name)

    if netifaces.AF_INET in addresses and new_ipv4:
        # Change IPv4 address
        old_ipv4 = addresses[netifaces.AF_INET][0]['addr']
        print(f"Changing IPv4 address from {old_ipv4} to {new_ipv4}")
        netifaces.ifaddresses(interface_name)[netifaces.AF_INET][0]['addr'] = new_ipv4

    if netifaces.AF_INET6 in addresses and new_ipv6:
        # Change IPv6 address
        old_ipv6 = addresses[netifaces.AF_INET6][0]['addr']
        print(f"Changing IPv6 address from {old_ipv6} to {new_ipv6}")
        netifaces.ifaddresses(interface_name)[netifaces.AF_INET6][0]['addr'] = new_ipv6

    print("IP addresses changed successfully.")


# Example usage:
# Change IPv4 and/or IPv6 addresses for the 'eth0' interface
change_ip_addresses('eth0', new_ipv4='192.168.1.100', new_ipv6='2001:db8::1')

if __name__ == '__main__':
    start_proxy_chain_gui()
