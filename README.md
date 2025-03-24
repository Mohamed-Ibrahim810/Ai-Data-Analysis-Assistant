Data Analysis Web App

![Data Analysis Assistant](https://img.shields.io/badge/Data-Analysis-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![Google Gemini AI](https://img.shields.io/badge/Google_Gemini_AI-4285F4?style=flat&logo=google&logoColor=white)

A powerful web application that helps users analyze and transform datasets with Google's Gemini AI (Flash 2.0). Upload CSV or Excel files, explore data, ask questions in natural language, transform data with various operations, and download the processed results.

🌐 **Try it now**: [Access the app on Streamlit Cloud](https://ai-data-analysis-assistant-5hpawoeffw2hlq6x6prqcc.streamlit.app/)

## Table of Contents

- [Table of Contents](#table-of-contents)
- [✨ Features](#-features)
  - [Data Analysis](#data-analysis)
  - [Data Transformation](#data-transformation)
  - [Data Management](#data-management)
- [🚀 Installation](#-installation)
  - [Cloud Version](#cloud-version)
  - [Local Setup](#local-setup)
- [📝 Usage](#-usage)
- [⚙️ Configuration](#️-configuration)
- [📁 Project Structure](#-project-structure)
- [🔧 Technologies Used](#-technologies-used)
- [🔑 API Key Setup](#-api-key-setup)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## ✨ Features

### Data Analysis

- AI-powered natural language analysis
- Data preview with shape, types, and sample rows
- Suggested example questions

### Data Transformation

- Filter data by values or ranges
- Add/remove columns
- Handle missing values
- Transform columns
- Convert data types
- Sort data

### Data Management

- Track transformation history
- Reset to original dataset
- Export as CSV or Excel

## 🚀 Installation

### Cloud Version

- Visit [Ai-Data-Analysis-Assistant](https://ai-data-analysis-assistant-5hpawoeffw2hlq6x6prqcc.streamlit.app/)
- No installation required

### Local Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Mohamed-Ibrahim810/Ai-Data-Analysis-Assistant.git
   cd data-analysis-web-app
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   # Windows: venv\Scripts\activate
   # macOS/Linux: source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your Google API key (see [API Key Setup](#-api-key-setup))

5. Run the application:
   ```bash
   streamlit run app.py
   ```

## 📝 Usage

1. **Upload dataset**: Select a CSV or Excel file
2. **Analyze data**:
   - View data preview
   - Ask questions about your data
3. **Transform data**:
   - Apply various transformations
   - Track transformation history
4. **Download results**: Save as CSV or Excel

## ⚙️ Configuration

The app uses a configuration dictionary in `app.py`:

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

## 📁 Project Structure

```
data-analysis-web-app/
├── app.py                      # Main application file
├── requirements.txt            # Python dependencies
├── .env.example                # Example environment variables
├── README.md                   # Project overview
├── DOCUMENTATION.md            # Technical documentation
├── USER_GUIDE.md               # User guide with examples
├── images/                     # Web app images
└── sample_data/                # Sample datasets
    ├── README.md               # Sample dataset info
    └── sales_sample.csv        # Sample sales dataset
```

## 🔧 Technologies Used

- Streamlit: Web application framework
- Pandas: Data manipulation and analysis
- Google Generative AI: AI-powered analysis (Gemini model)
- XlsxWriter: Excel file creation
- python-dotenv: Environment variable management

## 🔑 API Key Setup

This application requires a Google API key for Gemini AI:

1. **Environment Variable**:

   ```bash
   export GOOGLE_API_KEY=your_api_key_here
   ```

2. **.env File**:
   Create a `.env` file with:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

To obtain a key:

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Use it in one of the methods above

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

---

Created by [Mohamed Ibrahim Mohamed] - [GitHub Profile](https://github.com/Mohamed-Ibrahim810)
