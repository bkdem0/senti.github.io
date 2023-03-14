import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
from PIL import Image
import altair as alt
import seaborn as sns

# Set page configuration
st.set_page_config(page_title="Sentiment Analysis Dashboard", page_icon=":bar_chart:", layout="wide")
st.title("Sentiment Analysis Dashboard")
# uploaded_file = st.sidebar.file_uploader("Choose a review file", type=("csv","xlsx"))

# if uploaded_file is not None:
#     df = pd.read_csv(uploaded_file)
df = pd.read_csv("openai_keywords.csv")

df1=(df[["text","sentiment"]])




# Define function to generate pie chart
def generate_pie_chart(df):
    counts = df["sentiment"].value_counts()
    positive_count = counts.get("Positive", 0)
    neutral_count = counts.get("Neutral", 0)
    negative_count = counts.get("Negative", 0)
    labels = ["Positive", "Neutral", "Negative"]
    values = [positive_count, neutral_count, negative_count]
    colors = ["#11ba5d", "#FFBF00", "#fa586d"]
    fig_sentiment = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3, marker=dict(colors=colors))])
    return fig_sentiment

# Define function to generate stacked bar chart
def generate_bar_chart(df):
    df['keywords_2'] = df['keywords_2'].astype('str').str.lower()
    df['keywords_2'] = df['keywords_2'].str.replace('.','')
    df['keywords_2'] = df['keywords_2'].str.replace('"','')
    df_pos = df[df['sentiment']=='Positive']
    pos_count = df_pos.keywords_2.str.split(",",expand=True).stack().value_counts()
    pos_count = pd.DataFrame(pos_count).reset_index()
    pos_count.columns = ['word','count']
    pos_count['sentiment']='Positive'
    # pos_count.sort_values(by="count",ascending=True)
    pos_count_2=pos_count.head(15)
    fig_pos = px.histogram(pos_count_2, x='count', y='word',orientation='h', color_discrete_sequence=[ '#11ba5d'])
    fig_pos.update_traces(text=pos_count_2['count'], texttemplate='%{text:.2s}', textposition='outside')
    fig_pos.update_layout(uniformtext_minsize=8, uniformtext_mode='show' )
    return fig_pos

def generate_bar_chart1(df):
    df['keywords_2'] = df['keywords_2'].astype('str').str.lower()
    df['keywords_2'] = df['keywords_2'].str.replace('.','')
    df['keywords_2'] = df['keywords_2'].str.replace('"','')
    df_neutral = df[df['sentiment']=='Neutral']
    neu_count = df_neutral.keywords_2.str.split(",",expand=True).stack().value_counts()
    neu_count = pd.DataFrame(neu_count).reset_index()
    neu_count.columns = ['word','count']
    neu_count['sentiment']='Neutral'
    neu_count_2=neu_count.head(15)
    fig_neu = px.histogram(neu_count_2, x='count', y='word', color_discrete_sequence=[ '#FFBF00'])
    fig_neu.update_traces(text=neu_count_2['count'], texttemplate='%{text:.2s}', textposition='outside')
    fig_neu.update_layout(uniformtext_minsize=8, uniformtext_mode='show')
    return fig_neu

def generate_bar_chart2(df):
    df['keywords_2'] = df['keywords_2'].astype('str').str.lower()
    df['keywords_2'] = df['keywords_2'].str.replace('.','')
    df['keywords_2'] = df['keywords_2'].str.replace('"','')
    df_neg = df[df['sentiment']=='Negative']
    neg_count = df_neg.keywords_2.str.split(",",expand=True).stack().value_counts()
    neg_count = pd.DataFrame(neg_count).reset_index()
    neg_count.columns = ['word','count']
    neg_count['sentiment']='Negative'
    neg_count_2=neg_count.head(15)
    # fig_neg = px.histogram(neg_count_2, x='count', y='word', color_discrete_sequence=[ '#fa586d'])
    fig_neg = px.histogram(neg_count_2, x='count', y='word', color_discrete_sequence=[ '#fa586d'])
    fig_neg.update_traces(text=neg_count_2['count'], texttemplate='%{text:.2s}', textposition='outside')
    fig_neg.update_layout(uniformtext_minsize=8, uniformtext_mode='show')
    return fig_neg


