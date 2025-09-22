# CORD-19 Metadata Analysis 📊

A comprehensive analysis of the CORD-19 dataset metadata, exploring patterns in COVID-19 research publications through data exploration, visualization, and an interactive web application.

## 📖 Overview
This project analyzes the metadata from the CORD-19 dataset, which contains information about COVID-19 and coronavirus-related research papers. The analysis provides insights into publication trends, journal distributions, and common themes in COVID-19 research through data visualization and an interactive Streamlit dashboard.

## 🚀 Features
Data Exploration: Comprehensive analysis of dataset structure and quality

Temporal Analysis: Publication trends over time, focusing on the COVID-19 pandemic period

Journal Analysis: Identification of top publishing journals and sources

Text Analysis: Word frequency analysis and word clouds of paper titles

Interactive Dashboard: Streamlit web application with filters and visualizations

Data Cleaning: Robust handling of missing values and inconsistent date formats

## 📊 Key Insights
### Publication Trends
Explosive growth in COVID-19 research publications starting in 2020

Identification of key journals leading coronavirus research

Temporal patterns reflecting the pandemic timeline

### Text Analysis
Most frequent words in paper titles reveal research focus areas

Common themes include clinical studies, transmission, and therapeutic approaches

Evolution of research topics over time

### Data Quality
Analysis of missing values across different metadata fields

Strategies for handling incomplete records

Data validation and cleaning approaches

## 🛠️ Installation
Prerequisites
Python 3.7 or higher

pip (Python package installer)

Steps
Clone the repository:
```bash
git clone https://github.com/Jenny-light/Frameworks_Assignment.git
cd cord19-metadata-analysis
```
Install required packages:
```
pip install -r requirements.txt
Download the CORD-19 metadata file:
```
Visit the CORD-19 dataset page

Download the metadata.csv file

Place it in the project root directory

## 📁 Project Structure

week8assignment/

├── metadata.csv          # CORD-19 metadata file (not included in the repository)

├── analysis.py           # Main analysis script

├── app.py               # Streamlit application

├── cord19_analysis.png  # Generated visualization

├── wordcloud.png        # Word cloud image

└── README.md           # Project documentation

## 🎯 Usage
Running the Analysis
Execute the main analysis script to generate visualizations and insights:

```bash
python src/analysis.py
```
This will:

Load and clean the metadata

Generate statistical summaries

Create visualizations in the outputs/ directory

Display key findings in the console

Launching the Streamlit App
Start the interactive dashboard:

```bash
streamlit run src/app.py
```
The application will open in your default browser at http://localhost:8501

Interactive Features
Year Range Filter: Adjust publication year range using sliders

Journal Selection: Filter by top publishing journals

Word Analysis: Explore frequent words in paper titles

Data Sampling: Browse random samples of the dataset

## 📈 Sample Visualizations
Analysis
<img width="4470" height="3569" alt="cord19_analysis" src="https://github.com/user-attachments/assets/b373e461-99a7-4abf-9d48-7b14a15900b2" />

Title Word Cloud
<img width="3334" height="1774" alt="wordcloud" src="https://github.com/user-attachments/assets/5ead918f-d54a-4280-99b7-543b0a6ac961" />


## 🔍 Key Findings
1. Rapid Research Response
Unprecedented growth in publications during 2020-2021

Peak publication rates correlating with pandemic waves

2. Journal Distribution
Concentration of COVID-19 research in medical and virology journals

High-impact journals leading the publication effort

3. Research Focus Areas
Clinical studies and case reports dominate

Significant focus on transmission dynamics and prevention

Growing emphasis on therapeutic approaches over time

## 🎓 Technical Details
Data Processing Pipeline
Data Loading: Efficient handling of large CSV files

Data Cleaning: Missing value imputation and date standardization

Feature Engineering: Creation of derived variables (word counts, publication years)

Analysis: Statistical summaries and pattern identification

Visualization: Multiple chart types for comprehensive insights

Technologies Used
Pandas: Data manipulation and analysis

Matplotlib/Seaborn: Data visualization

WordCloud: Text analysis visualization

Streamlit: Interactive web application

NumPy: Numerical computations

## 🚧 Challenges & Solutions
Data Quality Issues
Challenge: High percentage of missing abstracts and inconsistent date formats

Solution: Strategic imputation and flexible date parsing functions

Performance Optimization
Challenge: Large dataset size (~1GB+)

Solution: Efficient memory usage and selective column loading

Text Processing
Challenge: Noise in title text and special characters

Solution: Regular expressions and custom stop word lists

## 📚 Learnings
This project demonstrates:

End-to-end data science workflow from raw data to interactive application

Best practices in data cleaning and validation

Effective visualization techniques for different data types

Building user-friendly interfaces for data exploration

Handling real-world dataset challenges and inconsistencies

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

Fork the project

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments
Allen Institute for AI for maintaining the CORD-19 dataset

Kaggle for hosting the dataset

The research community for their contributions to COVID-19 literature

Python Instructors at the Power Learn Project Community

## 📞 Contact
For questions or suggestions, please open an issue or contact:

Jennifer Omoregie

Email: jennylightomoregie@gmail.com

LinkedIn: https://www.linkedin.com/in/jennifer-omoregie-83388232a?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app 



