import os
import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString

BASE_URL = "https://www.respirework.com"
OUTPUT_PATH = "sitemap.xml"
PAGES_DIR = "."

def get_all_html_files(directory):
    html_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                path = os.path.relpath(os.path.join(root, file), start=directory)
                if "node_modules" not in path and "scripts" not in path and path != "404.html":
                    html_files.append(path)
    return html_files

def build_sitemap(urls):
    urlset = Element('urlset')
    urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")

    for path in urls:
        url = SubElement(urlset, "url")
        loc = SubElement(url, "loc")
        loc.text = f"{BASE_URL}/{path.replace(os.sep, '/')}"
        lastmod = SubElement(url, "lastmod")
        lastmod.text = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    return parseString(tostring(urlset)).toprettyxml(indent="  ")

if __name__ == "__main__":
    pages = get_all_html_files(PAGES_DIR)
    sitemap = build_sitemap(pages)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(sitemap)
    print(f"Sitemap generated with {len(pages)} URLs.")
