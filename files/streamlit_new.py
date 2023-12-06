import streamlit as st
import pandas as pd  # Import the Pandas library
from preprocess.keyword_search import search_keyword, trending_topics, cached_data
import time
import datetime
import matplotlib.pyplot as plt
import numpy as np
from streamlit_card import card

#from PIL import Image
#from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

st.set_page_config(page_title="News and Biases",layout="wide")

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


        if "selected_option" not in st.session_state:
            st.session_state.selected_option = lst1[0]

        selected_option = st.selectbox("Select an option:", lst1)
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
