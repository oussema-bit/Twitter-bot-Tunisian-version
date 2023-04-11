import snscrape.modules.twitter as sntwitter #alias
import pandas as pd
import datetime
import random
import os

with open('keywordsFR.txt', 'r') as file:
    keywordsFR = [line.strip(',\n') for line in file.readlines()]

keywordsFRForQuery=" OR ".join(keywordsFR)

with open('keywordsAR.txt', 'r') as file:
    keywordsAR = [line.strip(',\n') for line in file.readlines()]

keywordsARForQuery=" OR ".join(keywordsAR)

choice=1
while True:
    startdate_str = input("Enter the start date 'YYYY-MM-DD': ")
    startdate_obj = datetime.datetime.strptime(startdate_str, '%Y-%m-%d')

    enddate_str = input("Enter the end date 'YYYY-MM-DD': ")
    enddate_obj = datetime.datetime.strptime(enddate_str, '%Y-%m-%d')

    source = input("Enter the source from twitter: ")
    testquery = "(from:" + source + ")"
    language = ""
    for tweet in sntwitter.TwitterSearchScraper(testquery).get_items():
        language = tweet.lang
        break
    if language == "ar":
        query = "until:"+enddate_obj.strftime("%Y-%m-%d")+" since:"+startdate_obj.strftime("%Y-%m-%d")+" (from:RadiomosaiqueFM)" + "(" + keywordsARForQuery + ") " + "تونس OR تونسي OR تونسية OR تونسيون"
    elif language == "fr":
        query = "(" + keywordsFRForQuery + ") " + "(Tunis OR Tunisie OR Tunisien OR Tunisienne OR Tunisiens)" + " (from:" + source + ") " + "until:" + enddate_obj.strftime(
            "%Y-%m-%d") + " since:" + startdate_obj.strftime("%Y-%m-%d")

    else:
        query = "(" + keywordsFRForQuery + ") " + "(Tunis OR Tunisia OR Tunisian OR Tunisians)" + " (from:" + source + ") " + "until:" + enddate_obj.strftime(
            "%Y-%m-%d") + " since:" + startdate_obj.strftime("%Y-%m-%d")

    limit = int(input("Enter number of tweets you want to extract (type 0 if you want to extract all tweet): "))
    tweets = []
    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        if limit != 0:
            if len(tweets) == limit:
                break
        test = False
        for check in tweets:
            if check[2][0:10] == tweet.rawContent[0:10]:
                test = True
        if not test:
            tweets.append([tweet.date.strftime("%b-%d-%Y"), tweet.user.username, tweet.rawContent, tweet.retweetCount,
                           tweet.likeCount, tweet.viewCount, tweet.replyCount])
    df = pd.DataFrame(tweets, columns=['Date', 'Username', 'Content', 'Retweet Count', 'Like Count', 'View Count',
                                       'Reply Count'])

    random_number = random.randint(0, 99)
    csvName = source + str(random_number) + language +startdate_obj.strftime("%Y-%m-%d")+enddate_obj.strftime("%Y-%m-%d")+ '.csv'
    csv_file=df.to_csv(csvName, index=False)
    read_file = pd.read_csv(csvName)
    xlsxName=source + str(random_number) + language +startdate_obj.strftime("%Y-%m-%d")+enddate_obj.strftime("%Y-%m-%d")+'.xlsx'
    read_file.to_excel(r'Excel/'+xlsxName, index=None, header=True)
    print("Check the excel file under Excel/" + xlsxName + " !!")
    os.remove(csvName)
    choice=input("If you wish to continue mining press enter else type 0 to quit:[enter] ")
    if choice == "0":
        break



