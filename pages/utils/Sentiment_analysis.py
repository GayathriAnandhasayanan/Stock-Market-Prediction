import streamlit as st
import spacy
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import yfinance as yf

# Load the FinBERT model and tokenizer
model = BertForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone")
tokenizer = BertTokenizer.from_pretrained("yiyanghkust/finbert-tone")

# Load the NER model
nlp = spacy.load('en_core_web_lg')


# Function to get the sentiment scores
def get_sentiment_scores(text):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1).tolist()[0]
    return probabilities


# Function to get the sentiment label
def get_sentiment_label(sentiment_scores):
    max_score_index = sentiment_scores.index(max(sentiment_scores))
    if max_score_index == 0:
        return "Negative"
    elif max_score_index == 1:
        return "Neutral"
    else:
        return "Positive"


# Function to get the stock codes from company names using yfinance
def get_stock_codes(company_names):
    stock_codes = {}
    for company_name in company_names:
        try:
            ticker = yf.Ticker(company_name)
            if ticker.info:
                stock_codes[company_name] = ticker.info['symbol'].upper()
            else:
                stock_codes[company_name] = company_name.upper()
        except Exception as e:
            print(f"Error occurred while fetching stock code for {company_name}: {e}")

    return stock_codes


# Function to perform Named Entity Recognition
def perform_ner(text):
    doc = nlp(text)
    company_names = []
    for ent in doc.ents:
        if ent.label_ == "ORG":
            company_names.append(ent.text)
    return company_names


# Streamlit app
def sentiment_analysis_main():
    st.title("Financial News Sentiment Analysis")

    st.write("Kindly provide text for analysis:")
    text_input = st.text_area("", height=100)

    if st.button("Analyze"):
        if text_input.strip() == "":
            st.warning("Please enter some text.")
        else:
            # Perform sentiment analysis
            sentiment_scores = get_sentiment_scores(text_input)
            sentiment_label = get_sentiment_label(sentiment_scores)
            st.write(f"The sentiment of your provided text is {sentiment_label}")
            st.write("Sentiment Scores:")
            st.write(f"Negative: {sentiment_scores[0] * 100:.2f}%")
            st.progress(sentiment_scores[0])
            st.write(f"Neutral: {sentiment_scores[1] * 100:.2f}%")
            st.progress(sentiment_scores[1])
            st.write(f"Positive: {sentiment_scores[2] * 100:.2f}%")
            st.progress(sentiment_scores[2])

            # Perform Named Entity Recognition and extract stock codes
            company_names = perform_ner(text_input)
            stock_codes = get_stock_codes(company_names)
            st.write("Discovered Company Names and Stock Codes:")
            for company_name, stock_code in stock_codes.items():
                st.write(f"{company_name}: {stock_code}")


if __name__ == "__main__":
    sentiment_analysis_main()
