# Data Analysis Web App - User Guide

This guide will help you get started with the Data Analysis Web App and show you how to make the most of its features.

## Table of Contents

- [Data Analysis Web App - User Guide](#data-analysis-web-app---user-guide)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Cloud Access (Recommended)](#cloud-access-recommended)
    - [Local Installation](#local-installation)
  - [Uploading Your Data](#uploading-your-data)
  - [Analyzing Your Data](#analyzing-your-data)
  - [Transforming Your Data](#transforming-your-data)
    - [1. Filter Data](#1-filter-data)
    - [2. Add/Remove Columns](#2-addremove-columns)
    - [3. Handle Missing Values](#3-handle-missing-values)
    - [4. Transform Column](#4-transform-column)
    - [5. Change Data Type](#5-change-data-type)
    - [6. Sort Data](#6-sort-data)
    - [Resetting Your Data](#resetting-your-data)
  - [Downloading Your Results](#downloading-your-results)
  - [Tips and Best Practices](#tips-and-best-practices)
  - [Troubleshooting](#troubleshooting)
    - [Common Issues and Solutions](#common-issues-and-solutions)

## Getting Started

You can access the Data Analysis Web App in two ways:

### Cloud Access (Recommended)

1. Visit the app at [your-app-url-here](your-app-url-here)
2. No installation required
3. Works on any device with a web browser
4. Always up to date with the latest features

Benefits of using the cloud version:

- No setup required
- Access from anywhere
- No local resources used
- Automatic updates
- Works on any device (desktop, tablet, mobile)

### Local Installation

If you prefer to run the app locally:

1. Launch the application by running:
   ```bash
   streamlit run app.py
   ```
2. The application will open in your default web browser at `http://localhost:8501`
3. Make sure you have your Google API key set up (see the README.md for instructions)

## Uploading Your Data

1. On the main page, you'll see a file uploader widget
2. Click on "Browse files" or drag and drop your file
3. The application accepts CSV and Excel (.xlsx) files up to 100MB in size
4. Once uploaded, your data will be displayed in the application

**Example:**

- If you have a sales dataset named `sales_data.csv`, upload this file to begin analysis

## Analyzing Your Data

After uploading your data, navigate to the "Data Analysis" tab:

1. **Preview Your Data**

   - Expand the "Preview of the dataset" section to see:
     - Dataset shape (rows × columns)
     - First 5 rows of data
     - Column types

2. **Ask Questions About Your Data**
   - Type your question in the text input field
   - Click Enter to submit your question
   - The AI will analyze your data and provide an answer

**Example Questions:**

- "What is the average sales amount?"
- "Is there a correlation between customer age and purchase amount?"
- "What are the top 5 products by revenue?"
- "How many missing values are in each column?"
- "What is the distribution of customer locations?"

## Transforming Your Data

Navigate to the "Data Transformation" tab to modify your dataset:

### 1. Filter Data

**For categorical columns:**

1. Select "Filter Data" from the dropdown
2. Choose a categorical column (e.g., "Country")
3. Select values to keep (e.g., "USA", "Canada")
4. Click "Apply Filter"

**For numeric columns:**

1. Select "Filter Data" from the dropdown
2. Choose a numeric column (e.g., "Price")
3. Use the slider to set a range (e.g., $10-$50)
4. Click "Apply Filter"

### 2. Add/Remove Columns

**To remove columns:**

1. Select "Add/Remove Columns" from the dropdown
2. Choose "Remove Columns"
3. Select columns to remove
4. Click "Remove Selected Columns"

**To create a new column with a calculation:**

1. Select "Add/Remove Columns" from the dropdown
2. Choose "Create New Column"
3. Enter a name for the new column (e.g., "Discount_Price")
4. Select "Simple Calculation"
5. Choose a column (e.g., "Price")
6. Select an operation (e.g., "Multiply")
7. Enter a value (e.g., 0.9 for 10% discount)
8. Click "Create Column"

**To combine columns:**

1. Select "Add/Remove Columns" from the dropdown
2. Choose "Create New Column"
3. Enter a name (e.g., "Full_Name")
4. Select "Combine Columns"
5. Choose columns to combine (e.g., "First_Name", "Last_Name")
6. Enter a separator (e.g., " ")
7. Click "Create Column"

### 3. Handle Missing Values

**To drop rows with missing values:**

1. Select "Handle Missing Values" from the dropdown
2. Choose "Drop rows with missing values"
3. Select columns to check for missing values
4. Click "Drop Rows"

**To fill missing values:**

1. Select "Handle Missing Values" from the dropdown
2. Choose "Fill missing values"
3. Select a column with missing values
4. Choose a fill method:
   - For numeric columns: Mean, Median, or Custom value
   - For text columns: Most frequent value or Custom value
5. Click "Fill Missing Values"

### 4. Transform Column

**For numeric columns:**

1. Select "Transform Column" from the dropdown
2. Choose a numeric column
3. Select a transformation:
   - Normalize (0-1)
   - Standardize (z-score)
   - Log transform
   - Square root
4. Click "Apply Transformation"

**For text columns:**

1. Select "Transform Column" from the dropdown
2. Choose a text column
3. Select a transformation:
   - Convert to uppercase
   - Convert to lowercase
   - One-hot encode
4. Click "Apply Transformation"

### 5. Change Data Type

1. Select "Change Data Type" from the dropdown
2. Choose a column
3. Select a new data type:
   - int
   - float
   - string
   - category
   - boolean
   - datetime
4. Click "Change Data Type"

### 6. Sort Data

1. Select "Sort Data" from the dropdown
2. Choose a column to sort by
3. Select sort order (Ascending or Descending)
4. Click "Sort Data"

### Resetting Your Data

If you want to undo all transformations:

1. Click "Reset to Original Data" at the top of the transformation tab

## Downloading Your Results

After analyzing and transforming your data, navigate to the "Download Data" tab:

1. Select your preferred file format (CSV or Excel)
2. Enter a filename (without extension)
3. Click the download button

**Note:** If you choose Excel format, your transformation history will be included as a separate sheet in the workbook.

## Tips and Best Practices

1. **Start with data exploration**

   - Before transforming your data, use the AI analysis to understand your dataset

2. **Check transformation history**

   - Expand the "Transformation History" section to review all changes made

3. **Handle missing values early**

   - Address missing values before performing other transformations

4. **Use appropriate transformations**

   - For skewed numeric data, consider log transformations
   - For categorical data with many categories, consider grouping or one-hot encoding

5. **Save intermediate results**

   - Download your data after important transformations as a backup

6. **Ask specific questions**
   - When using the AI analysis, be specific in your questions for better results

## Troubleshooting

### Common Issues and Solutions

**File upload errors:**

- Ensure your file is in CSV or Excel format
- Check that the file size is under 100MB
- Try saving your Excel file as CSV if problems persist

**Missing values in results:**

- Check if your data contains NaN or null values
- Use the "Handle Missing Values" transformation to address them

**Data type errors:**

- If a transformation fails due to data type issues, use the "Change Data Type" option first
- Ensure numeric operations are only applied to numeric columns

**API key issues:**

- Verify that your Google API key is correctly set up
- Check that the key has access to the Gemini API

**Performance issues with large datasets:**

- Consider filtering or sampling your data to reduce size
- Focus on relevant columns by removing unnecessary ones

If you encounter any other issues, please refer to the project's GitHub repository for support.
