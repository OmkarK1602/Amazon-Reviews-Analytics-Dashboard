# app.py
import streamlit as st
import pandas as pd
import numpy as np
import re

# Set up the page
st.set_page_config(
    page_title="Amazon Reviews Analyzer", 
    page_icon="📊", 
    layout="wide"
)

# Title and description
st.title("📊 Amazon Product Review Analyzer")
st.markdown("""
This interactive dashboard analyzes Amazon product reviews to discover patterns in customer feedback.
**Upload limit: 500MB** - Large file support enabled.
""")

# Simple sentiment analysis function
def simple_sentiment(text):
    """
    A very basic sentiment analyzer using keyword matching
    Returns: -1 (negative), 0 (neutral), 1 (positive)
    """
    if not isinstance(text, str):
        return 0
    
    text = text.lower()
    
    # Positive words
    positive_words = ['good', 'great', 'excellent', 'awesome', 'amazing', 'love', 
                     'perfect', 'best', 'wonderful', 'fantastic', 'nice', 'happy',
                     'recommend', 'satisfied', 'pleased', 'outstanding', 'superb']
    
    # Negative words
    negative_words = ['bad', 'terrible', 'awful', 'horrible', 'hate', 'disappoint',
                     'poor', 'worst', 'waste', 'broken', 'problem', 'issue', 'defective',
                     'return', 'refund', 'complaint', 'damaged', 'useless']
    
    positive_count = sum(1 for word in positive_words if word in text)
    negative_count = sum(1 for word in negative_words if word in text)
    
    if positive_count > negative_count:
        return 1
    elif negative_count > positive_count:
        return -1
    else:
        return 0

# Optimized CSV reading function for large files
def read_large_csv(file, sample_size=10000):
    """Read large CSV files efficiently with sampling"""
    try:
        # First, try to read the full file with optimized settings
        df = pd.read_csv(
            file, 
            nrows=sample_size,  # Read only sample rows
            usecols=lambda col: col in ['Score', 'Text', 'HelpfulnessNumerator', 'HelpfulnessDenominator', 'Summary'],
            dtype={'Score': 'int8', 'HelpfulnessNumerator': 'int32', 'HelpfulnessDenominator': 'int32'},
            engine='python'  # More memory efficient
        )
        return df
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None

# File uploader
uploaded_file = st.file_uploader(
    "Choose a CSV file (up to 500MB)", 
    type="csv",
    help="Large Amazon reviews dataset supported"
)

