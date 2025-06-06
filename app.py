import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt

from helper import most_common_words

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file=st.sidebar.file_uploader("Choose a file.")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data= bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)

    st.dataframe(df)

    #fetch unique users
    user_list=df['user'].unique().tolist()
    user_list.remove('groupnotification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user=st.sidebar.selectbox("Show analysis wrt", user_list)
    num_messages, words, num_media_messages, num_links= helper.fetch_stats(selected_user, df)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages, num_links=helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4=st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media")
            st.title(num_media_messages)
        with col4:
            st.header("Total Links")
            st.title(num_links)

    st.title("Monthly timeline")
    timeline=helper.monthly_timeline(selected_user, df)
    fig, ax=plt.subplots()
    ax.plot(timeline['time'],timeline['message'])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    st.title("Activity Map")
    col1, col2= st.columns(2)
    with col1:
        st.header("Most busy day")
        busy_day=helper.week_activity_map(selected_user, df)
        fig, ax= plt.subplots()
        ax.bar(busy_day.index, busy_day.values)
        st.pyplot(fig)
    with col2:
        st.header("Most busy month")
        busy_month=helper.month_activity_map(selected_user, df)
        fig,ax=plt.subplots()
        ax.bar(busy_month.index, busy_month.values)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    if selected_user=='Overall':
        st.title("Most busy users")
        x, new_df=helper.most_busy_users(df)
        fig, ax=plt.subplots()
        col1, col2= st.columns(2)
        with col1:
            ax.bar(x.index, x.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)
    st.title("WordCloud")
    df_wc=helper.create_wordcloud(selected_user, df)
    fig, ax=plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)
    st.title("Most common words")
    most_common_df=helper.most_common_words(selected_user, df)

    fig, ax= plt.subplots()
    ax.bar(most_common_df[0], most_common_df[1])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)
    st.dataframe(most_common_df)



    emoji_df=helper.emoji_helper(selected_user, df)
    st.title("Emoji Analysis")
    st.dataframe(emoji_df)


