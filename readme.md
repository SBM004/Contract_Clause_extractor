# ClauseExtractor

A Python application that extracts and indexes legal clauses from PDF contracts using Google's Gemini AI, OpenSearch, and MySQL.

## Features

- Extract clauses from PDF contracts automatically using Gemini AI
- Store extracted clauses in MySQL database 
- Index clauses using OpenSearch for semantic search
- REST API endpoints for uploading PDFs and searching clauses
- Supports filtering by contract type and contract ID

## Prerequisites

- Python 3.13+
- MySQL Server
- OpenSearch Server
- Google Cloud API key for Gemini AI

## Installation

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv .Clause
source .Clause/bin/activate  # Linux/Mac
.Clause\Scripts\activate     # Windows
```
```bash
3.Install dependencies:

pip install -r requirements.txt

```
4.Configure environment variables in .env:
```bash
GOOGLE_API_KEY="your-google-api-key"
```

5.Set up MySQL database:
```bash
# Update connection settings in connection.py
database="mydb"
user="myuser" 
password="pass"
host="localhost"
```
6.Set up OpenSearch:
```bash
# Update OpenSearch settings in opensearch.py
hosts=[{"host": "localhost", "port": 9200}]
http_auth=("admin", "<your strong password>")
```

7.Search for clauses:
```bash
POST /search
Content-Type: application/json
{
    "prompt": "Find confidentiality clauses in contract 123456"
}

or

{

    "prompt": "clauses “Confidential Information” shall mean and include all non-public information, written or oral, disclosed, directly or indirectly, through any means of communication or observation (including oral, graphic, written or electronic form) by the Disclosing Party or any of its affiliates or representatives  in contract_id 397755d5-f6c7-4769-bc91-8afbe061b454""
}

this will search the closest clauses based on embedding and vectorization
```

Project Structure
app.py - Flask application entry point
embedder.py - Text embedding using MiniLM model
extractor.py - PDF text extraction and clause parsing
database.py - MySQL database operations
opensearch.py - OpenSearch indexing and search
gemini.py - Google Gemini AI integration
router - API route handlers
PDFS - PDF storage directory
clause - Temporary JSON storage
API Endpoints
GET / - Health check
POST /upload - Upload PDF contract
POST /search - Search clauses semantically


Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

