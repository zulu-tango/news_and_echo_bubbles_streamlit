import streamlit as st
import pandas as pd  # Import the Pandas library
import time
from datetime import date, timedelta
import os
import ast
from collections import Counter
st.set_page_config(page_title="News and Biases",layout="wide")

@st.cache_data
def load_data():
    data = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSeyYvY90yVnOHNhcuIVla0yLYl5bsaWmFvPKWvBdHk09SEseL5HNpUCuCpcPq5OkbBStoN5iYvaPqv/pub?output=csv')
    return data

def trending_topics():
    df = load_data()
    for index, row in enumerate(df.keywords):
        df.keywords[index] = ast.literal_eval(df.keywords[index])


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
    topic_4 = trending.word[3]
    topic_5 = trending.word[4]

    return topic_1, topic_2, topic_3, topic_4, topic_5

def search_keyword(topic):
    #search from raw data post-embedding and training
    #find way to search from sql for streamlit demo
    df_ll, df_l, df_c, df_r, df_rr = biases()

    keyword = topic
    returned_articles = []
    for index, row in enumerate(df_ll.keywords):
        if keyword in row:
            returned_articles.append((df_ll['title'][index],df_ll['pred_class'][index],df_ll['link'][index],df_ll.keywords[index][keyword])) ##TODO get key names out into dataframe
    output_df_ll = pd.DataFrame(returned_articles,columns=['title','bias','link','keyword_score'])
    output_df_ll = output_df_ll.sort_values(by=['keyword_score'],ascending=False)

    returned_articles = []
    for index, row in enumerate(df_l.keywords):
        if keyword in row:
            returned_articles.append((df_l['title'][index],df_l['pred_class'][index],df_l['link'][index],df_l.keywords[index][keyword]))
    output_df_l = pd.DataFrame(returned_articles,columns=['title','bias','link','keyword_score'])
    output_df_l = output_df_l.sort_values(by=['keyword_score'],ascending=False)

    returned_articles = []
    for index, row in enumerate(df_c.keywords):
        if keyword in row:
            returned_articles.append((df_c['title'][index],df_c['pred_class'][index],df_c['link'][index],df_c.keywords[index][keyword]))
    output_df_c = pd.DataFrame(returned_articles,columns=['title','bias','link','keyword_score'])
    output_df_c = output_df_c.sort_values(by=['keyword_score'],ascending=False)

    returned_articles = []
    for index, row in enumerate(df_r.keywords):
        if keyword in row:
            returned_articles.append((df_r['title'][index],df_r['pred_class'][index],df_r['link'][index],df_r.keywords[index][keyword]))
    output_df_r = pd.DataFrame(returned_articles,columns=['title','bias','link','keyword_score'])
    output_df_r = output_df_r.sort_values(by=['keyword_score'],ascending=False)

    returned_articles = []
    for index, row in enumerate(df_rr.keywords):
        if keyword in row:
            returned_articles.append((df_rr['title'][index],df_rr['pred_class'][index],df_rr['link'][index],df_rr.keywords[index][keyword]))
    output_df_rr = pd.DataFrame(returned_articles,columns=['title','bias','link','keyword_score'])
    output_df_rr = output_df_rr.sort_values(by=['keyword_score'],ascending=False)

    return output_df_ll[:2], output_df_l[:2], output_df_c[:2], output_df_r[:2], output_df_rr[:2]

def biases():
    df = load_data()
    for index, row in enumerate(df.keywords):
        df.keywords[index] = ast.literal_eval(df.keywords[index])

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

def trending():
    # TODO: code trending topics function
    topic_1, topic_2, topic_3, topic_4, topic_5 = trending_topics()
    return topic_1, topic_2, topic_3, topic_4, topic_5

def search(query):
    # Perform a search operation (replace this with your own search logic)

    # For demonstration, creating three different DataFrames with different columns

    df_ll, df_l, df_c, df_r, df_rr = search_keyword(query)
    df_ll.style.hide(axis="index")
    return df_ll[['bias','title','link']],df_l[['bias','title','link']],df_c[['bias','title','link']],df_r[['bias','title','link']],df_rr[['bias','title','link']]

def clickable_cells(row):
    # Create a button for each cell in the row
    for col, value in row.iteritems():
        button_label = f"Click {value} in {col}"
        if st.button(button_label):
            # Handle the button click here (e.g., display more information)
            st.write(f"You clicked {value} in {col}")

