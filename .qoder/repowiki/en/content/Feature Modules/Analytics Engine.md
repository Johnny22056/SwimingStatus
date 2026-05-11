# Analytics Engine

<cite>
**Referenced Files in This Document**
- [app.py](file://app.py)
- [analytics.py](file://src/analytics.py)
- [models.py](file://src/models.py)
- [storage.py](file://src/storage.py)
- [validation.py](file://src/validation.py)
- [config.py](file://src/config.py)
- [insights.py](file://src/insights.py)
- [research_service.py](file://src/research_service.py)
- [README.md](file://README.md)
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
This document describes the analytics engine module responsible for swimming performance analysis. It covers performance calculation algorithms (time progression analysis, stroke comparison methodologies, and personal best tracking), visualization creation with Plotly (chart types, interactive features, and data formatting), the analytics pipeline from raw data input to visual output (filtering, statistical calculations, and trend identification), integration with the storage system for data retrieval, and the validation layer for data quality assurance. It also includes examples of common analytical queries, visualization outputs, performance metrics, and performance optimization strategies for large datasets and caching.

## Project Structure
The analytics engine is implemented as part of a Streamlit application that ingests swimming meet screenshots, extracts structured race data, stores it locally, and provides interactive analytics and insights.

```mermaid
graph TB
subgraph "Application Layer"
APP["app.py<br/>Streamlit UI"]
end
subgraph "Analytics Layer"
PA["analytics.py<br/>PerformanceAnalytics"]
IG["insights.py<br/>InsightGenerator"]
RS["research_service.py<br/>ResearchService"]
end
subgraph "Data Layer"
ST["storage.py<br/>DataStore, ScreenshotIndex"]
VL["validation.py<br/>Validation Utilities"]
MD["models.py<br/>SwimEvent, BodyMetrics"]
CFG["config.py<br/>Paths & Config"]
end
APP --> PA
APP --> IG
APP --> RS
PA --> ST
IG --> ST
RS --> ST
PA --> VL
PA --> MD
IG --> MD
RS --> CFG
ST --> CFG
```

**Diagram sources**
- [app.py:1-447](file://app.py#L1-L447)
- [analytics.py:13-184](file://src/analytics.py#L13-L184)
- [insights.py:11-150](file://src/insights.py#L11-L150)
- [research_service.py:10-94](file://src/research_service.py#L10-L94)
- [storage.py:10-107](file://src/storage.py#L10-L107)
- [validation.py:1-103](file://src/validation.py#L1-L103)
- [models.py:7-55](file://src/models.py#L7-L55)
- [config.py:1-29](file://src/config.py#L1-L29)

**Section sources**
- [README.md:1-63](file://README.md#L1-L63)
- [requirements.txt:1-10](file://requirements.txt#L1-L10)

## Core Components
- PerformanceAnalytics: Central analytics class providing time progression, stroke comparison, personal bests, age-adjusted performance, and dashboard summaries.
- InsightGenerator: Generates trend insights, identifies strengths/weaknesses, and produces training suggestions.
- ResearchService: Searches benchmark resources and caches results for comparison.
- DataStore and ScreenshotIndex: Local JSON-based persistence for swim events, body metrics, and screenshot metadata.
- Validation utilities: Time format validation and conversions, plus required-field checks.
- SwimEvent and BodyMetrics models: Typed data structures for analytics and visualization.

**Section sources**
- [analytics.py:13-184](file://src/analytics.py#L13-L184)
- [insights.py:11-150](file://src/insights.py#L11-L150)
- [research_service.py:10-94](file://src/research_service.py#L10-L94)
- [storage.py:10-107](file://src/storage.py#L10-L107)
- [validation.py:1-103](file://src/validation.py#L1-L103)
- [models.py:7-55](file://src/models.py#L7-L55)

## Architecture Overview
The analytics pipeline begins with screenshot ingestion and OCR extraction, followed by validation and persistence. The analytics engine loads data, performs calculations, and renders visualizations via Plotly. Insights and research comparison augment the analytics with contextual trends and benchmarks.

```mermaid
sequenceDiagram
participant UI as "Streamlit UI (app.py)"
participant Store as "DataStore (storage.py)"
participant Val as "Validation (validation.py)"
participant PA as "PerformanceAnalytics (analytics.py)"
participant IG as "InsightGenerator (insights.py)"
participant RS as "ResearchService (research_service.py)"
UI->>Store : Load swim events
UI->>Val : Validate extracted data
UI->>Store : Persist validated events
UI->>PA : Request time progression chart
PA->>Store : Load swim events
PA->>PA : Filter by stroke/distance
PA->>UI : Plotly figure (line chart)
UI->>IG : Request trend insights
IG->>Store : Load swim events
IG->>IG : Compute improvements per event key
IG->>UI : Insights list
UI->>RS : Request benchmark comparison
RS->>PA : Load personal bests
RS->>RS : Search cached benchmarks
RS->>UI : Benchmark comparison results
```

**Diagram sources**
- [app.py:60-280](file://app.py#L60-L280)
- [storage.py:30-62](file://src/storage.py#L30-L62)
- [validation.py:75-103](file://src/validation.py#L75-L103)
- [analytics.py:30-184](file://src/analytics.py#L30-L184)
- [insights.py:14-120](file://src/insights.py#L14-L120)
- [research_service.py:31-84](file://src/research_service.py#L31-L84)

## Detailed Component Analysis

### PerformanceAnalytics
Responsibilities:
- Convert swim events to a DataFrame with normalized time and date.
- Filter time progression data by stroke and distance.
- Create interactive line charts for time progression.
- Aggregate stroke comparison data and produce radar charts.
- Compute personal bests per stroke-distance-course combination.
- Calculate age-adjusted performance metrics by computing improvement rates across grouped event keys.
- Provide dashboard summary statistics.

Key algorithms and logic:
- Time progression filtering: Applies stroke and distance filters and sorts by date.
- Stroke comparison normalization: Uses inverse ratio of average time to compute scores, enabling “higher is better” interpretation.
- Personal best tracking: Iterates events and keeps the minimal time per (stroke, distance, course) tuple, preserving associated metadata.
- Age-adjusted performance: Groups by event_key constructed from stroke, distance, and course; computes improvement percentage between first and last times.

Visualization creation:
- Line chart: Uses Plotly Express line chart with markers and reversed y-axis to show faster times at the top. Hover template displays formatted time strings.
- Radar chart: Uses Plotly Graph Objects Scatterpolar with cyclic theta and fill toself for a radar-like visualization.

```mermaid
classDiagram
class PerformanceAnalytics {
+get_events_df() DataFrame
+get_time_progression(stroke, distance) DataFrame
+create_time_progression_chart(stroke, distance) Figure
+get_stroke_comparison_data() DataFrame
+create_stroke_radar_chart() Figure
+get_personal_bests() DataFrame
+get_age_adjusted_performance() DataFrame
+get_dashboard_summary() Dict
}
class DataStore {
+load_swim_events() SwimEvent[]
+add_swim_event(event) void
}
class SwimEvent {
+to_dict() dict
+from_dict(data) SwimEvent
}
class Validation {
+validate_time_format(time_str) Tuple
+time_to_seconds(time_str) float
+seconds_to_time(total_seconds) str
+validate_swim_event_data(data) Tuple
}
PerformanceAnalytics --> DataStore : "loads events"
PerformanceAnalytics --> Validation : "converts time"
PerformanceAnalytics --> SwimEvent : "iterates"
```

**Diagram sources**
- [analytics.py:13-184](file://src/analytics.py#L13-L184)
- [storage.py:30-44](file://src/storage.py#L30-L44)
- [validation.py:26-103](file://src/validation.py#L26-L103)
- [models.py:24-29](file://src/models.py#L24-L29)

**Section sources**
- [analytics.py:16-184](file://src/analytics.py#L16-L184)

### InsightGenerator
Responsibilities:
- Generate trend insights by grouping events by stroke-distance-course and computing improvement percentages between first and last times.
- Identify strengths and weaknesses by computing average pace per stroke (time per meter).
- Assess potential based on trend counts, consistency, and strengths.
- Provide training suggestions tailored to the weakest stroke and general drills.

Processing logic:
- Trend insights: Threshold-based classification (>5% improvement, <-5% decline, neutral).
- Strengths/weaknesses: Average pace per stroke computed from total time divided by distance; lower pace indicates stronger performance.
- Potential assessment: Aggregates counts and generates trajectory and recommendation.
- Training suggestions: Provides drills per stroke and general recommendations.

```mermaid
flowchart TD
Start([Start]) --> LoadEvents["Load swim events"]
LoadEvents --> GroupEvents["Group by (stroke,distance,course)"]
GroupEvents --> SortDates["Sort by date"]
SortDates --> ComputeFirstLast["Compute first and last times"]
ComputeFirstLast --> CalcImprovement["Calculate improvement (%)"]
CalcImprovement --> Classify{"Improvement > 5% ?"}
Classify --> |Yes| Positive["Add positive insight"]
Classify --> |No| DeclineCheck{"Improvement < -5% ?"}
DeclineCheck --> |Yes| Warning["Add warning insight"]
DeclineCheck --> |No| Neutral["Add neutral insight"]
Positive --> End([End])
Warning --> End
Neutral --> End
```

**Diagram sources**
- [insights.py:14-63](file://src/insights.py#L14-L63)

**Section sources**
- [insights.py:14-150](file://src/insights.py#L14-L150)

### ResearchService
Responsibilities:
- Search benchmark resources using DuckDuckGo search.
- Cache results to reduce repeated network requests.
- Compare personal best against benchmark results.

Processing logic:
- Search: Constructs a query string and executes DuckDuckGo search; caches results keyed by stroke, distance, age, and gender.
- Comparison: Retrieves personal best from PerformanceAnalytics and pairs it with benchmark results.

```mermaid
sequenceDiagram
participant UI as "UI"
participant RS as "ResearchService"
participant PA as "PerformanceAnalytics"
participant Cache as "Cache File"
participant DDG as "DuckDuckGo"
UI->>RS : search_benchmarks(stroke, distance, age, gender)
RS->>Cache : load_cache()
alt cache miss
RS->>DDG : text(query)
DDG-->>RS : results
RS->>Cache : save_cache(results)
else cache hit
Cache-->>RS : cached results
end
RS-->>UI : benchmark results
UI->>RS : get_comparison(stroke, distance, age, gender)
RS->>PA : get_personal_bests()
PA-->>RS : PB DataFrame
RS-->>UI : comparison with benchmarks
```

**Diagram sources**
- [research_service.py:31-84](file://src/research_service.py#L31-L84)
- [analytics.py:114-139](file://src/analytics.py#L114-L139)

**Section sources**
- [research_service.py:10-94](file://src/research_service.py#L10-L94)

### Data Models and Storage
- SwimEvent: Typed dataclass representing a single race result with date, meet name, stroke, distance, time, splits, course, round, rank, age group, source screenshot, heat/lane, and swimmer name. Includes serialization helpers.
- BodyMetrics: Typed dataclass for body measurements with BMI computation property.
- DataStore: JSON-based persistence for swim events and body metrics; provides load/save/add operations and ensures directories exist.
- ScreenshotIndex: Manages screenshot metadata index with add, list, get, and remove operations.

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
+bmi float
+to_dict() dict
+from_dict(data) BodyMetrics
}
class DataStore {
+load_swim_events() SwimEvent[]
+save_swim_events(events) void
+add_swim_event(event) void
+load_body_metrics() BodyMetrics[]
+save_body_metrics(metrics) void
+add_body_metric(metric) void
}
class ScreenshotIndex {
+load() Dict
+save(index) void
+add(metadata) void
+list_all() Dict[]
+get_by_path(path) Dict
+remove_by_path(path) bool
}
```

**Diagram sources**
- [models.py:7-55](file://src/models.py#L7-L55)
- [storage.py:10-107](file://src/storage.py#L10-L107)

**Section sources**
- [models.py:7-55](file://src/models.py#L7-L55)
- [storage.py:10-107](file://src/storage.py#L10-L107)

### Validation Layer
Responsibilities:
- Validate time format (MM:SS.ss or SS.ss) and required fields.
- Convert between time string and seconds and vice versa.

Processing logic:
- Time format validation uses regex patterns defined in configuration.
- Conversions handle colon-separated minutes:seconds and decimal seconds.

```mermaid
flowchart TD
Start([Start]) --> ValidateFormat["Validate time format"]
ValidateFormat --> FormatOK{"Valid format?"}
FormatOK --> |No| ReturnError["Return error"]
FormatOK --> |Yes| ConvertToSeconds["Convert to seconds"]
ConvertToSeconds --> ReturnSeconds["Return seconds"]
ReturnError --> End([End])
ReturnSeconds --> End
```

**Diagram sources**
- [validation.py:7-60](file://src/validation.py#L7-L60)
- [config.py:26-29](file://src/config.py#L26-L29)

**Section sources**
- [validation.py:1-103](file://src/validation.py#L1-L103)
- [config.py:26-29](file://src/config.py#L26-L29)

### Visualization Creation with Plotly
Chart types and features:
- Time progression line chart:
  - Chart type: Plotly Express line with markers.
  - Interactive features: Hover template shows date and formatted time; y-axis reversed to place faster times at the top.
  - Data formatting: Uses seconds for axis and original time strings for hover.
- Stroke comparison radar chart:
  - Chart type: Plotly Graph Objects Scatterpolar with cyclic theta and fill toself.
  - Normalization: Scores computed as inverse ratio of average time scaled to 0–100; higher is better.
  - Layout: Radial axis range 0–100, no legend, centered title.

```mermaid
sequenceDiagram
participant UI as "UI"
participant PA as "PerformanceAnalytics"
participant PD as "Pandas DataFrame"
participant PX as "Plotly Express"
participant GO as "Plotly Graph Objects"
UI->>PA : create_time_progression_chart(stroke, distance)
PA->>PD : get_time_progression(stroke, distance)
alt DataFrame empty
PA-->>UI : empty Figure
else DataFrame not empty
PA->>PX : px.line(..., markers=True)
PX-->>PA : Figure
PA->>PA : update_layout(yaxis_autorange="reversed", hovertemplate)
PA->>PA : update_traces(customdata=time_strings)
PA-->>UI : Figure
end
UI->>PA : create_stroke_radar_chart()
PA->>PD : get_stroke_comparison_data()
alt DataFrame empty
PA-->>UI : empty Figure
else DataFrame not empty
PA->>GO : go.Figure(Scatterpolar(...))
GO-->>PA : Figure
PA->>PA : update_layout(polar, title)
PA-->>UI : Figure
end
```

**Diagram sources**
- [analytics.py:30-112](file://src/analytics.py#L30-L112)

**Section sources**
- [analytics.py:30-112](file://src/analytics.py#L30-L112)

## Dependency Analysis
External dependencies:
- Streamlit: UI framework for the application.
- Pandas: Data manipulation and aggregation.
- Plotly: Interactive charting library.
- Pillow: Image handling for thumbnails.
- DuckDuckGo Search: Web search for benchmarks.
- OpenAI: Used by other services (not covered here).
- python-dotenv: Environment configuration.

Internal dependencies:
- app.py depends on analytics, insights, research_service, storage, validation, and models.
- analytics.py depends on models, validation, and storage.
- insights.py depends on models, validation, and storage.
- research_service.py depends on config and storage.
- storage.py depends on config and models.

```mermaid
graph LR
APP["app.py"] --> PA["analytics.py"]
APP --> IG["insights.py"]
APP --> RS["research_service.py"]
PA --> ST["storage.py"]
IG --> ST
RS --> CFG["config.py"]
PA --> VL["validation.py"]
PA --> MD["models.py"]
ST --> CFG
```

**Diagram sources**
- [app.py:10-20](file://app.py#L10-L20)
- [analytics.py:8-10](file://src/analytics.py#L8-L10)
- [insights.py:5-8](file://src/insights.py#L5-L8)
- [research_service.py:6-7](file://src/research_service.py#L6-L7)
- [storage.py:6-7](file://src/storage.py#L6-L7)
- [config.py:1-29](file://src/config.py#L1-L29)

**Section sources**
- [requirements.txt:1-10](file://requirements.txt#L1-L10)
- [app.py:10-20](file://app.py#L10-L20)

## Performance Considerations
- Data loading and filtering:
  - Use DataFrame filtering and sorting efficiently; avoid repeated conversions by precomputing time_seconds and date during DataFrame construction.
  - Cache frequently accessed datasets (e.g., personal bests) to reduce repeated computations.
- Visualization rendering:
  - Minimize data duplication in hover templates; pass customdata arrays directly to traces.
  - Prefer vectorized operations for normalization and scoring.
- Large dataset optimization:
  - Paginate or limit visible data in UI components.
  - Use categorical filtering (stroke, distance) to reduce dataset size before plotting.
- Caching strategies:
  - ResearchService caches benchmark search results keyed by query parameters.
  - Consider adding a lightweight in-memory cache for analytics results (e.g., personal bests, stroke comparison data) to avoid recomputation on rapid UI updates.
- I/O optimization:
  - Batch writes to JSON files; avoid frequent disk writes during bulk operations.
  - Ensure directories exist before writing to prevent exceptions.

[No sources needed since this section provides general guidance]

## Troubleshooting Guide
Common issues and resolutions:
- Empty analytics output:
  - Ensure swim events are persisted and not empty; verify DataStore.load_swim_events returns data.
  - Check that time strings conform to expected formats; use validate_time_format to diagnose.
- No data for selection:
  - Verify that the selected stroke and distance combinations exist in the dataset; filter by available values.
- Benchmark search failures:
  - Confirm internet connectivity and DuckDuckGo availability; inspect cache file permissions.
- Time format errors:
  - Validate time strings using validate_time_format and convert with time_to_seconds; ensure seconds_to_time formatting is consistent.
- Performance degradation:
  - Reduce dataset size by applying filters; consider caching results; avoid unnecessary reruns in Streamlit.

**Section sources**
- [validation.py:7-103](file://src/validation.py#L7-L103)
- [storage.py:14-28](file://src/storage.py#L14-L28)
- [research_service.py:14-53](file://src/research_service.py#L14-L53)

## Conclusion
The analytics engine provides a robust foundation for swimming performance analysis, combining efficient data processing, insightful visualizations, and actionable insights. By leveraging typed models, validation utilities, and JSON-based persistence, it supports scalable growth and reliable data quality. Integrations with research services and trend analysis enhance the platform’s ability to guide training decisions and benchmark progress.

[No sources needed since this section summarizes without analyzing specific files]

## Appendices

### Common Analytical Queries and Outputs
- Time progression:
  - Query: Select a stroke and distance; engine filters events and sorts by date.
  - Output: Line chart with markers; hover shows date and formatted time; faster times appear higher.
- Stroke comparison:
  - Query: Aggregate best times per stroke; normalize scores.
  - Output: Radar chart with cyclic theta and filled area; higher scores indicate better relative performance.
- Personal bests:
  - Query: Minimal time per (stroke, distance, course).
  - Output: Tabular view of best times with associated dates and meets.
- Age-adjusted performance:
  - Query: Group by event_key; compute improvement percentage between first and last times.
  - Output: Summary table with improvement percent, number of races, and event identifiers.
- Trend insights:
  - Query: Group by stroke-distance-course; compute improvement percentiles.
  - Output: Categorized insights (positive, warning, neutral) with messages and data points.
- Research comparison:
  - Query: Retrieve personal best and search benchmarks.
  - Output: Comparison card with personal best, benchmark references, and note about percentile estimation.

**Section sources**
- [analytics.py:30-184](file://src/analytics.py#L30-L184)
- [insights.py:14-150](file://src/insights.py#L14-L150)
- [research_service.py:31-84](file://src/research_service.py#L31-L84)