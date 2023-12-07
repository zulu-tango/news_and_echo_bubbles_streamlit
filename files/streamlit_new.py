import streamlit as st
import pandas as pd
import time
import datetime
import ast
import os
from datetime import date
import matplotlib.pyplot as plt
import numpy as np
from streamlit_card import card
from collections import Counter
import base64

from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

from google.oauth2 import service_account
from google.cloud import bigquery
st.set_page_config(page_title="News and Biases",layout="wide")
# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

GCP_PROJECT = 'news-and-echo-bubbles'

with open('files/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

add_bg_from_local(os.path.join(os.getcwd(), 'images', 'background.jpg'))

st.sidebar.image("https://raw.githubusercontent.com/zulu-tango/news_and_echo_bubbles_streamlit/master/images/News_logo.png", use_column_width=True)


@st.cache_data
def cached_data():
    '''function that returns the full master district df.
    Dataframe contains district name (primary key), lat_lons for the center,
    lat_lons for the edges of rectangle around area, and the area of the
    rectangle in Hectares'''

    query = f"""
            SELECT *
            FROM `{GCP_PROJECT}.preproc_scraped_news.scraped_news_preproc_prob__2023_12_07`
        """

    query_job = client.query(query)
    result = query_job.result()
    df = result.to_dataframe()

    for index, row in enumerate(df.keywords):
        df.keywords[index] = ast.literal_eval(df.keywords[index])

    print(df.info())
    df['pdate']= pd.to_datetime(df['pdate'],format='ISO8601').dt.date
    return df

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
    topic_1 = 'trump'
    topic_2 = 'biden'
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

def card_selection(card_id, selected_card):
    # Check if the current card is selected
    is_selected = card_id == selected_card

    # Define the card content
    card_content = f"Card {card_id} {'(Selected)' if is_selected else ''}"

    # Display the card as a button
    if st.button(card_content):
        # Update the selected card when the button is clicked
        return card_id
    else:
        return selected_card

def page_home():
    st.image("https://raw.githubusercontent.com/zulu-tango/news_and_echo_bubbles_streamlit/master/images/header_image_new.png", width=900)


    #add trending topics box header
    st.markdown(
        """
        <div style="text-align: center; align-items: center; justify-content: center; display: flex; height: 60px; border:1px solid #d3d3d3; padding: 1px; border-radius: 20px; background-color: #f5f5f5;">
            <h1 style="color: #333;font-size: 24px;">TODAY'S TRENDING TOPICS</h1>
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
            <div style="text-align: center; align-items: center; justify-content: center; display: flex; height: 40px; border:1px solid #d3d3d3; padding: 1px; border-radius: 20px; background-color: #f5f5f5;">
                <h1 style="color: #333;font-size: 16px;margin:0;">{topic_1.capitalize()}</h1>
            </div>
            """,
            unsafe_allow_html=True)

    with tt_2:
        st.markdown(
            f"""
            <div style="text-align: center; align-items: center; justify-content: center; display: flex; height: 40px; border:1px solid #d3d3d3; padding: 1px; border-radius: 20px; background-color: #f5f5f5;">
                <h1 style="color: #333;font-size: 16px;margin:0;">{topic_2.capitalize()}</h1>
            </div>
            """,
            unsafe_allow_html=True)

    with tt_3:
        st.markdown(
            f"""
            <div style="text-align: center; align-items: center; justify-content: center; display: flex; height: 40px; border:1px solid #d3d3d3; padding: 1px; border-radius: 20px; background-color: #f5f5f5;">
                <h1 style="color: #333;font-size: 16px;margin:0;">{topic_3.capitalize()}</h1>
            </div>
            """,
            unsafe_allow_html=True)

    with tt_4:
        st.markdown(
            f"""
            <div style="text-align: center; align-items: center; justify-content: center; display: flex; height: 40px; border:1px solid #d3d3d3; padding: 1px; border-radius: 20px; background-color: #f5f5f5;">
                <h1 style="color: #333;font-size: 16px;margin:0;">{topic_4.capitalize()}</h1>
            </div>
            """,
            unsafe_allow_html=True)

    with tt_5:
            st.markdown(
                f"""
                <div style="text-align: center; align-items: center; justify-content: center; display: flex; height: 40px; border:1px solid #d3d3d3; padding: 1px; border-radius: 20px; background-color: #f5f5f5;">
                    <h1 style="color: #333;font-size: 16px;margin:0;">{topic_5.capitalize()}</h1>
                </div>
                """,
                unsafe_allow_html=True)

    for i in range(1):
        st.text("")

    # st.markdown(
    #         f"""
    #         <div style="text-align: left;">
    #             <h1 style="color: #FFFFFF;font-size: 20px;margin:0;">ENTER A SEARCH TOPIC:</h1>
    #         </div>
    #         """,
    #         unsafe_allow_html=True)

    # Define the text input box
    topic = st.text_input("SEARCH WORD: ",topic_1)
    # st.markdown('''
    #             <style>
    #             textarea {
    #                 font-size: 2rem !important;
    #                 } </style>''', unsafe_allow_html=True)


    #add the date range
    start_date = datetime.date(2023,11,1)
    end_date = datetime.datetime.now()
    dec_1 = datetime.date(2023,12,1)

    date = st.date_input('Search in Date Range:',(dec_1,end_date), start_date,end_date,format='DD/MM/YYYY')
    date_1 = date[0]
    date_2 = date[1]

    # click the search button for results
    if st.button("Search",type='primary') or st.session_state.get('searched'):
        st.session_state['searched'] = True

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
                                        "width": "420px",
                                        "align": "left",
                                        "height": "100px",
                                        "border-radius": "10px",
                                        'background-color': '#004687',
                                        'margin': '0 auto',
                                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                                    },
                                    "text": {
                                        'font-size':"14px",
                                        "font-family": "Source Sans Pro"
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
                                        "width": "420px",
                                        "height": "100px",
                                        "border-radius": "10px",
                                        'background-color': '#6699CC',
                                        'margin': '0 auto',
                                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                                    },
                                    "text": {
                                        'font-size':"14px",
                                        "font-family": "Source Sans Pro"
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
                                        "width": "420px",
                                        "height": "100px",
                                        "border-radius": "10px",
                                        'background-color': 'white',
                                        'margin': '0 auto',
                                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                                    },
                                    "text": {
                                        'font-size':"14px",
                                        "font-family": "Source Sans Pro"
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
                                        "width": "420px",
                                        "height": "100px",
                                        "border-radius": "10px",
                                        'background-color': '#AA0000',
                                        'margin': 'auto',
                                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                                    },
                                    "text": {
                                        'font-size':"14px",
                                        "font-family": "Source Sans Pro"
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
                                        "width": "420px",
                                        "height": "100px",
                                        "border-radius": "10px",
                                        'background-color': '#E67150',
                                        'margin': '0 auto',
                                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                                    },
                                    "text": {
                                        'font-size':"14px",
                                        "font-family": "sans serif"
                                    }
                                })

        progress_bar.empty()

        lst1 = [df_ll['title'][i] for i in range(len(df_ll['title']))]
        lst2 = [df_l['title'][i] for i in range(len(df_l['title']))]
        lst3 = [df_c['title'][i] for i in range(len(df_c['title']))]
        lst4 = [df_rr['title'][i] for i in range(len(df_rr['title']))]
        lst5 = [df_r['title'][i] for i in range(len(df_r['title']))]

        lst1.extend(lst2)
        lst1.extend(lst3)
        lst1.extend(lst4)
        lst1.extend(lst5)

        col_1_1, col_1_2 = st.columns(2)
        with col_1_1:
            if "selected_option" not in st.session_state:
                st.session_state.selected_option = ""
            selected_option = st.selectbox("Select an option", lst1)
            st.session_state.selected_option = selected_option

        with col_1_2:
            word_cloud_pipe(df_ll,df_l,df_c,df_r,df_rr)

    # Button to navigate to the second page
    if st.button("Get more information on this article"):
        # Redirect to the second page
        st.session_state.selected_page = "Article"
        st.experimental_set_query_params(page='Article')
        st.experimental_rerun()


