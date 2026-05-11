# Development Guide

<cite>
**Referenced Files in This Document**
- [README.md](file://README.md)
- [app.py](file://app.py)
- [requirements.txt](file://requirements.txt)
- [src/__init__.py](file://src/__init__.py)
- [src/config.py](file://src/config.py)
- [src/models.py](file://src/models.py)
- [src/storage.py](file://src/storage.py)
- [src/screenshot_manager.py](file://src/screenshot_manager.py)
- [src/ocr_service.py](file://src/ocr_service.py)
- [src/validation.py](file://src/validation.py)
- [src/analytics.py](file://src/analytics.py)
- [src/insights.py](file://src/insights.py)
- [src/research_service.py](file://src/research_service.py)
- [src/qa_service.py](file://src/qa_service.py)
</cite>

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Core Components](#core-components)
4. [Architecture Overview](#architecture-overview)
5. [Detailed Component Analysis](#detailed-component-analysis)
6. [Dependency Analysis](#dependency-analysis)
7. [Performance Considerations](#performance-considerations)
8. [Testing Strategy](#testing-strategy)
9. [Development Workflow](#development-workflow)
10. [Deployment Instructions](#deployment-instructions)
11. [Code Quality and Contribution Guidelines](#code-quality-and-contribution-guidelines)
12. [Troubleshooting Guide](#troubleshooting-guide)
13. [Conclusion](#conclusion)
14. [Appendices](#appendices)

## Introduction
This guide documents how to contribute to the Swimming Data Analysis Platform. It explains the codebase structure, architectural patterns, testing strategy, development workflow, deployment steps, and quality standards. The platform is a local Streamlit application that ingests swimming meet screenshots, extracts structured race data via AI, tracks body metrics, performs analytics, compares against benchmarks, generates insights, and supports Q&A.

## Project Structure
The repository follows a feature-layered organization:
- src/: Core application modules (services, models, storage, analytics)
- data/: Local JSON storage for swim events, body metrics, screenshot index, and research cache
- assets/, openspec/: Supporting assets and specification artifacts
- app.py: Streamlit entrypoint implementing UI pages and orchestration
- requirements.txt: Dependencies

```mermaid
graph TB
A["app.py<br/>Streamlit UI"] --> B["src/config.py<br/>Paths & env"]
A --> C["src/models.py<br/>Data models"]
A --> D["src/storage.py<br/>JSON persistence"]
A --> E["src/screenshot_manager.py<br/>Upload/gallery"]
A --> F["src/ocr_service.py<br/>AI OCR"]
A --> G["src/validation.py<br/>Time & field validation"]
A --> H["src/analytics.py<br/>Charts & summaries"]
A --> I["src/insights.py<br/>Insights & suggestions"]
A --> J["src/research_service.py<br/>Benchmarks"]
A --> K["src/qa_service.py<br/>Q&A"]
```

**Diagram sources**
- [app.py:1-447](file://app.py#L1-L447)
- [src/config.py:1-29](file://src/config.py#L1-L29)
- [src/models.py:1-55](file://src/models.py#L1-L55)
- [src/storage.py:1-107](file://src/storage.py#L1-L107)
- [src/screenshot_manager.py:1-136](file://src/screenshot_manager.py#L1-L136)
- [src/ocr_service.py:1-144](file://src/ocr_service.py#L1-L144)
- [src/validation.py:1-103](file://src/validation.py#L1-L103)
- [src/analytics.py:1-184](file://src/analytics.py#L1-L184)
- [src/insights.py:1-150](file://src/insights.py#L1-L150)
- [src/research_service.py:1-94](file://src/research_service.py#L1-L94)
- [src/qa_service.py:1-174](file://src/qa_service.py#L1-L174)

**Section sources**
- [README.md:1-63](file://README.md#L1-L63)
- [app.py:1-447](file://app.py#L1-L447)
- [src/config.py:1-29](file://src/config.py#L1-L29)

## Core Components
- Data models: SwimEvent and BodyMetrics define the persisted entities with serialization helpers.
- Storage: DataStore persists SwimEvent and BodyMetrics as JSON; ScreenshotIndex manages screenshot metadata.
- Services:
  - OCRService: Vision-language extraction from screenshots using Alibaba Cloud.
  - QAService: Natural language Q&A using structured data context.
  - ResearchService: DuckDuckGo search for benchmarks with caching.
  - Analytics: Time progression, stroke comparison, personal bests, and dashboard summary.
  - Insights: Trend analysis, strengths/weaknesses, potential assessment, training suggestions.
  - ScreenshotManager: Upload, deduplication, thumbnails, and gallery operations.
- Validation: Time parsing/format validation and required-field checks.
- UI Orchestration: app.py coordinates pages, session state, and service integrations.

**Section sources**
- [src/models.py:1-55](file://src/models.py#L1-L55)
- [src/storage.py:1-107](file://src/storage.py#L1-L107)
- [src/ocr_service.py:1-144](file://src/ocr_service.py#L1-L144)
- [src/qa_service.py:1-174](file://src/qa_service.py#L1-L174)
- [src/research_service.py:1-94](file://src/research_service.py#L1-L94)
- [src/analytics.py:1-184](file://src/analytics.py#L1-L184)
- [src/insights.py:1-150](file://src/insights.py#L1-L150)
- [src/screenshot_manager.py:1-136](file://src/screenshot_manager.py#L1-L136)
- [src/validation.py:1-103](file://src/validation.py#L1-L103)
- [app.py:1-447](file://app.py#L1-L447)

## Architecture Overview
The system is a Streamlit desktop app with a modular service layer:
- UI layer: app.py renders pages and orchestrates service calls.
- Service layer: specialized services encapsulate domain logic.
- Persistence layer: JSON files under data/.
- External integrations: Alibaba Cloud APIs for OCR/Q&A, DuckDuckGo for benchmarks.

```mermaid
graph TB
subgraph "UI Layer"
U["app.py"]
end
subgraph "Services"
O["OCRService"]
Q["QAService"]
R["ResearchService"]
A["Analytics"]
I["Insights"]
V["Validation"]
end
subgraph "Persistence"
DS["DataStore (JSON)"]
SI["ScreenshotIndex (JSON)"]
end
subgraph "External"
AC["Alibaba Cloud API"]
DDG["DuckDuckGo Search"]
end
U --> O
U --> Q
U --> R
U --> A
U --> I
O --> AC
Q --> AC
R --> DDG
U --> DS
U --> SI
A --> DS
I --> DS
R --> DS
O --> V
```

**Diagram sources**
- [app.py:1-447](file://app.py#L1-L447)
- [src/ocr_service.py:1-144](file://src/ocr_service.py#L1-L144)
- [src/qa_service.py:1-174](file://src/qa_service.py#L1-L174)
- [src/research_service.py:1-94](file://src/research_service.py#L1-L94)
- [src/analytics.py:1-184](file://src/analytics.py#L1-L184)
- [src/insights.py:1-150](file://src/insights.py#L1-L150)
- [src/storage.py:1-107](file://src/storage.py#L1-L107)
- [src/validation.py:1-103](file://src/validation.py#L1-L103)

## Detailed Component Analysis

### Data Models
SwimEvent and BodyMetrics are dataclasses with to_dict/from_dict helpers and a BMI property for BodyMetrics.

```mermaid
classDiagram
class SwimEvent {
+string date
+string meet_name
+string stroke
+int distance
+string time
+string[] splits
+string course
+string round
+int rank
+string age_group
+string source_screenshot
+string heat_lane
+string swimmer_name
+to_dict() dict
+from_dict(data) SwimEvent
}
class BodyMetrics {
+string date
+float height_cm
+float weight_kg
+float arm_span_cm
+string notes
+to_dict() dict
+from_dict(data) BodyMetrics
+bmi() float
}
```

**Diagram sources**
- [src/models.py:7-55](file://src/models.py#L7-L55)

**Section sources**
- [src/models.py:1-55](file://src/models.py#L1-L55)

### Storage Layer
DataStore persists SwimEvent and BodyMetrics as JSON arrays. ScreenshotIndex maintains a JSON index of screenshots with metadata and checksums.

```mermaid
classDiagram
class DataStore {
+load_swim_events() SwimEvent[]
+save_swim_events(events) void
+add_swim_event(event) void
+load_body_metrics() BodyMetrics[]
+save_body_metrics(metrics) void
+add_body_metric(metric) void
-_load_json(path) dict[]
-_save_json(path, data) void
}
class ScreenshotIndex {
+load() dict
+save(index) void
+add(metadata) void
+list_all() dict[]
+get_by_path(path) dict
+remove_by_path(path) bool
}
```

**Diagram sources**
- [src/storage.py:10-107](file://src/storage.py#L10-L107)

**Section sources**
- [src/storage.py:1-107](file://src/storage.py#L1-L107)

### Screenshot Manager
Handles upload, deduplication by filename and checksum, thumbnail generation, and gallery operations.

```mermaid
flowchart TD
Start(["Upload Request"]) --> Save["Save file to organized path"]
Save --> Exists{"Filename exists?"}
Exists --> |Yes| Abort1["Abort: duplicate filename"]
Exists --> |No| Checksum["Compute MD5 checksum"]
Checksum --> DupByHash{"Checksum matches existing?"}
DupByHash --> |Yes| Cleanup["Delete saved file"] --> Abort2["Abort: duplicate content"]
DupByHash --> |No| Index["Add metadata to index"]
Index --> Done(["Success"])
Abort1 --> Done
Abort2 --> Done
```

**Diagram sources**
- [src/screenshot_manager.py:26-82](file://src/screenshot_manager.py#L26-L82)

**Section sources**
- [src/screenshot_manager.py:1-136](file://src/screenshot_manager.py#L1-L136)

### OCR Service
Encodes images and sends them to Alibaba Cloud’s vision-language model to extract structured race data. Validates output and attaches confidence/error metadata.

```mermaid
sequenceDiagram
participant UI as "UI"
participant OCR as "OCRService"
participant API as "Alibaba Cloud API"
UI->>OCR : "extract_from_screenshot(path)"
OCR->>OCR : "encode image to base64"
OCR->>API : "chat.completions.create(messages, model)"
API-->>OCR : "raw text JSON"
OCR->>OCR : "clean markdown, parse JSON"
OCR->>OCR : "validate_swim_event_data(data)"
OCR-->>UI : "(is_valid, data, message)"
```

**Diagram sources**
- [src/ocr_service.py:49-119](file://src/ocr_service.py#L49-L119)

**Section sources**
- [src/ocr_service.py:1-144](file://src/ocr_service.py#L1-L144)

### QA Service
Builds a structured context from stored data and conversation history, classifies queries, and responds using the text model.

```mermaid
sequenceDiagram
participant User as "User"
participant QA as "QAService"
participant API as "Alibaba Cloud API"
User->>QA : "answer(question)"
QA->>QA : "_get_data_context()"
QA->>QA : "_classify_query(question)"
QA->>API : "chat.completions.create(messages)"
API-->>QA : "response"
QA->>QA : "store in conversation_history"
QA-->>User : "answer"
```

**Diagram sources**
- [src/qa_service.py:76-134](file://src/qa_service.py#L76-L134)

**Section sources**
- [src/qa_service.py:1-174](file://src/qa_service.py#L1-L174)

### Research Service
Searches benchmarks via DuckDuckGo, caches results, and compares personal bests.

```mermaid
sequenceDiagram
participant UI as "UI"
participant RS as "ResearchService"
participant Cache as "Cache File"
participant DDGS as "DuckDuckGo"
UI->>RS : "search_benchmarks(stroke, dist, age)"
RS->>Cache : "load_cache()"
alt cache hit
Cache-->>RS : "cached results"
else cache miss
RS->>DDGS : "text(query, max_results=5)"
DDGS-->>RS : "results"
RS->>Cache : "save_cache(results)"
end
RS-->>UI : "results"
```

**Diagram sources**
- [src/research_service.py:31-54](file://src/research_service.py#L31-L54)

**Section sources**
- [src/research_service.py:1-94](file://src/research_service.py#L1-L94)

### Analytics
Provides dashboards, time progression charts, stroke comparison radar, personal bests, and summary statistics.

```mermaid
flowchart TD
Load["Load SwimEvents as DataFrame"] --> Filter["Filter by stroke/distance"]
Filter --> Sort["Sort by date"]
Sort --> Chart["Create Plotly chart"]
Chart --> Output["Return figure"]
```

**Diagram sources**
- [src/analytics.py:30-60](file://src/analytics.py#L30-L60)

**Section sources**
- [src/analytics.py:1-184](file://src/analytics.py#L1-L184)

### Insights
Generates trend insights, identifies strengths/weaknesses, assesses potential, and suggests drills.

```mermaid
flowchart TD
Start(["Generate Insights"]) --> PB["Load personal bests"]
PB --> Groups["Group by stroke-distance"]
Groups --> Trends["Compute improvements"]
Trends --> Strengths["Identify strongest/weakest strokes"]
Strengths --> Assessment["Assess trajectory & consistency"]
Assessment --> Suggestions["Generate drill suggestions"]
Suggestions --> End(["Return insights"])
```

**Diagram sources**
- [src/insights.py:14-120](file://src/insights.py#L14-L120)

**Section sources**
- [src/insights.py:1-150](file://src/insights.py#L1-L150)

### Validation Utilities
Ensures time formats and required fields are valid.

```mermaid
flowchart TD
In(["validate_swim_event_data"]) --> Req["Check required fields"]
Req --> Time["Validate time format"]
Time --> Splits["Validate each split"]
Splits --> Out(["Return (is_valid, errors)"])
```

**Diagram sources**
- [src/validation.py:75-103](file://src/validation.py#L75-L103)

**Section sources**
- [src/validation.py:1-103](file://src/validation.py#L1-L103)

## Dependency Analysis
Key internal dependencies:
- app.py depends on all services and storage.
- Services depend on models, storage, and validation.
- Analytics and Insights depend on DataStore and validation.
- ResearchService depends on DataStore and external DuckDuckGo.
- OCRService and QAService depend on external Alibaba Cloud.

```mermaid
graph LR
APP["app.py"] --> ST["storage.py"]
APP --> SM["screenshot_manager.py"]
APP --> OC["ocr_service.py"]
APP --> AN["analytics.py"]
APP --> IN["insights.py"]
APP --> RS["research_service.py"]
APP --> QA["qa_service.py"]
OC --> VL["validation.py"]
AN --> VL
IN --> AN
RS --> ST
OC --> CFG["config.py"]
QA --> CFG
RS --> CFG
ST --> CFG
SM --> CFG
```

**Diagram sources**
- [app.py:1-447](file://app.py#L1-L447)
- [src/storage.py:1-107](file://src/storage.py#L1-L107)
- [src/screenshot_manager.py:1-136](file://src/screenshot_manager.py#L1-L136)
- [src/ocr_service.py:1-144](file://src/ocr_service.py#L1-L144)
- [src/analytics.py:1-184](file://src/analytics.py#L1-L184)
- [src/insights.py:1-150](file://src/insights.py#L1-L150)
- [src/research_service.py:1-94](file://src/research_service.py#L1-L94)
- [src/qa_service.py:1-174](file://src/qa_service.py#L1-L174)
- [src/validation.py:1-103](file://src/validation.py#L1-L103)
- [src/config.py:1-29](file://src/config.py#L1-L29)

**Section sources**
- [app.py:1-447](file://app.py#L1-L447)
- [src/config.py:1-29](file://src/config.py#L1-L29)

## Performance Considerations
- JSON I/O: DataStore writes entire arrays on each write; consider batching writes for bulk operations.
- Image processing: Thumbnail generation uses Pillow; avoid repeated resampling by caching images.
- API calls: OCR and Q&A calls are network-bound; add retry/backoff and consider local caching for repeated prompts.
- Analytics: Convert to DataFrame once per report; reuse computed series to avoid recomputation.
- UI reruns: Minimize unnecessary st.rerun() calls and keep heavy computations outside render path.

## Testing Strategy
Current state: No dedicated tests directory was found in the repository snapshot. Recommended approach:
- Unit tests: Use pytest to test services (OCRService, QAService, ResearchService, Analytics, Insights) with mocked external APIs and file system.
- Integration tests: Verify end-to-end flows (upload → OCR → validation → persistence → analytics).
- Mocking: Replace Alibaba Cloud client and DuckDuckGo with fakes; stub file system for storage tests.
- Coverage: Aim for >80% coverage on services and utilities.
- CI: Add a GitHub Actions workflow to run tests on push and pull requests.

## Development Workflow
Local setup
- Install dependencies: pip install -r requirements.txt
- Set environment: export ALIBABA_CLOUD_API_KEY="your-api-key"
- Run: streamlit run app.py

Debugging tips
- Enable Streamlit’s developer mode and logs.
- Use st.exception() around service calls to surface exceptions.
- Log API responses and errors for OCR/QA.
- Validate time formats early in the pipeline to fail fast.

Code review checklist
- Clear separation of concerns (UI vs services vs storage).
- Proper error handling and user-friendly messages.
- Minimal duplication; reuse validation and analytics utilities.
- Environment variables for secrets; no hardcoded credentials.

**Section sources**
- [README.md:15-31](file://README.md#L15-L31)
- [requirements.txt:1-10](file://requirements.txt#L1-10)
- [app.py:36-402](file://app.py#L36-L402)

## Deployment Instructions
Local/desktop
- Package as a Streamlit app; ensure data/ directory is included.
- Distribute with Python 3.9+ and installed requirements.

Production considerations
- Secrets management: Store API keys in environment variables or a secrets manager.
- Data backup: Automate JSON exports and offsite backups.
- Rate limits: Respect Alibaba Cloud and DuckDuckGo quotas; implement retries with backoff.
- Monitoring: Add basic logging and health checks for API connectivity.

[No sources needed since this section provides general guidance]

## Code Quality and Contribution Guidelines
Standards
- Naming: Use snake_case for modules and functions; PascalCase for classes.
- Modules: One responsibility per module; keep services cohesive.
- Comments: Docstrings for public functions/classes; inline comments for complex logic.
- Imports: Group standard library, third-party, and local imports.

Documentation
- Update README.md for new features and breaking changes.
- Add module docstrings and function-level docs for public APIs.

Branching and PRs
- Feature branches; small, focused commits.
- Include tests and update docs.
- Request reviews from maintainers.

**Section sources**
- [src/__init__.py:1-2](file://src/__init__.py#L1-L2)

## Troubleshooting Guide
Common issues
- Missing API key: UI shows a warning; set ALIBABA_CLOUD_API_KEY and restart.
- OCR failures: Check image encoding and response parsing; validate time formats.
- Empty analytics: Ensure sufficient data; verify time formats and dates.
- Benchmark search errors: DuckDuckGo may rate limit; cache results and retry.

Where to look
- API status indicator in footer.
- Error messages returned by OCRService and QAService.
- Validation errors attached to extracted data.

**Section sources**
- [app.py:441-447](file://app.py#L441-L447)
- [src/ocr_service.py:49-119](file://src/ocr_service.py#L49-L119)
- [src/qa_service.py:76-134](file://src/qa_service.py#L76-L134)
- [src/validation.py:75-103](file://src/validation.py#L75-L103)

## Conclusion
This guide outlined the platform’s architecture, component responsibilities, and development practices. By following the structure and guidelines here, contributors can reliably add features, maintain quality, and deploy confidently.

## Appendices

### Adding a New Feature: Step-by-Step Example
- Define data model changes in models.py if needed.
- Extend storage in storage.py if persisting new entities.
- Implement service logic in a new module under src/.
- Integrate UI in app.py with appropriate page/tab.
- Add validation in validation.py if applicable.
- Write unit tests and integration tests.
- Update README.md with usage notes.

[No sources needed since this section provides general guidance]