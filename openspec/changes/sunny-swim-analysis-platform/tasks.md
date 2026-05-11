## 1. Project Setup

- [x] 1.1 Create project directory structure (`data/`, `src/`, `tests/`, `assets/`)
- [x] 1.2 Set up Python virtual environment and `requirements.txt` with Streamlit, Qwen Model Studio SDK, pandas, matplotlib, plotly, Pillow, duckduckgo-search
- [x] 1.3 Create `data/screenshots/` and `data/extracted/` directories with `.gitkeep`
- [x] 1.4 Initialize `.gitignore` for Python projects and data files
- [x] 1.5 Create `config.py` with project paths and OCR settings

## 2. Data Models and Storage

- [x] 2.1 Define `SwimEvent` dataclass with fields: date, meet_name, stroke, distance, time, splits, course, round, rank, age_group, source_screenshot
- [x] 2.2 Define `BodyMetrics` dataclass with fields: date, height_cm, weight_kg, arm_span_cm, notes
- [x] 2.3 Implement `DataStore` class for JSON-based persistence with load/save methods
- [x] 2.4 Implement screenshot metadata index (`data/screenshots/index.json`) with add/list/get methods
- [x] 2.5 Add data validation layer for time formats (MM:SS.ss, SS.ss) and required fields

## 3. Screenshot Data Ingestion

- [x] 3.1 Build Streamlit upload widget for single/batch screenshot uploads
- [x] 3.2 Implement folder structure creation (`data/screenshots/<meet-name>/<date>/`)
- [x] 3.3 Add duplicate detection using filename comparison and MD5 checksum
- [x] 3.4 Build screenshot gallery view with thumbnails and metadata display
- [x] 3.5 Implement screenshot deletion with confirmation and index cleanup

## 4. OCR Data Extraction

- [x] 4.1 Integrate Alibaba Cloud Model Studio Service for vision-language based comprehensive data extraction from screenshots
- [x] 4.2 Build structured data parser for Alibaba Cloud Model Studio Service extraction output including all SwimEvent fields extractable from screenshots: date, meet_name, stroke, distance, time, splits, course, round, rank, age_group, and heat/lane info
- [x] 4.3 Implement confidence scoring per extracted field (0-100%)
- [x] 4.4 Build manual correction UI for low-confidence extractions in Streamlit
- [x] 4.5 Create `extracted_data.json` schema and save validated extractions
- [x] 4.6 Configure Alibaba Cloud Model Studio Service prompt templates for different screenshot formats (Meet Mobile, Hy-Tek, manual results)
- [x] 4.7 Implement fallback manual entry form when OCR completely fails

## 5. Body Metrics Tracking

- [x] 5.1 Build Streamlit form for body metrics input (date, height, weight, arm span, notes)
- [x] 5.2 Implement `data/body_metrics.json` storage with append semantics
- [x] 5.3 Add BMI calculation utility function
- [x] 5.4 Build body metrics history table with edit/delete capabilities
- [x] 5.5 Create line charts for height, weight, BMI progression over time using Plotly

## 6. Performance Analytics

- [x] 6.1 Build data aggregation pipeline to group events by stroke, distance, and date
- [x] 6.2 Implement time-to-seconds and seconds-to-time conversion utilities
- [x] 6.3 Create line charts for time progression by stroke and distance
- [x] 6.4 Build age-adjusted performance calculation (time improvement normalized by age)
- [x] 6.5 Implement radar chart for stroke comparison using Plotly
- [x] 6.6 Build personal best tracker with automatic PB detection per event
- [x] 6.7 Create dashboard summary with key stats (total meets, events, PBs count)

## 7. Research Comparison

- [x] 7.1 Integrate DuckDuckGo search for swimming benchmarks and age-group standards
- [x] 7.2 Build search query generator based on stroke, distance, age, and gender
- [x] 7.3 Implement research result caching in `data/research_cache.json`
- [x] 7.4 Build benchmark comparison UI showing Sunny's time vs found benchmarks
- [x] 7.5 Add percentile calculation based on benchmark data
- [x] 7.6 Allow manual input of benchmark URLs for specific comparisons

## 8. Insight Generation

- [x] 8.1 Build trend analysis engine (improvement rate, consistency, plateau detection)
- [x] 8.2 Implement strength/weakness identification by stroke comparison
- [x] 8.3 Create insight template generator with data citations
- [x] 8.4 Build potential assessment algorithm using progression rate + benchmark gaps
- [x] 8.5 Implement training suggestion engine with drill recommendations per stroke
- [x] 8.6 Add Streamlit section for generated insights with refresh capability

## 9. Interactive Q&A

- [x] 9.1 Build chat interface in Streamlit using `st.chat_message` and `st.chat_input`
- [x] 9.2 Implement query classifier to identify question types (PB, trend, comparison, advice)
- [x] 9.3 Build data retrieval functions for each question type
- [x] 9.4 Integrate Alibaba Cloud Model Studio's Qwen Model for natural language response generation
- [x] 9.5 Implement context tracking for multi-turn conversations
- [x] 9.6 Add data grounding layer ensuring all answers include specific data citations
- [x] 9.7 Build guardrails to reject out-of-scope questions

## 10. Main Application Integration

- [x] 10.1 Create `app.py` main entry point with sidebar navigation
- [x] 10.2 Implement page routing: Upload, Gallery, Body Metrics, Analytics, Research, Insights, Q&A
- [x] 10.3 Add session state management for data refresh across pages
- [x] 10.4 Build data export feature (JSON/CSV backup)
- [x] 10.5 Add simple data import/restore from backup
- [x] 10.6 Create README with setup instructions and usage guide
- [x] 10.7 Run end-to-end test with sample screenshots