def word_cloud_pipe(df1,df2,df3,df4,df5):
    x = get_words(df1,df2,df3,df4,df5)
    wordcloud(x)

def type_list(df):
    df["keyword_key_words"] = list(df["key"])
    return df

def get_words(df1,df2,df3,df4,df5):
    # ic(df1)
    # ic(df2)
    big_df = pd.concat([df1,df2,df3,df4,df5],axis=0).reset_index()

    big_df = type_list(big_df)

    empty_list = []

    for row in list(big_df["keyword_key_words"]):
        for elem in row:
            empty_list.append(elem)

    x = ' '.join(empty_list)

    return x

def wordcloud(x):
    ### import mask
    # mask = np.array(Image.open("https://raw.githubusercontent.com/zulu-tango/news_and_echo_bubbles_streamlit/master/images/news_mask.png"))

    #mask = np.array(Image.open(os.path.abspath('raw_data/news_mask.png')))

    ### instantiate word cloud
    # wordcloud = WordCloud(mask = mask, max_font_size=500, max_words=55, background_color="white", font_path = 'raw_data/fonts/tower_of_silence/towerofsilenceexpand.ttf',
    #                   collocations=True,colormap = 'coolwarm', contour_width=2.0, contour_color='black').generate(x) #mode="RGBA", colormap = 'Reds', background_color="rgba(255, 255, 255, 0)"

    ### instantiate word cloud
    wordcloud = WordCloud(max_font_size=200, max_words=55, background_color="white", #font_path = 'raw_data/fonts/tower_of_silence/towerofsilenceexpand.ttf',
                      collocations=True,colormap = 'coolwarm', contour_width=2.0, contour_color='black').generate(x) #mode="RGBA", colormap = 'Reds', background_color="rgba(255, 255, 255, 0)"

    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation="bilinear")
    #ax.set_title('Related Topics')
    ax.axis('off')
    st.pyplot(fig,clear_figure=True,use_container_width=True)


