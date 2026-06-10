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
            
            # Inject a timestamp overlay into the webpage before screenshotting
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
                    div.style.fontSize = '24px';
                    div.style.fontWeight = 'bold';
                    div.style.fontFamily = 'Arial, sans-serif';
                    div.style.zIndex = '2147483647'; // Max z-index to ensure it's on top
                    div.style.borderRadius = '8px';
                    div.style.boxShadow = '0 4px 6px rgba(0,0,0,0.3)';
                    div.innerText = 'Captured: {current_time}';
                    if (document.body) {{
                        document.body.appendChild(div);
                    }} else {{
                        document.documentElement.appendChild(div);
                    }}
                }}""")
            except Exception as e:
                pass # If the page is completely broken or empty, we can't inject JS, but we'll still take the screenshot
            
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