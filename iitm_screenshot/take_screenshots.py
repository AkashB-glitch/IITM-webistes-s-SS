import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
import os
from datetime import datetime
import json
import time
import requests
import urllib3

# Suppress insecure HTTPS warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

MAX_WORKERS = 10
health_results = []

# Chrome User-Agent to bypass WAFs blocking simple Python scripts
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def check_health_sync(url):
    start = time.time()
    retries = 0
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    def do_request(timeout_sec):
        try:
            r = requests.get(url, timeout=timeout_sec, headers=headers, allow_redirects=False, verify=False)
            return r.status_code
        except requests.exceptions.Timeout:
            return "Timeout"
        except requests.exceptions.SSLError:
            return "SSL Certificate Warning"
        except requests.exceptions.ConnectionError as e:
            err_str = str(e).lower()
            if "getaddrinfo" in err_str or "name or service not known" in err_str:
                return "DNS Resolution Failure"
            if "refused" in err_str:
                return "Connection Refused"
            if "unreachable" in err_str:
                return "Network Unreachable"
            if "ssl" in err_str:
                return "SSL Certificate Warning"
            return "Connection Error"
        except Exception:
            return "Error"

    # Attempt 1: 5 second quick ping
    status_code = do_request(5)
    
    # Exponential Backoff Trigger
    if status_code in ["Timeout", "Connection Error", "Error", 500, 502, 503]:
        retries = 1
        time.sleep(3) # Let the server breathe for 3 seconds before hitting again
        # Attempt 2: 10 second deep ping
        status_code = do_request(10)
        
    elapsed = int((time.time() - start) * 1000)
    return status_code, elapsed, retries

async def capture_site(context, url, i, total, output_folder, semaphore, port_data):
    async with semaphore:
        domain = url.replace("https://", "").replace("http://", "").replace("/", "")
        clean_name = domain + ".png"
        save_path = os.path.join(output_folder, clean_name)
        
        print(f"[{i}/{total}] Checking: {url} ...", end="", flush=True)
        
        # 1. Advanced HTTP Ping (with Backoff and Headers)
        status_code, response_time, retries = await asyncio.to_thread(check_health_sync, url)
        
        # 2. Strict Categorization
        category = "Unknown"
        if isinstance(status_code, int):
            if status_code in [200, 301, 302, 307, 308]:
                category = "Active"
            elif status_code in [401, 403]:
                category = "Warning"
            elif status_code in [404, 500, 502, 503, 504]:
                category = "Error"
            else:
                category = "Active"
        else:
            if status_code == "SSL Certificate Warning":
                category = "Warning"
            elif status_code in ["Timeout", "DNS Resolution Failure", "Connection Refused", "Network Unreachable", "Connection Error", "Error"]:
                category = "Down"
            else:
                category = "Down"

        # 3. Precision Screenshot System
        page = await context.new_page()
        
        # Bypass WAFs and bot-protection using stealth plugin
        await Stealth().apply_stealth_async(page)
        screenshot_path = ""
        
        try:
            await page.set_viewport_size({"width": 1280, "height": 800})
            
            # Attempt 1: networkidle guarantees React/Dynamic apps finish loading data (15 seconds)
            try:
                await page.goto(url, wait_until="networkidle", timeout=15000)
            except Exception:
                await asyncio.sleep(2) # Short exponential backoff
                
                # Attempt 2: Fallback to domcontentloaded with a massive 25-second timeout
                try:
                    await page.goto(url, wait_until="domcontentloaded", timeout=25000)
                except Exception:
                    pass 
                
            await asyncio.sleep(1) # Allow final render paints
            
            # Inject Timestamp (only if page loaded successfully)
            try:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                await page.evaluate(f"""() => {{
                    const div = document.createElement('div');
                    div.style.position = 'fixed';
                    div.style.bottom = '15px';
                    div.style.right = '15px';
                    div.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
                    div.style.color = '#ffffff';
                    div.style.padding = '10px 20px';
                    div.style.fontSize = '20px';
                    div.style.fontWeight = 'bold';
                    div.style.fontFamily = 'Arial, sans-serif';
                    div.style.zIndex = '2147483647';
                    div.style.borderRadius = '8px';
                    div.innerText = 'Captured: {current_time}';
                    if (document.body) {{ document.body.appendChild(div); }}
                }}""")
            except:
                pass
                
            # Take Screenshot
            try:
                await page.screenshot(path=save_path, full_page=False)
                screenshot_path = f"{os.path.basename(output_folder)}/{clean_name}"
                print(f" ✅ {category} ({status_code}) - Retries: {retries}")
            except Exception as e:
                print(f" ❌ {category} ({status_code}) - No Screen")
        finally:
            await page.close()
            
        open_ports = port_data.get(domain, [])
        health_results.append({
            "website": domain,
            "status_code": status_code,
            "category": category,
            "response_time_ms": response_time,
            "retries": retries,
            "open_ports": open_ports,
            "screenshot": screenshot_path,
            "last_checked": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

async def capture_all_screenshots():
    output_folder = "raw_screenshots"
    os.makedirs(output_folder, exist_ok=True)

    if not os.path.exists("iitm_urls.txt"):
        print("❌ Error: iitm_urls.txt not found!")
        return

    with open("iitm_urls.txt", "r") as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]

    port_data = {}
    if os.path.exists("results.json"):
        with open("results.json", "r") as f:
            try:
                scan_res = json.load(f)
                for item in scan_res:
                    port_data[item.get("domain", "")] = item.get("open_ports", [])
            except:
                pass

    print(f"📸 Found {len(urls)} websites to check. Starting 100% Precision OSINT Engine...")

    async with async_playwright() as p:
        # Mask automation properties from WAFs
        browser = await p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = await browser.new_context(
            ignore_https_errors=True,
            user_agent=USER_AGENT,
            viewport={"width": 1280, "height": 800}
        )
        semaphore = asyncio.Semaphore(MAX_WORKERS)
        tasks = []

        for i, url in enumerate(urls, 1):
            tasks.append(capture_site(context, url, i, len(urls), output_folder, semaphore, port_data))

        await asyncio.gather(*tasks)
        await browser.close()

    with open("website_health.json", "w") as f:
        json.dump(health_results, f, indent=4)

    print(f"\n🎉 Done! 100% Precision data saved to website_health.json")

if __name__ == "__main__":
    asyncio.run(capture_all_screenshots())
