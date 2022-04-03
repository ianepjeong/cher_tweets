import requests
import os
import json
import pandas as pd
import argparse

bearer_token = '<replace with your Twitter bearer token>'
search_url = "https://api.twitter.com/2/tweets/search/recent"
query_params = {'query': '(from:cher -is:retweet)','tweet.fields': 'author_id'}

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def go_through_pages(df,token,n,oldest_id):
    page = 0
    query_params = {'query': '(from:cher -is:retweet)',
                    'tweet.fields': 'author_id',
                    'until_id': oldest_id,
                   'next_token': token}
    while page < n:
        try:
            json_response = connect_to_endpoint(search_url, query_params)
            result_df = pd.DataFrame(json_response['data'])
            df = pd.concat([df, result_df])
            token = json_response['meta']['next_token']
            oldest_id = json_response['meta']['oldest_id']
            page += 1
            if page % 50 == 0:
                print(f'got through {page} pages')
        except:
            break
    return df, json_response['meta']['next_token'], oldest_id

def save_token(token,oldest_id):
    f = open("/Users/ianjeong/Desktop/cher_tweets/next_token.txt", "w")
    f.write(token)
    f.close()

    f = open("/Users/ianjeong/Desktop/cher_tweets/oldest_id.txt", "w")
    f.write(oldest_id)
    f.close()

def main(n):
    json_response = connect_to_endpoint(search_url, query_params)
    df = pd.DataFrame(json_response['data'])
    token = json_response['meta']['next_token']
    oldest_id = json_response['meta']['oldest_id']
    result_df, next_token, oldest_id = go_through_pages(df,token,n,oldest_id)
    return result_df, next_token, oldest_id

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-n', '--n_pages', required=True, help="How many pages of tweets to query")
    ap.add_argument('-o', '--output', required=False, help="Output csv filename", default='/Users/ianjeong/Desktop/cher_tweets/tweets.csv')
    args = ap.parse_args()
    df, token, oldest_id = main(int(args.n_pages))
    df.to_csv(args.output)
    save_token(token, oldest_id)
    
    