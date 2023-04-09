#%%
#Getting the title of the channel
# -------------------------------------------------------------------------

from selenium import webdriver

path = "C:/Users/angelleung/Angel's Programs/chromedriver.exe"

driver = webdriver.Chrome(path)

#driver.get("http://www.youtube.com")
driver.get("https://www.youtube.com/c/Pomato%E5%B0%8F%E8%96%AF%E8%8C%84/featured")

print(driver.title)

#%%
#Name of video, views, time, url
# -------------------------------------------------------------------------
from bs4 import BeautifulSoup

# provide the url of the channel whose data you want to fetch
#urls = input("Pls provide the link of the yt channel that you would like to fetch: \n>> ")
#print(urls)
urls = ['https://www.youtube.com/c/EmilyLauszemei'] #Emily Lau
#urls = ['https://www.youtube.com/channel/UCAaGaynFpku5cAx6OOSrW-w'] #HoneyWorks
#urls = ['https://www.youtube.com/c/Pomato%E5%B0%8F%E8%96%AF%E8%8C%84/featured'] #Pomato

def main():
	path = "C:/Users/angelleung/Angel's Programs/chromedriver.exe"
	driver = webdriver.Chrome(path)
	for url in urls:
		driver.get('{}/videos?view=0&sort=p&flow=grid'.format(url))
		content = driver.page_source.encode('utf-8').strip()
		soup = BeautifulSoup(content, 'lxml')
		titles = soup.findAll('a', id='video-title')
		views = soup.findAll(
			'span', class_='style-scope ytd-grid-video-renderer')
		video_urls = soup.findAll('a', id='video-title')
		print('Channel: {}'.format(url))
		i = 0 # views and time
		j = 0 # urls

		for title in titles[:50]:
			print('\n{}\t{}\t{}\thttps://www.youtube.com{}'.format(title.text,
																views[i].text, views[i+1].text, video_urls[j].get('href')))
			i += 2
			j += 1

main()
#Reference: https://www.geeksforgeeks.org/how-to-extract-youtube-data-in-python/

#%%
# Getting channel information (Subscribers/Views/Playlist_id etc) 
# -------------------------------------------------------------------------
#Method 1 *MODIFIED
#Putting all the outputs into a (big) list
from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns

api_key = 'AIzaSyDHZQ3RhfUl98j0fbQYCnoXMPdgx35sF2U'
channel_ids = ['UCHOmxBZKt6uCFqoCvRHnSgQ', #ViuTV
               #'UCCuqona7-Ql_Dkc1IUJ2qaQ', #Emily Lau
               #'UC1Z8QzZRBv4fQ-Pd8js1rEg', #阿冰阿冰
               #'UCKZRL75vTjqbgd0WVdqF3Qg', #天月-あまつき
               #'UCLKlTvJPcIfs2f_wGMnozwA' #May in Hong Kong
               'UCgwv23FVv3lqh567yagXfNg', #DisneyMusicVEVO
               'UCAzKFALPuF_EPe-AEI0WFFw', #TwoSetViolin
               'UCLeuoGy_hUDTBf5Hk0ynrpQ', #DisneyChannelUK
               'UCvC4D8onUfXzvjTOM-dBfEA'#Marvel
               ]
               
#get the youtube service
youtube = build('youtube','v3',developerKey=api_key) #service name, version

def get_channel_stats(youtube,channel_ids):
    all_data = []

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        #convert the list into a string
        id = ','.join(channel_ids)
    )
    response = request.execute()
    #return response #==> output as json file

    for i in range(len(response['items'])):
        data = dict(Channel_name = response['items'][i]['snippet']['title'],
                Subscribers = response['items'][i]['statistics']['subscriberCount'],
                Views = response['items'][i]['statistics']['viewCount'],
                VideoCount = response['items'][i]['statistics']['videoCount'],
                PlayList_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads']) #,
                #Description = response['items'][i]['snippet']['description'])
        all_data.append(data)
    return all_data #response #data

get_channel_stats(youtube,channel_ids)

channel_statistics = get_channel_stats(youtube,channel_ids)
channel_data = pd.DataFrame(channel_statistics)
#channel_data = channel_data.set_index('Channel_name') #Set Name as index
channel_data

#visualization
#Change the data types from "object" to numeric to proceed
channel_data['Subscribers']=pd.to_numeric(channel_data['Subscribers'])
channel_data['Views']=pd.to_numeric(channel_data['Views'])
channel_data['VideoCount']=pd.to_numeric(channel_data['VideoCount'])
channel_data.dtypes #Check the types of data

sns.set(rc={'figure.figsize':(10,8)})
ax = sns.barplot(x='Channel_name',y='Subscribers',data=channel_data)
ax = sns.barplot(x='Channel_name',y='Views',data=channel_data)
ax = sns.barplot(x='Channel_name',y='VideoCount',data=channel_data)

#locatinh
playlist_id = channel_data.loc[channel_data['Channel_name']=='TwoSetViolin','PlayList_id'].iloc[0]
playlist_id

#Function to get video IDs
def fetch_video_ids(youtube,playlist_id):
    request = youtube.playlistItems().list(
        part = 'contentDetails',
        playlistId = playlist_id,
        maxResults = 50) #50 is the max value that can be passed
    response = request.execute()
    #return response

    video_ids = []

    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])
    
    #Loop over ever page to get ALL video ids presents
    next_page_token = response.get('nextPageToken') #Will return False if not detected
    more_pages = True

    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
                request = youtube.playlistItems().list(
                    part = 'contentDetails',
                    playlistId = playlist_id,
                    maxResults = 50, #50 is the max value that can be passed
                    pageToken = next_page_token) 
                response = request.execute()

                for i in range(len(response['items'])):
                    video_ids.append(response['items'][i]['contentDetails']['videoId'])
                
                next_page_token = response.get('nextPageToken')

    return video_ids #response
