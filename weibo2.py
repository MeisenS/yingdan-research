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
            if clean_text[-2::] == '全文':
                full_text = full_tweet(cur_id)
                clean_text = clean_html(full_text)
            
            tags = extract_hashtags(clean_text)

            tweet_data = {
                'id': cur_id,
                'date': tweet_date,
                'geolocation': tweet.get('mblog').get('region_name'),
                'tweets': clean_text,
                'tags': ', '.join(tags),
                'likes': tweet.get('mblog').get('attitudes_count'),
                'comments': tweet.get('mblog').get('comments_count'),
                'reposts': tweet.get('mblog').get('reposts_count'),
                'star_id': uuid,
                'screen_name': tweet.get('mblog').get('user').get('screen_name'),
                'gender': tweet.get('mblog').get('user').get('gender'),
                'description': tweet.get('mblog').get('user').get('description'),
                'follow_count': tweet.get('mblog').get('user').get('followers_count'),
                'statuses_count': tweet.get('mblog').get('user').get('statuses_count'),
                'verification': tweet.get('mblog').get('user').get('verified'),
                'verified_reason': tweet.get('mblog').get('user').get('verified_reason'),
            }

            write_to_csv(tweet_data, headers=False)
          
            
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


def write_to_csv(tweet_data, headers=False):
    file_path = 'celeb_gov(12months).csv'
    headers = not os.path.exists(file_path)  

    df_tweet = pd.DataFrame([tweet_data])
    df_tweet.to_csv(file_path, mode='a', index=False, header=headers)


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
    for uid in need:
        if type(uid)==type(2.0):
            uid=int(uid)
        print(f"Processing: {uid}")
        get_tweets_by_date(int(uid), span=12)



if __name__ == '__main__':
    main()

