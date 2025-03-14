Data Analysis Web App - Technical Documentation

This document provides detailed technical information about the Data Analysis Web App, including its architecture, implementation details, and code explanations.

-Table of Contents-

- [Architecture Overview](#architecture-overview)
- [Core Components](#core-components)
- [Data Flow](#data-flow)
- [Implementation Details](#implementation-details)
  - [Main Application Structure](#main-application-structure)
  - [Configuration](#configuration)
  - [Data Loading and Caching](#data-loading-and-caching)
- [AI Integration](#ai-integration)
- [Session State Management](#session-state-management)
- [Data Transformation Operations](#data-transformation-operations)
  - [1. Filter Data](#1-filter-data)
  - [2. Add/Remove Columns](#2-addremove-columns)
  - [3. Handle Missing Values](#3-handle-missing-values)
  - [4. Transform Columns](#4-transform-columns)
  - [5. Change Data Types](#5-change-data-types)
  - [6. Sort Data](#6-sort-data)
- [File Handling](#file-handling)
  - [Download Features:](#download-features)
  - [Download Process:](#download-process)
- [Error Handling](#error-handling)
- [Performance Considerations](#performance-considerations)
- [Security Considerations](#security-considerations)
- [Future Enhancements](#future-enhancements)
- [Deployment](#deployment)
  - [Streamlit Cloud Deployment](#streamlit-cloud-deployment)
    - [Deployment Features:](#deployment-features)
    - [Accessing the App:](#accessing-the-app)
    - [Cloud Configuration:](#cloud-configuration)
  - [Local Deployment](#local-deployment)

## Architecture Overview

The Data Analysis Web App is built using Streamlit, a Python framework for creating data applications.
The application follows a single-page architecture with tabbed navigation to organize different functionalities.
It integrates Google's Generative AI (Gemini) for natural language data analysis.

The application is designed to be:

- **User-friendly**: Simple interface with clear instructions
- **Responsive**: Efficient data handling with caching for large datasets
- **Flexible**: Support for various data formats and transformation operations
- **Secure**: API keys stored in environment variables or secrets

## Core Components

1. **Data Loading**: Handles file uploads and parsing
2. **Data Analysis**: Integrates with Gemini AI for natural language queries
3. **Data Transformation**: Provides various data manipulation operations
4. **Data Export**: Enables downloading transformed data in different formats
5. **Session Management**: Maintains state across user interactions

## Data Flow

1. User uploads a CSV or Excel file
2. File is parsed into a pandas DataFrame and cached
3. User interacts with the data through the UI
4. Transformations are applied to the DataFrame in memory
5. Transformation history is tracked in session state
6. Transformed data can be downloaded in CSV or Excel format

## Implementation Details

### Main Application Structure

The application is structured around a main Streamlit app with tabbed navigation:

1. **Data Analysis Tab**: Displays data preview and AI-powered analysis
2. **Data Transformation Tab**: Provides various data transformation options
3. **Download Data Tab**: Allows exporting the transformed data

### Configuration

The application uses a central configuration dictionary (`CONFIG`) to manage settings:

```python
CONFIG = {
    'MAX_FILE_SIZE': 100 * 1024 * 1024,  # 100MB
    'PREVIEW_ROWS': 5,
    'ALLOWED_EXTENSIONS': ['.csv', '.xlsx'],
    'TYPE_MAPPING': {
        'int': 'int64',
        'float': 'float64',
        'string': 'string',
        'category': 'category',
        'boolean': 'bool'
    }
}
```

This centralized configuration makes it easy to adjust application parameters without modifying core logic.

### Data Loading and Caching

The application uses Streamlit's caching mechanism to improve performance when loading data:

```python
@st.cache_data
def load_data(file):
    try:
        if not any(file.name.endswith(ext) for ext in CONFIG['ALLOWED_EXTENSIONS']):
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
            return None

        if file.name.endswith(".csv"):
            return pd.read_csv(file)
        else:  # Excel
            return pd.read_excel(file)
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None
```

This caching ensures that data is only loaded once, even if the user interacts with different parts of the application.

## AI Integration

The application integrates with Google's Generative AI (Gemini) to provide natural language data analysis:

```python
def get_api_key():
    api_key = os.getenv("GOOGLE_API_KEY") or (
        st.secrets["GOOGLE_API_KEY"] if hasattr(st, "secrets") and "GOOGLE_API_KEY" in st.secrets else None
    )
    if api_key:
        genai.configure(api_key=api_key)
    return api_key
```

When a user asks a question about their data, the application:

1. Constructs a detailed prompt with information about the DataFrame
2. Sends the prompt to the Gemini model
3. Displays the response to the user

The prompt includes:

- DataFrame shape and columns
- Data types
- Statistical summary
- Sample rows
- Missing value information
- Categorical column details
- Correlations for numeric columns

## Session State Management

The application uses Streamlit's session state to maintain data and state across user interactions:

```python
# Initialize session state variables
for key, default_value in {
    'transformed_df': None,
    'original_df': None,
    'transformation_history': [],
    'current_file': None
}.items():
    if key not in st.session_state:
        st.session_state[key] = default_value
```

This allows the application to:

- Track the original and transformed DataFrames
- Maintain a history of transformations
- Remember the current file being processed
- Reset to the original data when needed

## Data Transformation Operations

The application supports various data transformation operations:

### 1. Filter Data

- Filter categorical columns by selecting values
- Filter numeric columns by specifying ranges

### 2. Add/Remove Columns

- Remove selected columns
- Create new columns through calculations or combinations

### 3. Handle Missing Values

- Drop rows with missing values
- Fill missing values with mean, median, mode, or custom values

### 4. Transform Columns

- Normalize numeric columns (0-1 range)
- Standardize numeric columns (z-score)
- Apply log or square root transformations
- Convert text to uppercase/lowercase
- One-hot encode categorical columns

### 5. Change Data Types

- Convert columns to different data types
- Parse datetime columns

### 6. Sort Data

- Sort the dataset by any column in ascending or descending order

Each transformation is recorded in the transformation history, allowing users to track changes made to the data.

## File Handling

The application uses Streamlit's native download button functionality for all file downloads, providing a consistent and reliable download experience:

```python
def create_download_button(data, filename, mime_type, transformation_history=None):
    buffer = io.BytesIO()

    if mime_type == "text/csv":
        data.to_csv(buffer, index=False)
    else:  # Excel
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            data.to_excel(writer, index=False, sheet_name='Data')
            if transformation_history:
                pd.DataFrame({"Transformation": transformation_history}).to_excel(
                    writer, index=False, sheet_name='Transformation History'
                )

    buffer.seek(0)
    return st.download_button(
        label=f"📥 Download {filename}",
        data=buffer,
        file_name=filename,
        mime=mime_type
    )
```

### Download Features:

- **CSV Downloads**: Simple data export without transformation history
- **Excel Downloads**: Includes both data and transformation history in separate sheets
- **Memory Efficient**: Uses BytesIO buffer for file creation
- **User-Friendly**: Consistent download button interface for all file sizes

### Download Process:

1. User selects the desired file format (CSV or Excel)
2. Enters a filename (default: "transformed_data")
3. Clicks the download button
4. File is generated in memory and downloaded through the browser

The application supports two main download formats:

1. **CSV Format**:

   ```python
   def get_csv_download_link(df, filename):
       return create_download_button(df, filename, "text/csv")
   ```

2. **Excel Format**:
   ```python
   def get_excel_download_link(df, filename, transformation_history=None):
       return create_download_button(
           df, filename,
           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
           transformation_history
       )
   ```

## Error Handling

The application includes error handling throughout to provide a robust user experience:

- File loading errors are caught and displayed to the user
- Data type conversion errors include helpful messages
- Transformations that could cause errors (like division by zero) include checks

## Performance Considerations

Several optimizations are implemented to handle large datasets efficiently:

- Data loading is cached to prevent redundant processing
- Data previews show limited rows to reduce memory usage
- Transformation operations are applied in-place when possible

## Security Considerations

The application securely handles API keys through:

- Environment variables
- .env file loading
- Streamlit secrets management

No API keys are exposed in the code or UI.

## Future Enhancements

Potential improvements for future versions:

1. **Advanced Visualizations**: Add interactive charts and graphs
2. **Custom Transformations**: Allow users to write custom transformation code
3. **Data Validation**: Add data quality checks and validation rules
4. **Automated Insights**: Provide automatic data profiling and insights
5. **Export Transformation Code**: Generate Python code for transformations
6. **Collaborative Features**: Add sharing and collaboration capabilities
7. **Additional File Formats**: Support for more data formats (JSON, Parquet, etc.)
8. **Machine Learning Integration**: Add predictive modeling capabilities

## Deployment

### Streamlit Cloud Deployment

The application is deployed on Streamlit Cloud, making it accessible to users without any installation requirements.

#### Deployment Features:

- **Cloud Hosting**: App runs on Streamlit's secure cloud infrastructure
- **Automatic Updates**: Changes pushed to the main branch are automatically deployed
- **Environment Management**: Secrets and environment variables managed through Streamlit Cloud
- **Resource Scaling**: Automatic resource management based on usage
- **SSL Security**: Secure HTTPS connection for all users

#### Accessing the App:

- Production URL: [Ai-Data-analysis-Assistant](https://ai-data-analysis-assistant-5hpawoeffw2hlq6x6prqcc.streamlit.app/)
- No authentication required
- Works on all modern web browsers
- Responsive design for desktop and mobile devices

#### Cloud Configuration:

1. **Environment Variables**:

   - Managed through Streamlit Cloud's secrets management
   - API keys and sensitive data stored securely

2. **Resource Limits**:

   - Memory: Based on Streamlit Cloud's community tier limits
   - File Upload: Maximum 100MB (configured in app)
   - Session Duration: Managed by Streamlit Cloud

3. **Performance Optimizations**:
   - Caching enabled for data loading
   - Efficient memory management for file operations
   - Streamlined download functionality

### Local Deployment

For users who prefer to run the application locally:

- Follow installation instructions in README.md
- Configure environment variables locally
- Access through localhost:8501
