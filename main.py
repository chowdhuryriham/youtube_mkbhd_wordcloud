import nltk
nltk.download('punkt')
nltk.download('stopwords')
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from os import path, getcwd
import PIL.Image
from langdetect import detect
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from youtube_transcript_api import YouTubeTranscriptApi

from googleapiclient.discovery import build
# Your API key (Replace with your actual API key)
api_key = 'AIzaSyAFmImey5MdQd3dX4qXpibPzUhTEF7bxOU'

# Playlist ID from the provided URL
playlist_id = 'PLBsP89CPrMeM2MmF4suOeT0vsic9nEC2Y'

# Placeholder function to retrieve video transcript (simulated)
def get_video_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = ''
        
        for transcript in transcript_list:
            # Check the language of each transcript
            language = detect(transcript['text'])
            
            # Check if the detected language is English ('en')
            if language == 'en':
                transcript_text += transcript['text'] + ' '
        
        return transcript_text

    except Exception as e:
        print("An error occurred:", e)
        return None

def punctuation_stop(text):
    try:
        if text is None:
            print("Input text is None.")
            return None
        # Remove punctuation from the text
        cleaned_text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Tokenize the text into words
        word_tokens = word_tokenize(cleaned_text)
        
        # Get the list of English stopwords
        stop_words = set(stopwords.words('english'))
        
        # Remove stopwords and filter out non-alphabetic words
        filtered_words = [word.lower() for word in word_tokens if word.lower() not in stop_words and word.isalpha()]
        
        # Join the filtered words back into a sentence
        filtered_text = ' '.join(filtered_words)
        
        return filtered_text
    except Exception as e:
        print("An error occurred while processing text:", e)
        return None

# YouTube playlist URL or ID (Replace with your playlist)

def get_video_ids_from_playlist(playlist_id,api_key):
    # Build the YouTube Data API service
    youtube = build('youtube', 'v3', developerKey=api_key)
    video_ids = []

    # Retrieve videos from the playlist
    next_page_token = None
    while True:
        playlist_items = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50,  # Adjust as needed
            pageToken=next_page_token if next_page_token else ''
        ).execute()

        # Extract video IDs from the playlist
        for item in playlist_items['items']:
            video_id = item['contentDetails']['videoId']
            video_ids.append(video_id)

        next_page_token = playlist_items.get('nextPageToken')

        if not next_page_token:
            break

    return video_ids

# Get video transcripts from the playlist

video_ids = get_video_ids_from_playlist(playlist_id,api_key)

all_text = ""
for video_id in video_ids:
    transcript = get_video_transcript(video_id)
    if transcript is not None:
        # Process the transcript text
        filtered_text = punctuation_stop(transcript)
        # Remove unwanted words
        all_text += filtered_text + " "

# Get the current working directory
directory = getcwd()
print(all_text) 
# Load an image file as a mask for the word cloud (Replace with your image file)

youtube_logo= np.array(PIL.Image.open("youtube_social_icon_red.png"))

# Generate the word cloud
wordcloud = WordCloud(mask=youtube_logo,background_color="white").generate(all_text)

# Display the WordCloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')

# Overlay the word cloud on the YouTube logo
plt.imshow(youtube_logo, aspect='auto', extent=plt.gca().get_xlim() + plt.gca().get_ylim(), alpha=0.5)
plt.show()
