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
                # Try to load the page (timeout after 5 seconds so we don't get stuck forever)
                await page.goto(url, timeout=5000)
            except Exception as e:
                error_msg = str(e).split('\n')[0]
                print(f" ⚠️ Failed or slow ({error_msg}) - taking picture anyway...", end="")
                
            # Wait exactly 5 seconds for whatever is on the screen to settle
            await asyncio.sleep(5)
            
            try:
                # Take the screenshot!
                await page.screenshot(path=save_path, full_page=False)
                print(" ✅ Saved!")
            except Exception as screenshot_error:
                print(f" ❌ Could not capture screen: {screenshot_error}")
                
        await browser.close()
    print(f"\n🎉 Done! Check the '{output_folder}' folder on your computer for the pictures.")

if __name__ == "__main__":
    asyncio.run(capture_all_screenshots())