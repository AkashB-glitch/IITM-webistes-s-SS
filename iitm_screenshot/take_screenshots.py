import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
import os
from datetime import datetime
import json
import time
import requests
import urllib3
import socket

# Suppress insecure HTTPS warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

MAX_WORKERS = 10
health_results = []

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def check_http_sync(url):
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    def do_req(timeout_sec):
        start = time.time()
        try:
            r = requests.get(url, timeout=timeout_sec, headers=headers, allow_redirects=True, verify=True)
            elapsed = int((time.time() - start) * 1000)
            return r.status_code, r.url, elapsed, False, True, None
        except requests.exceptions.SSLError:
            try:
                start2 = time.time()
                r = requests.get(url, timeout=timeout_sec, headers=headers, allow_redirects=True, verify=False)
                elapsed = int((time.time() - start2) * 1000)
                return r.status_code, r.url, elapsed, True, True, None
            except Exception as e:
                return None, url, None, True, True, str(e)
        except Exception as e:
            return None, url, None, False, False, str(e)

    status_code, final_url, elapsed, ssl_warning, ssl_available, err = do_req(5)
    retries = 0
    if err or status_code in [500, 502, 503, 504] or status_code is None:
        retries = 1
        time.sleep(3)
        status_code, final_url, elapsed, ssl_warning, ssl_available, err = do_req(10)
        
    return status_code, final_url, elapsed, ssl_warning, ssl_available, err, retries

async def check_port(domain, port):
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(domain, port), timeout=5.0)
        writer.close()
        await writer.wait_closed()
        return port
    except:
        return None

async def capture_site(context, url, i, total, output_folder, semaphore):
    async with semaphore:
        domain = url.replace("https://", "").replace("http://", "").replace("/", "")
        clean_name = domain + ".png"
        save_path = os.path.join(output_folder, clean_name)
        
        print(f"[{i}/{total}] Checking: {url} ...", end="", flush=True)
        
        # 1. DNS Resolution
        try:
            await asyncio.to_thread(socket.gethostbyname, domain)
            dns_resolved = True
        except socket.gaierror:
            dns_resolved = False

        # 2. Port Check
        port_tasks = [check_port(domain, p) for p in [80, 443, 8080, 8443]]
        open_ports_raw = await asyncio.gather(*port_tasks)
        open_ports = [p for p in open_ports_raw if p is not None]

        # 3. HTTP Check
        if dns_resolved:
            status_code, final_url, response_time, ssl_warning, ssl_available, err, retries = await asyncio.to_thread(check_http_sync, url)
        else:
            status_code, final_url, response_time, ssl_warning, ssl_available, err, retries = None, url, 0, False, False, "DNS Failed", 0

        # 4. Screenshot & Title
        page_title = None
        screenshot_success = False
        screenshot_path = ""
        
        if dns_resolved and (len(open_ports) > 0 or status_code is not None):
            page = await context.new_page()
            await Stealth().apply_stealth_async(page)
            try:
                await page.set_viewport_size({"width": 1280, "height": 800})
                try:
                    await page.goto(url, wait_until="networkidle", timeout=30000)
                except Exception:
                    await asyncio.sleep(2)
                    try:
                        await page.goto(url, wait_until="domcontentloaded", timeout=45000)
                    except Exception:
                        pass
                
                await asyncio.sleep(3)
                
                try:
                    page_title = await page.title()
                    if not page_title:
                        page_title = None
                except:
                    pass

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
                    
                try:
                    await page.screenshot(path=save_path, full_page=False)
                    if os.path.exists(save_path) and os.path.getsize(save_path) > 0:
                        screenshot_success = True
                        screenshot_path = f"{os.path.basename(output_folder)}/{clean_name}"
                except:
                    pass
            finally:
                await page.close()

        # 5. Confidence Score
        confidence = 0
        if dns_resolved: confidence += 25
        if len(open_ports) > 0: confidence += 25
        if page_title: confidence += 25
        if screenshot_success: confidence += 25

        # 6. Strict Classification Rules
        category = "Unknown"
        is_down = False
        
        if not dns_resolved:
            is_down = True
        elif len(open_ports) == 0 and status_code is None:
            is_down = True
        elif err and any(e in err.lower() for e in ["refused", "unreachable", "timeout"]):
            if not screenshot_success and not page_title:
                is_down = True
        elif status_code is None and not page_title:
            is_down = True
            
        if is_down:
            category = "Down"
        elif status_code in [404, 410, 500, 502, 503, 504]:
            category = "Error"
        elif status_code in [401, 403]:
            if screenshot_success or page_title:
                category = "Active"
            else:
                category = "Restricted"
        elif status_code in [200, 201, 204, 301, 302, 307, 308]:
            category = "Active"
        elif screenshot_success and page_title:
            category = "Active"
        elif ssl_available and not ssl_warning and len(open_ports) > 0:
            category = "Active"
        else:
            if confidence >= 50:
                category = "Warning"
            else:
                category = "Down"

        print(f" {category} ({status_code}) - Score: {confidence} - Retries: {retries}")
        
        health_results.append({
            "website": domain,
            "dns_resolved": dns_resolved,
            "open_ports": open_ports,
            "http_status": status_code,
            "final_url": final_url,
            "response_time_ms": response_time,
            "ssl_available": ssl_available,
            "ssl_warning": ssl_warning,
            "page_title": page_title,
            "screenshot_success": screenshot_success,
            "screenshot": screenshot_path,
            "retries": retries,
            "confidence_score": confidence,
            "category": category,
            "last_checked": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

async def capture_all_screenshots():
    output_folder = "raw_screenshots"
    os.makedirs(output_folder, exist_ok=True)

    if not os.path.exists("iitm_urls.txt"):
        print("Error: iitm_urls.txt not found!")
        return

    with open("iitm_urls.txt", "r") as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]

    print(f"Found {len(urls)} websites to check. Starting 100% Precision OSINT Engine...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = await browser.new_context(
            ignore_https_errors=True,
            user_agent=USER_AGENT,
            viewport={"width": 1280, "height": 800}
        )
        semaphore = asyncio.Semaphore(MAX_WORKERS)
        tasks = []

        for i, url in enumerate(urls, 1):
            tasks.append(capture_site(context, url, i, len(urls), output_folder, semaphore))

        await asyncio.gather(*tasks)
        await browser.close()

    with open("website_health.json", "w") as f:
        json.dump(health_results, f, indent=4)

    print(f"\\nDone! 100% Precision data saved to website_health.json")

if __name__ == "__main__":
    asyncio.run(capture_all_screenshots())
