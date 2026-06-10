import json
import socket
from concurrent.futures import ThreadPoolExecutor
import os

# Common web ports to check
PORTS = [80, 443, 8080, 8443, 22, 21, 3306]

def check_port(domain, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((domain, port))
        sock.close()
        if result == 0:
            return port
    except Exception:
        pass
    return None

def scan_domain(domain):
    print(f"Scanning {domain}...")
    open_ports = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_port, domain, p): p for p in PORTS}
        for future in futures:
            res = future.result()
            if res:
                open_ports.append(res)
    return {"domain": domain, "open_ports": sorted(open_ports)}

def main():
    with open("iitm_urls.txt", "r") as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]
    
    domains = [u.replace("https://", "").replace("http://", "").split("/")[0] for u in urls]
    
    print(f"Starting port scan for {len(domains)} domains...")
    results = []
    
    # Use ThreadPoolExecutor to scan multiple domains concurrently
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(scan_domain, domain) for domain in domains]
        for future in futures:
            try:
                res = future.result()
                results.append(res)
            except Exception as e:
                pass

    with open("results.json", "w") as f:
        json.dump(results, f, indent=4)
    print("Scan complete! Saved to results.json")

if __name__ == "__main__":
    main()
