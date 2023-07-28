import streamlit as st
import finnhub
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import plotly.graph_objects as go
import datetime
from pages.utils.Sentiment_analysis import get_sentiment_scores, get_sentiment_label, sentiment_analysis_main


# Replace YOUR_API_KEY with your actual Finnhub API key
finnhub_client = finnhub.Client(api_key="cj16eq1r01qhv0uhjss0cj16eq1r01qhv0uhjssg")

st.set_page_config(page_title='Sentiment Analysis', page_icon='📈', layout='wide')


def convert_unix_to_datetime(unix_time):
    return datetime.datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')


def get_company_news(stock_code, start_date, end_date):
    raw_news = finnhub_client.company_news(stock_code, _from=start_date, to=end_date)
    if raw_news and "error" not in raw_news:
        # Filter out the 'image' and 'id' fields and convert timestamps
        filtered_news = [{key: value for key, value in item.items() if key not in ['image', 'id']} for item in raw_news]
        for item in filtered_news:
            item['datetime'] = convert_unix_to_datetime(item['datetime'])
            sentiment_scores = get_sentiment_scores(item['headline'])
            item['Negative'] = sentiment_scores[0]
            item['Neutral'] = sentiment_scores[1]
            item['Positive'] = sentiment_scores[2]
        return filtered_news
    return None


def news_main():
    st.title("FinS - Financial news with Sentiment Analysis ")

    option_col1, option_col2, option_col3, option_col4 = st.columns(4)
    with option_col1:
        start_date = st.date_input("Select the start date")
    with option_col2:
        end_date = st.date_input("Select the end date")
    with option_col4:
        stock_code = st.text_input("Enter a stock code (e.g., AAPL, GOOGL)", "AAPL")

    # Fetch and display the news

    if start_date > end_date:
        st.error("Error: Start date cannot be after end date.")
    else:
        news = get_company_news(stock_code, str(start_date), str(end_date))
        if news:
            # Create a DataFrame with the modified data
            df = pd.DataFrame(news)
            df['datetime'] = pd.to_datetime(df['datetime'])
            sentiment_labels = df.apply(
                lambda row: get_sentiment_label([row['Negative'], row['Neutral'], row['Positive']]), axis=1)
            df['Sentiment'] = sentiment_labels
            df['Negative'] = df['Negative'].apply(lambda score: f"{score:.2%}")
            df['Neutral'] = df['Neutral'].apply(lambda score: f"{score:.2%}")
            df['Positive'] = df['Positive'].apply(lambda score: f"{score:.2%}")

            # Visualize sentiment distribution with a bar chart
            sentiment_counts = df['Sentiment'].value_counts()
            sentiment_chart = px.bar(sentiment_counts, x=sentiment_counts.index, y=sentiment_counts.values,
                                     labels={'x': 'Sentiment', 'y': 'Count'}, color=sentiment_counts.index,
                                     title='Sentiment Distribution of News Articles')

            # Visualize sentiment distribution with a bar chart
            sentiment_counts = df['Sentiment'].value_counts()
            sentiment_chart = px.bar(sentiment_counts, x=sentiment_counts.index, y=sentiment_counts.values,
                                     labels={'x': 'Sentiment', 'y': 'Count'}, color=sentiment_counts.index,
                                     title='Sentiment Distribution of News Articles')

            # Visualize word cloud based on summary text
            summary_text = " ".join(df['summary'].dropna())  # Combine all summary texts into a single string
            wordcloud = WordCloud(width=500, height=300, background_color='white').generate(summary_text)

            # Create a Plotly figure for the word cloud
            wordcloud_data = wordcloud.words_
            wordcloud_fig = go.Figure(go.Bar(
                x=list(wordcloud_data.values()),
                y=list(wordcloud_data.keys()),
                orientation='h',
                marker_color='rgba(50, 171, 96, 0.6)'  # Adjust the color as needed
            ))
            wordcloud_fig.update_layout(
                title="Word Cloud of News Article Summaries",
                xaxis_title="Frequency",
                yaxis_title="Word",
                margin=dict(l=0, r=0, t=30, b=0)
            )

            # Display the plots in two columns
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(sentiment_chart)

            with col2:
                st.plotly_chart(wordcloud_fig)

            # Display the news table with clickable links
            st.dataframe(df[['datetime', 'headline', 'Sentiment', 'Negative', 'Neutral', 'Positive', 'related',
                             'source', 'summary', 'url']], height=600)
        else:
            st.error("No news found for the given stock and date range.")


if __name__ == "__main__":
    news_main()
    sentiment_analysis_main()
