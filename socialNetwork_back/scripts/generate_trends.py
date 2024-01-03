# -*- coding: utf-8 -*-

import django
import os
import sys



sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "socialNetwork_back.settings")
django.setup()

#https://www.geeksforgeeks.org/python-extract-hashtags-from-text/


from post.models import Post
from collections import Counter
from post.models import Post, Trend
from datetime import datetime, timedelta
from django.utils import timezone

# function to print all the hashtags in a text
def extract_hashtags(text, trends):
 
 
    # splitting the text into words
    for word in text.split():
 
        # checking the first character of every word
        if word[0] == '#':
            # adding the word
            trends.append(word[1:])
    
    return trends

for trend in Trend.objects.all():
    trend.delete()
 
#selection de tous les posts
posts = Post.objects.all()
trends = []
this_hour = timezone.now().replace(minute=0, second=0, microsecond=0)
one_day = this_hour - timedelta(hours=48)

print(Post.objects.filter(created_at__gte=(one_day)))

for post in Post.objects.filter(created_at__gte=(one_day)):
    extract_hashtags(post.body, trends)

print(trends)
#counter compte de le nbre pour chaque element et most common(5) donne le top 5
trends_counter = Counter(trends).most_common(3)

for trend in trends_counter:
    Trend.objects.create(hashtag=trend[0], occurence=trend[1])
    print(trend[0], trend[1])
    print('trend object:', Trend.objects.all())






