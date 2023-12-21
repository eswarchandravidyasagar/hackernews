import streamlit as st
import requests
from datetime import datetime, timezone

# Function to check if the story is from today
def is_story_from_today(timestamp):
    story_date = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    today = datetime.now(tz=timezone.utc)
    return story_date.date() == today.date()

# Function to fetch top stories from Hacker News
def get_top_stories(limit=100):
    response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty")
    if response.status_code == 200:
        story_ids = response.json()[:limit]
        stories = []
        for story_id in story_ids:
            story_response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json?print=pretty")
            if story_response.status_code == 200:
                story_data = story_response.json()
                if is_story_from_today(story_data.get('time', 0)):
                    stories.append(story_data)
            if len(stories) >= 20:
                break
        return stories
    else:
        return []

# Streamlit app
st.title("  Top 20 latest  Hacker News Stories")

# Fetch and display stories
top_stories = get_top_stories()
for story in top_stories:
    st.subheader(story.get("title"))
    st.write(f"Score: {story.get('score')}")
    st.write(f"By: {story.get('by')}")
    url = story.get("url")
    if url:
        st.write(f"[Read More]({url})")
    st.write("---")
