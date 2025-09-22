# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import re

def load_data():
    """Load and clean the dataset"""
    df = pd.read_csv('metadata.csv')

    # Basic cleaning
    df['abstract'] = df['abstract'].fillna('')
    df['title'] = df['title'].fillna('Unknown Title')
    df['journal'] = df['journal'].fillna('Unknown Journal')
    
    # Convert dates
    def convert_date(date_str):
        try:
            if pd.isna(date_str):
                return pd.NaT
            if isinstance(date_str, str):
                if len(str(date_str)) == 4:
                    return pd.to_datetime(str(date_str) + '-01-01')
            return pd.to_datetime(date_str, errors='coerce')
        except:
            return pd.NaT
    
    df['publish_time'] = df['publish_time'].apply(convert_date)
    df['publication_year'] = df['publish_time'].dt.year
    df = df[df['publication_year'] >= 2010]  # Focus on recent years
    
    return df

def main():
    st.set_page_config(page_title="CORD-19 Metadata Analysis", layout="wide")
    
    st.title("📊 CORD-19 Dataset Analysis")
    st.markdown("""
    This interactive dashboard explores the metadata from the CORD-19 dataset, 
    containing COVID-19 related research papers.
    """)
    
    # Load data
    with st.spinner('Loading data...'):
        df = load_data()
    
    # Sidebar filters
    st.sidebar.header("Filters")
    min_year = int(df['publication_year'].min())
    max_year = int(df['publication_year'].max())
    year_range = st.sidebar.slider(
        "Publication Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )
    
    # Filter data based on selections
    filtered_df = df[(df['publication_year'] >= year_range[0]) & 
                    (df['publication_year'] <= year_range[1])]
    
    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Papers", len(filtered_df))
        st.metric("Papers with Abstracts", 
                 len(filtered_df[filtered_df['abstract'].str.len() > 0]))
    
    with col2:
        st.metric("Date Range", f"{year_range[0]} - {year_range[1]}")
        st.metric("Unique Journals", filtered_df['journal'].nunique())
    
    # Tabs for different analyses
    tab1, tab2, tab3, tab4 = st.tabs(["Publications Over Time", "Top Journals", 
                                     "Title Analysis", "Data Sample"])
    
    with tab1:
        st.subheader("Publications Over Time")
        yearly_counts = filtered_df['publication_year'].value_counts().sort_index()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(yearly_counts.index, yearly_counts.values, marker='o', linewidth=2)
        ax.set_title('Number of Publications Over Time')
        ax.set_xlabel('Year')
        ax.set_ylabel('Number of Publications')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
    
    with tab2:
        st.subheader("Top Publishing Journals")
        top_n = st.slider("Number of journals to show", 5, 20, 10)
        top_journals = filtered_df['journal'].value_counts().head(top_n)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        top_journals.plot(kind='barh', ax=ax)
        ax.set_title(f'Top {top_n} Journals by Publication Count')
        ax.set_xlabel('Number of Publications')
        st.pyplot(fig)
    
    with tab3:
        st.subheader("Title Word Analysis")
        
        # Word frequency
        all_titles = ' '.join(filtered_df['title'].astype(str))
        words = re.findall(r'\b[a-z]{3,}\b', all_titles.lower())
        stop_words = {'the', 'and', 'for', 'with', 'using', 'based', 'study', 
                     'review', 'analysis', 'covid', '19', 'sars', 'cov', '2'}
        filtered_words = [word for word in words if word not in stop_words]
        word_freq = Counter(filtered_words).most_common(15)
        
        # Word cloud
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Top 15 Words in Titles**")
            word_df = pd.DataFrame(word_freq, columns=['Word', 'Frequency'])
            st.dataframe(word_df, height=400)
        
        with col2:
            st.write("**Word Cloud**")
            wordcloud = WordCloud(width=400, height=300, background_color='white').generate(' '.join(filtered_words))
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)
    
    with tab4:
        st.subheader("Data Sample")
        st.write(f"Showing 10 random papers from the dataset ({len(filtered_df)} total):")
        sample_cols = ['title', 'journal', 'publication_year', 'authors']
        sample_df = filtered_df[sample_cols].sample(min(10, len(filtered_df)))
        st.dataframe(sample_df)
        
        # Data summary
        st.subheader("Data Summary")
        st.write(f"**Dataset Shape:** {filtered_df.shape}")
        st.write("**Column Information:**")
        col_info = pd.DataFrame({
            'Column': filtered_df.columns,
            'Non-Null Count': filtered_df.notnull().sum(),
              'Data Type': filtered_df.dtypes.astype(str)
        })
        st.dataframe(col_info)

if __name__ == "__main__":
    main()