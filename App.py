from collections import Counter

import helper
import emoji

import pandas as pd
import streamlit as st
import seaborn as sns
import Preprocessor

import matplotlib.pyplot as plt

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a File")
if uploaded_file is not None:
    bytes = uploaded_file.getvalue()
    data = bytes.decode('utf-8')
    data1 = Preprocessor.preprocessor(data)

    st.dataframe(data1)
    # fetch unique user
    user_list = data1['user'].unique().tolist()
    user_list.remove('Notification')
    user_list.sort()
    user_list.insert(0, "overall")

    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, data1)
        st.title("Top statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Total links shared")
            st.title(num_links)



        #Daily Timeline
        st.title("Daily Time")
        daily_timeline = helper.daily_time(selected_user, data1)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['date2'],daily_timeline['message'], color="black")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity map
        st.title('Weekly Activiy Map')
        col1,col2=st.columns(2)

        with col1:
            st.header("Most busy Weeks")
            busy_day=helper.weekly_activity(selected_user, data1)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most busy Months")
            busy_month = helper.monthly_activity_map(selected_user, data1)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Heatmap")
        user_heatmap=helper.Activity_heatmap(selected_user,data1)
        fig,ax=plt.subplots()
        ax = sns.heatmap(user_heatmap)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)



        # Finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            col1, col2 = st.columns(2)

        # Finding the busiest users in the group(Group Level)
        if selected_user == 'overall':
            st.title('Most Busy Users')
            x, new_data1 = helper.most_busy_users(data1)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='violet')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_data1)

        # most common words

        most_common_df = helper.most_common_words(selected_user, data1)

        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        st.title('most common words')

        st.pyplot(fig)
        st.dataframe(most_common_df)
