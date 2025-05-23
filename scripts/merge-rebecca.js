const Parser = require("rss-parser");
const fs = require("fs");

const parser = new Parser();
const feeds = [
  "https://www.tor.com/feed/",
  "https://bookriot.com/feed/",
  "https://www.reddit.com/r/Fantasy/.rss"
];

(async () => {
  let allItems = [];

  for (const url of feeds) {
    try {
      const feed = await parser.parseURL(url);
      const items = feed.items.slice(0, 3).map(item => ({
        title: item.title,
        link: item.link,
        pubDate: item.pubDate,
        description: item.contentSnippet || item.content || ""
      }));
      allItems = allItems.concat(items);
    } catch (err) {
      console.error("Error fetching feed:", url, err.message);
    }
  }

  allItems.sort((a, b) => new Date(b.pubDate) - new Date(a.pubDate));
  const itemsXml = allItems.slice(0, 10).map(item => `
    <item>
      <title><![CDATA[${item.title}]]></title>
      <link>${item.link}</link>
      <description><![CDATA[${item.description}
        <br/><a href="https://respirework.com/buy-now">Buy Onyx Storm Now – $9.99</a>]]>
      </description>
      <pubDate>${item.pubDate}</pubDate>
    </item>
  `).join("");

  const output = `<?xml version="1.0" encoding="UTF-8" ?>
  <rss version="2.0">
    <channel>
      <title>Rebecca Yarros News Feed</title>
      <link>https://respirework.com/rss/rebecca-yarros</link>
      <description>Auto-generated feed for fans of Rebecca Yarros</description>
      ${itemsXml}
    </channel>
  </rss>`;

  fs.mkdirSync("docs/rss", { recursive: true });
  fs.writeFileSync("docs/rss/rebecca-yarros.xml", output);
})();
