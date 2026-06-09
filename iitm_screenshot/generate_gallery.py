import os

folder = "raw_screenshots"

html = """
<!DOCTYPE html>
<html>
<head>
<title>IITM Screenshots</title>
<style>
body { font-family: Arial; margin: 20px; }
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fill,minmax(300px,1fr));
    gap: 20px;
}
.card {
    border: 1px solid #ccc;
    padding: 10px;
}
img {
    width: 100%;
}
</style>
</head>
<body>
<h1>IITM Website Screenshots</h1>
<div class="grid">
"""

for img in sorted(os.listdir(folder)):
    if img.endswith(".png"):
        html += f'''
        <div class="card">
            <p>{img}</p>
            <a href="{folder}/{img}">
                <img src="{folder}/{img}">
            </a>
        </div>
        '''

html += "</div></body></html>"

with open("index.html", "w") as f:
    f.write(html)

print("index.html created")
