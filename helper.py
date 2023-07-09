import seaborn as sns
from urlextract import URLExtract

from collections import Counter
import pandas as pd

extractor = URLExtract()


def fetch_stats(selected_user, data1):
    if selected_user != 'overall':
        data1 = data1[data1['user'] == selected_user]

    num_messages = data1.shape[0]
    words = []
    for message in data1['message']:
        words.extend(message.split())

        # fetch number of media messages
        num_media_messages = data1[data1['message'] == '<Media omitted>/n'].shape[0]

        # Fetch number of links
        links = []
        for message in data1['message']:
            links.extend(extractor.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(data1):
    x = data1['user'].value_counts().head()
    data1 = round((data1['user'].value_counts() / data1.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percentage'})
    return x, data1


def most_common_words(selected_user, data1):
    f = open('stop_words', 'r')
    stop_words = f.read()
    if selected_user != 'overall':
        data1 = data1[data1['user'] == selected_user]

    temp = data1[data1['user'] != 'Notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.extend(word)

    df = pd.DataFrame(Counter(words).most_common(20))
    return df


def daily_time(selected_user, data1):
    if selected_user != 'overall':
        data1 = data1[data1['user'] == selected_user]
    daily_timeline = data1.groupby('date2').count()['message'].reset_index()

    return daily_timeline
def weekly_activity(selected_user,data1):
    if selected_user != 'overall':
        data1 = data1[data1['user'] == selected_user]

    return data1['day1'].value_counts()
def monthly_activity_map(selected_user,data1):
    if selected_user != 'overall':
        data1 = data1[data1['user'] == selected_user]
    return data1['month'].value_counts()

def Activity_heatmap(selected_user,data1):
    if selected_user != 'overall':
        data1 = data1[data1['user'] == selected_user]

    heatmap = data1.pivot_table(index='day1', columns='period', values='message', aggfunc='count').fillna(0)
    return heatmap
