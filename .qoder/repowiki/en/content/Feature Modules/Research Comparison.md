# Research Comparison

<cite>
**Referenced Files in This Document**
- [research_service.py](file://src/research_service.py)
- [storage.py](file://src/storage.py)
- [models.py](file://src/models.py)
- [validation.py](file://src/validation.py)
- [analytics.py](file://src/analytics.py)
- [config.py](file://src/config.py)
- [app.py](file://app.py)
- [spec.md](file://openspec/changes/sunny-swim-analysis-platform/specs/research-comparison/spec.md)
- [tasks.md](file://openspec/changes/sunny-swim-analysis-platform/tasks.md)
- [requirements.txt](file://requirements.txt)
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
10. [Appendices](#appendices)

## Introduction
This document describes the research comparison module that enables benchmark analysis against age-group standards. It covers the ResearchService class implementation, DuckDuckGo search integration, benchmark data retrieval, and comparison workflows. It also documents the age-group standard lookup system, distance-based comparisons, performance percentile calculations, research caching, integration with the storage system for persistent research data and user preferences, and error handling for search failures and invalid inputs.

## Project Structure
The research comparison feature is implemented primarily in the research service and integrates with analytics, storage, and configuration modules. The Streamlit application exposes a dedicated Research page to drive user interactions.

```mermaid
graph TB
subgraph "Application Layer"
APP["app.py"]
end
subgraph "Research Module"
RS["ResearchService<br/>search_benchmarks(), get_comparison(), add_manual_benchmark_url()"]
CFG["config.py<br/>RESEARCH_CACHE_FILE"]
end
subgraph "Analytics & Storage"
PA["PerformanceAnalytics<br/>get_personal_bests()"]
DS["DataStore<br/>load_swim_events()"]
ST["storage.py"]
MD["models.py"]
VL["validation.py"]
end
subgraph "External"
DDG["DuckDuckGo Search API"]
end
APP --> RS
RS --> CFG
RS --> PA
PA --> DS
DS --> ST
RS --> DDG
```

**Diagram sources**
- [app.py:282-318](file://app.py#L282-L318)
- [research_service.py:10-94](file://src/research_service.py#L10-L94)
- [config.py:14](file://src/config.py#L14)
- [analytics.py:115-138](file://src/analytics.py#L115-L138)
- [storage.py:30-44](file://src/storage.py#L30-L44)
- [models.py:7-29](file://src/models.py#L7-L29)

**Section sources**
- [app.py:282-318](file://app.py#L282-L318)
- [research_service.py:10-94](file://src/research_service.py#L10-L94)
- [config.py:14](file://src/config.py#L14)
- [analytics.py:115-138](file://src/analytics.py#L115-L138)
- [storage.py:30-44](file://src/storage.py#L30-L44)
- [models.py:7-29](file://src/models.py#L7-L29)

## Core Components
- ResearchService: Orchestrates DuckDuckGo search, caches results, and builds comparison payloads using personal bests.
- PerformanceAnalytics: Provides personal bests for stroke-distance-course combinations.
- DataStore: Loads swim events persisted in JSON for analytics.
- Config: Defines cache file path and time format constants.
- Streamlit UI: Exposes controls to select stroke, distance, and age and triggers research actions.

Key responsibilities:
- Search: Generate DuckDuckGo query from stroke, distance, age, and gender; cache results keyed by query signature.
- Comparison: Retrieve personal best for the selected event; combine with benchmark references.
- Caching: Persist cache to a JSON file to avoid repeated external searches.
- Integration: Use analytics to fetch personal bests and storage to persist swim events.

**Section sources**
- [research_service.py:31-84](file://src/research_service.py#L31-L84)
- [analytics.py:115-138](file://src/analytics.py#L115-L138)
- [storage.py:30-44](file://src/storage.py#L30-L44)
- [config.py:14](file://src/config.py#L14)
- [app.py:282-318](file://app.py#L282-L318)

## Architecture Overview
The research comparison workflow connects user input to DuckDuckGo search, caches results, and enriches the response with personal best data.

```mermaid
sequenceDiagram
participant User as "User"
participant UI as "Streamlit Research Page"
participant RS as "ResearchService"
participant DDG as "DuckDuckGo Search"
participant Cache as "Research Cache File"
participant PA as "PerformanceAnalytics"
participant DS as "DataStore"
User->>UI : Select stroke, distance, age
UI->>RS : search_benchmarks(stroke, distance, age)
RS->>Cache : load_cache()
alt Cache hit
Cache-->>RS : cached results
RS-->>UI : results
else Cache miss
RS->>DDG : text(query, max_results=5)
DDG-->>RS : search results
RS->>Cache : save_cache(results)
RS-->>UI : results
end
UI->>RS : get_comparison(stroke, distance, age)
RS->>PA : get_personal_bests()
PA->>DS : load_swim_events()
DS-->>PA : events
PA-->>RS : personal bests
RS-->>UI : comparison payload
```

**Diagram sources**
- [app.py:282-318](file://app.py#L282-L318)
- [research_service.py:31-84](file://src/research_service.py#L31-L84)
- [analytics.py:115-138](file://src/analytics.py#L115-L138)
- [storage.py:30-44](file://src/storage.py#L30-L44)
- [config.py:14](file://src/config.py#L14)

## Detailed Component Analysis

### ResearchService
Responsibilities:
- Load and save research cache from/to a JSON file.
- Search DuckDuckGo for benchmarks using a generated query.
- Compare personal best against benchmark references.
- Support manual benchmark URL addition.

Implementation highlights:
- Cache key: constructed from stroke, distance, age, and gender.
- DuckDuckGo query: combines stroke, distance, age, and gender into a natural-language query.
- Error handling: On DuckDuckGo failure, returns a structured error result.
- Comparison payload: includes personal best, benchmark references, and a note indicating that percentile calculation requires specific benchmark tables.

```mermaid
classDiagram
class ResearchService {
+load_cache() Dict
+save_cache(cache) void
+search_benchmarks(stroke, distance, age, gender) List
+get_comparison(stroke, distance, age, gender) Dict
+add_manual_benchmark_url(url, description) void
}
```

**Diagram sources**
- [research_service.py:10-94](file://src/research_service.py#L10-L94)

**Section sources**
- [research_service.py:14-53](file://src/research_service.py#L14-L53)
- [research_service.py:31-84](file://src/research_service.py#L31-L84)

### DuckDuckGo Search Integration
- Query construction: Uses stroke, distance, age, and gender to form a search query.
- Search execution: Uses the DuckDuckGo SDK to fetch up to five results.
- Result caching: Stores results under a cache key derived from the query signature.

```mermaid
flowchart TD
Start(["search_benchmarks(stroke, distance, age, gender)"]) --> BuildKey["Build cache key from inputs"]
BuildKey --> LoadCache["Load cache file"]
LoadCache --> CacheHit{"Cache hit?"}
CacheHit --> |Yes| ReturnCached["Return cached results"]
CacheHit --> |No| BuildQuery["Build DuckDuckGo query"]
BuildQuery --> DDGS["Execute DDGS.text(query, max_results=5)"]
DDGS --> SaveCache["Save results to cache"]
SaveCache --> ReturnResults["Return results"]
ReturnCached --> End(["Exit"])
ReturnResults --> End
```

**Diagram sources**
- [research_service.py:31-53](file://src/research_service.py#L31-L53)

**Section sources**
- [research_service.py:31-53](file://src/research_service.py#L31-L53)
- [requirements.txt:6](file://requirements.txt#L6)

### Benchmark Data Retrieval and Comparison
- Personal best retrieval: Uses PerformanceAnalytics to fetch the best time for the selected stroke-distance-course combination.
- Comparison payload: Includes stroke, distance, personal best, benchmark references, and a note indicating that percentile calculation requires specific benchmark tables.

```mermaid
sequenceDiagram
participant RS as "ResearchService"
participant PA as "PerformanceAnalytics"
participant DS as "DataStore"
participant DDG as "DuckDuckGo Search"
RS->>PA : get_personal_bests()
PA->>DS : load_swim_events()
DS-->>PA : events
PA-->>RS : personal bests
RS->>DDG : search_benchmarks(...)
DDG-->>RS : benchmark references
RS-->>RS : assemble comparison payload
```

**Diagram sources**
- [research_service.py:55-84](file://src/research_service.py#L55-L84)
- [analytics.py:115-138](file://src/analytics.py#L115-L138)
- [storage.py:30-44](file://src/storage.py#L30-L44)

**Section sources**
- [research_service.py:55-84](file://src/research_service.py#L55-L84)
- [analytics.py:115-138](file://src/analytics.py#L115-L138)
- [storage.py:30-44](file://src/storage.py#L30-L44)

### Age-Group Standard Lookup and Distance-Based Comparisons
- Inputs: stroke, distance, age, and gender.
- Age-group standard lookup: Implemented via DuckDuckGo search with queries tailored to age-group benchmarks.
- Distance-based comparisons: The system selects the personal best for the exact stroke-distance-course combination and compares it against benchmark references.

```mermaid
flowchart TD
Inputs["Inputs: stroke, distance, age, gender"] --> QueryGen["Generate DuckDuckGo query"]
QueryGen --> Search["Search DuckDuckGo"]
Search --> Results["Retrieve benchmark references"]
Results --> PB["Fetch personal best via PerformanceAnalytics"]
PB --> Compare["Assemble comparison payload"]
Compare --> Output["Return comparison results"]
```

**Diagram sources**
- [research_service.py:31-84](file://src/research_service.py#L31-L84)
- [analytics.py:115-138](file://src/analytics.py#L115-L138)

**Section sources**
- [research_service.py:31-84](file://src/research_service.py#L31-L84)
- [analytics.py:115-138](file://src/analytics.py#L115-L138)

### Performance Percentile Calculations
- Current state: The comparison payload includes a note indicating that percentile calculation requires specific benchmark tables.
- Future enhancement: Implement percentile estimation by parsing benchmark tables and computing percentiles relative to age-group distributions.

```mermaid
flowchart TD
Start(["Comparison Payload"]) --> HasTables{"Have benchmark tables?"}
HasTables --> |No| Note["Include note: percentile requires specific tables"]
HasTables --> |Yes| Parse["Parse benchmark tables"]
Parse --> Compute["Compute percentile vs age-group"]
Compute --> Include["Include percentile in payload"]
Note --> End(["Exit"])
Include --> End
```

**Diagram sources**
- [research_service.py:82-84](file://src/research_service.py#L82-L84)

**Section sources**
- [research_service.py:82-84](file://src/research_service.py#L82-L84)

### Research Caching Mechanism
- Cache file: Defined in configuration as a JSON file under the data directory.
- Cache key: Constructed from stroke, distance, age, and gender.
- Persistence: On cache miss, results are saved to the cache file; on subsequent requests, cached results are returned immediately.

```mermaid
flowchart TD
Request["Cache Request"] --> Load["Load cache file"]
Load --> Exists{"Cache exists?"}
Exists --> |No| Init["Initialize empty cache"]
Exists --> |Yes| Use["Use existing cache"]
Init --> Use
Use --> Hit{"Cache hit for key?"}
Hit --> |Yes| Return["Return cached results"]
Hit --> |No| Search["Perform DuckDuckGo search"]
Search --> Save["Save results to cache"]
Save --> Return
```

**Diagram sources**
- [research_service.py:14-29](file://src/research_service.py#L14-L29)
- [config.py:14](file://src/config.py#L14)

**Section sources**
- [research_service.py:14-29](file://src/research_service.py#L14-L29)
- [config.py:14](file://src/config.py#L14)

### Integration with Storage System
- Swim events: Loaded via DataStore to support personal best computation.
- Data models: SwimEvent and BodyMetrics define the persisted structures.
- Validation: Utilities validate time formats and required fields to ensure data quality.

```mermaid
classDiagram
class DataStore {
+load_swim_events() SwimEvent[]
+save_swim_events(events) void
+add_swim_event(event) void
}
class SwimEvent {
+date : string
+meet_name : string
+stroke : string
+distance : int
+time : string
+splits : string[]
+course : string
+round : string
+rank : int
+age_group : string
+source_screenshot : string
+heat_lane : string
+swimmer_name : string
+to_dict() dict
+from_dict(data) SwimEvent
}
class BodyMetrics {
+date : string
+height_cm : float
+weight_kg : float
+arm_span_cm : float
+notes : string
+bmi : float
+to_dict() dict
+from_dict(data) BodyMetrics
}
DataStore --> SwimEvent : "loads"
DataStore --> BodyMetrics : "loads"
```

**Diagram sources**
- [storage.py:30-61](file://src/storage.py#L30-L61)
- [models.py:7-29](file://src/models.py#L7-L29)
- [models.py:32-46](file://src/models.py#L32-L46)

**Section sources**
- [storage.py:30-61](file://src/storage.py#L30-L61)
- [models.py:7-29](file://src/models.py#L7-L29)
- [models.py:32-46](file://src/models.py#L32-L46)

### Streamlit UI Integration
- Controls: Stroke selection, distance selection, and age input.
- Actions: Search benchmarks and display results; show performance vs benchmarks.
- Behavior: Triggers ResearchService methods and renders results in expandable sections.

```mermaid
sequenceDiagram
participant UI as "Streamlit UI"
participant RS as "ResearchService"
UI->>RS : search_benchmarks(stroke, distance, age)
RS-->>UI : results
UI->>RS : get_comparison(stroke, distance, age)
RS-->>UI : comparison payload
```

**Diagram sources**
- [app.py:282-318](file://app.py#L282-L318)
- [research_service.py:31-84](file://src/research_service.py#L31-L84)

**Section sources**
- [app.py:282-318](file://app.py#L282-L318)

## Dependency Analysis
- DuckDuckGo SDK: Used for search functionality.
- Pandas and Plotly: Used by analytics for data manipulation and visualization.
- Streamlit: Drives the UI and page routing.

```mermaid
graph LR
RS["ResearchService"] --> DDG["duckduckgo-search"]
PA["PerformanceAnalytics"] --> PD["pandas"]
PA --> PL["plotly"]
APP["app.py"] --> RS
APP --> PA
```

**Diagram sources**
- [requirements.txt:6](file://requirements.txt#L6)
- [analytics.py:1-11](file://src/analytics.py#L1-L11)
- [app.py:16-19](file://app.py#L16-L19)

**Section sources**
- [requirements.txt:1-10](file://requirements.txt#L1-L10)
- [analytics.py:1-11](file://src/analytics.py#L1-L11)
- [app.py:16-19](file://app.py#L16-L19)

## Performance Considerations
- Caching reduces repeated external API calls and improves responsiveness.
- DuckDuckGo search is limited to a small number of results; results are cached to minimize latency.
- Personal best retrieval depends on stored events; ensure data is persisted to avoid repeated computations.

[No sources needed since this section provides general guidance]

## Troubleshooting Guide
Common issues and resolutions:
- DuckDuckGo search failures: The service returns a structured error result when search fails. Verify network connectivity and DuckDuckGo availability.
- Invalid inputs: Ensure stroke, distance, and age are valid. The UI enforces numeric age bounds.
- No personal best found: If no swim events match the selected stroke-distance-course combination, the comparison returns an error message.
- Cache corruption: If the cache file is malformed, the service falls back to an empty cache and continues operation.

**Section sources**
- [research_service.py:52-53](file://src/research_service.py#L52-L53)
- [research_service.py:67-68](file://src/research_service.py#L67-L68)
- [research_service.py:21-22](file://src/research_service.py#L21-L22)

## Conclusion
The research comparison module integrates DuckDuckGo search with personal best data to deliver benchmark-aware insights. It leverages caching to optimize repeated searches, persists swim events for analytics, and provides a clear UI for exploring performance versus standards. Future enhancements can include explicit percentile calculation by parsing benchmark tables.

[No sources needed since this section summarizes without analyzing specific files]

## Appendices

### Examples of Research Queries
- Freestyle 100m for a 10-year-old female: “freestyle 100m swimming benchmark time age 10 female”
- Backstroke 200m for a 12-year-old male: “backstroke 200m swimming benchmark time age 12 male”

**Section sources**
- [research_service.py:44](file://src/research_service.py#L44)

### Benchmark Comparison Results
- Personal best: Retrieved from personal bests dataset.
- Benchmark references: Up to five DuckDuckGo search results.
- Note: Percentile calculation requires specific benchmark tables.

**Section sources**
- [research_service.py:70-84](file://src/research_service.py#L70-L84)

### Performance Assessment Workflows
- Step 1: Select stroke, distance, and age.
- Step 2: Trigger search to retrieve benchmark references.
- Step 3: Retrieve personal best for the selected event.
- Step 4: Assemble comparison payload and render results.

**Section sources**
- [app.py:282-318](file://app.py#L282-L318)
- [research_service.py:31-84](file://src/research_service.py#L31-L84)

### Research Data Validation and Standardization
- Time format validation: Supports MM:SS.ss and SS.ss formats.
- Required fields: Validates presence of date, meet_name, stroke, distance, and time.
- Split validation: Ensures split times conform to the same format rules.

**Section sources**
- [validation.py:7-23](file://src/validation.py#L7-L23)
- [validation.py:62-102](file://src/validation.py#L62-L102)

### Specification Alignment
- Requirement: Search latest swimming research and benchmarks.
- Requirement: Compare against benchmarks and calculate percentile rankings.
- Requirement: Research caching to avoid repeated searches.

**Section sources**
- [spec.md:3-22](file://openspec/changes/sunny-swim-analysis-platform/specs/research-comparison/spec.md#L3-L22)
- [tasks.md:53-60](file://openspec/changes/sunny-swim-analysis-platform/tasks.md#L53-L60)