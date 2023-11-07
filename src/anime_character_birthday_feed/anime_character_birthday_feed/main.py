#! /usr/bin/env python
import feedgenerator
import requests
import json
import datetime
from anime_character_birthday_feed.idol_images import idol_images

# today = datetime.date.today()
today = datetime.datetime(2023, 8, 18, 9, 55, 28)

feed = feedgenerator.Rss201rev2Feed(
    title="本日、誕生日のアイドルマスター ミリオンライブ！のアイドルを紹介🎂",
    link="https://millionlive-anime.idolmaster-official.jp/",
    description="本日" + str(today.month) + "月" + str(today.day) + "日が誕生日のアイドルは...",
    language="ja",
)

response = requests.get("https://api.matsurihi.me/api/mltd/v2/idols")
idols = json.loads(response.text)

for idol in idols:
    if (
        idol["birthday"]["month"] == today.month
        and idol["birthday"]["day"] == today.day
    ):
        for image in idol_images:
            if image["name"] in idol["fullName"]:
                feed.add_item(
                    title=idol["fullName"] + "（" + idol["fullNameRuby"] + "）",
                    link=image["url"],
                    description=idol["firstName"]
                    + "ちゃんは、"
                    + idol["birthplace"]["name"]
                    + "出身で、趣味は"
                    + idol["hobby"]
                    + "、好きなことは"
                    + idol["favorites"]
                    + "✨",
                    pubdate=today,
                )

with open("dist/anime_character_birthday_feed.rss", "w") as fp:
    feed.write(fp, "utf-8")
