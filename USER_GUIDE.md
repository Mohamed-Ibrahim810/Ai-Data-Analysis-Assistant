# Data Analysis Web App - User Guide

A concise guide to help you use the Data Analysis Web App effectively.

## Table of Contents

- [Data Analysis Web App - User Guide](#data-analysis-web-app---user-guide)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Cloud Access](#cloud-access)
    - [Local Installation](#local-installation)
  - [Uploading Data](#uploading-data)
  - [Analyzing Data](#analyzing-data)
  - [Transforming Data](#transforming-data)
    - [1. Filter Data](#1-filter-data)
    - [2. Add/Remove Columns](#2-addremove-columns)
    - [3. Handle Missing Values](#3-handle-missing-values)
    - [4. Transform Column](#4-transform-column)
    - [5. Change Data Type](#5-change-data-type)
    - [6. Sort Data](#6-sort-data)
    - [Reset Data](#reset-data)
  - [Downloading Results](#downloading-results)
  - [Tips for Best Results](#tips-for-best-results)
  - [Troubleshooting](#troubleshooting)

## Getting Started

### Cloud Access

- Visit [Ai-Data-analysis-Assistant](https://ai-data-analysis-assistant-5hpawoeffw2hlq6x6prqcc.streamlit.app/)
- No installation required

### Local Installation

```bash
streamlit run app.py
```

- Ensure your Google API key is configured (see README.md)

## Uploading Data

- Click "Browse files" or drag and drop your CSV/Excel file (max 100MB)
- Data will display automatically after upload

## Analyzing Data

1. **Preview Your Data**

   - See dataset shape, first rows, and column types

2. **Ask Questions**
   - Type natural language questions in the input field
   - Example questions:
     - "What is the average sales amount?"
     - "Which region has the highest average sales?"
     - "What is the correlation between price and quantity?"
     - "How many missing values are in each column?"

## Transforming Data

### 1. Filter Data

- **Categorical columns:** Select values to keep
- **Numeric columns:** Set range using slider

### 2. Add/Remove Columns

- **Remove columns:** Select columns to remove
- **Create new column:**
  - Simple calculation (e.g., Price × 0.9 for discount)
  - Combine columns (e.g., First_Name + Last_Name)

### 3. Handle Missing Values

- **Drop rows:** Remove rows with missing values in selected columns
- **Fill values:** Replace with mean, median, mode, or custom value

### 4. Transform Column

- **Numeric:** Normalize, standardize, log transform, square root
- **Text:** Convert case, one-hot encode

### 5. Change Data Type

- Convert columns to int, float, string, category, boolean, or datetime

### 6. Sort Data

- Select column and sort direction

### Reset Data

- Click "Reset to Original Data" to undo all transformations

## Downloading Results

- Navigate to "Download Data" tab
- Select format (CSV or Excel)
- Enter filename
- Click download button

## Tips for Best Results

1. **Start with exploration** before transformation
2. **Check transformation history** to review changes
3. **Handle missing values early** in your workflow
4. **Use appropriate transformations** for your data type
5. **Ask specific questions** for better AI analysis

## Troubleshooting

- **File upload errors:** Ensure file is CSV or Excel format under 100MB
- **Missing data:** Use data preview to check dataset structure
- **Slow performance:** Consider reducing dataset size for large files
- **API key issues:** Verify your Google API key is correctly configured
