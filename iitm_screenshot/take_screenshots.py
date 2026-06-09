import asyncio
from playwright.async_api import async_playwright
import os
from datetime import datetime

async def capture_all_screenshots():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_folder = f"/var/www/html/{timestamp}"
    os.makedirs(output_folder, exist_ok=True)
    
    if not os.path.exists("iitm_urls.txt"):
        print("❌ Error: iitm_urls.txt not found! Please make sure it's in this folder.")
        return
        
    with open("iitm_urls.txt", "r") as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]
        
    print(f"📸 Found {len(urls)} websites to photograph. Starting browser...")

    async with async_playwright() as p:
        # Launch browser in headless mode
        browser = await p.chromium.launch(headless=True) 
        
        # FIX 1: Ignore certificate errors (fixes pages like archive.iitm.ac.in)
        context = await browser.new_context(ignore_https_errors=True)
        page = await context.new_page()
        
        # Set standard desktop screen size
        await page.set_viewport_size({"width": 1280, "height": 800})
        
        for i, url in enumerate(urls, 1):
            clean_name = url.replace("https://", "").replace("http://", "").replace("/", "_") + ".png"
            save_path = os.path.join(output_folder, clean_name)
            
            print(f" [{i}/{len(urls)}] Visiting: {url} ...", end="", flush=True)
            
            try:
                # FIX 2: Wait for main structure layout rather than waiting forever for heavy backgrounds
                await page.goto(url, wait_until="domcontentloaded", timeout=25000)
                
                # Give it a tiny 2-second breathing room to visually render
                await asyncio.sleep(2) 
                
                # Take the first-page screenshot
                await page.screenshot(path=save_path, full_page=False)
                print(" ✅ Saved!")
                
            except Exception as e:
                print(f" ❌ Failed (Timeout or page error)")
                
        await browser.close()
    print(f"\n🎉 Done! Check the '{output_folder}' folder on your computer for the pictures.")

if __name__ == "__main__":
    asyncio.run(capture_all_screenshots())