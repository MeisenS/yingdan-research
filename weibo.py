import datetime
from weibo_scraper import *
from dateutil import tz
import pandas as pd


def get_tweets_by_date(weiboname, span:int):
    now = datetime.datetime.now(tz=tz.tzlocal())
    six_months_ago = now - datetime.timedelta(days=span*30)  
    
    for tweet in get_weibo_tweets_by_name(name = weiboname, pages=100):  
       
        tweet_date_str = tweet['mblog']['created_at']
        tweet_date = datetime.datetime.strptime(tweet_date_str, '%a %b %d %H:%M:%S %z %Y')

        if tweet_date > six_months_ago:
            print(tweet.get('mblog').get('text'))
        else:
            break



def laod_file(file_path):
    df = pd.read_excel(file_path, engine='openpyxl')
    names = df['name']  

    return names.tolist()


def main():
    namelist = laod_file('taiwan_celeb.xlsx')
    print(namelist[0])
    get_tweets_by_date(namelist[0],span=12)


if __name__ == '__main__':
    main()