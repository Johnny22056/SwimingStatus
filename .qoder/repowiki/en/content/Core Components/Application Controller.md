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
- [src/insights.py](file://src/insights.py)
- [src/qa_service.py](file://src/qa_service.py)
- [requirements.txt](file://requirements.txt)
- [README.md](file://README.md)
</cite>

## Update Summary
**Changes Made**
- **Enhanced UI Modernization**: Implemented bordered container layouts with `st.container(border=True)` across all major pages
- **KPI Card Design**: Added gradient-styled KPI cards with bordered containers for data visualization
- **Improved Visual Styling**: Enhanced table interactions with bordered containers and improved popup dialogs
- **Course Filter Addition**: Added Course filter to Race Log page for better swim record organization
- **BMI Commentary Panel**: Integrated BMI Commentary panel to Body Metrics page with color-coded health indicators
- **Container-Based Layout**: Migrated from basic containers to bordered container layouts for consistent visual hierarchy

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Core Components](#core-components)
4. [Architecture Overview](#architecture-overview)
5. [Detailed Component Analysis](#detailed-component-analysis)
6. [Dark Theme Implementation](#dark-theme-implementation)
7. [Enhanced Navigation System](#enhanced-navigation-system)
8. [Modernized Page Layouts](#modernized-page-layouts)
9. [Container-Based UI Components](#container-based-ui-components)
10. [Page Routing and Content](#page-routing-and-content)
11. [Dependency Analysis](#dependency-analysis)
12. [Performance Considerations](#performance-considerations)
13. [Troubleshooting Guide](#troubleshooting-guide)
14. [Conclusion](#conclusion)

## Introduction
This document provides comprehensive documentation for the main application controller (app.py) of the Swimming Data Analysis Platform. The controller orchestrates a modern Streamlit-based UI with six main pages: Performance, Data Import, Race Log, Benchmarks, Insights, and AI Coach. The application features a comprehensive dark theme implementation with custom CSS styling, enhanced navigation structure, and modernized visual components including bordered container layouts, KPI card designs, and improved visual styling across multiple pages.

**Updated** Enhanced with modern UI design patterns featuring bordered container layouts, gradient-styled KPI cards, improved visual hierarchy, and specialized panels including Course filters and BMI commentary systems.

## Project Structure
The application follows a modular architecture with a clear separation between UI orchestration (app.py) and domain services located under src/. Key directories and files:
- app.py: Central Streamlit application controller and page router with modernized UI components
- src/: Domain services and utilities
  - config.py: Configuration constants and environment variables
  - models.py: Data models for SwimEvent and BodyMetrics
  - storage.py: File-based persistence layer
  - screenshot_manager.py: Screenshot ingestion and gallery management
  - ocr_service.py: Alibaba Cloud OCR integration
  - validation.py: Data validation utilities
  - analytics.py: Performance analytics and visualizations
  - insights.py: Trend analysis and training suggestions
  - qa_service.py: Natural language Q&A
- requirements.txt: Dependencies
- README.md: Project overview and usage

```mermaid
graph TB
A["app.py<br/>Streamlit Controller<br/>Modernized UI Components"] --> B["src/config.py<br/>Configuration"]
A --> C["src/models.py<br/>Data Models"]
A --> D["src/storage.py<br/>Persistence Layer"]
A --> E["src/screenshot_manager.py<br/>Screenshot Manager"]
A --> F["src/ocr_service.py<br/>OCR Service"]
A --> G["src/validation.py<br/>Validation Utilities"]
A --> H["src/analytics.py<br/>Analytics Engine"]
A --> I["src/insights.py<br/>Insight Generator"]
A --> J["src/qa_service.py<br/>QA Service"]
K["requirements.txt"] --> A
L["README.md"] --> A
```

**Diagram sources**
- [app.py:1-1468](file://app.py#L1-L1468)
- [src/config.py:1-29](file://src/config.py#L1-L29)
- [src/models.py:1-55](file://src/models.py#L1-L55)
- [src/storage.py:1-107](file://src/storage.py#L1-L107)
- [src/screenshot_manager.py:1-136](file://src/screenshot_manager.py#L1-L136)
- [src/ocr_service.py:1-144](file://src/ocr_service.py#L1-L144)
- [src/validation.py:1-103](file://src/validation.py#L1-L103)
- [src/analytics.py:1-315](file://src/analytics.py#L1-L315)
- [src/insights.py:1-150](file://src/insights.py#L1-L150)
- [src/qa_service.py:1-174](file://src/qa_service.py#L1-L174)

**Section sources**
- [app.py:1-1468](file://app.py#L1-L1468)
- [README.md:1-66](file://README.md#L1-L66)

## Core Components
The application controller centers around several key components with modern UI enhancements:

- **Modernized Container System**: Implements bordered container layouts (`st.container(border=True)`) across all major pages for consistent visual hierarchy
- **Enhanced KPI Card Design**: Features gradient-styled KPI cards with bordered containers for dashboard summaries and metrics display
- **Advanced Filter Systems**: Includes Course filter in Race Log page and BMI Commentary panel in Body Metrics page
- **Improved Table Interactions**: Enhanced table styling with bordered containers and popup dialogs for screenshot previews
- **Container-Based Layout**: Migrated from basic containers to bordered container layouts for better visual separation and organization
- **Dark Theme Integration**: Seamless integration of modern UI components with existing dark theme styling
- **Responsive Container Design**: Adaptive container layouts that work across different screen sizes and resolutions

Key implementation patterns:
- Streamlit page routing using session state to control visibility
- Custom CSS styling for dark theme with enhanced container styling
- Bordered container layouts for visual separation and organization
- Gradient-styled KPI cards with consistent design language
- Spinner usage for async operations (OCR extraction, research search)
- Responsive layout using Streamlit columns and bordered containers
- Error handling with user-friendly feedback messages
- Inter-page data sharing via session state variables

**Section sources**
- [app.py:76-150](file://app.py#L76-L150)
- [app.py:152-176](file://app.py#L152-L176)
- [app.py:179-205](file://app.py#L179-L205)
- [app.py:208-1468](file://app.py#L208-L1468)

## Architecture Overview
The application employs a layered architecture with clear separation of concerns and modern UI styling:

```mermaid
graph TB
subgraph "Presentation Layer"
UI["Streamlit UI<br/>Pages: Performance, Data Import,<br/>Race Log, Benchmarks, Insights,<br/>AI Coach<br/>Modernized Container System"]
end
subgraph "Controller Layer"
CTRL["App Controller<br/>Session State<br/>Page Routing<br/>Container-Based UI"]
end
subgraph "Domain Services"
OCR["OCR Service<br/>Alibaba Cloud API"]
QA["QA Service<br/>Alibaba Cloud API"]
ANA["Analytics Engine<br/>Performance Charts<br/>Enhanced PB Management"]
RES["Research Service<br/>Benchmark Search"]
INS["Insight Generator<br/>Trend Analysis"]
END
subgraph "Data Layer"
STORE["DataStore<br/>JSON Persistence"]
IDX["ScreenshotIndex<br/>Metadata Index"]
CFG["Config<br/>Environment Variables"]
END
subgraph "External Services"
ALI["Alibaba Cloud<br/>Model Studio"]
DDG["DuckDuckGo Search<br/>Benchmarks"]
END
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
- [app.py:1-1468](file://app.py#L1-L1468)
- [src/ocr_service.py:12-21](file://src/ocr_service.py#L12-L21)
- [src/qa_service.py:12-22](file://src/qa_service.py#L12-L22)
- [src/analytics.py:13-14](file://src/analytics.py#L13-L14)
- [src/insights.py:11-12](file://src/insights.py#L11-L12)
- [src/storage.py:10-62](file://src/storage.py#L10-L62)
- [src/screenshot_manager.py:14-15](file://src/screenshot_manager.py#L14-L15)
- [src/config.py:1-29](file://src/config.py#L1-29)

## Detailed Component Analysis

### Dark Theme Implementation
The application features a comprehensive dark theme implementation with custom CSS styling:

```mermaid
flowchart TD
Start([App Startup]) --> SetPageConfig["Set Page Config<br/>Wide Layout, Expanded Sidebar"]
SetPageConfig --> HideElements["Hide Streamlit Default Menu<br/>and Deploy Button"]
HideElements --> ApplyCSS["Apply Custom CSS Styling"]
ApplyCSS --> DarkTheme["Dark Theme Styles:<br/>#18181B Background<br/>#27272A Secondary<br/>#06B6D4 Accent"]
DarkTheme --> HoverEffects["Sidebar Button Hover Effects<br/>Blue Accent with Transition"]
HoverEffects --> DataFrameStyles["Enhanced DataFrame Styling<br/>Dark Headers, Hover Effects"]
DataFrameStyles --> ButtonStyles["Custom Button Styling<br/>Gradient Backgrounds<br/>Focus States"]
ButtonStyles --> InputStyles["Input Field Styling<br/>Blue Focus Borders<br/>Box Shadows"]
InputStyles --> ContainerStyles["Container Styling<br/>Bordered Containers<br/>Rounded Corners"]
ContainerStyles --> End([Modern UI Ready])
```

**Diagram sources**
- [app.py:68-74](file://app.py#L68-L74)
- [app.py:76-150](file://app.py#L76-L150)

Key dark theme features:
- **Sidebar Styling**: Custom hover effects with blue accent (#06B6D4) and smooth transitions
- **Button Styling**: Gradient backgrounds (#18181B to #27272A), rounded corners (8px), and focus states
- **DataFrame Enhancement**: Dark headers with uppercase styling, hover effects, and improved borders
- **Input Fields**: Blue focus borders with box shadows and enhanced visual feedback
- **Container Styling**: Bordered containers with rounded corners (12px) and subtle padding (12px)
- **KPI Card Design**: Gradient backgrounds with left-side accent borders and shadow effects

**Section sources**
- [app.py:76-150](file://app.py#L76-L150)

### Enhanced Navigation System
The sidebar implements a structured navigation interface with Analysis and Tools sections:

```mermaid
sequenceDiagram
participant User as "User"
participant Sidebar as "Enhanced Sidebar"
participant AnalysisSection as "Analysis Section"
participant ToolsSection as "Tools Section"
participant Controller as "switch_page()"
participant Streamlit as "st.rerun()"
User->>Sidebar : Click Navigation Button
Sidebar->>AnalysisSection : Handle Analysis Buttons
Sidebar->>ToolsSection : Handle Tools Buttons
AnalysisSection->>Controller : switch_page(page_name)
ToolsSection->>Controller : switch_page(page_name)
Controller->>Controller : Update st.session_state.page
Controller->>Streamlit : st.rerun()
Streamlit-->>User : Re-render Active Page with Modern UI
```

**Diagram sources**
- [app.py:179-205](file://app.py#L179-L205)
- [app.py:174-176](file://app.py#L174-L176)

Navigation structure with Analysis and Tools sections:
- **Analysis Section** (Primary Navigation):
  - Benchmarks (Chinese National Standards)
  - Performance (Analytics Dashboard)
  - Insights (Trend Analysis)
  - AI Coach (Q&A Interface)
- **Tools Section** (Secondary Navigation):
  - Data Import (Screenshot Upload)
  - Race Log (All Swim Records)
  - Body Metrics (Physical Measurements)

**Section sources**
- [app.py:179-205](file://app.py#L179-L205)

### Modernized Page Layouts
The application implements modern container-based layouts with enhanced visual components:

```mermaid
flowchart TD
ModernLayout([Modern Layout System]) --> BorderContainers["Bordered Container System<br/>st.container(border=True)"]
BorderContainers --> KPICards["KPI Card Design<br/>Gradient Backgrounds<br/>Left Accent Borders"]
BorderContainers --> FilterSystems["Advanced Filter Systems<br/>Course Filter<br/>BMI Commentary"]
KPICards --> Dashboard["Dashboard Layout<br/>4-Column KPI Grid"]
FilterSystems --> RaceLog["Enhanced Race Log<br/>Course Filter + Filters"]
FilterSystems --> BodyMetrics["Body Metrics<br/>BMI Commentary Panel"]
Dashboard --> Performance["Performance Analytics<br/>PB Tables + Charts"]
Performance --> ContainerLayout["Container-Based Layout<br/>Consistent Visual Hierarchy"]
```

**Diagram sources**
- [app.py:688-740](file://app.py#L688-L740)
- [app.py:811-851](file://app.py#L811-L851)
- [app.py:861-877](file://app.py#L861-L877)
- [app.py:1411-1419](file://app.py#L1411-L1419)

Key modernization features:
- **Bordered Container System**: Consistent use of `st.container(border=True)` across all major pages
- **KPI Card Design**: Gradient-styled cards with bordered containers for dashboard metrics
- **Advanced Filter Systems**: Course filter in Race Log and BMI commentary panel in Body Metrics
- **Enhanced Table Interactions**: Bordered containers with improved popup dialogs
- **Container-Based Layout**: Organized sections with visual separation and consistent styling

**Section sources**
- [app.py:688-740](file://app.py#L688-L740)
- [app.py:811-851](file://app.py#L811-L851)
- [app.py:861-877](file://app.py#L861-L877)
- [app.py:1411-1419](file://app.py#L1411-L1419)

### Container-Based UI Components
The application extensively uses bordered container layouts for consistent visual organization:

```mermaid
sequenceDiagram
participant Page as "Page Component"
participant Container as "Bordered Container"
participant Content as "UI Content"
participant Styling as "Container Styling"
Page->>Container : Create Container with border=True
Container->>Styling : Apply CSS Styling
Styling->>Container : Background : #18181B<br/>Border : #3F3F46<br/>Radius : 12px<br/>Padding : 12px
Container->>Content : Render Content Inside
Content-->>Page : Display with Modern Styling
```

**Diagram sources**
- [app.py:144-149](file://app.py#L144-L149)

Container styling specifications:
- **Background**: `#18181B` (dark gray background)
- **Border**: `#3F3F46` (medium gray border)
- **Border Radius**: `12px` (rounded corners)
- **Padding**: `12px` (internal spacing)
- **Accent Color**: `#06B6D4` (blue accent for KPI cards)

**Section sources**
- [app.py:144-149](file://app.py#L144-L149)

### Session State Management
The controller initializes essential session state variables with modern UI awareness:

```mermaid
flowchart TD
Start([App Startup]) --> InitPage["Initialize 'page' = 'Performance'"]
InitPage --> InitChat["Initialize 'chat_history' = []"]
InitChat --> InitLast["Initialize 'last_extraction' = None"]
InitLast --> InitQA["Initialize 'qa_service' = QAService()"]
InitQA --> SyncHistory["Sync Conversation History"]
SyncHistory --> InitStats["Initialize Upload Statistics"]
InitStats --> ModernUIReady["Modern UI Ready<br/>Container System Active"]
ModernUIReady --> End([Session Ready])
```

**Diagram sources**
- [app.py:152-171](file://app.py#L152-L171)

Key session state variables:
- page: Current active page identifier (default: "Performance")
- chat_history: Conversation history for AI Coach
- last_extraction: Most recent OCR extraction result
- qa_service: Persistent QA service instance with conversation history sync
- upload_success_count, upload_failed_count, upload_duplicate_count: Import statistics
- upload_new_count: New upload counter

**Section sources**
- [app.py:152-171](file://app.py#L152-L171)

### Page Routing and Content
The application routes to six main pages with modernized content and styling:

#### Data Import Page
Handles screenshot ingestion, OCR extraction, and data validation with enhanced UI:

```mermaid
sequenceDiagram
participant User as "User"
participant ImportPage as "Data Import Page"
participant SM as "ScreenshotManager"
participant OCR as "OCRService"
participant DS as "DataStore"
participant VA as "Validation"
User->>ImportPage : Select File + Enter Details
ImportPage->>SM : save_uploaded_screenshot()
SM-->>ImportPage : Success/Failure + Message
ImportPage->>ImportPage : Show Spinner "Extracting..."
ImportPage->>OCR : extract_from_screenshot()
OCR->>OCR : Encode Image + Call API
OCR-->>ImportPage : Extraction Result + Data
ImportPage->>VA : validate_swim_event_data()
VA-->>ImportPage : Validation Result + Errors
ImportPage->>DS : add_swim_event()
DS-->>ImportPage : Confirmation
ImportPage-->>User : Success/Error Messages with Modern UI
```

**Diagram sources**
- [app.py:208-656](file://app.py#L208-L656)
- [src/screenshot_manager.py:27-82](file://src/screenshot_manager.py#L27-L82)
- [src/ocr_service.py:49-119](file://src/ocr_service.py#L49-L119)
- [src/validation.py:75-103](file://src/validation.py#L75-L103)
- [src/storage.py:40-44](file://src/storage.py#L40-L44)

#### Race Log Page
Provides comprehensive swim records management with enhanced table interactions and Course filter:

```mermaid
flowchart TD
LoadEvents([Load Swim Events]) --> CheckEvents{"Events Available?"}
CheckEvents --> |No| ShowInfo["Show Info Message"]
CheckEvents --> |Yes| CreateDF["Create DataFrame with<br/>Age Calculation"]
CreateDF --> Filters["Apply Stroke/Distance/Meet/Course Filters"]
Filters --> DisplayTable["Display Enhanced Table<br/>with Bordered Container"]
DisplayTable --> RowSelection["Enable Single-Row Selection"]
RowSelection --> ScreenshotPreview["Show Source Screenshot<br/>with Popup Dialog"]
ScreenshotPreview --> DownloadCSV["Download CSV with<br/>Modern Styling"]
```

**Diagram sources**
- [app.py:658-764](file://app.py#L658-L764)

#### Performance Analytics Page
Features comprehensive performance visualization with enhanced Personal Bests interaction and KPI cards:

```mermaid
flowchart TD
LoadEvents([Load Swim Events]) --> CheckEvents{"Events Available?"}
CheckEvents --> |No| ShowInfo["Show Info Message"]
CheckEvents --> |Yes| Summary["Generate Dashboard Summary<br/>with Gradient KPI Cards"]
Summary --> PBTables["Create LC/SC/Other PB Tables<br/>with Bordered Containers"]
PBTables --> RowSelection["Enable Single-Row Selection<br/>with Popup Dialogs"]
RowSelection --> ScreenshotPreview["Automatic Screenshot Preview<br/>in Popup Dialog"]
ScreenshotPreview --> Insights["Generate Performance Insights"]
Insights --> Report["Download HTML Report<br/>with Enhanced Styling"]
```

**Diagram sources**
- [app.py:854-1240](file://app.py#L854-L1240)
- [src/analytics.py:36-65](file://src/analytics.py#L36-L65)
- [src/analytics.py:43-60](file://src/analytics.py#L43-L60)
- [src/analytics.py:91-112](file://src/analytics.py#L91-L112)
- [src/analytics.py:115-138](file://src/analytics.py#L115-L138)

#### Benchmarks Page
Displays Chinese National Swimming Standards with OCR import capability and bordered container styling:

```mermaid
sequenceDiagram
participant User as "User"
participant Benchmarks as "Benchmarks Page"
participant OCR as "OCRService"
participant DDG as "DuckDuckGo Search"
User->>Benchmarks : Select Long/Short Course Tabs
Benchmarks-->>User : Display Standards Tables with Containers
User->>Benchmarks : Upload Standards Screenshot
Benchmarks->>OCR : Extract Standards via OCR
OCR->>OCR : Process Image + Extract JSON
OCR-->>Benchmarks : Return Extracted Standards
Benchmarks-->>User : Display Extracted Results in Containers
```

**Diagram sources**
- [app.py:1242-1343](file://app.py#L1242-L1343)

#### Insights Page
Generates trend analysis and training recommendations with enhanced presentation and KPI cards:

```mermaid
flowchart TD
LoadData([Load Swim Events]) --> CheckData{"Data Available?"}
CheckData --> |No| ShowInfo["Show Info Message"]
CheckData --> |Yes| TrendInsights["Generate Trend Insights<br/>with Bordered Containers"]
TrendInsights --> Strengths["Identify Strengths/Weaknesses<br/>with KPI Cards"]
Strengths --> Assessment["Assess Potential<br/>with Gradient KPI Cards"]
Assessment --> Suggestions["Generate Training Suggestions<br/>with Priority Indicators"]
Suggestions --> Render["Render All Insights<br/>with Modern Container Styling"]
```

**Diagram sources**
- [app.py:1345-1432](file://app.py#L1345-L1432)
- [src/insights.py:14-63](file://src/insights.py#L14-L63)
- [src/insights.py:66-87](file://src/insights.py#L66-L87)
- [src/insights.py:90-111](file://src/insights.py#L90-L111)
- [src/insights.py:122-149](file://src/insights.py#L122-L149)

#### AI Coach Page
Provides natural language interaction with swimming data using enhanced chat interface:

```mermaid
sequenceDiagram
participant User as "User"
participant Chat as "Enhanced Chat Interface"
participant QA as "QAService"
participant DS as "DataStore"
participant PA as "PerformanceAnalytics"
participant API as "Alibaba Cloud API"
User->>Chat : Enter Question
Chat->>Chat : Append to chat_history<br/>with Modern Styling
Chat->>QA : answer(question)
QA->>DS : Load Swim Events/Metrics
QA->>PA : Get Personal Bests
QA->>API : Call Qwen Text Model
API-->>QA : Generated Answer
QA-->>Chat : Append Assistant Response
Chat-->>User : Display Conversation<br/>with Enhanced Styling
```

**Diagram sources**
- [app.py:1434-1466](file://app.py#L1434-L1466)
- [src/qa_service.py:76-134](file://src/qa_service.py#L76-L134)
- [src/qa_service.py:23-57](file://src/qa_service.py#L23-L57)

**Section sources**
- [app.py:208-1468](file://app.py#L208-L1468)

## Dependency Analysis
The application exhibits clear dependency relationships between modules with enhanced styling integration:

```mermaid
graph TB
APP["app.py<br/>Modern UI Controller"] --> CFG["src/config.py"]
APP --> MOD["src/models.py"]
APP --> ST["src/storage.py"]
APP --> SM["src/screenshot_manager.py"]
APP --> OCR["src/ocr_service.py"]
APP --> VAL["src/validation.py"]
APP --> ANA["src/analytics.py"]
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
INS --> ST
INS --> ANA
```

**Diagram sources**
- [app.py:10-19](file://app.py#L10-L19)
- [src/screenshot_manager.py:10-11](file://src/screenshot_manager.py#L10-L11)
- [src/ocr_service.py:8-9](file://src/ocr_service.py#L8-L9)
- [src/qa_service.py:6-9](file://src/qa_service.py#L6-L9)
- [src/analytics.py:8-10](file://src/analytics.py#L8-L10)
- [src/insights.py:5-8](file://src/insights.py#L5-L8)

Key dependency patterns:
- Loose coupling through shared interfaces (DataStore, ScreenshotIndex)
- Clear separation of concerns (UI orchestration vs. business logic)
- External service integration via configuration-driven approach
- Circular dependencies avoided through service composition
- **Enhanced styling integration** through custom CSS and bordered container system

**Section sources**
- [app.py:10-19](file://app.py#L10-L19)
- [src/storage.py:10-107](file://src/storage.py#L10-L107)
- [src/screenshot_manager.py:14-15](file://src/screenshot_manager.py#L14-L15)

## Performance Considerations
The application implements several performance optimization strategies with enhanced UI considerations:

- **Asynchronous Operations**: Uses Streamlit spinners during OCR extraction and research searches to maintain UI responsiveness
- **Data Caching**: Research results cached to reduce API calls and improve response times
- **Efficient Data Loading**: Lazy loading of dataframes and selective rendering of charts with modern container styling
- **Memory Management**: Session state cleanup and persistent service instances minimize memory overhead
- **Responsive Layout**: Adaptive column widths and container-based rendering for optimal screen utilization
- **Optimized Table Rendering**: Single-row selection mode reduces unnecessary re-renders and improves table interaction performance
- **Dark Theme Performance**: Custom CSS applied once at startup, minimizing runtime styling overhead
- **Container System Optimization**: Bordered container layouts designed for efficient rendering and minimal overhead
- **Enhanced Visual Feedback**: Smooth transitions and hover effects optimized for modern browsers

Best practices implemented:
- Spinner usage for long-running operations
- Conditional rendering based on data availability
- Efficient chart generation with Plotly and modern container styling
- Minimal re-renders through targeted state updates
- **Smart screenshot path resolution** to minimize file system operations
- **Custom CSS optimization** for reduced styling overhead
- **Container-based layout optimization** for consistent performance across different screen sizes

## Troubleshooting Guide
Common issues and solutions with modern UI considerations:

**Modern UI Issues:**
- Verify bordered container styling is properly applied with `st.container(border=True)`
- Check container radius and padding settings for consistent visual appearance
- Ensure gradient KPI cards render correctly across different browsers
- Verify container styling compatibility with Streamlit version

**Navigation Problems:**
- Confirm Analysis and Tools section buttons are properly configured
- Verify page routing logic for new page names (Performance, Data Import, etc.)
- Check for circular dependencies in callback functions
- Ensure session state synchronization for all pages

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

**Enhanced Table Interaction Issues:**
- Verify selection_mode="single-row" and on_select="rerun" parameters are correctly configured
- Check that screenshot paths are properly stored in source_screenshot field
- Ensure three path resolution strategies have appropriate fallback order
- Verify popup dialog functionality works with modern container styling

**Screenshot Preview Problems:**
- Verify screenshot files exist at the resolved path locations
- Check file permissions for screenshot directory access
- Ensure SCREENSHOTS_DIR configuration points to correct location

**Container System Issues:**
- Verify bordered container syntax: `st.container(border=True)`
- Check container styling CSS is properly loaded
- Ensure container radius and padding settings are consistent
- Verify container styling compatibility with Streamlit version

**KPI Card Display Problems:**
- Check gradient background CSS syntax
- Verify left accent border styling
- Ensure container padding is sufficient for card content
- Check color contrast for accessibility compliance

**Section sources**
- [app.py:183-236](file://app.py#L183-L236)
- [src/ocr_service.py:55-56](file://src/ocr_service.py#L55-L56)
- [src/qa_service.py:87-88](file://src/qa_service.py#L87-L88)
- [src/research_service.py:52-53](file://src/research_service.py#L52-L53)

## Conclusion
The Swimming Data Analysis Platform demonstrates robust Streamlit application architecture with comprehensive modern UI enhancements and container-based design patterns. The main application controller effectively orchestrates six distinct functional areas organized into Analysis and Tools sections while maintaining responsive user experience through strategic use of session state, spinners, and modular service design.

**Updated** The recent enhancements significantly modernize the user interface with comprehensive bordered container layouts, gradient-styled KPI cards, and improved visual styling across multiple pages. The addition of Course filter to Race Log page and BMI Commentary panel to Body Metrics page provides enhanced functionality and specialized analysis capabilities. The migration from basic containers to bordered container layouts creates a consistent visual hierarchy that improves user experience and data organization.

The platform successfully bridges local data persistence with cloud-based AI services, providing a scalable foundation for swimming performance analysis and insights generation. The container-based UI system ensures consistent visual presentation across different screen sizes and resolutions, while the modern styling enhances readability and user engagement.

The dark theme implementation combined with bordered containers and gradient KPI cards creates a professional, data-driven interface that supports both casual users and serious swimmers seeking detailed performance analysis. The structured navigation with Analysis and Tools sections, enhanced with modern container styling, provides a logical workflow for users from data ingestion to performance analysis and AI-powered insights.

Future enhancements could include advanced container animation effects, expanded visualization capabilities for performance trends and comparisons, additional customization options for the container styling system, and enhanced accessibility features for container-based UI components.