def color_cells_row_wise(row):
    # Define a function to apply color to cells based on values in the row
    colors = ['background-color: #004687' if val == 'left' else 'background-color: #6699CC' if val == 'leans left' else 'background-color: #AA0000' if val == 'right' else 'background-color: #E67150' if val == 'leans right' else 'background-color: white' for val in row]
    return colors



def main():
    #pd.set_option('display.max_colwidth', None)

    container = st.container()
    logo_col, header_col = container.columns(2)

    # Add a logo
    with logo_col:
        logo = st.image("/home/zoetustain/code/zulu-tango/news_and_echo_bubbles_streamlit/News_logo.png", width=250)

    # Boxed header
    with header_col:
        news_all, news_uk, news_us = st.columns(3)
        # five buttons on the same row

        if news_all.button('', key='logo_button', help='Click to go to the logo URL'):
            st.write('You selected all news sources')
            # Add the action you want when the logo is clicked

        # Logo image
        st.image("/home/zoetustain/code/zulu-tango/news_and_echo_bubbles/images/world_flag.png", width=50)

        # world = st.image("/home/zoetustain/code/zulu-tango/news_and_echo_bubbles/images/world_flag.png", width=50)
        # image_world = st.image('/home/zoetustain/code/zulu-tango/news_and_echo_bubbles/images/world_flag.png', width=100)
        # button_world = world.button('world',key='button_world')
        button_uk = news_uk.button('UK')
        button_us = news_us.button('US')

        st.markdown(
            """
            <div style="text-align: center; border:1px solid #d3d3d3; padding: 10px; border-radius: 10px; background-color: #f5f5f5;">
                <h1 style="color: #333;font-size: 20px;">TRENDING TOPICS</h1>
            </div>
            """,
            unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        topic_1, topic_2, topic_3, topic_4, topic_5 = trending()
        tt_1, tt_2, tt_3, tt_4, tt_5 = st.columns(5)
        # five buttons on the same row
        button_topic_1 = tt_1.button(topic_1)
        button_topic_2 = tt_2.button(topic_2)
        button_topic_3 = tt_3.button(topic_3)
        button_topic_4 = tt_4.button(topic_4)
        button_topic_5 = tt_5.button(topic_5)




    topic = st.text_input("ENTER A SEARCH TOPIC: ", '')
    #date_options = pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03'])

    #selected_option = st.slider("Select an date range", options=pd.DataFrame[1, 2, 3, 4, 5])
    # start_time = st.slider(
    #     "When do you start?",
    #     value=date.today(),
    #     format="DD/MM/YY")
    # st.write("Start time:", start_time)

    date_range = st.slider("Date range:", min_value = date.today(), max_value= date.today()-timedelta(14), value=(date.today(), date.today()-timedelta(14)))

    # Add a search button
    if st.button("Search"):
        #st.markdown("<h4 style='color: green; font-size: 10px;'>Searching articles... Please wait.</h4>", unsafe_allow_html=True)
        progress_bar = st.progress(0, text='searching articles... please wait')

        # Perform the search when the button is clicked
        df_ll, df_l, df_c, df_r, df_rr = search(topic)

        for percent_complete in range(100):
                time.sleep(0.02)
                progress_bar.progress(percent_complete + 1)


        df_left = pd.concat([df_ll,df_l],ignore_index=True)
        df_right = pd.concat([df_rr,df_r],ignore_index=True)

        styled_df_left = df_left.style.apply(color_cells_row_wise, axis=1)
        styled_df_centre = df_c.style.apply(color_cells_row_wise, axis=1)
        styled_df_right = df_right.style.apply(color_cells_row_wise, axis=1)

        # for i in range(2):
        #     df_ll_styled = df_left.style.applymap(color_cells(df_ll.bias[i]))


        col1, col2, col3 = st.columns(3)
        col1.dataframe(styled_df_left)
        col2.dataframe(styled_df_centre)
        col3.dataframe(styled_df_right)

        progress_bar.empty()


    # # Add a placeholder for dynamic content
    # placeholder = st.empty()

    # # Add a click functionality
    # if st.button("Select and article for more information"):
    #     st.table(df_ll)
    #     # Show extra information when the button is clicked
    #     placeholder.text("Extra Information: This is additional information revealed when you click the button.")



if __name__ == "__main__":
    main()
