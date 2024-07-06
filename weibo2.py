import datetime
import pandas as pd
from weibo_scraper import *
from dateutil import tz
from bs4 import BeautifulSoup
import re
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_tweets_by_date(uuid, span):
    now = datetime.datetime.now(tz=tz.tzlocal())
    six_months_ago = now - datetime.timedelta(days=span*30)
    ids = []
    dates = []

    tweets = []
    all_tags = [] 
    likes = []
    comments = []
    reposts = []
    geolocation = []

    screenName = ''
    verified_reason = ''
    description = ''
    followers = ''
    statuses = ''
    verification = ''
    gender = ''
   
    zhiding = 0

    for tweet in get_weibo_tweets(tweet_container_id=get_tweet_containerid(uid=uuid), pages=100):
       
        tweet_date_str = tweet['mblog']['created_at']
        tweet_date = datetime.datetime.strptime(tweet_date_str, '%a %b %d %H:%M:%S %z %Y')

        if tweet_date > six_months_ago:
            tweet_text = tweet.get('mblog').get('text')
            clean_text = clean_html(tweet_text)
            cur_id = tweet.get('mblog').get('id')

            if(clean_text[-2::]=='全文'):
                neww=full_tweet(cur_id)
                tweets.append(neww)
                tags = extract_hashtags(neww)
            else:
                tweets.append(clean_text)
                tags = extract_hashtags(clean_text)
            all_tags.append(tags)  
            ids.append(cur_id)
            dates.append(tweet_date)
            likes.append(tweet.get('mblog').get('attitudes_count'))
            comments.append(tweet.get('mblog').get('comments_count'))
            reposts.append(tweet.get('mblog').get('reposts_count'))

            screenName = tweet.get('mblog').get('user').get('screen_name')
            verified_reason = tweet.get('mblog').get('user').get('verified_reason')
            description = tweet.get('mblog').get('user').get('description')
            followers = tweet.get('mblog').get('user').get('followers_count')
            statuses = tweet.get('mblog').get('user').get('statuses_count')
            verification = tweet.get('mblog').get('user').get('verified')
            gender = tweet.get('mblog').get('user').get('gender')
            geolocation.append(tweet.get('mblog').get('region_name'))
            
            if zhiding < 5:
                zhiding += 1
        elif(zhiding >= 5 and tweet_date <= six_months_ago):
            break

    return ids, dates, tweets, all_tags, likes, comments, reposts, uuid,screenName, description, followers, statuses, verification,verified_reason, gender, geolocation

def full_tweet(id):
    driver = webdriver.Chrome()
    url = 'https://m.weibo.cn/detail/'+id
    driver.get(url)
    text_box = driver.find_element(By.CLASS_NAME, "weibo-text")
    return(text_box.text)



def load_excel_as_json(file_path):
    df = pd.read_excel(file_path, engine='openpyxl')
    json_data = df.to_json(orient='records', force_ascii=False)
    final = json.loads(json_data)
    return final


def write_to_csv(ids, dates, tweets, tags, likes, comments, reposts, uuid,screenName, description, followers, statuses, verification,verified_reason, gender, geolocation):
   
    df_tweets = pd.DataFrame({
        'id': ids,
        'date': dates,
        'geolocation' : geolocation,
        'tweets': tweets,
        'tags': [', '.join(tag_list) for tag_list in tags],
        'likes': likes,
        'comments': comments,
        'reposts': reposts,
        'star_id' : uuid,
        'screen_name' : screenName,
        'gender' : gender,
        'description' : description,
        'follow_count' : followers,
        'statuses_count' : statuses,
        'verification' : verification,
        'verified_reason' : verified_reason,
        
    })

    file_path = 'celeb_gov(12months).csv'
    headers = not os.path.exists(file_path)

    df_tweets.to_csv(file_path, mode='a', index=False, header = headers)
    
    print(f"Data has been saved for {screenName}")

def write_other_page():
    pass


def clean_html(html_content):

    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator=' ')

    return text

def extract_hashtags(text):
    hashtags = re.findall(r'\#\w+', text)
    return hashtags

def main():
    name_uid_dict = load_excel_as_json('celebrity_media_gov.xlsx')
    need = []
    for item in name_uid_dict:
        need.append(item['uid_star'])
        need.append(item['province_media_uid'])
        need.append(item['city_media_uid'])
        need.append(item['province_gov_uid'])
        need.append(item['city_gov_uid'])
    need=set(need)
    for item in need:
        print(f"Processing: {item}")
        if type(item) == type(2.0):
            item = int(item)
        ids, dates, tweets, all_tags, likes, comments, reposts, uuid,screenName, description, followers, statuses, verification,verified_reason, gender, geolocation = get_tweets_by_date(item, span=12)
        write_to_csv(ids, dates, tweets, all_tags, likes, comments, reposts, uuid,screenName, description, followers, statuses, verification,verified_reason, gender, geolocation)
       
if __name__ == '__main__':
    main()

