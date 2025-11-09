# Political News Sentiment Analysis

A comprehensive web application for analyzing sentiment in Indian political news using Streamlit and News API.

## Features

- 🔐 **User Authentication**: Secure login and signup system
- 📰 **News Fetching**: Fetch latest political news from multiple sources
- 🏛️ **Party Selection**: Analyze news for 23+ Indian political parties
- 🗺️ **State Filtering**: Filter news by Indian states and union territories
- ⚙️ **Advanced Options**: Customize article count and sorting preferences
- 📊 **Sentiment Analysis**: Analyze sentiment of news articles
- 📄 **PDF Export**: Generate professional PDF reports
- 🎨 **Clean UI**: Modern, decluttered interface with logo branding

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your News API key in `config.py`

## Usage

Run the application:
```bash
streamlit run app.py
```

## Configuration

Edit `config.py` to add your News API key:
```python
NEWS_API_KEY = "your_api_key_here"
```

Get your free API key from [newsapi.org](https://newsapi.org)

## Default Credentials

- Username: `admin`
- Password: `password`

Or create a new account using the Sign Up option.

## Technologies Used

- **Streamlit**: Web application framework
- **News API**: News data provider
- **ReportLab**: PDF generation
- **Python**: Core programming language

## Files Structure

- `app.py`: Main application file
- `config.py`: Configuration settings
- `users_db.py`: User authentication and database
- `pdf_generator.py`: PDF report generation
- `requirements.txt`: Python dependencies
- `assets/`: Logo and image assets

## License

This project is for educational and analytical purposes.
