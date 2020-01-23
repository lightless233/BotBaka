import feedparser
import requests


p = {"http": "socks5://127.0.0.1:9050", "https": "socks5://127.0.0.1:9050"}
requests.get("https://seclists.org/rss/oss-sec.rss", proxies=p)
rss = feedparser.parse("https://seclists.org/rss/oss-sec.rss")