# df['keywords_2'] = df['keywords_2'].astype('str').str.lower()
# df['keywords_2'] = df['keywords_2'].str.replace('.','')
# df['keywords_2'] = df['keywords_2'].str.replace('"','')
# df_pos = df[df['sentiment']=='Positive']
# df_neutral = df[df['sentiment']=='Neutral']
# df_neg = df[df['sentiment']=='Negative']

# df_merged = pd.concat([df_pos, df_neg, df_neutral], ignore_index=True)

def generate_wordcloud(df):
    # color = 'black'
    # if df_merged == 'Positive':
    #     color = '#11ba5d'
    # elif df_merged == 'Neutral':
    #     color = '#FFBF00'
    # elif df_merged == 'Negative':
    #     color = '#fa586d'
    # return f'color: {color}'

    text = " ".join(review for review in df.text.astype(str))
    wordcloud = WordCloud(background_color="white",width=1200, height=800, max_words=200).generate(text)
    return wordcloud



def color_sentiment(val):
    color = 'black'
    if val == 'Positive':
        color = '#11ba5d'
    elif val == 'Neutral':
        color = '#FFBF00'
    elif val == 'Negative':
        color = '#fa586d'
    return f'color: {color}'
df_styled1 = df1.style.apply(lambda x: [color_sentiment(x.sentiment)]*len(x), axis=1)
# df_styled1 = df1.style.applymap(color_sentiment, subset=['sentiment'])

# Define function to show charts and wordcloud
def show_charts_and_wordcloud(df):
    # Generate charts
    
    fig_sentiment = generate_pie_chart(df)
    fig_wordcloud = px.imshow(generate_wordcloud(df), template='plotly_white')
    fig_wordcloud.update_layout(
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        plot_bgcolor="white",
    )
    fig_stacked = generate_bar_chart(df)
    fig_stacked1 = generate_bar_chart1(df)
    fig_stacked2 = generate_bar_chart2(df)

    # Display charts and wordcloud in two columns
    col1,col2,col3,col4= st.columns([2,1,1,1])
    # with col1:
    #     st.write("Data:")
    #     st.write(df[["text","sentiment"]])
    with col1:
        st.subheader("snippets")
        st.dataframe(df_styled1, height=900)
    
    with col2:
        st.subheader("Sentiment by Positive Keyword")
        st.plotly_chart(fig_stacked, use_container_width=True) 
        st.subheader("Wordcloud")
        st.plotly_chart(fig_wordcloud, use_container_width=True)

    with col3:
        st.subheader("Sentiment by Neutral Keyword")
        st.plotly_chart(fig_stacked1, use_container_width=True)    

    with col4:
        st.subheader("Sentiment by Negative Keyword")
        st.plotly_chart(fig_stacked2, use_container_width=True)
        st.subheader("Sentiment Share")
        st.plotly_chart(fig_sentiment, use_container_width=True) 



    # col7,col8= st.columns([2,2])
    # # Display pie chart and wordcloud in first column
    # # with col4:
    # #     st.subheader("Sentiment by Keyword")
    # #     st.plotly_chart(fig_stacked, use_container_width=True)
    # # with col5:
    # #     st.subheader("Top Positive Keyword")
    # #     st.plotly_chart('')    
    # #     # st.plotly_chart(fig_stacked1, use_container_width=True)
    # # with col6:
    # #     st.subheader("Top Negative Keyword")
    # #     st.plotly_chart(fig_stacked2, use_container_width=True)
    # with col7:
    #     st.subheader("Wordcloud")
    #     st.plotly_chart(fig_wordcloud, use_container_width=True)

    #     # st.plotly_chart(fig_stacked1, use_container_width=True)
    # with col8:
    #     st.subheader("Sentiment Share")
    #     st.plotly_chart(fig_sentiment, use_container_width=True) 


show_charts_and_wordcloud(df)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)