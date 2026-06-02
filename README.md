# Swimming Analytics Platform

A data-driven swimming performance analysis platform for tracking, analyzing, and visualizing competitive swimming results. Built with Streamlit and powered by Alibaba Cloud Model Studio (Qwen) for OCR and AI-powered insights.

## Features

- **Benchmarks** — Official 2025 Chinese Swimming Association female standards (LC/SC) with OCR import preview.
- **Performance** — Personal Bests (LC/SC), Time Development curves per stroke-distance with smooth splines, Level 1 / National / International Master reference lines, downloadable HTML report.
- **Insights** — Trend tables, strengths/weaknesses, potential assessment, training suggestions.
- **AI Coach** — Interactive Q&A about the swimmer's data via Qwen text model.
- **Data Import** — Single screenshot upload with OCR extraction, batch folder import (recursive), and Excel import with column mapping.
- **Race Log** — Sortable/filterable table of all swim events with Age Group, calculated Age, CSV download.
- **Body Metrics** — Track height/weight/BMI measurements over time.

## Tech Stack

- **Python / Streamlit** — Web application framework
- **Alibaba Cloud Model Studio** — Qwen VL for OCR, Qwen for Q&A/insights
- **Plotly** — Interactive charts and visualizations
- **Pandas** — Data processing
- **OpenAI-compatible API client** — Model Studio integration

## Setup

```bash
git clone https://github.com/Johnny22056/SwimingStatus.git
cd SwimingStatus

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in the project root:

```ini
ALIBABA_CLOUD_API_KEY=your_api_key_here
# Optional:
SWIMMER_NAME=Swimmer
SWIMMER_DOB=2011-08-06          # ISO date; enables Age column in Race Log
ALIBABA_CLOUD_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
QWEN_MODEL_NAME=qwen-vl-max
QWEN_TEXT_MODEL_NAME=qwen-max
```

Run the app:

```bash
streamlit run app.py
```

## Project Structure

```
app.py                     # Main Streamlit application
src/
  analytics.py             # Performance analytics + HTML report
  base_service.py          # Base class for Alibaba Cloud Model Studio clients
  config.py                # Environment, paths, swimmer identity, course overrides
  folder_dialog.py         # Native macOS folder selection dialog
  insights.py              # Trend insights and training suggestions
  models.py                # Data models (SwimEvent, BodyMetrics)
  ocr_service.py           # OCR extraction via Qwen VL
  qa_service.py            # Q&A service via Qwen
  screenshot_manager.py    # Screenshot ingestion, dedup, organization
  standards.py             # Chinese swimming standards (LC/SC)
  storage.py               # Atomic JSON persistence with backup rotation
  theme.py                 # Dark/light palette definitions
  validation.py            # Data validation and time parsing
tests/                     # pytest suite
data/
  swim_events.json         # Extracted swim records (gitignored)
  body_metrics.json        # Body measurement history (gitignored)
  screenshots/             # Organized screenshot images (gitignored)
```

## Tests

```bash
pip install pytest
pytest
```

## Notes

- Times are stored as the original strings shown on the screenshots (`MM:SS.ss` or `SS.ss`) and converted to seconds for comparison/plotting via `validation.time_to_seconds`.
- Records and screenshots are deduplicated on a composite key (date + stroke + distance + time + course) and on file checksum, respectively.
- The native folder picker (`Browse Folder` in batch import) is macOS-only; other platforms use the manual path field.
