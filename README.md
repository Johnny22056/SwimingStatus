# Sunny's Swimming Analytics Platform

A data-driven swimming performance analysis platform for tracking, analyzing, and visualizing competitive swimming results. Built with Streamlit and powered by Alibaba Cloud Model Studio (Qwen) for OCR and AI-powered insights.

## Features

- **Import** — Single screenshot upload with OCR extraction, batch folder import (recursive), and Excel file import with column mapping
- **Records** — Sortable/filterable table of all swim events with Age Group, calculated Age, download as CSV
- **Body Metrics** — Track height/weight/BMI measurements over time
- **National Standard** — Official 2025 Chinese Swimming Association female standards (LC/SC) with OCR import and Excel export
- **Analytics** — Personal Bests (LC/SC), Time Development curves per stroke-distance with smooth splines, National/International Master and Level 1 reference lines, downloadable HTML report
- **Insights** — AI-generated swimming performance insights
- **Q&A** — Interactive AI-powered question and answer about swimming performance

## Tech Stack

- **Python / Streamlit** — Web application framework
- **Alibaba Cloud Model Studio** — Qwen VL for OCR, Qwen for Q&A/insights
- **Plotly** — Interactive charts and visualizations
- **Pandas** — Data processing
- **OpenAI-compatible API client** — Model Studio integration

## Setup

```bash
# Clone the repo
git clone https://github.com/Johnny22056/SwimingStatus.git
cd SwimingStatus

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create a .env file with:
# ALIBABA_CLOUD_API_KEY=your_api_key_here

# Run the app
streamlit run app.py
```

## Project Structure

```
app.py                    # Main Streamlit application
src/
  analytics.py            # Performance analytics and HTML report generation
  base_service.py         # Base class for AI service clients
  config.py               # Configuration and paths
  folder_dialog.py        # Native OS folder selection dialog
  insights.py             # Trend insights and training suggestions
  models.py               # Data models (SwimEvent, BodyMetrics)
  ocr_service.py          # OCR extraction via Qwen VL
  qa_service.py           # Q&A service via Qwen
  research_service.py     # Web search and research comparison
  screenshot_manager.py   # Screenshot upload and organization
  storage.py              # JSON-based data persistence
  validation.py           # Data validation and time parsing
data/
  swim_events.json        # Extracted swim records
  body_metrics.json       # Body measurement history
  research_cache.json     # Cached research results
  screenshots/            # Organized screenshot images
```
