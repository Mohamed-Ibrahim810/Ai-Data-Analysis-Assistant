import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
import numpy as np
import io
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Configuration
CONFIG = {
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

# Set page configuration
st.set_page_config(page_title="Data Analysis Assistant", layout="wide")

# Initialize session state variables
for key, default_value in {
    'transformed_df': None,
    'original_df': None,
    'transformation_history': [],
    'current_file': None
}.items():
    if key not in st.session_state:
        st.session_state[key] = default_value

# Utility functions for data handling
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

# Function to handle CSV downloads
def get_csv_download_link(df, filename):
    return create_download_button(df, filename, "text/csv")

# Function to handle Excel downloads
def get_excel_download_link(df, filename, transformation_history=None):
    return create_download_button(
        df, filename, 
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        transformation_history
    )

# Cache data loading to improve performance
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

st.title("Data Analysis Assistant")

# Secure API key handling - get from environment variables or Streamlit secrets
def get_api_key():
    api_key = os.getenv("GOOGLE_API_KEY") or (
        st.secrets["GOOGLE_API_KEY"] if hasattr(st, "secrets") and "GOOGLE_API_KEY" in st.secrets else None
    )
    if api_key:
        genai.configure(api_key=api_key)
    return api_key

# Get API key securely
api_key = get_api_key()

# Configure Gemini AI with the API key
if api_key:
    # File uploader for dataset
    uploaded_file = st.file_uploader("Upload your dataset", type=["csv", "xlsx"])

    if uploaded_file is not None:
        # Check if a new file is being uploaded by comparing with the current filename
        if 'current_file' not in st.session_state or st.session_state.current_file != uploaded_file.name:
            # Reset session state for a new file
            st.session_state.original_df = None
            st.session_state.transformed_df = None
            st.session_state.transformation_history = []
            st.session_state.current_file = uploaded_file.name
            
        # Load the data with caching
        if st.session_state.original_df is None:
            df = load_data(uploaded_file)
            if df is not None and not df.empty:
                st.session_state.original_df = df.copy()
                st.session_state.transformed_df = df.copy()
            else:
                st.error("Failed to load the dataset. Please try again with a different file.")
                st.stop()
        
        # Use the transformed dataframe if it exists
        if st.session_state.transformed_df is not None:
            df = st.session_state.transformed_df
        
        # Create tabs for different functionalities
        tab1, tab2, tab3 = st.tabs(["Data Analysis", "Data Transformation", "Download Data"])
        
        with tab1:
            # Simplified preview of the data
            with st.expander("Preview of the dataset"):
                # Show basic dataset info
                st.write(f"Dataset shape: {df.shape[0]} rows × {df.shape[1]} columns")
                
                # Show first 5 rows
                st.write("Sample data (first 5 rows):")
                st.dataframe(df.head(), use_container_width=True)
                
                # Show column types in a more compact format
                st.write("Column types:")
                for col, dtype in zip(df.columns, df.dtypes):
                    st.write(f"• {col}: {dtype}")
            
            st.write("Ask a question about your dataset:")
            
            # Add example questions
            with st.expander("Example questions you can ask"):
                st.write("- What is the average of column X?")
                st.write("- What is the correlation between column X and Y?")
                st.write("- Show me a summary of the data grouped by column Z")
                st.write("- Are there any outliers in column X?")
                st.write("- What factors most strongly predict column X?")
            
            question = st.text_input("Enter your question")

            if question:
                try:
                    # Create DataFrame info more efficiently
                    df_info = {
                        'shape': df.shape,
                        'columns': df.columns.tolist(),
                        'dtypes': df.dtypes.to_dict(),
                        'describe': df.describe().to_string(),
                        'head': df.head().to_string(),
                        'missing': df.isnull().sum().to_dict()
                    }
                    
                    # Build the info string efficiently
                    info_parts = [
                        "DataFrame Information:",
                        f"- Shape: {df_info['shape']}",
                        f"- Columns: {df_info['columns']}",
                        f"- Data types: {df_info['dtypes']}",
                        "\nStatistical Summary:",
                        df_info['describe'],
                        "\nFirst 5 rows:",
                        df_info['head'],
                        "\nMissing Values:",
                        str(df_info['missing'])
                    ]
                    
                    # Add categorical info if exists
                    cat_cols = df.select_dtypes(include=['object', 'category']).columns
                    if not cat_cols.empty:
                        cat_info = {col: df[col].nunique() for col in cat_cols}
                        info_parts.extend([
                            "\nUnique Values (for categorical columns):",
                            ", ".join(f"{col}: {count} unique values" for col, count in cat_info.items())
                        ])
                    
                    # Add correlations if numeric columns exist
                    num_cols = df.select_dtypes(include=[np.number])
                    if not num_cols.empty:
                        info_parts.extend([
                            "\nCorrelations (for numeric columns):",
                            num_cols.corr().round(2).to_string()
                        ])
                    else:
                        info_parts.append("\nCorrelations: No numeric columns for correlation")
                    
                    # Join all parts efficiently
                    df_info = "\n".join(info_parts)
                    
                    # Create the prompt
                    prompt = f"""
                    You are a professional data analysis assistant analyzing a pandas DataFrame.
                    
                    {df_info}
                    
                    User question: {question}
                    
                    # Create the Gemini client and get response
                    client = genai.GenerativeModel("gemini-2.0-flash")
                    generation_config = {
                        "temperature": 0.2,
                        "top_p": 0.85,
                        "max_output_tokens": 1024
                    }
                    
                    with st.spinner("Analyzing your data..."):
                        response = client.generate_content(
                            prompt,
                            generation_config=generation_config
                        )
                        st.markdown("### Analysis Result")
                        st.markdown(response.text)
                        
                except Exception as e:
                    st.error(f"Unable to analyze the data: {str(e)}")
        
        with tab2:
            st.header("Transform Your Data")
            
            # Display transformation history
            if st.session_state.transformation_history:
                with st.expander("Transformation History"):
                    for i, transformation in enumerate(st.session_state.transformation_history):
                        st.write(f"{i+1}. {transformation}")
            
            # Option to reset to original data
            if st.button("Reset to Original Data"):
                st.session_state.transformed_df = st.session_state.original_df.copy()
                st.session_state.transformation_history = []
                st.success("Data reset to original state!")
                st.rerun()
            
            # Transformation options
            transform_option = st.selectbox(
                "Select transformation type:",
                ["Select an option", "Filter Data", "Add/Remove Columns", "Handle Missing Values", "Transform Column", "Change Data Type", "Sort Data"]
            )
            
            if transform_option == "Filter Data":
                col = st.selectbox("Select column to filter on:", df.columns)
                
                if col in df.select_dtypes(include=['object', 'category']).columns:
                    # For categorical columns, show unique values
                    unique_values = df[col].unique()
                    selected_values = st.multiselect("Select values to keep:", unique_values)
                    
                    if st.button("Apply Filter"):
                        if selected_values:
                            st.session_state.transformed_df = df[df[col].isin(selected_values)]
                            st.session_state.transformation_history.append(f"Filtered {col} to keep only {', '.join(map(str, selected_values))}")
                            st.success(f"Data filtered! Kept {len(st.session_state.transformed_df)} rows.")
                            st.rerun()
                else:
                    # For numeric columns, show range filter
                    min_val, max_val = float(df[col].min()), float(df[col].max())
                    filter_range = st.slider(f"Filter range for {col}:", min_val, max_val, (min_val, max_val))
                    
                    if st.button("Apply Filter"):
                        st.session_state.transformed_df = df[(df[col] >= filter_range[0]) & (df[col] <= filter_range[1])]
                        st.session_state.transformation_history.append(f"Filtered {col} to range {filter_range[0]} - {filter_range[1]}")
                        st.success(f"Data filtered! Kept {len(st.session_state.transformed_df)} rows.")
                        st.rerun()
            
            elif transform_option == "Add/Remove Columns":
                operation = st.radio("Select operation:", ["Remove Columns", "Create New Column"])
                
                if operation == "Remove Columns":
                    cols_to_remove = st.multiselect("Select columns to remove:", df.columns)
                    if st.button("Remove Selected Columns"):
                        if cols_to_remove:
                            st.session_state.transformed_df = df.drop(columns=cols_to_remove)
                            st.session_state.transformation_history.append(f"Removed columns: {', '.join(cols_to_remove)}")
                            st.success(f"Removed {len(cols_to_remove)} columns!")
                            st.rerun()
                
                else:  # Create New Column
                    new_col_name = st.text_input("New column name:")
                    calculation_type = st.selectbox(
                        "Calculation type:",
                        ["Simple Calculation", "Combine Columns"]
                    )
                    
                    if calculation_type == "Simple Calculation":
                        numeric_cols = df.select_dtypes(include=np.number).columns
                        if len(numeric_cols) > 0:
                            col_to_transform = st.selectbox("Select column to transform:", numeric_cols)
                            operation = st.selectbox("Select operation:", ["Add", "Subtract", "Multiply", "Divide"])
                            value = st.number_input("Enter value:")
                            
                            if st.button("Create Column"):
                                if new_col_name and col_to_transform:
                                    if operation == "Add":
                                        st.session_state.transformed_df[new_col_name] = df[col_to_transform] + value
                                    elif operation == "Subtract":
                                        st.session_state.transformed_df[new_col_name] = df[col_to_transform] - value
                                    elif operation == "Multiply":
                                        st.session_state.transformed_df[new_col_name] = df[col_to_transform] * value
                                    elif operation == "Divide" and value != 0:
                                        st.session_state.transformed_df[new_col_name] = df[col_to_transform] / value
                                    
                                    st.session_state.transformation_history.append(f"Created new column '{new_col_name}' = {col_to_transform} {operation} {value}")
                                    st.success(f"Created new column: {new_col_name}")
                                    st.rerun()
                        else:
                            st.warning("No numeric columns available for calculation.")
                    
                    else:  # Combine Columns
                        cols_to_combine = st.multiselect("Select columns to combine:", df.columns)
                        separator = st.text_input("Separator (for text columns):", " ")
                        
                        if st.button("Create Column"):
                            if new_col_name and cols_to_combine:
                                # Check if all selected columns are numeric
                                all_numeric = all(col in df.select_dtypes(include=np.number).columns for col in cols_to_combine)
                                
                                if all_numeric:
                                    # Sum numeric columns
                                    st.session_state.transformed_df[new_col_name] = df[cols_to_combine].sum(axis=1)
                                    operation_desc = "sum"
                                else:
                                    # Concatenate string columns
                                    st.session_state.transformed_df[new_col_name] = df[cols_to_combine].astype(str).agg(separator.join, axis=1)
                                    operation_desc = "concatenation with separator"
                                
                                st.session_state.transformation_history.append(f"Created new column '{new_col_name}' from {operation_desc} of {', '.join(cols_to_combine)}")
                                st.success(f"Created new column: {new_col_name}")
                                st.rerun()
            
            elif transform_option == "Handle Missing Values":
                strategy = st.selectbox(
                    "Select strategy:",
                    ["Drop rows with missing values", "Fill missing values"]
                )
                
                if strategy == "Drop rows with missing values":
                    cols_with_missing = df.columns[df.isnull().any()].tolist()
                    if not cols_with_missing:
                        st.info("No missing values found in the dataset.")
                    else:
                        selected_cols = st.multiselect("Select columns to check for missing values (leave empty for all):", cols_with_missing)
                        
                        if st.button("Drop Rows"):
                            if selected_cols:
                                st.session_state.transformed_df = df.dropna(subset=selected_cols)
                                st.session_state.transformation_history.append(f"Dropped rows with missing values in columns: {', '.join(selected_cols)}")
                            else:
                                st.session_state.transformed_df = df.dropna()
                                st.session_state.transformation_history.append("Dropped all rows with any missing values")
                            
                            st.success(f"Dropped rows with missing values. New shape: {st.session_state.transformed_df.shape}")
                            st.rerun()
                
                else:  # Fill missing values
                    cols_with_missing = df.columns[df.isnull().any()].tolist()
                    if not cols_with_missing:
                        st.info("No missing values found in the dataset.")
                    else:
                        col_to_fill = st.selectbox("Select column with missing values:", cols_with_missing)
                        
                        if col_to_fill:
                            if col_to_fill in df.select_dtypes(include=np.number).columns:
                                fill_method = st.selectbox(
                                    "Fill method for numeric column:",
                                    ["Mean", "Median", "Custom value"]
                                )
                                
                                if fill_method == "Custom value":
                                    fill_value = st.number_input("Enter value to fill with:")
                                
                                if st.button("Fill Missing Values"):
                                    if fill_method == "Mean":
                                        fill_value = df[col_to_fill].mean()
                                        st.session_state.transformed_df[col_to_fill] = df[col_to_fill].fillna(fill_value)
                                        st.session_state.transformation_history.append(f"Filled missing values in {col_to_fill} with mean ({fill_value:.2f})")
                                    elif fill_method == "Median":
                                        fill_value = df[col_to_fill].median()
                                        st.session_state.transformed_df[col_to_fill] = df[col_to_fill].fillna(fill_value)
                                        st.session_state.transformation_history.append(f"Filled missing values in {col_to_fill} with median ({fill_value:.2f})")
                                    else:
                                        st.session_state.transformed_df[col_to_fill] = df[col_to_fill].fillna(fill_value)
                                        st.session_state.transformation_history.append(f"Filled missing values in {col_to_fill} with custom value ({fill_value})")
                                    
                                    st.success(f"Filled missing values in column: {col_to_fill}")
                                    st.rerun()
                            else:
                                # For non-numeric columns
                                fill_method = st.selectbox(
                                    "Fill method for non-numeric column:",
                                    ["Most frequent value", "Custom value"]
                                )
                                
                                if fill_method == "Custom value":
                                    fill_value = st.text_input("Enter value to fill with:")
                                
                                if st.button("Fill Missing Values"):
                                    if fill_method == "Most frequent value":
                                        fill_value = df[col_to_fill].mode()[0]
                                        st.session_state.transformed_df[col_to_fill] = df[col_to_fill].fillna(fill_value)
                                        st.session_state.transformation_history.append(f"Filled missing values in {col_to_fill} with most frequent value ({fill_value})")
                                    else:
                                        st.session_state.transformed_df[col_to_fill] = df[col_to_fill].fillna(fill_value)
                                        st.session_state.transformation_history.append(f"Filled missing values in {col_to_fill} with custom value ({fill_value})")
                                    
                                    st.success(f"Filled missing values in column: {col_to_fill}")
                                    st.rerun()
            
            elif transform_option == "Transform Column":
                col_to_transform = st.selectbox("Select column to transform:", df.columns)
                
                if col_to_transform in df.select_dtypes(include=np.number).columns:
                    # For numeric columns
                    transform_type = st.selectbox(
                        "Select transformation:",
                        ["Normalize (0-1)", "Standardize (z-score)", "Log transform", "Square root"]
                    )
                    
                    if st.button("Apply Transformation"):
                        if transform_type == "Normalize (0-1)":
                            min_val = df[col_to_transform].min()
                            max_val = df[col_to_transform].max()
                            if max_val > min_val:  # Avoid division by zero
                                st.session_state.transformed_df[col_to_transform] = (df[col_to_transform] - min_val) / (max_val - min_val)
                                st.session_state.transformation_history.append(f"Normalized {col_to_transform} to range 0-1")
                        
                        elif transform_type == "Standardize (z-score)":
                            mean = df[col_to_transform].mean()
                            std = df[col_to_transform].std()
                            if std > 0:  # Avoid division by zero
                                st.session_state.transformed_df[col_to_transform] = (df[col_to_transform] - mean) / std
                                st.session_state.transformation_history.append(f"Standardized {col_to_transform} (z-score)")
                        
                        elif transform_type == "Log transform":
                            # Handle negative or zero values
                            min_val = df[col_to_transform].min()
                            if min_val <= 0:
                                offset = abs(min_val) + 1
                                st.session_state.transformed_df[col_to_transform] = np.log(df[col_to_transform] + offset)
                                st.session_state.transformation_history.append(f"Applied log transform to {col_to_transform} with offset {offset}")
                            else:
                                st.session_state.transformed_df[col_to_transform] = np.log(df[col_to_transform])
                                st.session_state.transformation_history.append(f"Applied log transform to {col_to_transform}")
                        
                        elif transform_type == "Square root":
                            # Handle negative values
                            min_val = df[col_to_transform].min()
                            if min_val < 0:
                                offset = abs(min_val)
                                st.session_state.transformed_df[col_to_transform] = np.sqrt(df[col_to_transform] + offset)
                                st.session_state.transformation_history.append(f"Applied square root transform to {col_to_transform} with offset {offset}")
                            else:
                                st.session_state.transformed_df[col_to_transform] = np.sqrt(df[col_to_transform])
                                st.session_state.transformation_history.append(f"Applied square root transform to {col_to_transform}")
                        
                        st.success(f"Transformed column: {col_to_transform}")
                        st.rerun()
                
                else:
                    # For categorical/text columns
                    transform_type = st.selectbox(
                        "Select transformation:",
                        ["Convert to uppercase", "Convert to lowercase", "One-hot encode"]
                    )
                    
                    if st.button("Apply Transformation"):
                        if transform_type == "Convert to uppercase":
                            st.session_state.transformed_df[col_to_transform] = df[col_to_transform].astype(str).str.upper()
                            st.session_state.transformation_history.append(f"Converted {col_to_transform} to uppercase")
                        
                        elif transform_type == "Convert to lowercase":
                            st.session_state.transformed_df[col_to_transform] = df[col_to_transform].astype(str).str.lower()
                            st.session_state.transformation_history.append(f"Converted {col_to_transform} to lowercase")
                        
                        elif transform_type == "One-hot encode":
                            # Get one-hot encoding
                            one_hot = pd.get_dummies(df[col_to_transform], prefix=col_to_transform)
                            # Drop the original column and join the one-hot encoded columns
                            st.session_state.transformed_df = pd.concat([df.drop(columns=[col_to_transform]), one_hot], axis=1)
                            st.session_state.transformation_history.append(f"One-hot encoded {col_to_transform}")
                        
                        st.success(f"Transformed column: {col_to_transform}")
                        st.rerun()
            
            elif transform_option == "Change Data Type":
                col_to_change = st.selectbox("Select column to change data type:", df.columns)
                
                # Show current data type and sample values
                current_type = df[col_to_change].dtype
                st.write(f"Current data type: {current_type}")
                st.write("Sample values:", df[col_to_change].head(CONFIG['PREVIEW_ROWS']).tolist())
                
                # Select new data type
                new_type = st.selectbox(
                    "Select new data type:",
                    list(CONFIG['TYPE_MAPPING'].keys()) + ["datetime"]
                )
                
                if st.button("Change Data Type"):
                    try:
                        if new_type == "datetime":
                            st.session_state.transformed_df[col_to_change] = pd.to_datetime(df[col_to_change])
                        else:
                            st.session_state.transformed_df[col_to_change] = df[col_to_change].astype(CONFIG['TYPE_MAPPING'][new_type])
                        
                        st.session_state.transformation_history.append(f"Changed data type of {col_to_change} from {current_type} to {new_type}")
                        st.success(f"Changed data type of {col_to_change} to {new_type}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error changing data type: {str(e)}")
                        st.info("Tip: Make sure the data in the column is compatible with the selected data type.")
            
            elif transform_option == "Sort Data":
                sort_col = st.selectbox("Select column to sort by:", df.columns)
                sort_order = st.radio("Sort order:", ["Ascending", "Descending"])
                
                if st.button("Sort Data"):
                    ascending = sort_order == "Ascending"
                    st.session_state.transformed_df = df.sort_values(by=sort_col, ascending=ascending)
                    st.session_state.transformation_history.append(f"Sorted data by {sort_col} in {sort_order.lower()} order")
                    st.success(f"Data sorted by: {sort_col}")
                    st.rerun()
        
        with tab3:
            st.header("Download Your Data")
            
            # Show smaller preview to reduce memory usage
            st.write("Preview of current data (first 3 rows):")
            st.dataframe(df.head(3))
            
            # Download options
            file_format = st.radio("Select file format:", ["CSV", "Excel"])
            filename = st.text_input("Enter filename (without extension):", "transformed_data")
            
            if filename:
                download_filename = f"{filename}.{'csv' if file_format == 'CSV' else 'xlsx'}"
                
                if file_format == "CSV":
                    get_csv_download_link(df, download_filename)
                else:  # Excel
                    get_excel_download_link(df, download_filename, st.session_state.transformation_history)
else:
    st.error("""
    API key not found. Please set up your Google API key using one of these methods:
    
    1. Create a `.env` file in the root directory with: `GOOGLE_API_KEY=your_api_key_here`
    2. Set an environment variable: `GOOGLE_API_KEY=your_api_key_here`
    3. Use Streamlit secrets management (recommended for deployment)
    
    For more information on Streamlit secrets, visit: https://docs.streamlit.io/library/advanced-features/secrets-management
    """)
    
    st.info("This application requires a Google API key to access Gemini AI for data analysis.")

# Add footer
st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info("This data analysis assistant helps you analyze and transform datasets with the assistance of Google's Gemini AI.")
