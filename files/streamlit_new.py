import streamlit as st
import pandas as pd
import time
import datetime
import ast
from datetime import date
import matplotlib.pyplot as plt
import numpy as np
from streamlit_card import card
from collections import Counter

from google.oauth2 import service_account
from google.cloud import bigquery

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

GCP_PROJECT = 'news-and-echo-bubbles'

@st.cache_data
def cached_data():
    '''function that returns the full master district df.
    Dataframe contains district name (primary key), lat_lons for the center,
    lat_lons for the edges of rectangle around area, and the area of the
    rectangle in Hectares'''

    query = f"""
            SELECT *
            FROM `{GCP_PROJECT}.preproc_scraped_news.scraped_news_preprocessed_2023_12_06`
        """

    query_job = client.query(query)
    result = query_job.result()
    df = result.to_dataframe()

    for index, row in enumerate(df.keywords):
        df.keywords[index] = ast.literal_eval(df.keywords[index])

    df['pdate']= pd.to_datetime(df['pdate']).dt.date
    return df

#from PIL import Image
#from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

st.set_page_config(page_title="News and Biases",layout="wide")


@st.cache_data
def trending_topics():
    df = cached_data()
    mask = df['pdate'] == df['pdate'].max()
    df = df[mask]
    df.reset_index(drop=True,inplace=True)

    list_of_keywords = []
    trending_topics = []
    for i in range(len(df.keywords)):
        for key in df.keywords[i].keys():
            list_of_keywords.append((key,))

    temp = set()
    counter = Counter(list_of_keywords)
    for word in list_of_keywords:
        if word not in temp:
            trending_topics.append((counter[word], ) + word)
            temp.add(word)

    trending = pd.DataFrame(trending_topics,columns=['count','word'])

    trending.sort_values(by='count',ascending=False,inplace=True)
    trending.reset_index(drop=True,inplace=True)
    topic_1 = trending.word[0]
    topic_2 = trending.word[1]
    topic_3 = trending.word[2]
    topic_4 = trending.word[4]
    topic_5 = trending.word[5]

    return topic_1, topic_2, topic_3, topic_4, topic_5

def search_keyword(topic,date_1,date_2):
    #search from raw data post-embedding and training
    #find way to search from sql for streamlit demo
    df_ll, df_l, df_c, df_r, df_rr = biases(date_1,date_2)

    keyword = topic
    returned_articles = []
    for index, row in enumerate(df_ll.keywords):
        if keyword in row:
            returned_articles.append((df_ll['link'][index],df_ll['pdate'][index],df_ll['title'][index],df_ll['author'][index],df_ll['text'][index],df_ll['urls'][index],df_ll['pred_class'][index],df_ll.keywords[index].keys(),df_ll.keywords[index][keyword])) ##TODO get key names out into dataframe
    output_df_ll = pd.DataFrame(returned_articles,columns=['link','pdate','title','author','text','urls','pred_class','key','keyword_score'])
    output_df_ll = output_df_ll.sort_values(by=['keyword_score'],ascending=False)
    output_df_ll.reset_index(drop=True,inplace=True)

    returned_articles = []
    for index, row in enumerate(df_l.keywords):
        if keyword in row:
            returned_articles.append((df_l['link'][index],df_l['pdate'][index],df_l['title'][index],df_l['author'][index],df_l['text'][index],df_l['urls'][index],df_l['pred_class'][index],df_l.keywords[index].keys(),df_l.keywords[index][keyword]))
    output_df_l = pd.DataFrame(returned_articles,columns=['link','pdate','title','author','text','urls','pred_class','key','keyword_score'])
    output_df_l = output_df_l.sort_values(by=['keyword_score'],ascending=False)
    output_df_l.reset_index(drop=True,inplace=True)

    returned_articles = []
    for index, row in enumerate(df_c.keywords):
        if keyword in row:
            returned_articles.append((df_c['link'][index],df_c['pdate'][index],df_c['title'][index],df_c['author'][index],df_c['text'][index],df_c['urls'][index],df_c['pred_class'][index],df_c.keywords[index].keys(),df_c.keywords[index][keyword]))
    output_df_c = pd.DataFrame(returned_articles,columns=['link','pdate','title','author','text','urls','pred_class','key','keyword_score'])
    output_df_c = output_df_c.sort_values(by=['keyword_score'],ascending=False)
    output_df_c.reset_index(drop=True,inplace=True)

    returned_articles = []
    for index, row in enumerate(df_r.keywords):
        if keyword in row:
            returned_articles.append((df_r['link'][index],df_r['pdate'][index],df_r['title'][index],df_r['author'][index],df_r['text'][index],df_r['urls'][index],df_r['pred_class'][index],df_r.keywords[index].keys(),df_r.keywords[index][keyword]))
    output_df_r = pd.DataFrame(returned_articles,columns=['link','pdate','title','author','text','urls','pred_class','key','keyword_score'])
    output_df_r = output_df_r.sort_values(by=['keyword_score'],ascending=False)
    output_df_r.reset_index(drop=True,inplace=True)

    returned_articles = []
    for index, row in enumerate(df_rr.keywords):
        if keyword in row:
            returned_articles.append((df_rr['link'][index],df_rr['pdate'][index],df_rr['title'][index],df_rr['author'][index],df_rr['text'][index],df_rr['urls'][index],df_rr['pred_class'][index],df_rr.keywords[index].keys(),df_rr.keywords[index][keyword]))
    output_df_rr = pd.DataFrame(returned_articles,columns=['link','pdate','title','author','text','urls','pred_class','key','keyword_score'])
    output_df_rr = output_df_rr.sort_values(by=['keyword_score'],ascending=False)
    output_df_rr.reset_index(drop=True,inplace=True)

    return output_df_ll, output_df_l, output_df_c, output_df_r, output_df_rr

