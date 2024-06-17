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
    all_tags = []  # This will store a list of lists of tags

    for tweet in get_weibo_tweets(tweet_container_id=get_tweet_containerid(uid=uuid), pages=100):
        tweet_date_str = tweet['mblog']['created_at']
        tweet_date = datetime.datetime.strptime(tweet_date_str, '%a %b %d %H:%M:%S %z %Y')

        if tweet_date > six_months_ago:
            tweet_text = tweet.get('mblog').get('text')
            clean_text = clean_html(tweet_text)
            tags = extract_hashtags(clean_text)
            tweets.append(clean_text)
            all_tags.append(tags)  # Append the list of tags for each tweet
        else:
            break

    return tweets, all_tags


def load_file(file_path):
    df = pd.read_excel(file_path, engine='openpyxl')
    return df['uid_star'].tolist()

def write_to_excel(tweets, tags):
    df = pd.DataFrame({
        'tweets': tweets,
        'tags': [', '.join(tag_list) for tag_list in tags]  # Convert list of tags to comma-separated strings
    })
    excel_file_path = 'tweet_texts.xlsx'
    df.to_excel(excel_file_path, index=False, engine='openpyxl')
    print(f"Data has been saved to {excel_file_path}")



def clean_html(html_content):
    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract text from the BeautifulSoup object
    text = soup.get_text(separator=' ')
    
    return text

def extract_hashtags(text):
    # Regex to find hashtags: \#\w+
    hashtags = re.findall(r'\#\w+', text)
    return hashtags


def main():
    namelist = load_file('taiwan_celeb.xlsx')
    for name in namelist:
        print(f"Processing: {name}")
        twitext, tags = get_tweets_by_date(name, span=6)
        write_to_excel(twitext, tags)


if __name__ == '__main__':
    main()
