import unicodedata
import pandas as pd
import os
import emot
import sys
import re

def keep_chr(ch):
    '''
    Find all characters that are classifed as punctuation in Unicode
    (except #, @, &) and combine them into a single string.
    '''
    return unicodedata.category(ch).startswith('P') and \
        (ch not in ("#", "@", "&"))

STOP_PREFIXES = ("@", "#", "http")
PUNCTUATION = " ".join([chr(i) for i in range(sys.maxunicode)
                        if keep_chr(chr(i))])
EMOT_OBJ = emot.core.emot() 

def process_string_data(tweets, case_sensitive):
    '''
    Turn the text of a tweet into a list of strings of interest.
    Excluded from the return list are:
    leading and trailing punctuations; hashtags; strings that yield empty
    after punctuations are removed; URLs, and mentions
    Inputs:
        tweets: pd Series
    Returns: list of lists of strings
    '''

    lst_tweets = []

    for _, tweet in tweets.iteritems():
        lst = []
        for word in tweet.split():
            word = word.strip(PUNCTUATION)
            word = word.strip("'s'")
            if not word:
                continue
            if not case_sensitive:
                word = word.lower()
            if word.startswith(STOP_PREFIXES):
                continue
            for w in re.split(',|\.|\”', word):
                if not len(w):
                    continue
                lst_word = deal_with_emoji(w)
                lst.extend(lst_word)
        lst_tweets.append(lst)

    return lst_tweets

def deal_with_emoji(word):
    '''
    Extract emojis and words from a compound of emojis and words.

    Input:
        word: str

    Returns: lst of str
    '''
    word = word.strip(PUNCTUATION)
    emoji_info= EMOT_OBJ.emoji(word)
    # BASE CASE
    if not emoji_info['value']:
        if not len(word):
            return []
        return [word]
    # RECURSIVE CASE
    lst = []
    pre = word[:emoji_info['location'][0][0]]
    if len(pre):
        lst.append(pre)
    lst.append(emoji_info['value'][0])
    post = word[emoji_info['location'][0][1]:]
    for x in deal_with_emoji(post):
        if len(x) and x == '️':
            continue
        lst.append(x)
    return lst