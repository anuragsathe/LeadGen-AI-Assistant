# LeadGen AI Assistant

An intelligent AI-powered lead generation system that identifies and analyzes potential business leads using advanced natural language processing and web search capabilities.

## 🎯 Overview

LeadGen AI Assistant leverages Google's Generative AI (Gemini) and LangChain to automatically discover small businesses that may need IT services. It performs targeted research to generate actionable sales leads with comprehensive contact information and personalized outreach messages.

## ✨ Features

- **AI-Powered Lead Discovery**: Uses Gemini 2.5 Flash for intelligent business identification
- **Automated Research**: Integrates web search and information gathering tools
- **Lead Analysis**: Generates comprehensive lead profiles including:
  - Company name and contact information
  - Email addresses and phone numbers
  - Service relevance summaries
  - Personalized outreach messages
- **Data Export**: Saves leads to formatted output files
- **Structured Output**: Uses Pydantic models for consistent, validated data

## 🛠️ Tech Stack

- **Python 3.x**
- **LangChain**: LLM orchestration and chains
- **Google Generative AI**: Gemini 2.5 Flash model
- **DuckDuckGo Search**: Web searching capabilities
- **BeautifulSoup4**: Web scraping
- **Pydantic**: Data validation

## 📋 Prerequisites

- Python 3.8 or higher
- Google API key (for Gemini access)
- Internet connection

## 🚀 Installation

1. **Clone the repository**:
```bash
git clone https://github.com/anuragsathe/LeadGen-AI-Assistant.git
cd LeadGen-AI-Assistant
```

2. **Create a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
Create a `.env` file in the root directory and add:
```
GOOGLE_API_KEY=your_google_api_key_here
```

Get your Google API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

## 💻 Usage

Run the lead generation script:
```bash
python main.py
```

The application will:
1. Initialize the Gemini AI model
2. Research and identify potential business leads
3. Generate structured lead profiles
4. Save results to `leads_output.txt`

### Output Format

Results are saved as structured JSON containing:
- **company**: Business name
- **contact_info**: Phone, address, or other contact details
- **email**: Email address if available
- **summary**: Why the business may need IT services
- **outreach_message**: Personalized message template
- **tools_used**: Relevant tools/services identified

## 📁 Project Structure

```
LeadGen-AI-Assistant/
├── main.py              # Main application entry point
├── tools.py             # Utility functions and tools
├── requirements.txt     # Python dependencies
├── leads_output.txt     # Generated leads output
├── .env                 # Environment variables (not committed)
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## 🔧 Configuration

Key settings in `main.py`:
- **Model**: Gemini 2.5 Flash
- **Temperature**: 0.3 (for consistent, focused responses)
- **Location**: Configurable (default: Vancouver, Canada)
- **Lead Count**: Set to 5 per query

## 📊 Example Output

```json
{
  "leads": [
    {
      "company": "Tech Solutions Inc",
      "contact_info": "+1 (604) 555-0123",
      "email": "info@techsolutions.com",
      "summary": "Growing marketing agency with legacy systems needing modernization",
      "outreach_message": "Your marketing team deserves modern IT infrastructure...",
      "tools_used": ["Cloud Migration", "Network Optimization"]
    }
  ]
}
```

## 🔐 Security

- API keys are stored in `.env` (never committed)
- Sensitive data is handled securely
- `.gitignore` excludes `venv/`, `__pycache__/`, and `.env`

## 🚀 Future Enhancements

- [ ] Multi-location lead generation
- [ ] CRM integration
- [ ] Email automation
- [ ] Lead scoring algorithms
- [ ] Database storage
- [ ] Web UI dashboard
- [ ] Scheduled lead generation jobs

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
