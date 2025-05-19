import feedparser, os, tweepy, textwrap

# ---- 情報源：暗号資産10本 + 不動産10本 + X検索2本 ----
FEEDS = [
  # --- 暗号資産 -----------------------
  "https://www.coindesk.com/arc/outboundfeeds/rss/",
  "https://cointelegraph.com/rss",
  "https://cryptoslate.com/feed/",
  "https://decrypt.co/news/feed",
  "https://www.theblock.co/rss",
  "https://cryptopotato.com/feed/",
  "https://thedefiant.io/feed/",
  "https://cryptonews.com/news/feed/",
  "https://research.binance.com/feed",
  "https://finance.yahoo.com/news/rssindex",   # あとで自動で絞り込み
  # --- 不動産投資 ---------------------
  "https://rss.app/feeds/xxxxxxxx.json",       # 楽待 (RSS.appで作成したURLを貼る)
  "https://pushum13.rssing.com/chan-7891744/latest.php", # 健美家
  "https://suumo.jp/journal/feed/",
  "https://www.homes.co.jp/cont/press/feed/",
  "https://jp.savills.co.jp/rss-feeds/news.rss",
  "https://rss.app/feeds/yyyyyyyy.json",       # 日経REマーケット (RSS.app)
  "https://www.worldpropertyjournal.com/japan/feed",
  "https://resources.realestate.co.jp/feed/",
  "https://www.realestate-tokyo.com/news/feed/",
  "https://www.japantimes.co.jp/real-estate/rss",
  # --- X 全体（Nitter検索RSSで代用）---
  "https://nitter.net/search/rss?q=ビットコイン",
  "https://nitter.net/search/rss?q=不動産投資",
]

# ---- 140字に収める超シンプル要約関数 ----
def summarize(title, summary, max_len=140):
    text = f"{title} {summary}"
    text = text.replace("\n", " ")
    return textwrap.shorten(text, width=max_len, placeholder="…")

# ---- X API クライアント ----
client = tweepy.Client(
    bearer_token=os.getenv("X_BEARER"),
    consumer_key=os.getenv("X_CONSUMER"),
    consumer_secret=os.getenv("X_SECRET"),
    access_token=os.getenv("X_ACCESS"),
    access_token_secret=os.getenv("X_ACCESS_SECRET"),
)

posted = 0  # 保険：１回で投稿しすぎないように数える

for url in FEEDS:
    feed = feedparser.parse(url)
    if not feed.entries:
        continue
    item = feed.entries[0]         # 各フィード最新１件だけ使う
    tweet_text = summarize(item.title, getattr(item, "summary", ""))
    tweet_full = f"{tweet_text}\n{item.link}\nDYOR／自己責任"
    # X の無料枠は 1,500ツイ/月 ≒ 50ツイ/日 → ここでは30件/日上限にする
    if len(tweet_full) <= 280 and posted < 30:
        client.create_tweet(text=tweet_full)
        posted += 1
