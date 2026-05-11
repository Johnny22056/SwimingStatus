## Context

Sunny is a young swimmer whose performance data exists only as screenshots from swimming meets (likely from apps like Meet Mobile or similar). There is no existing system to track, analyze, or derive insights from this data. The platform must be designed for a non-technical parent to use, with minimal friction for adding new data and asking questions. All data will be stored locally in the project directory.

## Goals / Non-Goals

**Goals:**
- Build a Python-based application that can be run locally without external servers
- Store raw screenshots in an organized folder structure
- Extract structured data from screenshots automatically
- Track body metrics over time via manual input
- Generate visual analytics (trends, comparisons, progress charts)
- Compare performance against published swimming research and benchmarks
- Provide natural-language Q&A about Sunny's swimming data
- Support incremental data addition as new meets occur

**Non-Goals:**
- Real-time data collection from wearable devices
- Mobile app or web deployment (local desktop only)
- Social features or sharing with other swimmers
- Coaching workflow management or practice planning
- Multi-user support (initially single-user: Sunny)
- Complex database infrastructure (keep it simple and file-based)

## Decisions

**Python + Streamlit for UI**
- Rationale: Streamlit provides the fastest path to an interactive data dashboard with minimal frontend code. It supports file uploads, data visualization, and chat interfaces natively. Alternative: React + Flask would require significantly more boilerplate for a single-user local app.

**File-based storage with JSON/CSV, not SQL**
- Rationale: The data volume is small (one swimmer, occasional meets) and file-based storage eliminates setup complexity. Screenshots stored as files; extracted data as JSON/CSV. Alternative: SQLite would add unnecessary complexity for this use case.

**OCR via Alibaba Cloud Model Studio Service**
- Rationale: Alibaba Cloud's Qwen vision-language model provides superior understanding of structured tabular data (like meet results) compared to traditional OCR, enabling extraction of comprehensive details including split times, heat/lane info, and rankings in a single API call. This approach captures all relevant swimming data from screenshots holistically rather than extracting raw text for post-processing. Alternative: Traditional OCR (Tesseract/PaddleOCR) requires complex post-processing pipelines and struggles with varying screenshot formats.

**Web search via DuckDuckGo or similar**
- Rationale: DuckDuckGo provides search without API keys, making the app fully self-contained. For swimming research, this is sufficient to find published studies and age-group benchmarks. Alternative: Google Custom Search would require API key management.

**LLM for Q&A and insight generation**
- Rationale: Alibaba Cloud Model Studio's Qwen Model can interpret extracted data, answer questions, and generate insights. Using the same service provider for both OCR and Q&A simplifies integration and credential management. The LLM receives structured context about Sunny's data to answer questions. Alternative: OpenAI API or local models via Ollama would require separate API keys and integration work.

**Data model: Event-centric**
- Rationale: Each screenshot typically contains meet results. The core entity is a `SwimEvent` with fields: date, meet name, stroke, distance, time, splits, course, round, rank, age group. Body metrics stored separately with timestamps. This model maps naturally to how parents receive data.

## Risks / Trade-offs

**[Risk] OCR accuracy on low-quality screenshots** → Mitigation: Implement manual correction UI for extracted data; store corrected values as ground truth to improve future OCR confidence

**[Risk] Screenshot formats vary by meet/app** → Mitigation: Start with most common format (Meet Mobile); design OCR pipeline to be configurable per format; allow manual entry as fallback

**[Risk] Swimming research search may return irrelevant results** → Mitigation: Pre-filter search queries with swimming-specific terms; allow user to provide specific research URLs for comparison

**[Risk] LLM hallucinations when analyzing data** → Mitigation: Always ground LLM responses in actual extracted data; include data citations in answers; allow user to verify insights against source data

**[Risk] Data loss if local files are corrupted** → Mitigation: Implement simple JSON backup/restore; suggest user commit data to git periodically

**[Trade-off] Simplicity vs. Accuracy**: Using file-based storage and local OCR prioritizes ease of use over enterprise-grade accuracy. Manual data correction is the escape hatch.
