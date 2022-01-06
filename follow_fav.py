import tweepy
import time
import datetime
import random

# キーワードに対してふぁぼる
def fav(query,api):
    posts = api.search_tweets(q=query, count=20)
    for post in posts:
        try:
            api.create_favorite(post.id)
        except Exception as e:
            print(e)
            pass
        time.sleep(5)

def follow(screen_name,api):

    followers = api.get_follower_ids(screen_name=screen_name)
    ran = random.randint(0,len(followers)-1)
    followers = followers[ran:ran + 100]

    for i in followers:
        try:
            user = api.get_user(id=i)
            followers_count = int(user.followers_count)
            friends_count = int(user.friends_count)

            if followers_count > 100 and friends_count > 100 and followers_count / friends_count < 1 and followers_count / friends_count > 0.5 and int(user.status.created_at.strftime('%Y%m%d')) > 20210610:
                api.create_friendship(id=user.id)
                print('フォロー数',friends_count,'フォロワー数',followers_count,'フォローしました')
            else:
                print('フォロー数',friends_count,'フォロワー数',followers_count,'フォローしませんでした')
            n = n + 1
            time.sleep(1)
        except Exception as e:
            print(e)
            pass

# 日曜日にフォロー解除を行う。それ以外はふぁぼる。
def followdestroy(api):
    followers = api.get_follower_ids(user_id='IFD_OCO3')
    friends = api.get_friend_ids(user_id='IFD_OCO3')

    if datetime.date.today().weekday() == 6:
        for f in friends:
            if f not in followers:
                print("ID:{}のフォローを解除します".format(api.get_user(user_id=f).screen_name))
                if api.get_user(user_id=f).screen_name != 'hirosetakao':
                    api.destroy_friendship(user_id=f)
    else:
        for f in friends:
            if f not in followers:
                tweets = api.user_timeline(id=f, count=2)
                for tweet in tweets:
                    print("=============================")
                    print(tweet.text)
                    try:
                        api.create_favorite(tweet.id)
                    except Exception as e:
                        print(e)

