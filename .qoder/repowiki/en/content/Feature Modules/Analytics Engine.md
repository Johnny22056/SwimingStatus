# Analytics Engine

<cite>
**Referenced Files in This Document**
- [app.py](file://app.py)
- [analytics.py](file://src/analytics.py)
- [insights.py](file://src/insights.py)
- [models.py](file://src/models.py)
- [storage.py](file://src/storage.py)
- [validation.py](file://src/validation.py)
- [config.py](file://src/config.py)
- [README.md](file://README.md)
</cite>

## Update Summary
**Changes Made**
- Enhanced chart visualization capabilities with container styling using `.chart-card` CSS class
- Improved benchmark subtitle formatting with cyan color styling (`#06B6D4`)
- Added new Gap to NM column functionality for performance gap calculations against national master standards
- Integrated comprehensive gap analysis in personal best tables for LC and SC course records
- Enhanced benchmark visualization system with real-time gap calculations and nearest target identification

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Core Components](#core-components)
4. [Architecture Overview](#architecture-overview)
5. [Detailed Component Analysis](#detailed-component-analysis)
6. [Advanced Analytics Features](#advanced-analytics-features)
7. [Enhanced Benchmark Visualization System](#enhanced-benchmark-visualization-system)
8. [HTML Report Generation](#html-report-generation)
9. [Performance Optimization](#performance-optimization)
10. [Troubleshooting Guide](#troubleshooting-guide)
11. [Conclusion](#conclusion)
11. [Appendices](#appendices)

## Introduction
This document describes the enhanced analytics engine module responsible for comprehensive swimming performance analysis. The system now provides advanced time progression analysis, stroke comparison methodologies, personal best tracking, time development analysis, HTML report generation with interactive Plotly charts, enhanced benchmark visualization with national/international master standards, comprehensive dashboard summaries, and integrated gap analysis functionality. It covers performance calculation algorithms, visualization creation processes, analytics pipeline from raw data input to visual output, integration with the storage system, and validation layer for data quality assurance.

## Project Structure
The analytics engine is implemented as part of a Streamlit application that ingests swimming meet screenshots, extracts structured race data, stores it locally, and provides interactive analytics, insights, benchmark visualization, gap analysis, and comprehensive reporting capabilities.

```mermaid
graph TB
subgraph "Application Layer"
APP["app.py<br/>Streamlit UI<br/>Enhanced Benchmark Visualization<br/>Gap Analysis"]
END
subgraph "Enhanced Analytics Layer"
PA["analytics.py<br/>PerformanceAnalytics<br/>Enhanced Analytics"]
IG["insights.py<br/>InsightGenerator<br/>Trend Analysis"]
END
subgraph "Data Layer"
ST["storage.py<br/>DataStore, ScreenshotIndex<br/>JSON Persistence"]
VL["validation.py<br/>Validation Utilities<br/>Time Format & Field Validation"]
MD["models.py<br/>SwimEvent, BodyMetrics<br/>Typed Data Structures"]
CFG["config.py<br/>Paths & Config<br/>Time Formats & Paths"]
END
subgraph "Standards Layer"
LC["LC_STANDARDS<br/>Chinese National Standards<br/>LC Course"]
SC["SC_STANDARDS<br/>Chinese National Standards<br/>SC Course"]
END
APP --> PA
APP --> IG
PA --> ST
IG --> ST
PA --> VL
PA --> MD
IG --> MD
ST --> CFG
APP --> LC
APP --> SC
```

**Diagram sources**
- [app.py:18-58](file://app.py#L18-L58)
- [analytics.py:14-315](file://src/analytics.py#L14-L315)
- [insights.py:14-200](file://src/insights.py#L14-L200)
- [storage.py:14-162](file://src/storage.py#L14-L162)
- [validation.py:1-203](file://src/validation.py#L1-L203)
- [models.py:7-55](file://src/models.py#L7-L55)
- [config.py:1-49](file://src/config.py#L1-L49)

**Section sources**
- [README.md:1-66](file://README.md#L1-L66)

## Core Components
- **PerformanceAnalytics**: Enhanced central analytics class providing time progression analysis, stroke comparison, personal bests, time development tracking, HTML report generation, comprehensive dashboard summaries, and gap analysis functionality.
- **InsightGenerator**: Advanced trend analysis generator that identifies performance improvements, weaknesses, and provides training recommendations.
- **DataStore and ScreenshotIndex**: Local JSON-based persistence for swim events, body metrics, and screenshot metadata with robust error handling.
- **Validation utilities**: Comprehensive time format validation, conversions, and required-field checks with detailed error reporting.
- **SwimEvent and BodyMetrics models**: Typed data structures with serialization helpers for analytics and visualization.
- **Chinese National Swimming Standards**: Integrated LC and SC course standards for benchmark visualization, gap analysis, and performance tracking.

**Section sources**
- [analytics.py:14-315](file://src/analytics.py#L14-L315)
- [insights.py:14-200](file://src/insights.py#L14-L200)
- [storage.py:14-162](file://src/storage.py#L14-L162)
- [validation.py:1-203](file://src/validation.py#L1-L203)
- [models.py:7-55](file://src/models.py#L7-L55)
- [app.py:18-58](file://app.py#L18-L58)

## Architecture Overview
The enhanced analytics pipeline begins with screenshot ingestion and OCR extraction, followed by comprehensive validation and persistence. The analytics engine now provides advanced time development analysis, generates interactive HTML reports with Plotly charts, delivers comprehensive insights through trend analysis and performance tracking, integrates Chinese National Swimming Standards for benchmark visualization and gap analysis, and includes enhanced container styling for better presentation.

```mermaid
sequenceDiagram
participant UI as "Streamlit UI (app.py)"
participant Store as "DataStore (storage.py)"
participant Val as "Validation (validation.py)"
participant PA as "PerformanceAnalytics (analytics.py)"
participant IG as "InsightGenerator (insights.py)"
participant LC as "LC_STANDARDS"
participant SC as "SC_STANDARDS"
UI->>Store : Load swim events
UI->>Val : Validate extracted data
UI->>Store : Persist validated events
UI->>PA : Request time development analysis
PA->>Store : Load swim events
PA->>PA : Analyze time progression trends
PA->>UI : Time development insights
UI->>IG : Request trend insights
IG->>Store : Load swim events
IG->>IG : Compute improvement patterns
IG->>UI : Advanced insights list
UI->>LC : Load LC standards
UI->>SC : Load SC standards
UI->>UI : Generate benchmark charts with enhanced subtitles
UI->>PA : Generate HTML report with container styling
PA->>Store : Load swim events
PA->>PA : Create interactive charts with .chart-card styling
PA->>UI : Complete HTML report with enhanced presentation
```

**Diagram sources**
- [app.py:729-991](file://app.py#L729-L991)
- [app.py:995-1105](file://app.py#L995-L1105)
- [storage.py:48-86](file://src/storage.py#L48-L86)
- [validation.py:102-129](file://src/validation.py#L102-L129)
- [analytics.py:66-162](file://src/analytics.py#L66-L162)
- [insights.py:18-90](file://src/insights.py#L18-L90)

## Detailed Component Analysis

### Enhanced PerformanceAnalytics
The PerformanceAnalytics class has been significantly expanded to provide comprehensive swimming performance analysis with advanced features:

**Core Responsibilities:**
- Convert swim events to a DataFrame with normalized time and date
- Filter time progression data by stroke and distance
- Create interactive line charts for time progression with spline interpolation
- Aggregate stroke comparison data and produce radar charts
- Compute personal bests per stroke-distance-course combination
- Analyze time development trends and generate insights
- Generate comprehensive HTML reports with interactive charts and container styling
- Provide dashboard summary statistics

**Advanced Algorithms and Logic:**
- **Time development analysis**: Groups events by stroke-distance combinations and calculates improvement trends over time
- **Performance insights**: Identifies most improved and most consistent stroke-distance combinations using variance analysis
- **HTML report generation**: Creates self-contained HTML documents with embedded Plotly charts, CSS styling, and enhanced container presentation
- **Dashboard summarization**: Provides comprehensive statistics including total meets, events, personal bests, and latest activity

**Visualization Creation:**
- **Interactive time development charts**: Uses Plotly Graph Objects with spline interpolation for smooth curves
- **Course-specific personal best tables**: Separate tables for SC (short course) and LC (long course) records with Gap to NM column
- **Enhanced HTML layout**: Modern CSS styling with container-based responsive design using `.chart-card` class
- **Container styling**: Implements `.chart-card` CSS class for consistent chart presentation with shadow effects and rounded corners

```mermaid
classDiagram
class PerformanceAnalytics {
+get_events_df() DataFrame
+get_personal_bests() DataFrame
+get_time_development_data() Dict
+get_time_development_insights() Dict
+generate_html_report() str
+get_dashboard_summary() Dict
}
class DataStore {
+load_swim_events() SwimEvent[]
+add_swim_event(event) Tuple
+save_swim_events(events) void
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
- [analytics.py:14-315](file://src/analytics.py#L14-L315)
- [storage.py:48-86](file://src/storage.py#L48-L86)
- [validation.py:30-87](file://src/validation.py#L30-L87)
- [models.py:24-29](file://src/models.py#L24-L29)

**Section sources**
- [analytics.py:14-315](file://src/analytics.py#L14-L315)

### Advanced InsightGenerator
The InsightGenerator has been enhanced to provide more sophisticated trend analysis and performance assessment:

**Enhanced Responsibilities:**
- Generate comprehensive trend insights across all stroke-distance-course combinations
- Identify performance strengths and weaknesses through average pace analysis
- Assess swimming potential based on progression trends and stroke development
- Generate prioritized training drill suggestions with stroke-specific recommendations

**Advanced Processing Logic:**
- **Multi-dimensional trend analysis**: Groups events by stroke-distance-course for comprehensive analysis
- **Performance strength assessment**: Calculates average pace per stroke to identify strengths and weaknesses
- **Potential assessment**: Evaluates training trajectory and consistency to provide future development guidance
- **Personalized training recommendations**: Generates stroke-specific drill recommendations based on performance analysis

```mermaid
flowchart TD
Start([Start]) --> LoadEvents["Load swim events"]
LoadEvents --> GroupEvents["Group by (stroke,distance,course)"]
GroupEvents --> SortDates["Sort by date"]
SortDates --> CalcImprovement["Calculate improvement percentages"]
CalcImprovement --> Classify{"Improvement > 5% ?"}
Classify --> |Yes| Positive["Add positive insight"]
Classify --> |No| DeclineCheck{"Improvement < -5% ?"}
DeclineCheck --> |Yes| Warning["Add warning insight"]
DeclineCheck --> |No| Neutral["Add neutral insight"]
Positive --> Strengths["Analyze stroke strengths"]
Warning --> Strengths
Neutral --> Strengths
Strengths --> Potential["Assess potential & trajectory"]
Potential --> Recommendations["Generate training recommendations"]
Recommendations --> End([End])
```

**Diagram sources**
- [insights.py:18-148](file://src/insights.py#L18-L148)

**Section sources**
- [insights.py:14-200](file://src/insights.py#L14-L200)

### Data Models and Storage
The data persistence layer provides robust JSON-based storage with comprehensive error handling and validation:

**Enhanced Data Models:**
- **SwimEvent**: Comprehensive dataclass with serialization helpers and validation support
- **BodyMetrics**: Enhanced with BMI calculation property and comprehensive validation

**Robust Storage Implementation:**
- **JSON-based persistence**: Reliable file-based storage with automatic backup creation
- **Duplicate detection**: Intelligent duplicate event detection using composite key fields
- **Error handling**: Comprehensive exception handling with logging and graceful degradation
- **Atomic operations**: Backup creation before file modifications to prevent data loss

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
+add_swim_event(event) Tuple
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
- [storage.py:14-162](file://src/storage.py#L14-L162)

**Section sources**
- [models.py:7-55](file://src/models.py#L7-L55)
- [storage.py:14-162](file://src/storage.py#L14-L162)

### Validation Layer
The validation system provides comprehensive data quality assurance with detailed error reporting:

**Enhanced Validation Capabilities:**
- **Time format validation**: Supports MM:SS.ss and SS.ss formats with comprehensive regex patterns
- **Field type validation**: Validates data types and constraints for all swim event fields
- **Required field checking**: Ensures all mandatory fields are present and non-empty
- **Split time validation**: Validates individual split times within race data

**Robust Processing Logic:**
- **Multi-format time parsing**: Handles both MM:SS.ss and SS.ss time formats
- **Error accumulation**: Collects multiple validation errors for comprehensive feedback
- **Graceful degradation**: Returns sensible defaults for invalid inputs with detailed logging

```mermaid
flowchart TD
Start([Start]) --> ValidateFormat["Validate time format"]
ValidateFormat --> FormatOK{"Valid format?"}
FormatOK --> |No| ReturnError["Return error"]
FormatOK --> |Yes| ConvertToSeconds["Convert to seconds"]
ConvertToSeconds --> ValidateFields["Validate field types"]
ValidateFields --> FieldsOK{"Valid types?"}
FieldsOK --> |No| ReturnFieldError["Return field errors"]
FieldsOK --> |Yes| ReturnSuccess["Return success"]
ReturnError --> End([End])
ReturnFieldError --> End
ReturnSuccess --> End
```

**Diagram sources**
- [validation.py:11-182](file://src/validation.py#L11-L182)
- [config.py:46-49](file://src/config.py#L46-L49)

**Section sources**
- [validation.py:1-203](file://src/validation.py#L1-L203)
- [config.py:46-49](file://src/config.py#L46-L49)

## Advanced Analytics Features

### Time Development Analysis
The enhanced analytics engine now provides comprehensive time development analysis:

**Key Features:**
- **Grouped analysis**: Groups events by stroke-distance combinations for meaningful trend analysis
- **Statistical insights**: Calculates most improved and most consistent performance patterns
- **Variance analysis**: Uses statistical variance to identify consistent performers
- **Trend categorization**: Classifies trends as improving, declining, or stable based on performance changes

**Processing Algorithm:**
1. Load all swim events from storage
2. Group events by (stroke, distance) combinations
3. Filter groups with more than 2 records for meaningful analysis
4. Calculate improvement from first to last recorded time
5. Compute variance for consistency analysis
6. Categorize trends based on improvement thresholds

**Section sources**
- [analytics.py:66-162](file://src/analytics.py#L66-L162)

### HTML Report Generation
The system now generates comprehensive HTML reports with interactive charts and enhanced container styling:

**Report Features:**
- **Self-contained documents**: HTML files with embedded CSS and Plotly JavaScript
- **Interactive charts**: Plotly charts with hover interactions and responsive design
- **Course-specific sections**: Separate personal best tables for SC and LC course records
- **Enhanced styling**: Modern CSS styling with container-based layout, `.chart-card` class, and improved presentation
- **Container styling**: Implements `.chart-card` CSS class for consistent chart presentation with shadow effects and rounded corners

**Report Structure:**
1. **Header section**: Report title and generation timestamp
2. **Personal best tables**: Separate tables for SC and LC course records with Gap to NM column
3. **Interactive charts**: Time development charts for each stroke-distance combination with enhanced presentation
4. **Responsive layout**: Mobile-friendly design with proper spacing, typography, and container styling

**Section sources**
- [analytics.py:165-295](file://src/analytics.py#L165-L295)

### Dashboard Summary Statistics
Enhanced dashboard provides comprehensive performance overview:

**Summary Metrics:**
- **Total meets**: Number of unique swimming meets attended
- **Total events**: Total number of recorded swimming events
- **Personal bests**: Count of personal best performances achieved
- **Available strokes**: List of all strokes in the dataset
- **Latest event**: Most recent event date for tracking recency

**Section sources**
- [analytics.py:297-315](file://src/analytics.py#L297-L315)

## Enhanced Benchmark Visualization System

### Advanced Chart Presentation System with Container Styling
The analytics engine now provides sophisticated benchmark visualization with enhanced presentation capabilities:

**Key Features:**
- **Container styling**: Implements `.chart-card` CSS class for consistent chart presentation
- **Enhanced container design**: Background color, padding, margin, shadow effects, and rounded corners
- **Improved visual hierarchy**: Better separation between chart sections and content
- **Responsive container layout**: Adapts to different screen sizes while maintaining visual consistency

**Container Styling Implementation:**
- **CSS class definition**: `.chart-card` with background, padding, margin, shadow, and border-radius properties
- **Chart card usage**: Wraps each time development chart in a `.chart-card` container
- **Consistent presentation**: Uniform styling across all benchmark visualization charts
- **Enhanced readability**: Improved contrast and spacing for better chart visibility

**Section sources**
- [analytics.py:272-273](file://src/analytics.py#L272-L273)
- [app.py:1065-1066](file://app.py#L1065-L1066)

### Enhanced Subtitle Formatting with Cyan Coloring
The benchmark visualization system now features improved subtitle formatting with enhanced color coding:

**Key Features:**
- **Cyan color styling**: Uses `#06B6D4` color for benchmark subtitle text
- **Enhanced readability**: Improved contrast and visual appeal for benchmark information
- **Consistent color scheme**: Unified color approach across all benchmark visualizations
- **Professional appearance**: Modern color coding for better user experience

**Subtitle Enhancement Details:**
- **Color specification**: `#06B6D4` (teal/cyan) for benchmark subtitle text
- **Font size adjustment**: `14px` font size for optimal readability
- **HTML styling**: Uses inline styles with `unsafe_allow_html=True` for color application
- **Contextual information**: Displays benchmark standards, gap calculations, and nearest targets

**Section sources**
- [app.py:1131](file://app.py#L1131)

### New Gap to NM Column Functionality
The system now includes comprehensive gap analysis functionality for performance tracking:

**Gap Analysis Features:**
- **Gap to National Master calculation**: Computes performance gap against National Master standards
- **Real-time gap computation**: Dynamic gap calculation based on current PB and standard values
- **Course-specific gap analysis**: Separate gap calculations for LC and SC course records
- **Formatted gap display**: Shows gaps in `±X.XXs` format for easy interpretation

**Gap Calculation Algorithm:**
1. **Event matching**: Matches PB events to corresponding standard entries
2. **Time conversion**: Converts standard and PB times to seconds for calculation
3. **Gap computation**: Calculates difference between PB and National Master standard
4. **Result formatting**: Formats gaps with `±` sign and two decimal places

**Gap Display Implementation:**
- **Column addition**: Adds `"Gap to NM"` column to LC and SC personal best tables
- **Dynamic calculation**: Applies `_compute_gap_to_nm` function to each PB record
- **Standard handling**: Uses appropriate standards source (LC or SC) based on course
- **Formatting**: Displays gaps with sign convention (negative for slower than standard)

**Section sources**
- [app.py:914-927](file://app.py#L914-L927)
- [app.py:933-937](file://app.py#L933-L937)

### Comprehensive Benchmark Visualization Capabilities
The enhanced analytics engine now provides sophisticated benchmark visualization with comprehensive gap analysis:

**Key Features:**
- **Dynamic benchmark reference lines**: Automatic addition of National Master, International Master, and Level 1 standards
- **Gap calculations**: Real-time gap analysis showing improvement needed to reach next standard
- **Color-coded annotations**: Distinct visual indicators for different standard levels
- **Contextual subtitles**: Informative benchmark information displayed with enhanced cyan coloring
- **Course-specific standards**: LC and SC standards integrated for accurate benchmarking
- **Nearest target identification**: Automatic detection of next achievable standard

**Enhanced Benchmark Integration Process:**
1. **Standard selection**: Automatically selects appropriate standards based on course (LC/SC)
2. **Event matching**: Matches swim events to corresponding standard entries
3. **Reference line placement**: Adds horizontal lines at standard times with annotations
4. **Gap computation**: Calculates gaps to nearest unachieved standard
5. **Subtitle generation**: Creates contextual benchmark information with enhanced color formatting
6. **Nearest target detection**: Identifies and displays gap to next achievable standard

**Visual Enhancement Details:**
- **National Master standards**: Green dashed lines with "National Master (运动健将)" annotation
- **International Master standards**: Gold dashed lines with "International Master (国际级健将)" annotation  
- **Level 1 standards**: Cyan dashed lines with "Level 1 (一级)" annotation
- **Enhanced subtitles**: Cyan-colored subtitle with benchmark information and gap details
- **Tick mark enhancement**: Standard times added to Y-axis tick labels with proper formatting

```mermaid
flowchart TD
Start([Chart Rendering]) --> GetStandards["Select standards source<br/>LC or SC"]
GetStandards --> MatchEvent["Match event to standard entry"]
MatchEvent --> HasStandards{"Standard found?"}
HasStandards --> |No| BasicChart["Render basic chart"]
HasStandards --> |Yes| AddRefLines["Add benchmark reference lines"]
AddRefLines --> CalcGaps["Calculate gaps to standards"]
CalcGaps --> GenerateSubtitles["Generate contextual subtitles<br/>with cyan coloring"]
GenerateSubtitles --> EnhanceTicks["Add standard times to ticks"]
EnhanceTicks --> FinalChart["Render enhanced chart with<br/>.chart-card styling"]
BasicChart --> End([Complete])
FinalChart --> End
```

**Diagram sources**
- [app.py:995-1105](file://app.py#L995-L1105)
- [app.py:1131](file://app.py#L1131)

**Section sources**
- [app.py:995-1105](file://app.py#L995-L1105)
- [app.py:18-58](file://app.py#L18-L58)

### Chinese National Swimming Standards Integration
The system integrates comprehensive Chinese National Swimming Standards for accurate benchmarking:

**Standards Coverage:**
- **LC Course Standards**: Long course (25m pool) standards for all major events
- **SC Course Standards**: Short course (23m pool) standards for all major events
- **Multi-level standards**: International Master, National Master, Level 1, and Level 2 benchmarks
- **Event coverage**: Complete coverage of freestyle, backstroke, breaststroke, butterfly, and individual medley events

**Standard Categories:**
- **International Master**: Highest competitive standard (国际级健将)
- **National Master**: National-level standard (运动健将)
- **Level 1**: First-class athlete standard (一级)
- **Level 2**: Second-class athlete standard (二级)

**Section sources**
- [app.py:18-58](file://app.py#L18-L58)

## HTML Report Generation

### Report Architecture
The HTML report generation creates comprehensive, self-contained documents with interactive visualizations and enhanced container styling:

**Technical Implementation:**
- **Plotly integration**: Uses `fig.to_html(include_plotlyjs="cdn")` for interactive chart embedding
- **CSS styling**: Embedded CSS with `.chart-card` class for modern, responsive design
- **Chart customization**: Custom hover templates with formatted time displays
- **Container styling**: Implements `.chart-card` CSS class for consistent chart presentation
- **Layout optimization**: Responsive container design with proper spacing and enhanced visual hierarchy

**Report Components:**
1. **Header section**: Title and generation timestamp
2. **Personal best tables**: Structured tables for SC and LC course records with Gap to NM column
3. **Interactive charts**: Time development plots with spline interpolation and container styling
4. **Enhanced design**: Modern styling with `.chart-card` class, improved typography, and container presentation

**Section sources**
- [analytics.py:165-295](file://src/analytics.py#L165-L295)

## Performance Optimization

### Data Processing Optimizations
The enhanced analytics engine implements several performance optimizations:

**Efficient Data Handling:**
- **Vectorized operations**: Pandas operations for fast data processing
- **Memory optimization**: Efficient DataFrame construction and filtering
- **Caching strategies**: Personal best data caching to avoid recomputation
- **Lazy loading**: On-demand data loading for large datasets

**Visualization Performance:**
- **Minimal data duplication**: Direct customdata passing to traces
- **Optimized chart rendering**: Efficient Plotly chart creation with container styling
- **Responsive sizing**: Appropriate chart dimensions for different screen sizes
- **Container styling optimization**: Efficient CSS class application for chart presentation

**Large Dataset Management:**
- **Filtering optimization**: Early filtering by stroke and distance combinations
- **Pagination support**: UI-level pagination for large event datasets
- **Incremental processing**: Batch processing for large data imports

## Troubleshooting Guide

### Common Issues and Resolutions
**Enhanced Troubleshooting:**
- **Empty analytics output**: Verify swim events persistence and DataStore.load_swim_events returns data
- **HTML report generation failures**: Check Plotly installation and internet connectivity for CDN resources
- **Time development analysis errors**: Ensure sufficient data points (minimum 3) for meaningful trend analysis
- **Performance degradation**: Use categorical filtering and consider data caching strategies
- **Report styling issues**: Verify CSS embedding, `.chart-card` class availability, and responsive design compatibility
- **Benchmark visualization errors**: Check standard data availability, event matching logic, and gap calculation
- **Gap calculation issues**: Verify time format conversion, standard value parsing, and Gap to NM column functionality
- **Container styling problems**: Ensure `.chart-card` CSS class is properly defined and applied

**Advanced Diagnostics:**
- **Data validation errors**: Use comprehensive validation functions to identify field issues
- **Storage corruption**: Check backup files and JSON format integrity
- **Chart rendering problems**: Verify Plotly version compatibility, browser support, and container styling
- **Standard integration issues**: Validate standard data structure, event name matching, and gap calculation logic
- **Gap analysis errors**: Check standard matching algorithm, time conversion accuracy, and result formatting

**Section sources**
- [validation.py:1-203](file://src/validation.py#L1-L203)
- [storage.py:18-45](file://src/storage.py#L18-L45)
- [analytics.py:165-295](file://src/analytics.py#L165-L295)

## Conclusion
The enhanced analytics engine provides a comprehensive foundation for swimming performance analysis, combining advanced time development analysis, interactive HTML reporting with enhanced container styling, sophisticated trend insights, benchmark visualization with Chinese National Swimming Standards, comprehensive gap analysis functionality, and robust data quality assurance. The system now supports comprehensive performance tracking, automated reporting with improved presentation, contextual benchmark analysis with gap calculations, and actionable insights for swimmers and coaches. By leveraging typed models, comprehensive validation utilities, JSON-based persistence with backup capabilities, integrated benchmark standards, and enhanced container styling with `.chart-card` class, it supports scalable growth and reliable data quality while delivering modern, interactive visualizations through Plotly integration with enhanced benchmark capabilities and comprehensive gap analysis.

## Appendices

### Advanced Analytical Queries and Outputs

**Enhanced Time Development Analysis:**
- **Query**: Group events by stroke-distance-course combinations with minimum 3 data points
- **Output**: Statistical insights including most improved, most consistent, and trend classifications
- **Visualizations**: Interactive charts with spline interpolation, container styling, and enhanced presentation

**Benchmark-Enhanced Visualization:**
- **Query**: Generate charts with National Master, International Master, and Level 1 reference lines with gap analysis
- **Output**: Enhanced charts with contextual subtitles showing gap calculations to nearest standards, cyan color formatting, and container styling
- **Features**: Color-coded benchmark lines, gap-to-standard calculations, course-specific standards integration, and improved visual presentation

**Comprehensive HTML Reporting:**
- **Query**: Generate self-contained HTML report with all personal bests, Gap to NM column, and benchmark-enhanced charts
- **Output**: Complete HTML document with embedded CSS, Plotly JavaScript, interactive charts, benchmark information, and enhanced container styling
- **Features**: Responsive design, course-specific tables, modern styling with `.chart-card` class, contextual benchmark subtitles, and gap analysis

**Enhanced Dashboard Summaries:**
- **Query**: Calculate comprehensive performance statistics across all swim events
- **Output**: Summary metrics including total meets, events, personal bests, available strokes, and latest activity
- **Usage**: Real-time performance overview for quick insights

**Advanced Trend Analysis:**
- **Query**: Analyze performance improvements across all stroke-distance-course combinations
- **Output**: Multi-dimensional insights with improvement percentages, trend classifications, and statistical analysis
- **Applications**: Training program evaluation and performance monitoring

**Gap Analysis Functionality:**
- **Query**: Calculate performance gaps against National Master standards for LC and SC course records
- **Output**: Personal best tables with Gap to NM column showing performance gaps in ±XX.XXs format
- **Features**: Real-time gap computation, course-specific analysis, formatted gap display, and standard matching

**Enhanced Container Styling:**
- **Query**: Apply `.chart-card` styling to all benchmark visualization charts
- **Output**: Charts with consistent container styling, shadow effects, rounded corners, and improved presentation
- **Features**: CSS class application, responsive design, visual hierarchy, and professional appearance

**Section sources**
- [analytics.py:66-315](file://src/analytics.py#L66-L315)
- [insights.py:18-200](file://src/insights.py#L18-L200)
- [app.py:995-1105](file://app.py#L995-L1105)
- [app.py:914-927](file://app.py#L914-L927)
- [app.py:272-273](file://app.py#L272-L273)
- [app.py:1131](file://app.py#L1131)