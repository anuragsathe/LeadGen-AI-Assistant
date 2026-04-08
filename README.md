# LeadGen AI Assistant

An intelligent AI-powered lead generation system that discovers and analyzes potential business leads using Google Gemini, LangChain, web search, and a Django REST API backend.

## 🎯 Overview

LeadGen AI Assistant offers two main entry points:
- A local command-line lead generation script (`main.py`) that produces structured lead output.
- A Django REST API service (`leadgen_api/`) that exposes a POST endpoint for lead generation.

The system combines web search, scraping, and AI prompt engineering to identify small businesses that may need IT services and return business profiles with outreach guidance.

## ✨ Features

- **AI-Powered Lead Research**: Uses Gemini 2.5 Flash through `langchain_google_genai`
- **Automated Data Gathering**: Combines search results and scraping to collect business information
- **REST API**: Provides a Django REST endpoint for remote lead generation requests
- **Structured Lead Output**: Returns validated JSON lead records
- **Flexible Usage**: Supports both standalone script execution and API-driven workflows

## 🛠️ Tech Stack

- **Python 3.8+**
- **Django 4.2**
- **Django REST Framework**
- **LangChain**
- **Google Generative AI** (Gemini 2.5 Flash)
- **DuckDuckGo Search**
- **BeautifulSoup4**
- **Pydantic**
- **python-dotenv**

## 📋 Prerequisites

- Python 3.8 or higher
- Google API key for Gemini access
- Internet connection

## 🚀 Installation

1. **Clone the repository**:
```bash
git clone https://github.com/anuragsathe/LeadGen-AI-Assistant.git
cd LeadGen-AI-Assistant
```

2. **Create and activate a virtual environment**:
```bash
python -m venv venv
venv\Scripts\activate    # Windows
# or
source venv/bin/activate  # macOS/Linux
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**:
Create a `.env` file in the repository root with:
```env
GOOGLE_API_KEY=your_google_api_key_here
```

### PostgreSQL setup
If you want to use PostgreSQL instead of the default SQLite database, add these values to `.env`:
```env
POSTGRES_DB=leadgen_db
POSTGRES_USER=leadgen_user
POSTGRES_PASSWORD=your_password_here
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
```

Then create the database and user in PostgreSQL and run migrations:
```bash
cd leadgen_api
python manage.py migrate
```

If no PostgreSQL environment variables are provided, the app will continue using SQLite automatically.

## 💻 Usage

### 1) Run the CLI lead generator

```bash
python main.py
```

This will:
- initialize the Gemini AI model
- search for relevant small businesses
- generate structured lead profiles
- save results to `leads_output.txt`

### 2) Run the Django REST API

Change to the Django project directory and run the server:

```bash
cd leadgen_api
python manage.py migrate
python manage.py runserver
```

Then submit a POST request to:

```http
POST http://127.0.0.1:8000/api/generate-leads/
```

Request body:
```json
{
  "industry": "marketing agency",
  "location": "Vancouver"
}
```

Example using `curl`:

```bash
curl -X POST http://127.0.0.1:8000/api/generate-leads/ \
  -H "Content-Type: application/json" \
  -d '{"industry":"marketing agency","location":"Vancouver"}'
```

Response format:
```json
{
  "leads": [
    "<lead data or error message>",
    "..."
  ]
}
```

## 📁 Project Structure

```
LeadGen-AI-Assistant/
├── main.py                     # Standalone lead generation script
├── tools.py                    # Utility functions and tools
├── requirements.txt            # Python dependencies
├── leads_output.txt            # Output from CLI lead generation
├── .env                        # Environment variables (not committed)
├── .gitignore                  # Git ignore rules
├── README.md                   # Project documentation
└── leadgen_api/                # Django REST API project
    ├── db.sqlite3              # Local SQLite database
    ├── manage.py               # Django management commands
    ├── leadgen_api/            # Django project settings and URLs
    │   ├── settings.py
    │   ├── urls.py
    │   ├── asgi.py
    │   └── wsgi.py
    └── leads/                  # Django app implementing the API
        ├── views.py
        ├── urls.py
        ├── models.py
        └── apps.py
```

## 🔧 Django API Details

The REST endpoint is implemented in `leadgen_api/leads/views.py` and available at:
- `POST /api/generate-leads/`

Required JSON fields:
- `industry`
- `location`

If required fields are missing, the endpoint returns a `400` response.

## 📊 Example JSON Output

```json
{
  "leads": [
    "{\"company\": \"Tech Solutions Inc\", \"contact_info\": \"+1 (604) 555-0123\", \"email\": \"info@techsolutions.com\", \"summary\": \"Growing marketing agency with legacy systems needing modernization\", \"outreach_message\": \"Your marketing team deserves modern IT infrastructure...\", \"tools_used\": [\"Cloud Migration\", \"Network Optimization\"]}"
  ]
}
```

## 🔐 Security

- Store `GOOGLE_API_KEY` in `.env` and do not commit it to source control
- This project is currently configured for development only
- For production, secure Django `SECRET_KEY` and set `DEBUG = False`

## 🚀 Future Enhancements

- [ ] Add authentication for the REST API
- [ ] Add lead scoring and ranking
- [ ] Add CRM integration
- [ ] Add batch lead generation and scheduling
- [ ] Add a web UI dashboard

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

**Anurag Sathe**
- GitHub: [@anuragsathe](https://github.com/anuragsathe)
- Email: anurag.sathe@example.com

## 🤝 Contributing

Contributions are welcome! Feel free to fork this repository and submit pull requests.

## 📧 Support

For issues, questions, or suggestions, please open an issue on the [GitHub repository](https://github.com/anuragsathe/LeadGen-AI-Assistant/issues).

---

**Note**: This tool is designed for legitimate business research and lead generation. Ensure compliance with all applicable laws and regulations when using this tool.
