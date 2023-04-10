import snscrape.modules.twitter as sntwitter
import pandas as pd

query = "(سياسة OR انتخابات OR حكومة OR مجلس OR دستور OR نظام OR قانون OR وزير OR رئيس OR الوزراء OR رئيس OR الجمهورية OR حزب OR تشريع OR قوة OR صندوق OR الانتخابات OR تظاهرات OR حرية OR التعبير OR حرية OR الصحافة) (from:RadiomosaiqueFM) until:2022-12-31 since:2010-01-01"
limit = int(input("Enter the number of tweets you want to extract: "))
tweets = []
i = 0
for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    if len(tweets) == limit:
        break
    test = False
    for check in tweets:
        if check[2][0:10] == tweet.rawContent[0:10]:
            test = True
    if not test:
        tweets.append([tweet.date.strftime("%b-%d-%Y"), tweet.user.username, tweet.rawContent,tweet.retweetCount,tweet.likeCount,tweet.viewCount,tweet.replyCount])
df = pd.DataFrame(tweets, columns=['Date', 'Username', 'Content','Retweet Count','Like Count','View Count','Reply Count'])
df.to_csv('my_dataframe.csv', index=False)
print("Check the csv !!")
