# main.py
# PART 1: Setup and Data Loading

# 1. Importing the necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob

print("✅ Libraries imported successfully!")

# 2. Load the dataset (using a small sample first)
print("Loading dataset...")
try:
    # Load only first 10,000 rows to make it fast
    df = pd.read_csv('Reviews.csv', nrows=10000)
    print("✅ Dataset loaded successfully!")
except FileNotFoundError:
    print("❌ ERROR: File 'Reviews.csv' not found.")
    print("Please make sure the file is in the same folder as this script.")
    exit()

# 3. First glimpse of the data
print(f"\nThe dataset has {df.shape[0]} rows and {df.shape[1]} columns.")
print("\nFirst 3 rows:")
print(df.head(3))

# 4. Show the column names
print("\nColumn names:")
print(list(df.columns))

# Add this line to pause and wait for you to press Enter before continuing
input("\nPress Enter to continue to Part 2...")

# PART 2: Data Cleaning

print("\n--- PART 2: Cleaning Data ---")

# 5. Create a 'Helpfulness_Ratio'
df['Helpfulness_Ratio'] = np.where(
    df['HelpfulnessDenominator'] > 0,
    df['HelpfulnessNumerator'] / df['HelpfulnessDenominator'],
    0
)

# 6. Create a 'Review_Length' feature
df['Review_Length'] = df['Text'].str.len()

# 7. Convert Unix time to readable date
df['Date'] = pd.to_datetime(df['Time'], unit='s')

# 8. Check for missing values
print("Missing values in each column:")
print(df.isnull().sum())

# 9. Show our new features
print("\nNew features created:")
print(df[['Helpfulness_Ratio', 'Review_Length', 'Date']].head())

input("\nPress Enter to continue to Part 3...")

# PART 3: Analyzing Ratings

print("\n--- PART 3: Analyzing Star Ratings ---")

# 10. Create the rating distribution plot
plt.figure(figsize=(10, 5))
rating_plot = sns.countplot(x='Score', data=df, palette='viridis')
plt.title('Distribution of Amazon Reviews by Star Rating')
plt.xlabel('Star Rating (1-5)')
plt.ylabel('Number of Reviews')

# Add count labels on top of bars
for p in rating_plot.patches:
    rating_plot.annotate(f'{int(p.get_height())}', 
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', 
                        xytext=(0, 9), 
                        textcoords='offset points')

plt.tight_layout()
plt.show()

print("📊 Check the chart window that opened!")

input("\nPress Enter to continue to Part 4...")

# PART 4: Analyzing Helpfulness

print("\n--- PART 4: What Makes Reviews Helpful? ---")

# 11. Create subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

# Plot 1: Helpfulness by Rating
sns.boxplot(x='Score', y='Helpfulness_Ratio', data=df, ax=ax1)
ax1.set_title('Helpfulness Ratio by Star Rating')

# Plot 2: Helpfulness vs Length
sns.scatterplot(x='Review_Length', y='Helpfulness_Ratio', 
                hue='Score', data=df, alpha=0.6, ax=ax2, 
                palette='viridis')
ax2.set_xscale('log')  # Important for long reviews
ax2.set_title('Helpfulness vs. Review Length (log scale)')
ax2.set_xlabel('Review Length (log scale)')

plt.tight_layout()
plt.show()

# 12. Calculate correlation
correlation = df['Review_Length'].corr(df['Helpfulness_Ratio'])
print(f"\n📈 Correlation between Review Length and Helpfulness: {correlation:.3f}")

if correlation > 0.3:
    print("➡️ Longer reviews tend to be more helpful!")
elif correlation < -0.3:
    print("➡️ Shorter reviews tend to be more helpful!")
else:
    print("➡️ Review length doesn't strongly affect helpfulness.")

input("\nPress Enter to continue to Part 5...")

# PART 5: Sentiment Analysis

print("\n--- PART 5: Analyzing Review Sentiment ---")
print("This might take a minute...")

# 13. Analyze sentiment of reviews
df['Sentiment'] = df['Text'].apply(lambda text: TextBlob(str(text)).sentiment.polarity)

# 14. Create sentiment vs rating plot
plt.figure(figsize=(10, 6))
sns.boxplot(x='Score', y='Sentiment', data=df)
plt.title('Sentiment Analysis of Reviews by Star Rating')
plt.xlabel('Star Rating')
plt.ylabel('Sentiment Score (-1 to +1)')
plt.show()

# 15. Find interesting examples
negative_5_star = df[(df['Score'] == 5) & (df['Sentiment'] < -0.3)]
positive_1_star = df[(df['Score'] == 1) & (df['Sentiment'] > 0.3)]

print(f"\n🤔 Found {len(negative_5_star)} reviews that are 5-star but negative sentiment")
print(f"🤔 Found {len(positive_1_star)} reviews that are 1-star but positive sentiment")

if len(negative_5_star) > 0:
    print("\nExample of a sarcastic-looking 5-star review:")
    print(negative_5_star['Text'].iloc[0][:500] + "...")  # Show first 500 characters

print("\n🎉 Analysis complete! Check all the charts that opened.")