#1354

video_ids = fetch_video_ids(youtube,playlist_id)
#video_ids

#Function to get video details
def get_video_details(youtube, video_ids):
    all_video_stats = []
    video_error = []
    for i in range(0,len(video_ids),50): #50 videos at a time
        request = youtube.videos().list(
        part="snippet,statistics",
        #Convert list into a string
        id=','.join(video_ids[i:i+50])) #Max pass 50 items at a time
        response = request.execute()
        
        try:
            for video in response['items']:
                video_stats = dict(Title = video['snippet']['title'],
                Published_date = video['snippet']['publishedAt'],
                Views = video['statistics']['viewCount'],
                Likes = video['statistics']['likeCount'] ,
                Comments = video['statistics']['commentCount']
                )
            all_video_stats.append(video_stats)
        except: #On error go to
            for video in response['items']:
                video_stats = dict(Title = video['snippet']['title'],
                #Published_date = video['snippet']['publishedAt'], 
                Views = video['statistics']['viewCount'],
                Likes = video['statistics']['likeCount']
                #Comments = video['statistics']['commentCount'] 
                )
            video_error.append(video_stats)
            #print(video_error)

    return response #len(all_video_stats)+len(video_error)

video_details = get_video_details(youtube,video_ids)
video_data = pd.DataFrame(video_details)
video_data

# %%
# Getting channel information (Subscribers/Views/Playlist_id etc) 
# -------------------------------------------------------------------------
#Method1: by Channel ID
#ID checker: https://commentpicker.com/youtube-channel-id.php

from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns

api_key = 'AIzaSyDHZQ3RhfUl98j0fbQYCnoXMPdgx35sF2U'
channel_id = 'UCHQoZ0_MHDXIgWeRvPTLTJw' #pomato
channel_ids = ['UCHOmxBZKt6uCFqoCvRHnSgQ', #ViuTV
               #'UCCuqona7-Ql_Dkc1IUJ2qaQ', #Emily Lau
               #'UC1Z8QzZRBv4fQ-Pd8js1rEg', #阿冰阿冰
               #'UCKZRL75vTjqbgd0WVdqF3Qg', #天月-あまつき
               #'UCLKlTvJPcIfs2f_wGMnozwA' #May in Hong Kong
               'UCgwv23FVv3lqh567yagXfNg', #DisneyMusicVEVO
               'UCAzKFALPuF_EPe-AEI0WFFw', #TwoSetViolin
               'UCLeuoGy_hUDTBf5Hk0ynrpQ', #DisneyChannelUK
               'UCvC4D8onUfXzvjTOM-dBfEA'#Marvel
               ]

#get the youtube service
youtube = build('youtube','v3',developerKey=api_key) #service name, version

#---Function to get channel statistics---
def get_channel_stats(youtube,channel_id):
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channel_id
    )
    response = request.execute()
    #return response #==> output as json file

    #data = response['items'][0]['snippet']['title'] #fetch title
    data = dict(Channel_name = response['items'][0]['snippet']['title'],
                Subscribers = response['items'][0]['statistics']['subscriberCount'],
                Views = response['items'][0]['statistics']['viewCount'],
                VideoCount = response['items'][0]['statistics']['videoCount'],
                PlayList_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']) #,
                #Description = response['items'][0]['snippet']['description'])
    return data

#get_channel_stats(youtube,channel_id)
print(get_channel_stats(youtube,channel_id))

all_data = []
for i in channel_ids:
    channel_id = i
    print(f"\nID: {channel_id}")
    print(get_channel_stats(youtube,channel_id))
    all_data.append(get_channel_stats(youtube,channel_id))
#print(f"all_data:{all_data}")

channel_data = pd.DataFrame(all_data)
channel_data

# %% -------------------------------------------------------------------------
#Method2: by youtube username

from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns

api_key = 'AIzaSyDHZQ3RhfUl98j0fbQYCnoXMPdgx35sF2U'
#ONLY "GoogleDevelopers" worked!!!!
channel_name = "GoogleDevelopers" #"Pomato小薯茄" #"Viu TV"

youtube = build('youtube','v3',developerKey=api_key) #service name, version

#---Function to get channel statistics---
def get_channel_stats(youtube,channel_name):
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        #id=channel_id,
        #forUsername= "GoogleDevelopers"
        forUsername= channel_name
    )
    response = request.execute()

    data = dict(Channel_name = response['items'][0]['snippet']['title'],
                Subscribers = response['items'][0]['statistics']['subscriberCount'],
                Views = response['items'][0]['statistics']['viewCount'],
                VideoCount = response['items'][0]['statistics']['videoCount'],
                Description = response['items'][0]['snippet']['description'],
                PlayList_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads'])
    return data #response #data

#get_channel_stats(youtube,channel_name)
print(f"\n{get_channel_stats(youtube,channel_name)}")
