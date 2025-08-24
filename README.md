# 📊 Amazon Reviews Analyzer

A Streamlit-based web application for analyzing Amazon product reviews, performing sentiment analysis, and identifying patterns in customer feedback.

## 📁 Dataset Information

This app works with Amazon review datasets in CSV format. The expected columns are:

**Required Columns:**
- `Score` (1-5 star rating)
- `Text` (Review content)
- `HelpfulnessNumerator` (Number of helpful votes)
- `HelpfulnessDenominator` (Total votes)

**Optional Columns:**
- `Summary` (Review headline)
- `ProfileName` (User name)
- `Time` (Timestamp)

## 📥 Where to Get CSV Files

### **Recommended Datasets:**

1. **Amazon Fine Food Reviews** (Ideal for testing)
   - **Download**: [Kaggle - Amazon Fine Food Reviews](https://www.kaggle.com/snap/amazon-fine-food-reviews)
   - **Size**: ~260MB
   - **Reviews**: 568,454 food reviews

2. **Amazon Electronics Reviews** 
   - **Download**: [Kaggle - Amazon Electronics](https://www.kaggle.com/datafiniti/consumer-reviews-of-amazon-products)
   - **Size**: ~30MB
   - **Reviews**: 34,000+ electronics reviews

3. **Amazon Product Reviews 2023**
   - **Download**: [Kaggle - Amazon Reviews 2023](https://www.kaggle.com/datasets/asaniczka/amazon-reviews-2023)
   - **Size**: ~100MB
   - **Reviews**: Latest Amazon reviews

### **How to Use:**
1. Create a free Kaggle account
2. Download any of the above datasets
3. Extract the CSV file
4. Upload it to the web app

## 🚀 Features

- **Rating Analysis**: Distribution and statistics of star ratings
- **Helpfulness Analysis**: Correlation between review length and helpfulness votes  
- **Sentiment Analysis**: Basic sentiment detection using keyword matching
- **Large File Support**: Handles datasets up to 500MB
- **Interactive Dashboard**: Real-time data exploration and visualization

## 🛠️ Tech Stack

- **Python** (Pandas, NumPy)
- **Streamlit** (Web framework)
- **Data Analysis** (Correlation, Statistics, Visualization)

## 📦 Installation & Usage

```bash
# 1. Install dependencies
pip install streamlit pandas numpy

# 2. Run the application
streamlit run app.py

# 3. Upload your CSV file through the web interface
