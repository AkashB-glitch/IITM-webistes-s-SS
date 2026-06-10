import json
import socket
from concurrent.futures import ThreadPoolExecutor

# Common ports
PORTS = [21, 22, 25, 53, 80, 110, 143, 443, 587, 993, 995, 3306, 8080]

results = []

def resolve_domain(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return None

def check_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.2)  # Faster timeout
        result = sock.connect_ex((ip, port))
        sock.close()

        if result == 0:
            return port

    except:
        pass

    return None

# Load targets
with open("targets.json", "r") as f:
    data = json.load(f)

for domain in data["targets"]:

    print(f"\n[*] Resolving {domain}...")

    ip = resolve_domain(domain)

    if not ip:
        print(f"[!] Cannot resolve {domain}")

        results.append({
            "domain": domain,
            "status": "unresolved"
        })

        continue

    print(f"[+] {domain} -> {ip}")

    open_ports = []

    # Multithreaded port checks
    with ThreadPoolExecutor(max_workers=50) as executor:

        futures = [executor.submit(check_port, ip, port) for port in PORTS]

        for future in futures:
            port = future.result()

            if port:
                print(f"    OPEN: {port}")
                open_ports.append(port)

    results.append({
        "domain": domain,
        "ip": ip,
        "open_ports": open_ports
    })

# Save results
with open("results.json", "w") as f:
    json.dump(results, f, indent=4)

print("\n[+] Scan completed")
print("[+] Results saved to results.json")