if uploaded_file is not None:
    try:
        # Show file info
        file_size = uploaded_file.size / (1024 * 1024)  # Convert to MB
        st.info(f"📁 File size: {file_size:.2f} MB")
        
        # Load data with progress
        with st.spinner('Loading data... (this may take a while for large files)'):
            @st.cache_data(show_spinner=False)
            def load_data(file):
                return read_large_csv(file, sample_size=10000)
            
            df = load_data(uploaded_file)
        
        if df is not None and len(df) > 0:
            st.success(f"✅ Successfully loaded {len(df):,} reviews!")
            
            # Show basic info
            st.subheader("📋 Dataset Overview")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Reviews", f"{len(df):,}")
            with col2:
                st.metric("File Size", f"{file_size:.1f} MB")
            with col3:
                st.metric("Columns", len(df.columns))
            
            st.subheader("👀 Data Preview")
            st.dataframe(df.head(3))
            
            # Memory optimization - drop unused columns temporarily
            columns_to_keep = [col for col in df.columns if col in ['Score', 'Text', 'HelpfulnessNumerator', 'HelpfulnessDenominator']]
            df = df[columns_to_keep]
            
            # Create tabs
            tab1, tab2, tab3 = st.tabs(["⭐ Ratings", "❤️ Helpfulness", "😊 Sentiment"])
            
            with tab1:
                st.header("Star Rating Analysis")
                
                if 'Score' in df.columns:
                    # Calculate rating distribution
                    rating_counts = df['Score'].value_counts().sort_index()
                    
                    # Display metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        avg_rating = df['Score'].mean()
                        st.metric("Average Rating", f"{avg_rating:.2f}")
                    with col2:
                        most_common = rating_counts.idxmax()
                        st.metric("Most Common Rating", most_common)
                    with col3:
                        total_reviews = len(df)
                        st.metric("Total Reviews", f"{total_reviews:,}")
                    
                    # Show rating distribution
                    st.subheader("Rating Distribution")
                    
                    # Create a simple table for ratings
                    rating_table = pd.DataFrame({
                        'Star Rating': rating_counts.index,
                        'Count': rating_counts.values,
                        'Percentage': (rating_counts.values / len(df) * 100).round(1)
                    })
                    st.dataframe(rating_table)
                    
                    # Simple bar chart using Streamlit
                    st.bar_chart(rating_counts)
                    
                else:
                    st.warning("⚠️ 'Score' column not found in the dataset")
            
            with tab2:
                st.header("Helpfulness Analysis")
                
                helpfulness_available = 'HelpfulnessNumerator' in df.columns and 'HelpfulnessDenominator' in df.columns
                
                if helpfulness_available:
                    # Calculate helpfulness ratio
                    df['Helpfulness_Ratio'] = np.where(
                        df['HelpfulnessDenominator'] > 0,
                        df['HelpfulnessNumerator'] / df['HelpfulnessDenominator'],
                        0
                    )
                    
                    # Helpfulness metrics
                    col1, col2 = st.columns(2)
                    with col1:
                        avg_help = df['Helpfulness_Ratio'].mean()
                        st.metric("Average Helpfulness", f"{avg_help:.3f}")
                    with col2:
                        helpful_reviews = len(df[df['Helpfulness_Ratio'] > 0])
                        st.metric("Helpful Reviews", f"{helpful_reviews:,}")
                    
                    # Helpfulness by rating
                    if 'Score' in df.columns:
                        st.subheader("Helpfulness by Star Rating")
                        help_by_rating = df.groupby('Score')['Helpfulness_Ratio'].mean()
                        
                        help_table = pd.DataFrame({
                            'Star Rating': help_by_rating.index,
                            'Average Helpfulness': help_by_rating.values.round(3)
                        })
                        st.dataframe(help_table)
                    
                    # Review length analysis if Text column exists
                    if 'Text' in df.columns:
                        # Calculate length for sample only to save memory
                        sample_df = df.sample(min(1000, len(df)))
                        sample_df['Review_Length'] = sample_df['Text'].astype(str).str.len()
                        
                        # Calculate correlation
                        correlation = sample_df['Review_Length'].corr(sample_df['Helpfulness_Ratio'])
                        if not pd.isna(correlation):
                            st.metric(
                                "Length vs Helpfulness Correlation", 
                                f"{correlation:.3f}",
                                help="1.0 = perfect correlation, 0 = no correlation"
                            )
                            
                            # Interpretation
                            if correlation > 0.3:
                                st.success("📝 **Insight:** Longer reviews tend to be more helpful!")
                            elif correlation < -0.3:
                                st.warning("📝 **Insight:** Shorter reviews tend to be more helpful!")
                            else:
                                st.info("📝 **Insight:** Review length doesn't strongly affect helpfulness.")
                
                else:
                    st.warning("⚠️ Helpfulness columns not found in dataset")
            
            with tab3:
                st.header("Sentiment Analysis")
                
                if 'Text' in df.columns:
                    with st.spinner('Analyzing sentiment... (analyzing sample of 500 reviews)'):
                        # Analyze sentiment for a sample to save memory
                        sample_size = min(500, len(df))
                        sample_df = df.sample(sample_size)
                        
                        sentiments = []
                        for text in sample_df['Text'].astype(str):
                            sentiment = simple_sentiment(text)
                            sentiments.append(sentiment)
                        
                        sample_df['Sentiment'] = sentiments
                    
                    # Sentiment metrics
                    positive = sum(1 for s in sentiments if s == 1)
                    negative = sum(1 for s in sentiments if s == -1)
                    neutral = sum(1 for s in sentiments if s == 0)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Positive Reviews", positive)
                    with col2:
                        st.metric("Negative Reviews", negative)
                    with col3:
                        st.metric("Neutral Reviews", neutral)
                    
                    # Sentiment distribution
                    st.subheader("Sentiment Distribution (Sample)")
                    
                    sentiment_counts = pd.Series(sentiments).value_counts()
                    sentiment_labels = {-1: 'Negative', 0: 'Neutral', 1: 'Positive'}
                    labeled_counts = sentiment_counts.rename(index=sentiment_labels)
                    
                    st.bar_chart(labeled_counts)
                    
                else:
                    st.warning("⚠️ 'Text' column not found in dataset")
        
        else:
            st.error("❌ Failed to load data. Please check the file format.")
    
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        st.info("Please make sure you're using a valid CSV file from the Amazon Reviews dataset.")

else:
    st.info("👆 Please upload a CSV file to begin analysis (up to 500MB).")
    st.markdown("""
    **Need test data? Download from:**
    - [Kaggle: Amazon Fine Food Reviews](https://www.kaggle.com/snap/amazon-fine-food-reviews)
    - [Kaggle: Amazon Electronics Reviews](https://www.kaggle.com/datafiniti/consumer-reviews-of-amazon-products)
    """)

# Footer
st.markdown("---")
st.markdown("### 🎓 Computer Engineering Final Year Project")
st.markdown("**Data Analytics Portfolio Project • Built with Streamlit**")
st.markdown("**⚡ Optimized for large files up to 500MB**")