def page_about():
    st.title("Article Information")
    #st.write("Selected option from the dropdown:", st.session_state.selected_option)
    #st.write(st.session_state.selected_option)

    data = cached_data()
    mask = data['title']==st.session_state.selected_option
    data = data[mask]
    data.reset_index(drop=True,inplace=True)

    col_info, col_bias = st.columns(2)

    wc = WordCloud(background_color="white", max_words=20)

    if data['pred_class'][0] == 'left':
        color = '#004687'
    elif data['pred_class'][0] == 'leans left':
        color = '#6699CC'
    elif data['pred_class'][0] == 'right':
        color= '#AA0000'
    elif data['pred_class'][0] == 'leans right':
        color = '#E67150'
    else:
        color='white'

    with col_info:
        #st.subheader("Info")
        st.write(f'Title: {data.title[0]}')
        #st.write(f'Author(s): {data.author[0]}')
        st.write(f'Here is a summary of the article: <br>{data.sum_text[0]}', unsafe_allow_html=True)

    with col_bias:
        hasClicked = card(
                            title=f"BIAS",
                            text=f"{data['pred_class'][0]} with a confidence of {round(data['pred_probas'][0],2)}",
                            styles={
                                    "card": {
                                        "width": "300px",
                                        "height": "100px",
                                        "border-radius": "10px",
                                        'background-color': f'{color}',
                                        'margin': '0 auto',
                                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                                    },
                                    "text": {
                                        'font-size':"16px",
                                        "font-family": "serif"
                                    }
                                })
        wc.generate_from_frequencies(data.keywords[0])
        # show
        fig, ax = plt.subplots(figsize=(2, 2))
        ax.imshow(wc, interpolation="bilinear")
        #ax.set_title('Related Topics')
        ax.axis('off')
        st.pyplot(fig,clear_figure=True,use_container_width=False)


    if st.button('Read full article'):
        st.write(f'{data.text[0]}')


def trending():
    topic_1, topic_2, topic_3, topic_4, topic_5 = trending_topics()
    return topic_1, topic_2, topic_3, topic_4, topic_5

def search(query,date_1, date_2):
    # Perform a search operation (replace this with your own search logic)
    df_ll, df_l, df_c, df_r, df_rr = search_keyword(query,date_1,date_2)
    df_ll.style.hide(axis="index")

    return df_ll[:2],df_l[:2],df_c[:2],df_r[:2],df_rr[:2]

