import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import re
import streamlit as st
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Load the metadata
print("Loading CORD-19 metadata...")
df = pd.read_csv('metadata.csv')

print("=== PART 1: DATA EXPLORATION ===")

# Examine first few rows
print("\n1. First few rows:")
print(df.head())

print("\n2. DataFrame dimensions:")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

print("\n3. Data types:")
print(df.dtypes)

print("\n4. Columns in the dataset:")
print(df.columns.tolist())

# Check for missing values
print("\n5. Missing values in important columns:")
important_cols = ['title', 'abstract', 'publish_time', 'journal', 'authors', 'doi']
missing_data = df[important_cols].isnull().sum()
missing_percent = (missing_data / len(df)) * 100
missing_df = pd.DataFrame({'Missing Count': missing_data, 'Percentage': missing_percent})
print(missing_df)

print("\n6. Basic statistics for numerical columns:")
print(df.describe())

# Additional exploration
print("\n7. Memory usage:")
print(df.info(memory_usage='deep')) 

print("\n=== PART 2: DATA CLEANING AND PREPARATION ===")

# Create a copy for cleaning
df_clean = df.copy()

print("1. Handling missing values...")
# Check columns with high missingness
high_missing_cols = missing_df[missing_df['Percentage'] > 50].index.tolist()
print(f"Columns with >50% missing values: {high_missing_cols}")

# Fill missing abstracts with empty string, titles with 'Unknown Title'
df_clean['abstract'] = df_clean['abstract'].fillna('')
df_clean['title'] = df_clean['title'].fillna('Unknown Title')

# For journals, fill with 'Unknown Journal'
df_clean['journal'] = df_clean['journal'].fillna('Unknown Journal')

# Convert publish_time to datetime
print("\n2. Converting date columns...")
def convert_publish_time(date_str):
    try:
        if pd.isna(date_str):
            return pd.NaT
        # Handle various date formats
        if isinstance(date_str, str):
            # Extract year if it's in format like "2020-03"
            if len(str(date_str)) == 7 and '-' in str(date_str):
                return pd.to_datetime(str(date_str) + '-01')
            # Handle just years
            elif len(str(date_str)) == 4:
                return pd.to_datetime(str(date_str) + '-01-01')
            else:
                return pd.to_datetime(date_str, errors='coerce')
        return pd.to_datetime(date_str, errors='coerce')
    except:
        return pd.NaT

df_clean['publish_time'] = df_clean['publish_time'].apply(convert_publish_time)

# Extract year from publication date
df_clean['publication_year'] = df_clean['publish_time'].dt.year

# Create abstract word count
df_clean['abstract_word_count'] = df_clean['abstract'].apply(lambda x: len(str(x).split()))

# Create title word count
df_clean['title_word_count'] = df_clean['title'].apply(lambda x: len(str(x).split()))

print(f"Date range: {df_clean['publication_year'].min()} - {df_clean['publication_year'].max()}")
print(f"Rows after cleaning: {len(df_clean)}")

# Remove rows with no title or invalid dates
initial_count = len(df_clean)
df_clean = df_clean[df_clean['title'] != 'Unknown Title']
df_clean = df_clean[df_clean['publication_year'] >= 1900]  # Reasonable year filter

print(f"Rows after removing invalid entries: {len(df_clean)}")
print(f"Removed {initial_count - len(df_clean)} invalid rows")  

print("\n=== PART 3: DATA ANALYSIS AND VISUALIZATION ===")

# Set up plotting style
plt.style.use('default')
sns.set_palette("husl")

# 1. Papers by publication year
print("1. Analyzing papers by publication year...")
yearly_counts = df_clean['publication_year'].value_counts().sort_index()
recent_years = yearly_counts[yearly_counts.index >= 2010]  # Focus on recent years

# 2. Top journals
print("2. Identifying top journals...")
top_journals = df_clean['journal'].value_counts().head(15)
top_journals = top_journals[top_journals.index != 'Unknown Journal']

