import json
import os

with open('website_health.json', 'r') as f:
    data = json.load(f)

for item in data:
    # RESTORE the screenshot path
    screenshot_candidate = f"raw_screenshots/{item['website']}.png"
    if os.path.exists(screenshot_candidate) and os.path.getsize(screenshot_candidate) > 0:
        item['screenshot_success'] = True
        item['screenshot'] = screenshot_candidate
    else:
        item['screenshot_success'] = False
        item['screenshot'] = ""
    
    # Recalculate confidence
    confidence = 0
    if item['dns_resolved']: confidence += 25
    if len(item['open_ports']) > 0: confidence += 25
    if item['page_title']: confidence += 25
    if item['screenshot_success']: confidence += 25
    item['confidence_score'] = confidence
    
    # Re-apply strict rules
    dns_resolved = item['dns_resolved']
    open_ports = item['open_ports']
    status_code = item['http_status']
    screenshot_success = item['screenshot_success']
    page_title = item['page_title']
    ssl_available = item['ssl_available']
    ssl_warning = item['ssl_warning']
    retries = item['retries']
    
    is_down = False
    if not dns_resolved:
        is_down = True
    elif len(open_ports) == 0 and status_code is None:
        is_down = True
    # If HTTP completely failed AND we don't have a page title, the screenshot is just an error page.
    elif status_code is None and not page_title:
        is_down = True
        
    if is_down:
        item['category'] = "Down"
    elif status_code in [404, 410, 500, 502, 503, 504]:
        item['category'] = "Error"
    elif status_code in [401, 403]:
        if screenshot_success or page_title:
            item['category'] = "Active"
        else:
            item['category'] = "Restricted"
    elif status_code in [200, 201, 204, 301, 302, 307, 308]:
        item['category'] = "Active"
    elif screenshot_success and page_title:
        item['category'] = "Active"
    elif ssl_available and not ssl_warning and len(open_ports) > 0:
        item['category'] = "Active"
    else:
        if confidence >= 50:
            item['category'] = "Warning"
        else:
            item['category'] = "Down"

with open('website_health.json', 'w') as f:
    json.dump(data, f, indent=4)
print("Data fixed successfully!")
