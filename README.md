# 🏊 Sunny's Swimming Data Analysis Platform

A local, AI-powered platform to track, analyze, and gain insights from Sunny's swimming performance data.

## Features

- **Screenshot Ingestion**: Upload swimming meet screenshots with automatic organization
- **AI-Powered OCR**: Extract structured race data using Alibaba Cloud Model Studio's Qwen vision-language model
- **Body Metrics Tracking**: Record height, weight, and arm span with BMI calculation
- **Performance Analytics**: Visualize time progression, stroke comparisons, and personal bests
- **Research Comparison**: Search and compare against swimming benchmarks
- **Insight Generation**: Automated trend analysis, potential assessment, and training suggestions
- **Interactive Q&A**: Natural language questions about Sunny's swimming data

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your Alibaba Cloud API key:
```bash
export ALIBABA_CLOUD_API_KEY="your-api-key-here"
```

3. Run the application:
```bash
streamlit run app.py
```

## Data Storage

All data is stored locally in the `data/` directory:
- `data/screenshots/` - Raw screenshot images
- `data/swim_events.json` - Extracted race results
- `data/body_metrics.json` - Body measurement history
- `data/research_cache.json` - Cached research results

## Usage

1. **Upload**: Add screenshots from swimming meets. The AI will automatically extract race details.
2. **Gallery**: Browse and manage uploaded screenshots.
3. **Body Metrics**: Track Sunny's physical development over time.
4. **Analytics**: View performance trends and comparisons.
5. **Research**: Compare times against age-group benchmarks.
6. **Insights**: Get AI-generated analysis and training suggestions.
7. **Q&A**: Ask questions about the data in natural language.

## Data Model

Each swim event includes:
- Date, meet name, stroke, distance, time
- Splits, course (LC/SC), round (heat/semifinal/final)
- Rank, age group, heat/lane info
- Source screenshot reference

## Requirements

- Python 3.9+
- Alibaba Cloud API key (for OCR and Q&A)
- Internet connection (for research search)
