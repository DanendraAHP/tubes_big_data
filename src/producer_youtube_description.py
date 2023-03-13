import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from time import sleep
#from kafka import KafkaProducer
import urllib.parse as p
import os
import pickle

# producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
#                          value_serializer=lambda x:
#                          x.encode('utf-8'))

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def youtube_authenticate():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "../config/credential.json"
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build(api_service_name, api_version, credentials=creds)
def get_video_id_by_url(url):
    """
    Return the Video ID from the video `url`
    """
    # split URL parts
    parsed_url = p.urlparse(url)
    # get the video ID by parsing the query of the URL
    video_id = p.parse_qs(parsed_url.query).get("v")
    if video_id:
        return video_id[0]
    else:
        raise Exception(f"Wasn't able to parse video URL: {url}")
def get_video_details(youtube, **kwargs):
    return youtube.videos().list(
        part="snippet,contentDetails,statistics",
        **kwargs
    ).execute()
def search(youtube, **kwargs):
    return youtube.search().list(
        part="snippet",
        **kwargs
    ).execute()
def create_message(video_id, video_response):
    items = video_response.get("items")[0]
    # get the description
    snippet         = items["snippet"]
    description   = snippet["description"]
    publish_time  = snippet["publishedAt"]
    return {
        'video id' : video_id,
        'description':description,
        'publish time' : publish_time
    }

# authenticate to YouTube API, only do this for first time using the script
youtube = youtube_authenticate()

#loop till the end of time
while True:
    response = search(youtube, q="python", maxResults=50)
    items = response.get("items")
    for item in items:
        try:
            # get the video ID
            video_id = item["id"]["videoId"]
            # get the video details
            video_response = get_video_details(youtube, id=video_id)
            # print the video details
            message = create_message(video_id, video_response)
            #producer.send('youtube-api', value=message)
            print(message)
            print("="*50)
        except:
            continue
    sleep(10)