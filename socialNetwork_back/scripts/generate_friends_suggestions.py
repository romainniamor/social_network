# -*- coding: utf-8 -*-

import django
import os
import sys



sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "socialNetwork_back.settings")
django.setup()

#https://www.geeksforgeeks.org/python-extract-hashtags-from-text/


from account.models import User

users = User.objects.all()

#suggested friends of friends
#simply case, app suggests friends of friends

for user in users:
    user.people_you_may_know.clear()
    print("find friends for", user)
    for friend in user.friends.all():
        print(user, 'is friend with', friend)
        for friendsfriend in friend.friends.all():
            if friendsfriend not in user.friends.all() and friendsfriend != user:
                print('sugested:', friendsfriend)
                user.people_you_may_know.add(friendsfriend)

        

# function to print all the hashtags in a text