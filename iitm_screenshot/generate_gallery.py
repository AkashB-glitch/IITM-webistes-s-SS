import os
import glob
import json
import pathlib
from datetime import datetime

folder = "raw_screenshots"

try:
    images = [img for img in sorted(os.listdir(folder)) if img.endswith(".png")]
except FileNotFoundError:
    images = []

total_count = len(images)

# Try to load port scan results
port_data = {}
results_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results.json")
if not os.path.exists(results_file):
    results_file = "results.json" # try current directory

if os.path.exists(results_file):
    try:
        with open(results_file, "r") as f:
            scan_results = json.load(f)
            for item in scan_results:
                port_data[item.get("domain", "")] = item.get("open_ports", [])
    except:
        pass

# Extract scan date and time from folder name
from datetime import datetime

scan_datetime = datetime.fromtimestamp(
    os.path.getmtime(folder)
).strftime("%Y-%m-%d %H:%M:%S")
html = f"""
<!DOCTYPE html>
<html>
<head>
<title>IITM Screenshots & Port Scan</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 20px; }}
.header {{ display: flex; justify-content: space-between; align-items: center; }}
.btn {{ padding: 10px 20px; background-color: #4c8bf5; color: white; border: none; cursor: pointer; border-radius: 5px; font-weight: bold; font-size: 16px; }}
.btn:hover {{ background-color: #3b76da; }}

/* Grid View Styles */
.grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill,minmax(300px,1fr));
    gap: 20px;
    margin-top: 20px;
}}
.card {{
    border: 1px solid #ccc;
    padding: 10px;
    border-radius: 5px;
}}
.card p {{ margin: 0 0 10px 0; font-weight: bold; word-break: break-all; }}
img {{ width: 100%; border-radius: 4px; }}

/* List View Styles */
.list-view {{ display: none; margin-top: 20px; }}
table {{ width: 100%; border-collapse: collapse; border: 1px solid #ccc; }}
th, td {{ border: 1px solid #ccc; padding: 12px; text-align: left; }}
th {{ background-color: #4a7ebb; color: white; }}
tr:nth-child(even) {{ background-color: #f2f2f2; }}
tr:nth-child(odd) {{ background-color: #e6ecf5; }}
a {{ color: #000; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
</style>
<script>
function toggleView() {{
    var grid = document.getElementById("gridView");
    var list = document.getElementById("listView");
    var btn = document.getElementById("toggleBtn");
    
    if (grid.style.display === "none") {{
        grid.style.display = "grid";
        list.style.display = "none";
        btn.innerText = "Switch to Text View List";
    }} else {{
        grid.style.display = "none";
        list.style.display = "block";
        btn.innerText = "Switch to Grid View";
    }}
}}
</script>
</head>
<body>

<div class="header">
    <div>
        <h1>IITM Website Screenshots</h1>
        <h2>Total Count: {total_count}</h2>
        <h3 style="color: #666; margin-top: -15px;">Scan Date & Time: {scan_datetime}</h3>
    </div>
    <button id="toggleBtn" class="btn" onclick="toggleView()">Switch to Text View List</button>
</div>

<!-- GRID VIEW -->
<div id="gridView" class="grid">
"""

# Populate Grid View
for img in images:
    domain = img.replace(".png", "")
    img_path = os.path.join(folder, img)
    file_uri = f"raw_screenshots/{img}"
    
    html += f'''
    <div class="card">
        <p>{domain}</p>
        <a href="{file_uri}" target="_blank">
            <img src="{file_uri}">
        </a>
    </div>
    '''

html += """
</div>

<!-- LIST VIEW -->
<div id="listView" class="list-view">
    <table>
        <tr>
            <th>Websites link</th>
            <th>Open ports</th>
        </tr>
"""

# Populate List View Table
for img in images:
    domain = img.replace(".png", "")
    website_url = f"https://{domain}"
    
    ports = port_data.get(domain, [])
    # Keep only valid port numbers (filter out null/None)
    valid_ports = [p for p in ports if p]
    
    if len(valid_ports) > 0:
        # Display exactly the ports that were discovered open on this specific server
        port_text = ", ".join(map(str, valid_ports))
    else:
        port_text = "443 (Default/Assumed)"

        
    html += f'''
        <tr>
            <td><a href="{website_url}" target="_blank" style="color: #0066cc;">{website_url}</a></td>
            <td>{port_text}</td>
        </tr>
    '''

html += """
    </table>
</div>

</body>
</html>
"""

output_html = "index.html"
with open(output_html, "w") as f:
    f.write(html)

print(f"Gallery created at: {os.path.abspath(output_html)}")
