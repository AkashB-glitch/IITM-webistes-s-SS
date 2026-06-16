import os
import json
import pathlib
from datetime import datetime

health_file = "website_health.json"
if not os.path.exists(health_file):
    print("Error: website_health.json not found! Please run take_screenshots.py first.")
    exit(1)

with open(health_file, "r") as f:
    health_data = json.load(f)

category_counts = {"Active": 0, "Warning": 0, "Error": 0, "Down": 0}
category_urls = {"Active": [], "Warning": [], "Error": [], "Down": []}

def get_style(category):
    if category == "Active":
        return "", "green", "badge-active", "border-active"
    elif category == "Warning":
        return "", "orange", "badge-warn", "border-warning"
    elif category == "Error":
        return "", "red", "badge-error", "border-error"
    else:
        return "⚫", "black", "badge-down", "border-down"

html = f"""<!DOCTYPE html>
<html>
<head>
<title>IITM Website Health Dashboard</title>
<style>
body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 30px; background-color: #f4f6f9; color: #333; }}
.header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; flex-wrap: wrap; gap: 20px; }}
.header h1 {{ margin: 0; color: #1a1a1a; font-size: 28px; }}
.header p {{ margin: 5px 0 0 0; color: #666; font-size: 14px; }}
.btn {{ padding: 10px 20px; background-color: #0056b3; color: white; border: none; cursor: pointer; border-radius: 6px; font-weight: bold; font-size: 15px; transition: background 0.2s; }}
.btn:hover {{ background-color: #004494; }}

/* Stats Box with Expandable Dropdown */
.stats-container {{ display: flex; gap: 20px; margin-bottom: 40px; flex-wrap: wrap; align-items: flex-start; }}
details.stat-box {{ background: white; padding: 25px 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); flex: 1; min-width: 220px; border-top: 5px solid #ccc; transition: transform 0.2s, box-shadow 0.2s; }}
details.stat-box[open] {{ box-shadow: 0 8px 16px rgba(0,0,0,0.1); }}
details.stat-box summary {{ cursor: pointer; list-style: none; text-align: center; outline: none; }}
details.stat-box summary::-webkit-details-marker {{ display: none; }}
details.stat-box h3 {{ margin: 0; color: #6c757d; font-size: 16px; font-weight: bold; display: flex; align-items: center; justify-content: center; gap: 8px; }}
details.stat-box p {{ margin: 15px 0 0 0; font-size: 32px; font-weight: bold; color: #212529; pointer-events: none; }}

.border-active {{ border-top-color: #28a745; }}
.border-warning {{ border-top-color: #ffc107; }}
.border-error {{ border-top-color: #dc3545; }}
.border-down {{ border-top-color: #343a40; }}

/* Dropdown Content */
.dropdown-links {{ margin-top: 20px; border-top: 1px solid #eee; padding-top: 15px; max-height: 250px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; text-align: left; }}
.dropdown-links a {{ color: #0056b3; text-decoration: none; font-size: 14px; font-weight: 600; word-break: break-all; padding: 5px; border-radius: 4px; transition: background 0.2s; }}
.dropdown-links a:hover {{ background: #f0f4f8; text-decoration: none; }}

/* Grid View */
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 25px; }}
.card {{ background: white; border: 1px solid #e9ecef; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.04); transition: transform 0.2s; }}
.card:hover {{ transform: translateY(-3px); box-shadow: 0 6px 12px rgba(0,0,0,0.1); }}
.card h4 {{ margin: 0 0 15px 0; font-size: 17px; word-break: break-all; }}
.card h4 a {{ color: #0056b3; text-decoration: none; }}
.card .badges {{ display: flex; gap: 8px; margin-bottom: 15px; font-size: 12px; font-weight: 600; flex-wrap: wrap; }}
.badge {{ padding: 5px 10px; border-radius: 6px; background: #f8f9fa; border: 1px solid #dee2e6; color: #495057; display: flex; align-items: center; gap: 5px; }}

.badge-active {{ background: #d4edda; color: #155724; border-color: #c3e6cb; }}
.badge-warn {{ background: #fff3cd; color: #856404; border-color: #ffeeba; }}
.badge-error {{ background: #f8d7da; color: #721c24; border-color: #f5c6cb; }}
.badge-down {{ background: #e2e3e5; color: #383d41; border-color: #d6d8db; }}

.card img {{ width: 100%; border-radius: 6px; margin-top: 5px; border: 1px solid #e9ecef; object-fit: cover; aspect-ratio: 16/9; }}

/* List View */
.list-view {{ display: none; }}
table {{ width: 100%; border-collapse: collapse; background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-radius: 10px; overflow: hidden; }}
th, td {{ padding: 15px; text-align: left; border-bottom: 1px solid #e9ecef; }}
th {{ background-color: #0056b3; color: white; font-weight: 600; font-size: 15px; }}
tr:hover {{ background-color: #f8f9fa; }}
td a {{ color: #0056b3; text-decoration: none; font-weight: 600; }}
.status-pill {{ padding: 6px 12px; border-radius: 20px; font-weight: 600; font-size: 13px; display: inline-flex; align-items: center; gap: 6px; }}
</style>
<script>
function toggleView() {{
    var grid = document.getElementById("gridView");
    var list = document.getElementById("listView");
    var btn = document.getElementById("toggleBtn");
    if (grid.style.display === "none") {{
        grid.style.display = "grid";
        list.style.display = "none";
        btn.innerText = "Switch to Table View";
    }} else {{
        grid.style.display = "none";
        list.style.display = "block";
        btn.innerText = "Switch to Gallery View";
    }}
}}

function filterByPort() {{
    var input = document.getElementById("portSearch");
    var portFilter = input.value.trim().toLowerCase();
    
    var items = document.querySelectorAll(".filterable-item");
    
    items.forEach(function(item) {{
        var itemPorts = item.getAttribute("data-ports") || "";
        var portMatch = (portFilter === "" || itemPorts.split(",").includes(portFilter));
        
        if (portMatch) {{
            item.style.display = "";
        }} else {{
            item.style.display = "none";
        }}
    }});
}}
</script>
</head>
<body>

<div class="header">
    <div>
        <h1>IITM Website Health Dashboard</h1>
        <p>Last Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    </div>
    <div style="display: flex; gap: 15px; align-items: center;">
        <input type="text" id="portSearch" onkeyup="filterByPort()" placeholder=" Search Port (e.g. 80, 443)" style="padding: 10px; border-radius: 6px; border: 1px solid #ccc; width: 250px; font-size: 15px; outline: none;">
        <button id="toggleBtn" class="btn" onclick="toggleView()">Switch to Table View</button>
    </div>
</div>
"""