def biases(date_1,date_2):
    df = cached_data()


    mask = (df.pdate >= date_1) & (df.pdate <=date_2)
    df = df[mask]
    df.reset_index(drop=True,inplace=True)

    mask_ll = df['pred_class'] =='left'
    mask_l = df['pred_class'] =='leans left'
    mask_c = df['pred_class'] =='centre'
    mask_r = df['pred_class'] =='leans right'
    mask_rr = df['pred_class'] =='right'
    df_ll = df[mask_ll]
    df_ll.reset_index(drop=True,inplace=True)
    df_l = df[mask_l]
    df_l.reset_index(drop=True,inplace=True)
    df_c = df[mask_c]
    df_c.reset_index(drop=True,inplace=True)
    df_r = df[mask_r]
    df_r.reset_index(drop=True,inplace=True)
    df_rr = df[mask_rr]
    df_rr.reset_index(drop=True,inplace=True)

    return df_ll, df_l, df_c, df_r, df_rr

def page_home():
    container = st.container()
    logo_col, header_col = container.columns(2)

    # Add a logo
    with logo_col:
        logo = st.image("https://raw.githubusercontent.com/zulu-tango/news_and_echo_bubbles_streamlit/master/images/News_logo.png", width=250)

    # Boxed header
    with header_col:
       #add trending topics box header
        st.markdown(
            """
            <div style="text-align: center; border:1px solid #d3d3d3; padding: 10px; border-radius: 1px; background-color: #f5f5f5;">
                <h1 style="color: #333;font-size: 20px;">TODAY'S TRENDING TOPICS</h1>
            </div>
            """,
            unsafe_allow_html=True)
        #add topics underneath the header
        st.markdown("<br>", unsafe_allow_html=True)

        topic_1, topic_2, topic_3, topic_4, topic_5 = trending()
        tt_1, tt_2, tt_3, tt_4, tt_5 = st.columns(5)
        with tt_1:
            st.markdown(
                f"""
                <div style="text-align: center; border:1px solid #d3d3d3; padding: 1px; border-radius: 1px; background-color: #f5f5f5;">
                    <h1 style="color: #333;font-size: 12px;margin:0;">{topic_1.capitalize()}</h1>
                </div>
                """,
                unsafe_allow_html=True)

        with tt_2:
            st.markdown(
                f"""
                <div style="text-align: center; border:1px solid #d3d3d3; padding: 1px; border-radius: 1px; background-color: #f5f5f5;">
                    <h1 style="color: #333;font-size: 12px;margin:0;">{topic_2.capitalize()}</h1>
                </div>
                """,
                unsafe_allow_html=True)

        with tt_3:
            st.markdown(
                f"""
                <div style="text-align: center; border:1px solid #d3d3d3; padding: 1px; border-radius: 1px; background-color: #f5f5f5;">
                    <h1 style="color: #333;font-size: 12px;margin:0;">{topic_3.capitalize()}</h1>
                </div>
                """,
                unsafe_allow_html=True)

        with tt_4:
            st.markdown(
                f"""
                <div style="text-align: center; border:1px solid #d3d3d3; padding: 1px; border-radius: 1px; background-color: #f5f5f5;">
                    <h1 style="color: #333;font-size: 12px;margin:0;">{topic_4.capitalize()}</h1>
                </div>
                """,
                unsafe_allow_html=True)

        with tt_5:
            st.markdown(
                f"""
                <div style="text-align: center; border:1px solid #d3d3d3; padding: 1px; border-radius: 1px; background-color: #f5f5f5;">
                    <h1 style="color: #333;font-size: 12px;margin:0;">{topic_5.capitalize()}</h1>
                </div>
                """,
                unsafe_allow_html=True)


    # add the search bar
    topic = st.text_input("ENTER A SEARCH TOPIC: ", '')

    #add the date range
    start_date = datetime.date(2023,11,1)
    end_date = datetime.datetime.now()
    dec_1 = datetime.date(2023,12,1)

    date = st.date_input('Search in Date Range:',(dec_1,end_date), start_date,end_date,format='DD/MM/YYYY')
    date_1 = date[0]
    date_2 = date[1]

    # click the search button for results
    if st.button("Search"):
        #add a design feature for a progress bar
        progress_bar = st.progress(0, text='searching articles... please wait')

        # Perform the search when the button is clicked
        df_ll, df_l, df_c, df_r, df_rr = search(topic,date_1,date_2)
        # TODO add functionality if topic buttons are clicked

        for percent_complete in range(100):
                time.sleep(0.02)
                progress_bar.progress(percent_complete + 1)

        # Create three columns
        col1, col2, col3 = st.columns(3)

        # Add buttons to each column
        with col1:
            st.subheader("Left")

            for i in range(len(df_ll)):
                                # URL of the image
                hasClicked = card(
                        title=f"{df_ll['title'].iloc[i]}",
                        text=f"{df_ll['urls'].iloc[i]}",
                        #url=f"{df_ll['link'].iloc[i]}",
                        styles={
                                    "card": {
                                        "width": "300px",
                                        "align": "left",
                                        "height": "100px",
                                        "border-radius": "10px",
                                        'background-color': '#004687',
                                        'margin': '0 auto',
                                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                                    },
                                    "text": {
                                        'font-size':"12px",
                                        "font-family": "serif"
                                    }
                                }
                                )
            for i in range(len(df_l)):
                                # URL of the image

                hasClicked = card(
                        title=f"{df_l['title'].iloc[i]}",
                        text=f"{df_l['urls'].iloc[i]}",
                        # url=f"{df_l['link'].iloc[i]}",
                        styles={
                                    "card": {
                                        "width": "300px",
                                        "height": "100px",
                                        "border-radius": "10px",
                                        'background-color': '#6699CC',
                                        'margin': '0 auto',
                                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                                    },
                                    "text": {
                                        'font-size':"12px",
                                        "font-family": "serif"
                                    }
                                }
                                                )
        with col2:
            st.subheader("Centre")
            for i in range(len(df_c)):
                hasClicked = card(
                            title=f"{df_c['title'].iloc[i]}",
                            text=f"{df_c['urls'].iloc[i]}",
                            #url=f"{df_c['link'].iloc[i]}",
                            styles={
                                    "card": {
                                        "width": "300px",
                                        "height": "100px",
                                        "border-radius": "10px",
                                        'background-color': 'white',
                                        'margin': '0 auto',
                                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                                    },
                                    "text": {
                                        'font-size':"12px",
                                        "font-family": "serif"
                                    }
                                }
                                                    )
        with col3:
            st.subheader("Right")

            for i in range(len(df_rr)):
                                # URL of the image
                hasClicked = card(
                            title=f"{df_rr['title'].iloc[i]}",
                            text=f"{df_rr['urls'].iloc[i]}",
                            #url=f"{df_rr['link'].iloc[i]}",
                            styles={
                                    "card": {
                                        "width": "400px",
                                        "height": "100px",
                                        "border-radius": "10px",
                                        'background-color': '#AA0000',
                                        'margin': '0 auto',
                                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                                    },
                                    "text": {
                                        'font-size':"12px",
                                        "font-family": "serif"
                                    }
                                })

            for i in range(len(df_r)):
                                # URL of the image

                hasClicked = card(
                            title=f"{df_r['title'].iloc[i]}",
                            text=f"{df_r['urls'].iloc[i]}",
                            # url=f"{df_r['link'].iloc[i]}",
                            styles={
                                    "card": {
                                        "width": "400px",
                                        "height": "100px",
                                        "border-radius": "10px",
                                        'background-color': '#E67150',
                                        'margin': '0 auto',
                                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                                    },
                                    "text": {
                                        'font-size':"12px",
                                        "font-family": "serif"
                                    }
                                })

        progress_bar.empty()

        lst1 = [df_ll['title'][i] for i in range(len(df_ll))]
        lst2 = [df_l['title'][i] for i in range(len(df_l))]
        lst3 = [df_c['title'][i] for i in range(len(df_c))]
        lst4 = [df_r['title'][i] for i in range(len(df_rr))]
        lst5 = [df_rr['title'][i] for i in range(len(df_r))]

        lst1.extend(lst2)
        lst1.extend(lst3)
        lst1.extend(lst4)
        lst1.extend(lst5)

        # if "selected_option" not in st.session_state:
        #     st.session_state.selected_option = lst1[0]
        # st.session_state.selected_option = None
        ##st.session_state.selected_option = st.selectbox("Select an option:", lst1)
        # print(selected_option)
        # st.session_state.selected_option = selected_option
        if "selected_option" not in st.session_state:
            st.session_state.selected_option = lst1[0]

        selected_option = st.selectbox("Select an option:", lst1, index=lst1.index(st.session_state.selected_option))
        st.session_state.selected_option = selected_option

    if st.button("Get more information"):
        st.session_state.selected_page = "Article"
        st.experimental_set_query_params(page='Article')
        st.experimental_rerun()

def page_about():
    st.title("Article Information")
    st.write("Selected option from the dropdown:", st.session_state.selected_option)

    data = cached_data()
    mask = data['title']==st.session_state.selected_option
    data = data[mask]
    data.reset_index(drop=True,inplace=True)
    st.write(f"""{data.text[0]}""")

def trending():
    topic_1, topic_2, topic_3, topic_4, topic_5 = trending_topics()
    return topic_1, topic_2, topic_3, topic_4, topic_5

def search(query,date_1, date_2):
    # Perform a search operation (replace this with your own search logic)
    df_ll, df_l, df_c, df_r, df_rr = search_keyword(query,date_1,date_2)
    df_ll.style.hide(axis="index")

    return df_ll[:2],df_l[:2],df_c[:2],df_r[:2],df_rr[:2]

def main():
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "Search"

    pages = ["Search", "Article"]

    st.sidebar.title("Contents")
    selected_page = st.sidebar.radio("Select a page", pages, index=pages.index(st.session_state.selected_page))
    st.session_state.selected_page = selected_page


    # Display content based on the selected page
    if st.session_state.selected_page == "Search":
        page_home()
    elif st.session_state.selected_page == "Article":
        page_about()

if __name__ == "__main__":
    main()
