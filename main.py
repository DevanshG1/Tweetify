"""
Group details
1. Name: Devansh Goswami
Roll no.: 2021460
Email id: devansh21460@iiitd.ac.in 

2. Name: Zubaida Fatima
Roll no.: 2021221
Email id: zubaida21221@iiitd.ac.in

Brief description:
This code uses two APIs, twitter API and spotify API. It displays the top 10 songs by an artist in a country and shows a few tweets from the past 7 days about a specific song by the artist.
It takes as input, the name of the artist and the country code. After that it searches for the artist on spotify and finds atmost 3 artists with similar names and displays the genre of music they create.
The user then inputs a numeric value for the genre of the artist. The program displays top 10 codes, after which user is asked to input the name of the song by the artist about which they want to view tweets.

API keys:
The authorization code lines and blocks have been taken from the respective developer supports.

For spotify API, the keys are the ClientID and ClientSecret.
For twitter API, the key is the bearer_token.
"""

import requests,json,urllib.parse
import spotipy

def display(c):
    if c==1:
        print('-'*125)
        print('\n')
    else:
        print('\n')
        print('-'*125)
        print('\n')

    

display(1)
print(' '*50,'TRACKS AND TWEETS')
display(2)
print('This program shows the user top 10 tracks by an artist in a country and a few tweets about a song by the artist')
display(2)

#Please remove the client ID and Secret if you decide to show the project to the class

# ClientID = "d740ed27ad7247daa137b0a0f316034a"
# ClientSecret = "a69ad700fdee4d5d826f01130777f667"
artist = input("Enter the name of the artist: ")
print('\n')
# Country=input("Enter the country code: ")
# display(2)

# Manage = spotipy.SpotifyClientCredentials(client_id=ClientID, client_secret=ClientSecret)
# query = spotipy.Spotify(client_credentials_manager=Manage)

# results=query.search(q='artist:' + artist, type='artist', limit=3)

# #Reading from spotify API as directed by Spotify documentation

# print('\nGENRE AND POPULARITY\n')

# for i in range(len(results['artists']['items'])):
#     if results['artists']['items'][i]['genres']!=[]:
#         print(i+1,'.',end=" ")
#         print('Genre: ', end=' ')
#         print(*results['artists']['items'][i]['genres'], sep=', ')
#         print()
#         print('Popularity: ' ,results['artists']['items'][i]['popularity'])
#         print('\n')
#         print("*"*100)
#         print('\n')

# while True:        
#     ch=int(input('Select a numbered option for Genre and Popularity of the artist: '))
#     if ch<=i+1:
#         break

# display(2)

# if ch==1:
#     artistid=results['artists']['items'][0]['id']
# elif ch==2:
#     artistid=results['artists']['items'][1]['id']
# elif ch==3:
#     artistid=results['artists']['items'][2]['id']
    

# tracks = query.artist_top_tracks(artistid,country=Country)

# a=[]
# print(f'\nTHE TOP 10 SONGS OF {artist.upper()} ARE: \n')
# for i in range(10):
#         a.append(tracks["tracks"][i]['name'])
# for i in range(len(a)):
#     print(f'{i+1}. {a[i]}')

# display(2)

#twitter api starts here

music=input(f'Enter the name of the song by {artist.upper()} about which you want to see tweets: ')
print('\n')


api_url='https://api.twitter.com/2/tweets/search/recent?'
query=f'-is:retweet ({music} {artist}) OR (#{artist} #{music}) OR ({music} #{artist}) OR ({artist} #{music})'

bearer_token = 'AAAAAAAAAAAAAAAAAAAAABoLaAEAAAAA8jiS3ENVxt2AD2HZXyrPvDj05%2BU%3DsHKLRiMDay9VbzVN0EQsIIq3E7l6prYiZvUK6JkXf7bUgkAe6U'

def bearer_oauth(r):
    '''
    Method required by bearer token authentication.
    '''

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

#taken from twitter's developer support for authorization

max_results=100
url=api_url+f'query={urllib.parse.quote(query)}&max_results=100'

#urllib.parse.quote() used to do http encoding

resp=requests.get(url,auth=bearer_oauth)

res=json.loads(resp.text)

#converting string dictionary to dictionary

f=open('twit.json','w')
json.dump(res,f)
f.close()



if resp.status_code==200:
    f=open('twit.json','r')
    data=json.load(f)


c=0
tweet_set=set()

if int(data['meta']['result_count'])>=10:    
    for ele in data['data']:
        tweet_set=tweet_set|{ele['text']}
        c+=1
'''
        if len(tweet_set)>10:
            break
'''
if int(data['meta']['result_count'])<10 and int(data['meta']['result_count'])!=0:
    for ele in data['data']:
        
        tweet_set=tweet_set|{ele['text']}
        c+=1

display(1)

if int(data['meta']['result_count'])>=100:
    print(f'Count: There were over a 100 tweets about {music.upper()} by {artist.upper()} in the past week\n')
    
else:
    print(f"Count: There were {data['meta']['result_count']} tweets about {music.upper()} by {artist.upper()} in the past week\n")


j=0
if int(data['meta']['result_count'])!=0:
    print(f'Out of these, there were {len(tweet_set)} unique tweets')
    display(2)
    print('Sample tweets:\n')
    print('*'*120)
    for set_ele in tweet_set:
        if len(tweet_set)>10:
            print('\n',set_ele,'\n')
            j+=1
            if j>10:
                break
        else:   
            print('\n',set_ele,'\n')
        print('*'*120)
    display(2)
