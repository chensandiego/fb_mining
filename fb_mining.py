
##https://developers.facebook.com/tools/explorer/
ACCESS_TOKEN=''

import requests

import json


base_url='https://graph.facebook.com/me'

fields='id,name,likes'

url='{0}?fields={1}&access_token={2}'.format(base_url,fields,ACCESS_TOKEN)

print(url)


content=requests.get(url).json()
print(json.dumps(content,indent=1))

#pip install facebook-sdk
import facebook
g=facebook.GraphAPI(ACCESS_TOKEN,version='2.7')
print(g.get_object('me'))

print(g.request("search",{'q':'Minning the web','type':'page'}))

print(g.get_connections(id='143246499557541',connection_name='likes'))
print(g.request("search",{'q':'Carina Lee','type':'user'}))


#brand analysis for facebook ''
taylor_swift_id='19614945368'
drake_id='83711079303'
beyonce_id='28940545600'



def get_total_fans(page_id):
    return int(g.get_object(id=page_id,fields=['fan_count'])['fan_count'])


def retrieve_page_feed(page_id,n_posts):
    """retrieve the first n_posts from a page feed in reverse chronological order"""
    feed=g.get_connections(page_id,'posts')
    posts=[]
    posts.extend(feed['data'])

    while len(posts)<n_posts:
        try:
            feed=requests.get(feed['paging']['next']).json()
            posts.extend(feed['data'])
        except  KeyError:
            print('reached end of feed')
            break

    if len(posts)>n_posts:
        posts=posts[:n_posts]
    print('{} item retrieved from feed'.format(len(posts)))
    return posts


print(retrieve_page_feed(drake_id,25))



def get_post_message(post):
    try:
        message=post['story']
    except KeyError:
        pass
    try:
        message=post['message']
    except KeyError:
        message=''
    return message.replace('\n',' ')




twift_fans=get_total_fans(taylor_swift_id)

drake_fans=get_total_fans(drake_id)

beyonce_fans=get_total_fans(beyonce_id)

#get total fans from three artists
print('Taylor Swift: {0} fans on Facebook'.format(twift_fans))

print('Drake: {0} fans on Facebook'.format(drake_fans))

print('Beyonce : {0} fans on Facebook'.format(beyonce_fans))


for artist in [taylor_swift_id,drake_id,beyonce_id]:
    print()
    feed=retrieve_page_feed(artist,5)
    for i, post in enumerate(feed):
        message=get_post_message(post)[:50]
        print('{0} - {1}'.format(i+1,message))




#measure fans engagement
def measure_reaction(post_id):
    """return number of likes,shares,and comments on a given post """

    likes=g.get_object(id=post_id,fields=['likes.limit(0).summary(true)'])['likes']['summary']['total_count']
    shares=g.get_object(id=post_id,fields=['shares.limit(0).summary(true)'])['shares']['count']
    comments=g.get_object(id=post_id,fields=['comments.limit(0).summary(true)'])['comments']['summary']['total_count']
    return likes,shares,comments


def measure_engagement(post_id,total_fans):
    """return the percentage of engagement from fans"""
    likes=g.get_object(id=post_id,fields=['likes.limit(0).summary(true)'])['likes']['summary']['total_count']
    sharess=g.get_object(id=post_id,fields=['shares.limit(0).summary(true)'])['shares']['count']
    comments=g.get_object(id=post_id,fields=['comments.limit(0).summary(true)'])['comments']['summary']['total_count']

    likes_pct=likes/total_fans *100.0
    shares_pct=shares/total_fans *100.0
    comments_pct=comments/total_fans *100.0
    return likes_pct,shares_pct,comments_pct


###retrieve last 5 msg from feeds print the reaction and level of engagement

artist_dict={'Taylor Swift':taylor_swift_id,
            'Drake':drake_id,
            'Beyonce':beyonce_id}


for name,page_id in artist_dict.items():
    print()
    print(name)
    print('---------------------------')
    feed=retrieve_page_feed(page_id,5)
    total_fans=get_total_fans(page_id)

    for i,post in enumerate(feed):
        message=get_post_message(post)[:30]
        post_id=post['id']
        likes,shares,comments=measure_reaction(post_id)
        likes_pct,shares_pct,comments_pct=measure_engagement(post_id,total_fans)

        print('{0} - {1}'.format(i+1,message))
        print('     Likes:{0} ({1:7.5f}%)'.format(likes,likes_pct))
        print('     Shares:{0} ({1:7.5f}%)'.format(shares,shares_pct))
        print('     Comments:{0} ({1:7.5f}%)'.format(comments,comments_pct))




import pandas as pd
import matplotlib

columns=['Name','Total Fans','Post Number','Post Date','Headline','Likes','Shares','Comments','Rel. likes','Rel. Shares','Rel. Comments']

musicians = pd.DataFrame(columns=columns)

for page_id in [taylor_swift_id,drake_id,beyonce_id]:
    name=g.get_object(id=page_id)['name']
    fans=get_total_fans(page_id)
    feed=retrieve_page_feed(page_id,10)
    for i,post in enumerate(feed):
        likes,shares,comments=measure_reaction(post['id'])
        likes_pct,shares_pct,comments_pct=measure_engagement(post['id'],fans)
        musicians=musicians.append({'Name':name,'Total Fans':fans,'Post Number':i+1,
                                    'Post Date':post['created_time'],
                                    'Headline':get_post_message(post),
                                    'Likes':likes,
                                    'Shares':shares,
                                    'Comments':comments,
                                    'Rel. likes':likes_pct,
                                    'Rel. shares':shares_pct,
                                    'Rel. Comments':comments_pct},ignore_index=True)


for col in ['Post Number','Total Fans','Likes','Shares','Comments']:
    musicians[col]=musicians[col].astype(int)


print (musicians.head())






musicians[musicians['Name']=='Drake'].plot(x='Post Number',y='Likes',kind='bar')

musicians[musicians['Name']=='Drake'].plot(x='Post Number',y='Shares',kind='bar')

musicians[musicians['Name']=='Drake'].plot(x='Post Number',y='Comments',kind='bar')


musicians[musicians['Name']=='Drake'].plot(x='Post Number',y='Rel. likes',kind='bar')

musicians[musicians['Name']=='Drake'].plot(x='Post Number',y='Rel. shares',kind='bar')

musicians[musicians['Name']=='Drake'].plot(x='Post Number',y='Rel. Comments',kind='bar')



musicians=musicians.set_index(['Name','Post Number'])

musicians.head()

musicians.unstack(level=0)


#calculate avg. engagement


print('Avg likes/ total fans')
print(musicians.unstack(level=0)['Rel. likes'].mean())


print('Avg shares/ total fans')
print(musicians.unstack(level=0)['Rel. shares'].mean())


print('Avg Comments/ total fans')
print(musicians.unstack(level=0)['Rel. Comments'].mean())