def page_profile():

    # set CSS style to round all images expect the one with the "exclude-me" tag (i.e. linkedin icons)
    st.markdown("""
    <style>
        img:not(#exclude-me) {border-radius: 50%}
    </style>

    """, unsafe_allow_html=True)

    ############################### Barnaby info #######################################
    # create two cols, one for profile photo and the other with the social networks links
    col1, mid, col2 = st.columns([1,2,20],gap="medium")

    with col1:
        st.image('https://raw.githubusercontent.com/zulu-tango/news_and_echo_bubbles_streamlit/master/images/Barney.png', width=105) #path of the picture

    with col2:
        st.markdown("**Barnaby KEMPSTER**")
        st.write("""
    <img src="https://github.githubassets.com/favicons/favicon.svg" width="20" border-radius="50"> **Github profile**: https://github.com/Barnaby323

    <img id='exclude-me' src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" width="20"> **LinkedIn**: https://www.linkedin.com/in/barnaby-kempster/
                """, unsafe_allow_html=True)
    # add large blank space
    ############################### Connor Gower info #######################################
    # create two cols, one for profile photo and the other with the social networks links
    col1, mid, col2 = st.columns([1,2,20],gap="medium")
    with col1:
        st.image('https://raw.githubusercontent.com/zulu-tango/news_and_echo_bubbles_streamlit/master/images/Connor.png', width=105)#path of the picture

    with col2:
        st.markdown("**Connor GOWER**")
        st.markdown("""
    <img class="image backArrow" src="https://github.githubassets.com/favicons/favicon.svg" width="20"> **Github profile**: https://github.com/connorgower

    <img id='exclude-me' src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" width="20"> **LinkedIn**: https://www.linkedin.com/in/connor-gower/


                """, unsafe_allow_html=True)

    # add large blank space
    ############################### Manuel Puente info #######################################
    # create two cols, one for profile photo and the other with the social networks links

    col1, mid, col2 = st.columns([1,2,20],gap="medium")

    with col1:
        st.image('https://raw.githubusercontent.com/zulu-tango/news_and_echo_bubbles_streamlit/master/images/Manuel.png', width=105)#path of the picture

    with col2:
        st.markdown("**Manuel PUENTE**")
        st.write("""
    <img src="https://github.githubassets.com/favicons/favicon.svg" width="20"> **Github profile**: https://github.com/Manu2023ds

    <img id='exclude-me' src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" width="20"> **LinkedIn**: https://www.linkedin.com/in/manuel-p-29223629/

                """, unsafe_allow_html=True)

    # add large blank space
    ############################### Zoe Tustain info #######################################
    # create two cols, one for profile photo and the other with the social networks links

    col1, mid, col2 = st.columns([1,2,20],gap="medium")

    with col1:
        st.image('https://raw.githubusercontent.com/zulu-tango/news_and_echo_bubbles_streamlit/master/images/Zoe.png', width=105)#path of the picture

    with col2:
        st.markdown("**Zoe TUSTAIN**")
        st.write("""
    <img src="https://github.githubassets.com/favicons/favicon.svg" width="20"> **Github profile**: https://github.com/zulu-tango

    <img id='exclude-me' src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" width="20"> **LinkedIn**: https://www.linkedin.com/in/zoetustain/

                """, unsafe_allow_html=True)

    # add large blank space
    ############################### COMLAN Renato info #######################################
    # create two cols, one for profile photo and the other with the social networks links
    col1, mid, col2 = st.columns([1,2,20],gap="medium")

    with col1:
        st.image('https://raw.githubusercontent.com/zulu-tango/news_and_echo_bubbles_streamlit/master/images/Renato.png', width=105)#path of the picture

    with col2:
        st.markdown("**Renato COMLAN**")
        st.write("""
    <img src="https://github.githubassets.com/favicons/favicon.svg" width="20"> **Github profile**: https://github.com/cmlnrnt

    <img id='exclude-me' src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" width="20"> **LinkedIn**: https://www.linkedin.com/in/renato-comlan/

                """, unsafe_allow_html=True)

def main():
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "About"

    pages = ["About","Search", "Article"]

    st.sidebar.title("Contents")
    selected_page = st.sidebar.radio("Select a page", pages, index=pages.index(st.session_state.selected_page))
    st.session_state.selected_page = selected_page


    # Display content based on the selected page
    if st.session_state.selected_page == "About":
        page_profile()
    elif st.session_state.selected_page == "Search":
        page_home()
    elif st.session_state.selected_page == "Article":
        page_about()

if __name__ == "__main__":
    main()
