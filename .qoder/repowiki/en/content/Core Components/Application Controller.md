# Application Controller

<cite>
**Referenced Files in This Document**
- [app.py](file://app.py)
- [src/config.py](file://src/config.py)
- [src/models.py](file://src/models.py)
- [src/storage.py](file://src/storage.py)
- [src/screenshot_manager.py](file://src/screenshot_manager.py)
- [src/ocr_service.py](file://src/ocr_service.py)
- [src/validation.py](file://src/validation.py)
- [src/analytics.py](file://src/analytics.py)
- [src/research_service.py](file://src/research_service.py)
- [src/insights.py](file://src/insights.py)
- [src/qa_service.py](file://src/qa_service.py)
- [requirements.txt](file://requirements.txt)
- [README.md](file://README.md)
</cite>

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Core Components](#core-components)
4. [Architecture Overview](#architecture-overview)
5. [Detailed Component Analysis](#detailed-component-analysis)
6. [Dependency Analysis](#dependency-analysis)
7. [Performance Considerations](#performance-considerations)
8. [Troubleshooting Guide](#troubleshooting-guide)
9. [Conclusion](#conclusion)

## Introduction
This document provides comprehensive documentation for the main application controller (app.py) of the Swimming Data Analysis Platform. The controller orchestrates a Streamlit-based UI with seven main pages: Upload, Gallery, Body Metrics, Analytics, Research, Insights, and Q&A. It manages session state across page navigations, coordinates UI interactions with backend services, and integrates external AI APIs for OCR and Q&A capabilities. The documentation covers initialization sequences, component instantiation, inter-page data sharing, error handling strategies, spinner usage for asynchronous operations, and responsive layout patterns.

## Project Structure
The application follows a modular architecture with a clear separation between UI orchestration (app.py) and domain services located under src/. Key directories and files:
- app.py: Central Streamlit application controller and page router
- src/: Domain services and utilities
  - config.py: Configuration constants and environment variables
  - models.py: Data models for SwimEvent and BodyMetrics
  - storage.py: File-based persistence layer
  - screenshot_manager.py: Screenshot ingestion and gallery management
  - ocr_service.py: Alibaba Cloud OCR integration
  - validation.py: Data validation utilities
  - analytics.py: Performance analytics and visualizations
  - research_service.py: Benchmark search and comparison
  - insights.py: Trend analysis and training suggestions
  - qa_service.py: Natural language Q&A
- requirements.txt: Dependencies
- README.md: Project overview and usage

```mermaid
graph TB
A["app.py<br/>Streamlit Controller"] --> B["src/config.py<br/>Configuration"]
A --> C["src/models.py<br/>Data Models"]
A --> D["src/storage.py<br/>Persistence Layer"]
A --> E["src/screenshot_manager.py<br/>Screenshot Manager"]
A --> F["src/ocr_service.py<br/>OCR Service"]
A --> G["src/validation.py<br/>Validation Utilities"]
A --> H["src/analytics.py<br/>Analytics Engine"]
A --> I["src/research_service.py<br/>Research Service"]
A --> J["src/insights.py<br/>Insight Generator"]
A --> K["src/qa_service.py<br/>QA Service"]
L["requirements.txt"] --> A
M["README.md"] --> A
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
- [src/research_service.py:1-94](file://src/research_service.py#L1-L94)
- [src/insights.py:1-150](file://src/insights.py#L1-L150)
- [src/qa_service.py:1-174](file://src/qa_service.py#L1-L174)

**Section sources**
- [app.py:1-447](file://app.py#L1-L447)
- [README.md:1-63](file://README.md#L1-L63)

## Core Components
The application controller centers around several key components:

- Session State Management: Initializes and maintains application state across page navigations and user interactions.
- Sidebar Navigation: Provides primary and secondary button styling based on the active page.
- Page Routing System: Implements seven main pages with distinct functionality and UI layouts.
- Service Coordination: Integrates OCR, analytics, research, insights, and Q&A services.
- Data Persistence: Uses JSON-based storage for swim events, body metrics, and screenshot indices.
- External API Integration: Connects to Alibaba Cloud Model Studio for OCR and Q&A.

Key implementation patterns:
- Streamlit page routing using session state to control visibility
- Spinner usage for async operations (OCR extraction, research search)
- Responsive layout using Streamlit columns and tabs
- Error handling with user-friendly feedback messages
- Inter-page data sharing via session state variables

**Section sources**
- [app.py:29-42](file://app.py#L29-L42)
- [app.py:45-58](file://app.py#L45-L58)
- [app.py:61-127](file://app.py#L61-L127)
- [app.py:129-166](file://app.py#L129-L166)
- [app.py:168-224](file://app.py#L168-L224)
- [app.py:226-280](file://app.py#L226-L280)
- [app.py:282-320](file://app.py#L282-L320)
- [app.py:321-370](file://app.py#L321-L370)
- [app.py:371-403](file://app.py#L371-L403)
- [app.py:405-447](file://app.py#L405-L447)

## Architecture Overview
The application employs a layered architecture with clear separation of concerns:

```mermaid
graph TB
subgraph "Presentation Layer"
UI["Streamlit UI<br/>Pages: Upload, Gallery,<br/>Body Metrics, Analytics,<br/>Research, Insights, Q&A"]
end
subgraph "Controller Layer"
CTRL["App Controller<br/>Session State<br/>Page Routing"]
end
subgraph "Domain Services"
OCR["OCR Service<br/>Alibaba Cloud API"]
QA["QA Service<br/>Alibaba Cloud API"]
ANA["Analytics Engine<br/>Performance Charts"]
RES["Research Service<br/>Benchmark Search"]
INS["Insight Generator<br/>Trend Analysis"]
end
subgraph "Data Layer"
STORE["DataStore<br/>JSON Persistence"]
IDX["ScreenshotIndex<br/>Metadata Index"]
CFG["Config<br/>Environment Variables"]
end
subgraph "External Services"
ALI["Alibaba Cloud<br/>Model Studio"]
DDG["DuckDuckGo Search<br/>Benchmarks"]
end
UI --> CTRL
CTRL --> OCR
CTRL --> QA
CTRL --> ANA
CTRL --> RES
CTRL --> INS
OCR --> ALI
QA --> ALI
RES --> DDG
CTRL --> STORE
CTRL --> IDX
CTRL --> CFG
STORE --> STORE
IDX --> STORE
```

**Diagram sources**
- [app.py:1-447](file://app.py#L1-L447)
- [src/ocr_service.py:12-21](file://src/ocr_service.py#L12-L21)
- [src/qa_service.py:12-22](file://src/qa_service.py#L12-L22)
- [src/analytics.py:13-14](file://src/analytics.py#L13-L14)
- [src/research_service.py:10-11](file://src/research_service.py#L10-L11)
- [src/insights.py:11-12](file://src/insights.py#L11-L12)
- [src/storage.py:10-62](file://src/storage.py#L10-L62)
- [src/screenshot_manager.py:14-15](file://src/screenshot_manager.py#L14-L15)
- [src/config.py:1-29](file://src/config.py#L1-L29)

## Detailed Component Analysis

### Session State Management
The controller initializes essential session state variables at startup and provides a page switching mechanism:

```mermaid
flowchart TD
Start([App Startup]) --> InitPage["Initialize 'page' = 'Upload'"]
InitPage --> InitChat["Initialize 'chat_history' = []"]
InitChat --> InitLast["Initialize 'last_extraction' = None"]
InitLast --> InitQA["Initialize 'qa_service' = QAService()"]
InitQA --> SwitchPage["switch_page() updates page state"]
SwitchPage --> Rerun["st.rerun() triggers UI refresh"]
Rerun --> End([Session Ready])
```

**Diagram sources**
- [app.py:29-42](file://app.py#L29-L42)

Key session state variables:
- page: Current active page identifier
- chat_history: Conversation history for Q&A
- last_extraction: Most recent OCR extraction result
- qa_service: Persistent QA service instance

**Section sources**
- [app.py:29-42](file://app.py#L29-L42)

### Sidebar Navigation System
The sidebar implements a responsive navigation interface with dynamic button styling:

```mermaid
sequenceDiagram
participant User as "User"
participant Sidebar as "Sidebar Buttons"
participant Controller as "switch_page()"
participant Streamlit as "st.rerun()"
User->>Sidebar : Click Navigation Button
Sidebar->>Controller : switch_page(page_name)
Controller->>Controller : Update st.session_state.page
Controller->>Streamlit : st.rerun()
Streamlit-->>User : Re-render Active Page
```

**Diagram sources**
- [app.py:45-58](file://app.py#L45-L58)
- [app.py:40-43](file://app.py#L40-L43)

Navigation buttons use container width and toggle between primary (active) and secondary (inactive) styles based on current page state.

**Section sources**
- [app.py:45-58](file://app.py#L45-L58)

### Upload Page Workflow
The Upload page handles screenshot ingestion, OCR extraction, and data validation:

```mermaid
sequenceDiagram
participant User as "User"
participant Upload as "Upload Page"
participant SM as "ScreenshotManager"
participant OCR as "OCRService"
participant DS as "DataStore"
participant VA as "Validation"
User->>Upload : Select File + Enter Details
Upload->>SM : save_uploaded_screenshot()
SM-->>Upload : Success/Failure + Message
Upload->>Upload : Show Spinner "Extracting..."
Upload->>OCR : extract_from_screenshot()
OCR->>OCR : Encode Image + Call API
OCR-->>Upload : Extraction Result + Data
Upload->>VA : validate_swim_event_data()
VA-->>Upload : Validation Result + Errors
Upload->>DS : add_swim_event()
DS-->>Upload : Confirmation
Upload-->>User : Success/Error Messages
```

**Diagram sources**
- [app.py:61-127](file://app.py#L61-L127)
- [src/screenshot_manager.py:27-82](file://src/screenshot_manager.py#L27-L82)
- [src/ocr_service.py:49-119](file://src/ocr_service.py#L49-L119)
- [src/validation.py:75-103](file://src/validation.py#L75-L103)
- [src/storage.py:40-44](file://src/storage.py#L40-L44)

Key features:
- Duplicate detection via filename and checksum
- Automatic OCR extraction with spinner feedback
- Data validation with detailed error reporting
- Structured SwimEvent creation and persistence

**Section sources**
- [app.py:61-127](file://app.py#L61-L127)
- [src/screenshot_manager.py:17-82](file://src/screenshot_manager.py#L17-L82)
- [src/ocr_service.py:49-119](file://src/ocr_service.py#L49-L119)
- [src/validation.py:75-103](file://src/validation.py#L75-L103)
- [src/storage.py:29-44](file://src/storage.py#L29-L44)

### Gallery Page Implementation
The Gallery page organizes screenshots by meet and provides management capabilities:

```mermaid
flowchart TD
Load([Load Screenshots]) --> CheckEmpty{"Any Screenshots?"}
CheckEmpty --> |No| ShowInfo["Show Info Message"]
CheckEmpty --> |Yes| Group["Group by Meet"]
Group --> Iterate["Iterate Meet Groups"]
Iterate --> Expand["Create Expander per Meet"]
Expand --> Thumbnail["Display Thumbnails"]
Thumbnail --> Manage["Provide Delete Buttons"]
Manage --> Delete["Delete Handler"]
Delete --> Refresh["Refresh Page"]
```

**Diagram sources**
- [app.py:129-166](file://app.py#L129-L166)
- [src/screenshot_manager.py:85-136](file://src/screenshot_manager.py#L85-L136)

**Section sources**
- [app.py:129-166](file://app.py#L129-L166)
- [src/screenshot_manager.py:85-136](file://src/screenshot_manager.py#L85-L136)

### Body Metrics Page
The Body Metrics page combines data entry with historical visualization:

```mermaid
sequenceDiagram
participant User as "User"
participant Form as "Body Metrics Form"
participant DS as "DataStore"
participant DF as "DataFrame"
participant Plotly as "Plotly Charts"
User->>Form : Fill Measurement Form
Form->>DS : add_body_metric()
DS-->>Form : Success
Form->>Form : st.rerun()
Form->>DS : load_body_metrics()
DS-->>Form : Metrics List
Form->>DF : Convert to DataFrame
DF->>Plotly : Create Progression Charts
Plotly-->>User : Render Line Charts
```

**Diagram sources**
- [app.py:168-224](file://app.py#L168-L224)
- [src/storage.py:46-61](file://src/storage.py#L46-L61)
- [src/models.py:32-55](file://src/models.py#L32-L55)

**Section sources**
- [app.py:168-224](file://app.py#L168-L224)
- [src/storage.py:46-61](file://src/storage.py#L46-L61)
- [src/models.py:32-55](file://src/models.py#L32-L55)

### Analytics Page
The Analytics page provides comprehensive performance visualization:

```mermaid
flowchart TD
LoadEvents([Load Swim Events]) --> CheckEvents{"Events Available?"}
CheckEvents --> |No| ShowInfo["Show Info Message"]
CheckEvents --> |Yes| Summary["Generate Dashboard Summary"]
Summary --> Progression["Create Time Progression Chart"]
Progression --> Radar["Create Stroke Radar Chart"]
Radar --> PersonalBests["Fetch Personal Bests"]
PersonalBests --> Render["Render All Visualizations"]
```

**Diagram sources**
- [app.py:226-280](file://app.py#L226-L280)
- [src/analytics.py:172-184](file://src/analytics.py#L172-L184)
- [src/analytics.py:43-60](file://src/analytics.py#L43-L60)
- [src/analytics.py:91-112](file://src/analytics.py#L91-L112)
- [src/analytics.py:115-138](file://src/analytics.py#L115-L138)

**Section sources**
- [app.py:226-280](file://app.py#L226-L280)
- [src/analytics.py:172-184](file://src/analytics.py#L172-L184)

### Research Page
The Research page enables benchmark comparison and performance analysis:

```mermaid
sequenceDiagram
participant User as "User"
participant Research as "Research Page"
participant RS as "ResearchService"
participant DDG as "DuckDuckGo Search"
participant Cache as "Research Cache"
User->>Research : Select Stroke/Distance/Age
Research->>RS : search_benchmarks()
RS->>Cache : Check Cache
alt Cache Hit
Cache-->>RS : Return Cached Results
else Cache Miss
RS->>DDG : Perform Text Search
DDG-->>RS : Search Results
RS->>Cache : Save to Cache
end
RS-->>Research : Benchmark Results
Research-->>User : Display Results + Comparison
```

**Diagram sources**
- [app.py:282-320](file://app.py#L282-L320)
- [src/research_service.py:32-54](file://src/research_service.py#L32-L54)
- [src/research_service.py:56-84](file://src/research_service.py#L56-L84)

**Section sources**
- [app.py:282-320](file://app.py#L282-L320)
- [src/research_service.py:32-54](file://src/research_service.py#L32-L54)
- [src/research_service.py:56-84](file://src/research_service.py#L56-L84)

### Insights Page
The Insights page generates trend analysis and training recommendations:

```mermaid
flowchart TD
LoadData([Load Swim Events]) --> CheckData{"Data Available?"}
CheckData --> |No| ShowInfo["Show Info Message"]
CheckData --> |Yes| Trend["Generate Trend Insights"]
Trend --> Strengths["Identify Strengths/Weaknesses"]
Strengths --> Assessment["Assess Potential"]
Assessment --> Suggestions["Generate Training Suggestions"]
Suggestions --> Render["Render All Insights"]
```

**Diagram sources**
- [app.py:321-370](file://app.py#L321-L370)
- [src/insights.py:14-63](file://src/insights.py#L14-L63)
- [src/insights.py:66-87](file://src/insights.py#L66-L87)
- [src/insights.py:90-111](file://src/insights.py#L90-L111)
- [src/insights.py:122-149](file://src/insights.py#L122-L149)

**Section sources**
- [app.py:321-370](file://app.py#L321-L370)
- [src/insights.py:14-63](file://src/insights.py#L14-L63)
- [src/insights.py:66-87](file://src/insights.py#L66-L87)
- [src/insights.py:90-111](file://src/insights.py#L90-L111)
- [src/insights.py:122-149](file://src/insights.py#L122-L149)

### Q&A Page
The Q&A page provides natural language interaction with swimming data:

```mermaid
sequenceDiagram
participant User as "User"
participant Chat as "Chat Interface"
participant QA as "QAService"
participant DS as "DataStore"
participant PA as "PerformanceAnalytics"
participant API as "Alibaba Cloud API"
User->>Chat : Enter Question
Chat->>Chat : Append to chat_history
Chat->>QA : answer(question)
QA->>DS : Load Swim Events/Metrics
QA->>PA : Get Personal Bests
QA->>API : Call Qwen Text Model
API-->>QA : Generated Answer
QA-->>Chat : Append Assistant Response
Chat-->>User : Display Conversation
```

**Diagram sources**
- [app.py:371-403](file://app.py#L371-L403)
- [src/qa_service.py:76-134](file://src/qa_service.py#L76-L134)
- [src/qa_service.py:23-57](file://src/qa_service.py#L23-57)

**Section sources**
- [app.py:371-403](file://app.py#L371-L403)
- [src/qa_service.py:76-134](file://src/qa_service.py#L76-L134)

### Data Export and Management
The footer provides comprehensive data management capabilities:

```mermaid
flowchart TD
Export["Export All Data"] --> LoadEvents["Load Swim Events"]
LoadEvents --> LoadMetrics["Load Body Metrics"]
LoadMetrics --> LoadScreenshots["Load Screenshot Index"]
LoadScreenshots --> CreateJSON["Create JSON Backup"]
CreateJSON --> Download["Download JSON File"]
Import["Import Backup"] --> UploadFile["Upload JSON File"]
UploadFile --> ParseJSON["Parse JSON Data"]
ParseJSON --> RestoreData["Restore Data to Files"]
RestoreData --> Success["Show Success Message"]
```

**Diagram sources**
- [app.py:405-447](file://app.py#L405-L447)

**Section sources**
- [app.py:405-447](file://app.py#L405-L447)

## Dependency Analysis
The application exhibits clear dependency relationships between modules:

```mermaid
graph TB
APP["app.py"] --> CFG["src/config.py"]
APP --> MOD["src/models.py"]
APP --> ST["src/storage.py"]
APP --> SM["src/screenshot_manager.py"]
APP --> OCR["src/ocr_service.py"]
APP --> VAL["src/validation.py"]
APP --> ANA["src/analytics.py"]
APP --> RES["src/research_service.py"]
APP --> INS["src/insights.py"]
APP --> QA["src/qa_service.py"]
SM --> ST
OCR --> VAL
OCR --> CFG
QA --> CFG
QA --> ST
QA --> ANA
ANA --> ST
ANA --> VAL
RES --> ST
INS --> ST
INS --> ANA
```

**Diagram sources**
- [app.py:10-19](file://app.py#L10-L19)
- [src/screenshot_manager.py:10-11](file://src/screenshot_manager.py#L10-L11)
- [src/ocr_service.py:8-9](file://src/ocr_service.py#L8-L9)
- [src/qa_service.py:6-9](file://src/qa_service.py#L6-L9)
- [src/analytics.py:8-10](file://src/analytics.py#L8-L10)
- [src/research_service.py:6-7](file://src/research_service.py#L6-L7)
- [src/insights.py:5-8](file://src/insights.py#L5-L8)

Key dependency patterns:
- Loose coupling through shared interfaces (DataStore, ScreenshotIndex)
- Clear separation of concerns (UI orchestration vs. business logic)
- External service integration via configuration-driven approach
- Circular dependencies avoided through service composition

**Section sources**
- [app.py:10-19](file://app.py#L10-L19)
- [src/storage.py:10-107](file://src/storage.py#L10-L107)
- [src/screenshot_manager.py:14-15](file://src/screenshot_manager.py#L14-L15)

## Performance Considerations
The application implements several performance optimization strategies:

- Asynchronous Operations: Uses Streamlit spinners during OCR extraction and research searches to maintain UI responsiveness
- Data Caching: Research results cached to reduce API calls and improve response times
- Efficient Data Loading: Lazy loading of dataframes and selective rendering of charts
- Memory Management: Session state cleanup and persistent service instances minimize memory overhead
- Responsive Layout: Adaptive column widths and container-based rendering for optimal screen utilization

Best practices implemented:
- Spinner usage for long-running operations
- Conditional rendering based on data availability
- Efficient chart generation with Plotly
- Minimal re-renders through targeted state updates

## Troubleshooting Guide
Common issues and solutions:

**OCR Extraction Failures:**
- Verify ALIBABA_CLOUD_API_KEY environment variable is set
- Check network connectivity to Alibaba Cloud endpoints
- Review extraction logs in session state for detailed error messages

**Data Import/Export Issues:**
- Ensure JSON backup files contain valid swim_events and body_metrics arrays
- Verify file permissions for data directory access
- Check for corrupted JSON formatting in backup files

**Performance Analytics Errors:**
- Confirm sufficient data points for chart generation
- Validate time format compliance (MM:SS.ss or SS.ss)
- Check stroke/distance combinations have available data

**Research Service Problems:**
- Verify internet connectivity for DuckDuckGo search
- Check cache file permissions and disk space
- Monitor API rate limits and retry mechanisms

**Session State Issues:**
- Use st.session_state.clear() to reset problematic states
- Verify page routing logic for navigation failures
- Check for circular dependencies in callback functions

**Section sources**
- [app.py:83-118](file://app.py#L83-L118)
- [src/ocr_service.py:55-56](file://src/ocr_service.py#L55-L56)
- [src/qa_service.py:87-88](file://src/qa_service.py#L87-L88)
- [src/research_service.py:52-53](file://src/research_service.py#L52-L53)

## Conclusion
The Swimming Data Analysis Platform demonstrates robust Streamlit application architecture with clear separation of concerns and comprehensive service integration. The main application controller effectively orchestrates seven distinct functional areas while maintaining responsive user experience through strategic use of session state, spinners, and modular service design. The platform successfully bridges local data persistence with cloud-based AI services, providing a scalable foundation for swimming performance analysis and insights generation. Future enhancements could include advanced caching strategies, enhanced error recovery mechanisms, and expanded visualization capabilities.