import datetime
import pandas as pd
from weibo_scraper import *
from dateutil import tz
from bs4 import BeautifulSoup
import re

def get_tweets_by_date(uuid, span):
    now = datetime.datetime.now(tz=tz.tzlocal())
    six_months_ago = now - datetime.timedelta(days=span*30)
    tweets = []
    all_tags = [] 
    likes = []
    comments = []
    reposts = []

    description = ''
    followers = ''
    statuses = ''
    verification = ''
    gender = ''
    geolocation = ''

    zhiding = 0

    for tweet in get_weibo_tweets(tweet_container_id=get_tweet_containerid(uid=uuid), pages=100):
       
        tweet_date_str = tweet['mblog']['created_at']
        tweet_date = datetime.datetime.strptime(tweet_date_str, '%a %b %d %H:%M:%S %z %Y')

        if tweet_date > six_months_ago:
            tweet_text = tweet.get('mblog').get('text')
            clean_text = clean_html(tweet_text)
            tags = extract_hashtags(clean_text)

            tweets.append(clean_text)
            all_tags.append(tags)  
            likes.append(tweet.get('mblog').get('attitudes_count'))
            comments.append(tweet.get('mblog').get('comments_count'))
            reposts.append(tweet.get('mblog').get('reposts_count'))

            description = tweet.get('mblog').get('user').get('description')
            followers = tweet.get('mblog').get('user').get('followers_count')
            statuses = tweet.get('mblog').get('user').get('statuses_count')
            verification = tweet.get('mblog').get('user').get('verified')
            gender = tweet.get('mblog').get('user').get('gender')
            geolocation = tweet.get('mblog').get('user').get('region_name')
            if zhiding < 5:
                
                zhiding += 1
        elif(zhiding >= 5 and tweet_date <= six_months_ago):
            break
            
                
        
    return tweets, all_tags, likes, comments, reposts, uuid, description, followers, statuses, verification, gender, geolocation


def load_file(file_path):
    df = pd.read_excel(file_path, engine='openpyxl')
    return dict(zip(df['name'], df['uid_star']))


def write_to_excel(names, tweets, tags, likes, comments, reposts, uuid, description, followers, statuses, verification, gender, geolocation):
    df = pd.DataFrame({
        'tweets': tweets,
        'tags': [', '.join(tag_list) for tag_list in tags],  # Convert list of tags to comma-separated strings
        'likes':likes,
        'comments':comments,
        'reposts':reposts,
    })
    
    df2= pd.DataFrame({
        'uid': uuid,
        'description': description,
        'followers':followers,
        'statuses':statuses,
        'verification':verification,
        'gender':gender,
        'geolocation':geolocation,
    },index=[0])
    
    with pd.ExcelWriter(names+'_tweet_texts.xlsx') as writer:
   
        df2.to_excel(writer, sheet_name="basic_info", index=False)
        df.to_excel(writer, sheet_name="tweets_within_6months", index=False)

    print(f"Data has been saved")


def clean_html(html_content):

    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator=' ')

    return text

def extract_hashtags(text):
    hashtags = re.findall(r'\#\w+', text)
    return hashtags

def main():
    name_uid_dict = load_file('taiwan_celeb.xlsx')
    for name, uuid in name_uid_dict.items():
        print(f"Processing: {name} with UID: {uuid}")
        tweets, tags, likes, comments, reposts, uuid, description, followers, statuses, verification, gender, geolocation= get_tweets_by_date(uuid, span=6)
        write_to_excel(name, tweets, tags, likes, comments, reposts, uuid, description, followers, statuses, verification, gender, geolocation)

if __name__ == '__main__':
    main()

