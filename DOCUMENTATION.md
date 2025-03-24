# Data Analysis Web App - Technical Documentation

This document provides technical information about the Data Analysis Web App architecture, implementation, and code details.

## Table of Contents

- [Data Analysis Web App - Technical Documentation](#data-analysis-web-app---technical-documentation)
  - [Table of Contents](#table-of-contents)
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
  - [Deployment Options](#deployment-options)
    - [Streamlit Cloud Deployment](#streamlit-cloud-deployment)
    - [Local Deployment](#local-deployment)

## Architecture Overview

The app uses Streamlit for a single-page architecture with tabbed navigation, integrating Google's Gemini AI (Flash 2.0) for natural language data analysis.

**Design Principles:**

- User-friendly interface with clear instructions
- Efficient data handling with caching
- Support for various data formats and transformations
- Secure API key management

## Core Components

1. **Data Loading**: File uploads and parsing
2. **Data Analysis**: Gemini AI integration for natural language queries
3. **Data Transformation**: Multiple data manipulation operations
4. **Data Export**: CSV/Excel download functionality
5. **Session Management**: State persistence across interactions

## Data Flow

1. User uploads CSV/Excel file → Parsed into pandas DataFrame and cached
2. User interacts through UI → Transformations applied to in-memory DataFrame
3. Transformation history tracked → Transformed data downloadable

## Implementation Details

### Main Application Structure

```python
# Main app with tabs
tab1, tab2, tab3 = st.tabs(["Data Analysis", "Data Transformation", "Download Data"])

with tab1:
    # Data preview and AI analysis

with tab2:
    # Data transformation options

with tab3:
    # Export functionality
```

### Configuration

Central configuration dictionary for easy parameter adjustment:

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

### Data Loading and Caching

Performance optimization through Streamlit's caching mechanism:

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

## AI Integration

The app integrates with Google's Generative AI (Gemini) for natural language data analysis:

```python
def get_api_key():
    api_key = os.getenv("GOOGLE_API_KEY") or (
        st.secrets["GOOGLE_API_KEY"] if hasattr(st, "secrets") and "GOOGLE_API_KEY" in st.secrets else None
    )
    if api_key:
        genai.configure(api_key=api_key)
    return api_key
```

The AI prompt includes DataFrame information:

- Shape and columns
- Data types and statistical summary
- Sample rows and missing values
- Categorical details and numeric correlations

## Session State Management

Streamlit's session state maintains data across interactions:

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

## Data Transformation Operations

### 1. Filter Data

- Filter categorical columns by value selection
- Filter numeric columns by range

### 2. Add/Remove Columns

- Remove selected columns
- Create calculated or combined columns

### 3. Handle Missing Values

- Drop rows with missing values
- Fill missing values (mean, median, mode, custom)

### 4. Transform Columns

- Normalize/standardize numeric columns
- Apply mathematical transformations
- Text case conversion
- One-hot encoding

### 5. Change Data Types

- Type conversion
- Datetime parsing

### 6. Sort Data

- Sort by any column with direction control

## File Handling

BytesIO buffer-based download implementation:

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

## Deployment Options

### Streamlit Cloud Deployment

- Zero-configuration hosting
- Automatic scaling
- Secure secrets management
- Always-on availability

### Local Deployment

- Standard Streamlit server
- Environment variable configuration
- Optional virtual environment isolation
