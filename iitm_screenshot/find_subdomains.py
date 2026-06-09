import requests
import json
import sys

def discover_iitm_sites():
    target_domain = "iitm.ac.in"
    # flush=True forces the terminal to print this out immediately
    print(f"🔍 Step 1: Connecting to public certificate database for {target_domain}...", flush=True)
    
    # We use hackertarget's API as a highly reliable alternative/backup
    url = f"https://api.hackertarget.com/hostsearch/?q={target_domain}"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200 or "error" in response.text.lower():
            print("⚠️ Primary API failed or throttled. Trying backup registry (this might take 30s)...", flush=True)
            # Backup: crt.sh JSON endpoint
            backup_url = f"https://crt.sh/?q=%.{target_domain}&output=json"
            response = requests.get(backup_url, timeout=25)
            
            if response.status_code != 200:
                print("❌ Both discovery APIs are timing out. Let's seed with primary known domains instead.", flush=True)
                use_fallback_list()
                return
            
            # Parse crt.sh format
            data = response.json()
            subdomains = {item['name_value'].lower() for item in data if "\n" not in item['name_value']}
        else:
            # Parse hackertarget format (comma-separated entries)
            lines = response.text.strip().split("\n")
            subdomains = {line.split(",")[0].lower() for line in lines if line}

        # Filter and clean wildcards
        subdomains = {sub for sub in subdomains if sub.endswith(target_domain) and not sub.startswith("*")}
        
        print(f"📋 Step 2: Found {len(subdomains)} potential subdomains. Verifying which ones are active...", flush=True)
        
        live_urls = []
        for i, sub in enumerate(sorted(subdomains), 1):
            full_url = f"https://{sub}"
            print(f"   [{i}/{len(subdomains)}] Checking {full_url} ...", end="", flush=True)
            try:
                # Use a very short timeout so one broken site doesn't stall the script
                res = requests.get(full_url, timeout=2, allow_redirects=True)
                if res.status_code < 400:
                    print(" ✅ LIVE", flush=True)
                    live_urls.append(full_url)
                else:
                    print(f" ❌ (Status {res.status_code})", flush=True)
            except requests.RequestException:
                print(" ❌ DEAD", flush=True)

        # Save results
        with open("iitm_urls.txt", "w") as f:
            for url in live_urls:
                f.write(url + "\n")
                
        print(f"\n🎉 Done! Successfully saved {len(live_urls)} live websites to 'iitm_urls.txt'", flush=True)

    except Exception as e:
        print(f"\n❌ Script encountered an error: {e}")
        print("Falling back to core list creation...")
        use_fallback_list()

def use_fallback_list():
    """Fallback function to guarantee you have a file to work with immediately."""
    core_domains = [
        "https://www.iitm.ac.in",
        "https://cse.iitm.ac.in",
        "https://ee.iitm.ac.in",
        "https://mech.iitm.ac.in",
        "https://biotech.iitm.ac.in",
        "https://smail.iitm.ac.in",
        "https://t5e.iitm.ac.in",
        "https://doms.iitm.ac.in"
    ]
    with open("iitm_urls.txt", "w") as f:
        for url in core_domains:
            f.write(url + "\n")
    print("📝 Created 'iitm_urls.txt' with the core primary IITM portals so you can keep moving forward!", flush=True)

if __name__ == "__main__":
    discover_iitm_sites()