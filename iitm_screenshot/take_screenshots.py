
import asyncio
from playwright.async_api import async_playwright
import os
from datetime import datetime

MAX_WORKERS = 10


async def capture_site(context, url, i, total, output_folder, semaphore):
    async with semaphore:
        page = await context.new_page()

        try:
            await page.set_viewport_size({"width": 1280, "height": 800})

            clean_name = (
                url.replace("https://", "")
                .replace("http://", "")
                .replace("/", "_")
                + ".png"
            )

            save_path = os.path.join(output_folder, clean_name)

            print(f"[{i}/{total}] Visiting: {url} ...", end="", flush=True)

            try:
                await page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=3000
                )
            except Exception as e:
                error_msg = str(e).split('\n')[0]
                print(
                    f" ⚠️ Failed or slow ({error_msg}) - taking picture anyway...",
                    end=""
                )

            await asyncio.sleep(1)

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

                    if (document.body) {{
                        document.body.appendChild(div);
                    }}
                }}""")
            except:
                pass

            try:
                await page.screenshot(
                    path=save_path,
                    full_page=False
                )
                print(" ✅ Saved!")
            except Exception as screenshot_error:
                print(
                    f" ❌ Could not capture screen: {screenshot_error}"
                )

        finally:
            await page.close()


async def capture_all_screenshots():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    output_folder = "raw_screenshots"

    os.makedirs(output_folder, exist_ok=True)

    if not os.path.exists("iitm_urls.txt"):
        print("❌ Error: iitm_urls.txt not found!")
        return

    with open("iitm_urls.txt", "r") as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]

    print(
        f"📸 Found {len(urls)} websites to photograph. "
        f"Starting browser with {MAX_WORKERS} workers..."
    )

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=True
        )

        context = await browser.new_context(
            ignore_https_errors=True
        )

        semaphore = asyncio.Semaphore(MAX_WORKERS)

        tasks = []

        for i, url in enumerate(urls, 1):
            tasks.append(
                capture_site(
                    context,
                    url,
                    i,
                    len(urls),
                    output_folder,
                    semaphore
                )
            )

        await asyncio.gather(*tasks)

        await browser.close()

    print(
        f"\n🎉 Done! Screenshots saved in '{output_folder}'"
    )


if __name__ == "__main__":
    asyncio.run(capture_all_screenshots())

