<?php
header("Content-Type: application/rss+xml; charset=UTF-8");

$feed_urls = [
    "https://www.tor.com/feed/",
    "https://www.fantasybookreview.co.uk/rss.xml",
    "https://www.reddit.com/r/Fantasy/.rss"
];

function fetch_feed_items($url) {
    $items = [];
    $rss = @simplexml_load_file($url);
    if ($rss && isset($rss->channel->item)) {
        foreach ($rss->channel->item as $item) {
            $items[] = [
                'title' => (string)$item->title,
                'link' => (string)$item->link,
                'description' => (string)$item->description,
                'pubDate' => (string)$item->pubDate
            ];
        }
    }
    return $items;
}

// Aggregate items
$all_items = [];
foreach ($feed_urls as $url) {
    $all_items = array_merge($all_items, fetch_feed_items($url));
}

// Sort items by date
usort($all_items, function($a, $b) {
    return strtotime($b['pubDate']) - strtotime($a['pubDate']);
});

// Output the merged RSS feed
echo "<?xml version='1.0' encoding='UTF-8'?>\n";
?>
<rss version="2.0">
  <channel>
    <title>Respirework Aggregated Fantasy Feed</title>
    <link>https://respirework.com/rss/aggregated</link>
    <description>Live updates from top fantasy RSS sources, merged by Respirework</description>
<?php foreach (array_slice($all_items, 0, 10) as $item): ?>
    <item>
      <title><?php echo htmlspecialchars($item['title']); ?></title>
      <link><?php echo htmlspecialchars($item['link']); ?></link>
      <description><![CDATA[
        <?php echo $item['description']; ?><br/>
        <a href="https://respirework.com/buy-now">Buy Onyx Storm Now – Only $9.99!</a>
      ]]></description>
      <pubDate><?php echo $item['pubDate']; ?></pubDate>
    </item>
<?php endforeach; ?>
  </channel>
</rss>
