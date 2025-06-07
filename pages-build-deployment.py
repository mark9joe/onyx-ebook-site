import os
import subprocess
from scripts import generate_pages, build_rss, build_sitemap

def run_script(path):
    try:
        subprocess.run(["python", path], check=True)
        print(f"✅ Ran: {path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {path}: {e}")

def ensure_directories():
    os.makedirs("news", exist_ok=True)
    print("📁 'news/' directory ensured.")

def main():
    print("🚀 Starting site build process...")

    ensure_directories()

    print("📰 Generating AMP pages...")
    generate_pages.main()

    print("📡 Generating RSS feed...")
    build_rss.generate_rss()

    print("🗺️ Generating Sitemap...")
    build_sitemap.generate_sitemap()

    print("🎉 Build process completed.")

if __name__ == "__main__":
    main()
