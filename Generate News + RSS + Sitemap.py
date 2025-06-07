name: Generate News + RSS + Sitemap

on: push: branches: - main schedule: - cron: '0 * * * *' # every minute

jobs: build: runs-on: ubuntu-latest steps: - name: 🔄 Checkout code uses: actions/checkout@v3

- name: 🐍 Set up Python
    uses: actions/setup-python@v4
    with:
      python-version: 3.11

  - name: 📦 Install dependencies
    run: pip install requests

  - name: 📰 Generate AMP Pages
    run: python scripts/generate_pages.py

  - name: 📡 Build RSS Feed
    run: python scripts/build_rss.py

  - name: 🗺️ Build Sitemap
    run: python scripts/build_sitemap.py

  - name: ☁️ Ping Google and Bing
    run: |
      curl https://www.google.com/ping?sitemap=https://respirework.com/sitemap.xml
      curl https://www.bing.com/ping?sitemap=https://respirework.com/sitemap.xml

  - name: ✅ Commit & Push changes
    run: |
      git config --global user.email "bot@respirework.com"
      git config --global user.name "RespireBot"
      git add .
      git commit -m "🤖 Auto-update news, rss, sitemap, and ping"
      git push
    env:
      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  - name: 🚀 Trigger Vercel Deployment
    run: |
      curl -X POST "https://api.vercel.com/v1/integrations/deploy/prj_YourProjectID/token=YourToken"
    env:
      VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}

  - name: 📣 Notify via Slack
    uses: slackapi/slack-github-action@v1.23.0
    with:
      payload: |
        {
          "text": "✅ RespireWork: AMP pages & sitemap updated and deployed."
        }
    env:
      SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}

  - name: 📲 Notify via Telegram
    run: |
      curl -s -X POST https://api.telegram.org/bot${{ secrets.TELEGRAM_BOT_TOKEN }}/sendMessage \
      -d chat_id=${{ secrets.TELEGRAM_CHAT_ID }} \
      -d text="✅ RespireWork: AMP pages & sitemap updated and deployed."