list_rows = ""
grid_cards = ""

for item in health_data:
    website = item["website"]
    status_code = item.get("status_code", "")
    category = item.get("category", "Unknown")
    response_time = item.get("response_time_ms", 0)
    retries = item.get("retries", 0)
    ports = item.get("open_ports", [])
    screenshot = item.get("screenshot", "")
    
    icon, color, badge_class, border_class = get_style(category)
    
    # Store data for Dropdown boxes
    if category in category_counts:
        category_counts[category] += 1
        category_urls[category].append(website)
        
    ports_str = ", ".join(map(str, ports)) if ports else "None"
    data_ports_attr = ",".join(map(str, ports)) if ports else ""
    status_code_str = str(status_code)
    
    # Grid Card
    grid_cards += f'''
    <div class="card filterable-item" data-ports="{data_ports_attr}">
        <h4><a href="https://{website}" target="_blank">{website}</a></h4>
        <div class="badges">
            <span class="badge {badge_class}">{icon} {category}</span>
            <span class="badge">HTTP: {status_code_str}</span>
            <span class="badge">{response_time}ms</span>
            <span class="badge"> {ports_str}</span>
            <span class="badge" title="Retries used"> {retries}</span>
        </div>
    '''
    if screenshot and os.path.exists(screenshot):
        file_uri = pathlib.Path(os.path.abspath(screenshot)).as_uri()
        grid_cards += f'<a href="{file_uri}" target="_blank"><img src="{file_uri}" alt="Screenshot" onerror="this.style.display=\'none\'"></a>'
    else:
        grid_cards += '<div style="background:#f8f9fa; color:#6c757d; text-align:center; padding: 40px 0; border-radius: 6px; font-size: 14px; border: 1px dashed #ced4da;">No Screenshot</div>'
    grid_cards += '</div>'
    
    # List Row
    list_rows += f'''
        <tr class="list-row filterable-item" data-ports="{data_ports_attr}">
            <td><a href="https://{website}" target="_blank">{website}</a></td>
            <td><span class="status-pill {badge_class}">{icon} {category}</span></td>
            <td><strong>{status_code_str}</strong></td>
            <td>{response_time} ms</td>
            <td>{ports_str}</td>
            <td>{retries}</td>
        </tr>
    '''

def build_dropdown(title, count, icon, border_class, urls):
    links_html = "".join([f'<a href="https://{u}" target="_blank">{u}</a>' for u in urls])
    if not links_html:
        links_html = '<p style="color:#999; font-size:13px; text-align:center;">No websites in this category.</p>'
        
    return f'''
    <details class="stat-box {border_class}">
        <summary>
            <h3>{icon} {title}</h3><p>{count}</p>
        </summary>
        <div class="dropdown-links">
            {links_html}
        </div>
    </details>
    '''

dropdowns_html = f"""
<div class="stats-container">
    {build_dropdown("Active", category_counts["Active"], "", "border-active", category_urls["Active"])}
    {build_dropdown("Warning", category_counts["Warning"], "", "border-warning", category_urls["Warning"])}
    {build_dropdown("Error", category_counts["Error"], "", "border-error", category_urls["Error"])}
    {build_dropdown("Down", category_counts["Down"], "⚫", "border-down", category_urls["Down"])}
</div>
"""

html += dropdowns_html + f"""
<!-- GRID VIEW -->
<div id="gridView" class="grid">
    {grid_cards}
</div>

<!-- LIST VIEW -->
<div id="listView" class="list-view">
    <table>
        <tr>
            <th>Website URL</th>
            <th>Health State</th>
            <th>HTTP Status</th>
            <th>Response Time</th>
            <th>Open Ports</th>
            <th>Retries</th>
        </tr>
        {list_rows}
    </table>
</div>

</body>
</html>
"""

output_html = "index.html"
with open(output_html, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Interactive Health Dashboard generated at: {os.path.abspath(output_html)}")
