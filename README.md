# Ai-Powered-Sales-Drop-Investigation-System
AI-Powered Sales Drop Investigation System that leverages LLMs, RAG, and data analytics to automatically identify sales decline patterns, uncover root causes, generate actionable insights, and visualize trends through interactive dashboards.
# 📉 AI-Powered Sales Drop Investigation System

## Overview
AI-Powered Sales Drop Investigation System that leverages Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), and data analytics to automatically identify sales decline patterns, uncover root causes, generate actionable insights, and visualize trends through interactive dashboards.
## Dataset

⚠️ Note: The original sales dataset has been removed from this repository to reduce storage usage and comply with GitHub repository size limitations.

Before running the project, download a sales dataset from Kaggle and place it in the `data/` directory.

Recommended Kaggle datasets:
- Superstore Sales Dataset
- Retail Sales Dataset
- Sales Forecasting Dataset
- E-commerce Sales Dataset

Example folder structure:

data/
├── sales_data.csv

After downloading the dataset, update the file path in the configuration file if required and execute the preprocessing pipeline.

## Running the Project

1. Download a sales dataset from Kaggle.
2. Place the dataset inside the `data/` folder.
3. Run preprocessing:

```bash
python preprocess.py
## Features
- Automated sales drop detection
- Root cause analysis using AI
- LLM-powered business insights
- RAG-based contextual recommendations
- Interactive Streamlit dashboards
- Trend and anomaly detection
- SQL-based sales analytics
- Data visualization and reporting

## Tech Stack
- Python
- Pandas
- NumPy
- Streamlit
- Plotly
- SQL
- LangChain
- FAISS
- Gemini/OpenAI

## Project Workflow

Sales Data → Data Processing → Sales Analysis → RAG Retrieval → LLM Investigation → Dashboard Insights

## Installation

```bash
git clone https://github.com/yourusername/AI-Powered-Sales-Drop-Investigation-System.git
cd AI-Powered-Sales-Drop-Investigation-System
pip install -r requirements.txt
