Data Analysis Web App

![Data Analysis Assistant](https://img.shields.io/badge/Data-Analysis-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![Google Gemini AI](https://img.shields.io/badge/Google_Gemini_AI-4285F4?style=flat&logo=google&logoColor=white)

A powerful web application that helps users analyze and transform their datasets with the assistance of Google's Gemini AI. This tool allows users to upload CSV or Excel files, explore data, ask questions in natural language, transform data with various operations, and download the processed results.

🌐 **Try it now**: [Access the app on Streamlit Cloud](https://ai-data-analysis-assistant-5hpawoeffw2hlq6x6prqcc.streamlit.app/)

📋 Table of Contents

- [✨ Features](#-features)
  - [Data Analysis](#data-analysis)
  - [Data Transformation](#data-transformation)
  - [Data Management](#data-management)
- [🎬 Demo](#-demo)
- [🚀 Installation](#-installation)
  - [Option 1: Use the Cloud Version](#option-1-use-the-cloud-version)
  - [Option 2: Run Locally](#option-2-run-locally)
    - [Prerequisites](#prerequisites)
    - [Steps](#steps)
- [📝 Usage](#-usage)
  - [Cloud Version](#cloud-version)
  - [Local Version](#local-version)
- [⚙️ Configuration](#️-configuration)
  - [Configuration Parameters:](#configuration-parameters)
- [📁 Project Structure](#-project-structure)
- [🔧 Technologies Used](#-technologies-used)
- [🔑 API Key Setup](#-api-key-setup)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## ✨ Features

### Data Analysis

- **AI-Powered Analysis**: Ask questions about your data in natural language and get intelligent responses
- **Data Preview**: Quick overview of dataset shape, column types, and sample rows
- **Example Questions**: Suggested questions to help users get started

### Data Transformation

- **Filter Data**: Filter rows based on column values or ranges
- **Add/Remove Columns**: Remove unwanted columns or create new calculated columns
- **Handle Missing Values**: Drop rows with missing values or fill them using various strategies
- **Transform Columns**: Apply mathematical transformations to numeric columns or text operations to categorical columns
- **Change Data Types**: Convert columns to different data types
- **Sort Data**: Order your dataset by any column

### Data Management

- **Transformation History**: Track all changes made to your dataset
- **Reset Option**: Revert to the original dataset at any time
- **Download Options**: Export your transformed data as CSV or Excel files

## 🎬 Demo

[Add screenshots or GIFs of your application here]

## 🚀 Installation

### Option 1: Use the Cloud Version

The easiest way to use the app is through Streamlit Cloud:

1. Visit [your-app-url-here](https://ai-data-analysis-assistant-5hpawoeffw2hlq6x6prqcc.streamlit.app/)
2. No installation required - just upload your data and start analyzing!
3. The app runs in your browser and works on any device

### Option 2: Run Locally

If you prefer to run the app locally:

#### Prerequisites

- Python 3.7+
- pip (Python package installer)

#### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/data-analysis-web-app.git
   cd data-analysis-web-app
   ```

2. Create a virtual environment

   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your Google API key (see [API Key Setup](#api-key-setup))

5. Run the application:
   ```bash
   streamlit run app.py
   ```

## 📝 Usage

### Cloud Version

1. Navigate to [your-app-url-here](https://ai-data-analysis-assistant-5hpawoeffw2hlq6x6prqcc.streamlit.app/) in your web browser
2. Upload your dataset and start analyzing!

### Local Version

1. **Start the application**:

   ```bash
   streamlit run app.py
   ```

2. **Upload your dataset**:

   - Click on the file uploader
   - Select a CSV or Excel file (up to 100MB)

3. **Analyze your data**:

   - Navigate to the "Data Analysis" tab
   - View the data preview
   - Type a question about your data in the text input
   - Review the AI-generated analysis

4. **Transform your data**:

   - Navigate to the "Data Transformation" tab
   - Select a transformation type
   - Configure the transformation parameters
   - Apply the transformation
   - Track your transformation history

5. **Download your data**:
   - Navigate to the "Download Data" tab
   - Select your preferred file format (CSV or Excel)
   - Enter a filename
   - Click the download button

## ⚙️ Configuration

The application uses a configuration dictionary that can be modified in the `app.py` file:

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

### Configuration Parameters:

- **MAX_FILE_SIZE**:

  - Maximum allowed file size for uploads (100MB)
  - Adjust based on your server's memory capacity
  - Format: bytes (100 _ 1024 _ 1024 = 100MB)

- **PREVIEW_ROWS**:

  - Number of rows shown in data previews (5)
  - Affects performance when displaying large datasets
  - Increase for more comprehensive previews

- **ALLOWED_EXTENSIONS**:

  - List of accepted file formats (['.csv', '.xlsx'])
  - Restricts file uploads to these formats
  - Add more formats if needed (requires implementation)

- **TYPE_MAPPING**:
  - Maps user-friendly names to pandas data types
  - Used in data type conversion operations
  - Customize based on your data needs

## 📁 Project Structure

```
data-analysis-web-app/
├── app.py                      # Main application file
├── requirements.txt            # Python dependencies
├── .env.example                # Example environment variables file
├── .gitignore                  # Git ignore file
├── LICENSE                     # MIT license
├── README.md                   # Project overview (this file)
├── DOCUMENTATION.md            # Technical documentation
├── USER_GUIDE.md               # User guide with examples
└── sample_data/                # Sample datasets for testing
    ├── README.md               # Information about sample datasets
    └── sales_sample.csv        # Sample sales dataset
```

## 🔧 Technologies Used

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Google Generative AI**: AI-powered data analysis (Gemini model)
- **XlsxWriter**: Excel file creation
- **python-dotenv**: Environment variable management

## 🔑 API Key Setup

This application requires a Google API key to access Gemini AI.
You can set up your API key using one of these methods:

1. **Environment Variable**:

   ```bash
   export GOOGLE_API_KEY=your_api_key_here
   ```

2. **.env File**:
   Create a `.env` file in the root directory with:

   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

To obtain a Google API key:

1. Go to the [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key and use it in one of the methods above

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Created by [Mohamed Ibrahim Mohamed Aljaria] - [Your GitHub Profile](https://github.com/yourusername)