# 3. Most frequent words in titles
print("3. Analyzing frequent words in titles...")
def clean_text(text):
    # Remove special characters and convert to lowercase
    text = re.sub(r'[^\w\s]', '', str(text))
    return text.lower()

# Get all titles and split into words
all_titles = ' '.join(df_clean['title'].astype(str))
cleaned_titles = clean_text(all_titles)
words = cleaned_titles.split()

# Remove common stop words
stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'from', 'as', 'that', 'this', 'these', 'those', 'which', 'what', 'when', 'where', 'who', 'whom', 'how', 'why', 'via', 'using', 'based', 'study', 'review', 'analysis', 'covid', '19', 'sars', 'cov', '2', 'coronavirus', 'pandemic'}
filtered_words = [word for word in words if word not in stop_words and len(word) > 2]

word_freq = Counter(filtered_words).most_common(20)

# Create visualizations
print("4. Creating visualizations...")
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# Plot 1: Publications over time
axes[0,0].plot(recent_years.index, recent_years.values, marker='o', linewidth=2)
axes[0,0].set_title('Number of Publications Over Time (2010+)', fontsize=14, fontweight='bold')
axes[0,0].set_xlabel('Year')
axes[0,0].set_ylabel('Number of Publications')
axes[0,0].tick_params(axis='x', rotation=45)
axes[0,0].grid(True, alpha=0.3)

# Plot 2: Top journals
top_journals_plot = top_journals.head(10)
axes[0,1].barh(range(len(top_journals_plot)), top_journals_plot.values)
axes[0,1].set_yticks(range(len(top_journals_plot)))
axes[0,1].set_yticklabels([journal[:50] + '...' if len(journal) > 50 else journal for journal in top_journals_plot.index])
axes[0,1].set_title('Top 10 Journals by Publication Count', fontsize=14, fontweight='bold')
axes[0,1].set_xlabel('Number of Publications')

# Plot 3: Word frequency
words, counts = zip(*word_freq)
axes[1,0].bar(range(len(words)), counts)
axes[1,0].set_xticks(range(len(words)))
axes[1,0].set_xticklabels(words, rotation=45, ha='right')
axes[1,0].set_title('Top 20 Words in Paper Titles', fontsize=14, fontweight='bold')
axes[1,0].set_ylabel('Frequency')

# Plot 4: Abstract word count distribution
axes[1,1].hist(df_clean['abstract_word_count'].clip(0, 500), bins=50, alpha=0.7)
axes[1,1].set_title('Distribution of Abstract Word Counts', fontsize=14, fontweight='bold')
axes[1,1].set_xlabel('Word Count')
axes[1,1].set_ylabel('Frequency')
axes[1,1].axvline(df_clean['abstract_word_count'].median(), color='red', linestyle='--', 
                 label=f'Median: {df_clean["abstract_word_count"].median():.0f}')
axes[1,1].legend()

plt.tight_layout()
plt.savefig('cord19_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# Word cloud
print("5. Generating word cloud...")
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(filtered_words))

plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Paper Titles', fontsize=16, fontweight='bold') 
plt.tight_layout()
plt.savefig('wordcloud.png', dpi=300, bbox_inches='tight')
plt.show()

# Print summary statistics
print("\n=== SUMMARY STATISTICS ===")
print(f"Total papers: {len(df_clean)}")
print(f"Papers with abstracts: {len(df_clean[df_clean['abstract'].str.len() > 0])}")
print(f"Time span: {df_clean['publication_year'].min()} - {df_clean['publication_year'].max()}")
print(f"Most recent year: {df_clean['publication_year'].max()} with {yearly_counts.max()} papers")
print(f"Median abstract length: {df_clean['abstract_word_count'].median()} words")
print(f"Unique journals: {df_clean['journal'].nunique()}")