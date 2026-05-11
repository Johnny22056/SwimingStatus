# Data Models

<cite>
**Referenced Files in This Document**
- [models.py](file://src/models.py)
- [validation.py](file://src/validation.py)
- [storage.py](file://src/storage.py)
- [config.py](file://src/config.py)
- [ocr_service.py](file://src/ocr_service.py)
- [app.py](file://app.py)
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
10. [Appendices](#appendices)

## Introduction
This document provides comprehensive data model documentation for the Swimming Data Analysis Platform. It focuses on two primary models:
- SwimEvent: captures race results, timing, splits, and related metadata
- BodyMetrics: captures anthropometric measurements and derived metrics

It explains field definitions, data types, constraints, business rules, validation utilities, type safety mechanisms, serialization patterns for JSON storage and retrieval, and practical examples of instantiation, validation workflows, and data transformation processes. It also outlines data integrity measures and error handling strategies for invalid inputs.

## Project Structure
The data models are implemented in a dedicated module and integrated with validation utilities, a JSON-based storage layer, and application pages that instantiate and persist these models.

```mermaid
graph TB
subgraph "Models"
M1["SwimEvent<br/>src/models.py"]
M2["BodyMetrics<br/>src/models.py"]
end
subgraph "Validation"
V1["validate_time_format<br/>src/validation.py"]
V2["validate_swim_event_data<br/>src/validation.py"]
V3["time_to_seconds<br/>src/validation.py"]
V4["seconds_to_time<br/>src/validation.py"]
end
subgraph "Storage"
S1["DataStore<br/>src/storage.py"]
S2["ScreenshotIndex<br/>src/storage.py"]
end
subgraph "Config"
C1["TIME_FORMAT_MM_SS<br/>src/config.py"]
C2["TIME_FORMAT_SS<br/>src/config.py"]
end
subgraph "App Integration"
A1["OCRService<br/>src/ocr_service.py"]
A2["Streamlit Pages<br/>app.py"]
end
M1 --> S1
M2 --> S1
V2 --> A1
V1 --> V3
V1 --> V4
C1 --> V1
C2 --> V1
A1 --> M1
A2 --> M1
A2 --> M2
```

**Diagram sources**
- [models.py:1-55](file://src/models.py#L1-L55)
- [validation.py:1-103](file://src/validation.py#L1-L103)
- [storage.py:1-107](file://src/storage.py#L1-L107)
- [config.py:26-29](file://src/config.py#L26-L29)
- [ocr_service.py:12-144](file://src/ocr_service.py#L12-L144)
- [app.py:1-447](file://app.py#L1-L447)

**Section sources**
- [README.md:50-57](file://README.md#L50-L57)
- [models.py:1-55](file://src/models.py#L1-L55)
- [storage.py:10-62](file://src/storage.py#L10-L62)
- [validation.py:7-102](file://src/validation.py#L7-L102)
- [config.py:26-29](file://src/config.py#L26-L29)
- [ocr_service.py:49-116](file://src/ocr_service.py#L49-L116)
- [app.py:97-113](file://app.py#L97-L113)

## Core Components
This section documents the SwimEvent and BodyMetrics models, their fields, types, defaults, and business rules.

- SwimEvent
  - Purpose: Represents a single swimming event result with associated metadata.
  - Fields and Types:
    - date: str (ISO format: YYYY-MM-DD)
    - meet_name: str
    - stroke: str (allowed values: freestyle, backstroke, breaststroke, butterfly, IM)
    - distance: int (in meters: 50, 100, 200, 400, 800, 1500)
    - time: str (MM:SS.ss or SS.ss format)
    - splits: List[str] (default: empty list)
    - course: str (default: empty string; allowed values: LC, SC)
    - round: str (default: empty string; allowed values: heat, semifinal, final)
    - rank: int (default: 0)
    - age_group: str (default: empty string)
    - source_screenshot: str (default: empty string; path to source screenshot)
    - heat_lane: str (default: empty string; e.g., "H3 L4")
    - swimmer_name: str (default: "Sunny")
  - Business Rules:
    - Required fields for validation: date, meet_name, stroke, distance, time.
    - time and splits must conform to MM:SS.ss or SS.ss format.
    - course and round are free-text with typical values LC/SC and heat/semifinal/final respectively.
    - rank is numeric; non-positive values are treated as unknown.
    - splits are optional; when present, each must be a valid time string.
  - Serialization:
    - to_dict(): returns a dictionary representation suitable for JSON.
    - from_dict(): constructs a SwimEvent from a dictionary.

- BodyMetrics
  - Purpose: Represents body measurements at a point in time with derived BMI.
  - Fields and Types:
    - date: str (ISO format: YYYY-MM-DD)
    - height_cm: float (default: 0.0)
    - weight_kg: float (default: 0.0)
    - arm_span_cm: float (default: 0.0)
    - notes: str (default: empty string)
  - Computed Property:
    - bmi: float; calculated as weight (kg) / (height (m))^2, rounded to two decimals; returns 0.0 if either height or weight is non-positive.
  - Business Rules:
    - Non-negative numeric values are expected; negative values are treated as missing.
    - BMI is computed only when both height and weight are positive.
  - Serialization:
    - to_dict(): returns a dictionary representation suitable for JSON.
    - from_dict(): constructs a BodyMetrics from a dictionary.

**Section sources**
- [models.py:7-30](file://src/models.py#L7-L30)
- [models.py:32-55](file://src/models.py#L32-L55)
- [README.md:50-57](file://README.md#L50-L57)

## Architecture Overview
The data model layer integrates with validation utilities and a JSON-based storage layer. The application pages orchestrate model instantiation and persistence.

```mermaid
sequenceDiagram
participant UI as "Streamlit UI<br/>app.py"
participant OCR as "OCRService<br/>src/ocr_service.py"
participant VAL as "Validation<br/>src/validation.py"
participant DS as "DataStore<br/>src/storage.py"
participant MOD as "Models<br/>src/models.py"
UI->>OCR : "extract_from_screenshot(image_path)"
OCR->>OCR : "build prompt and call LLM"
OCR-->>UI : "Tuple(success, data, message)"
UI->>VAL : "validate_swim_event_data(data)"
VAL-->>UI : "Tuple(is_valid, errors)"
UI->>MOD : "SwimEvent(...)"
MOD-->>UI : "SwimEvent instance"
UI->>DS : "add_swim_event(event)"
DS->>DS : "load_swim_events()"
DS->>DS : "append(event)"
DS->>DS : "save_swim_events(events)"
DS-->>UI : "None"
```

**Diagram sources**
- [app.py:97-113](file://app.py#L97-L113)
- [ocr_service.py:49-116](file://src/ocr_service.py#L49-L116)
- [validation.py:75-102](file://src/validation.py#L75-L102)
- [storage.py:30-44](file://src/storage.py#L30-L44)
- [models.py:24-29](file://src/models.py#L24-L29)

## Detailed Component Analysis

### SwimEvent Model
- Structure and Relationships
  - SwimEvent is a dataclass with explicit fields and defaults.
  - Provides to_dict() and from_dict() for JSON serialization and deserialization.
  - Used by DataStore for persistence and by UI pages for rendering and analytics.

- Field Definitions and Constraints
  - Required fields validated during ingestion: date, meet_name, stroke, distance, time.
  - Time and splits validated against regex patterns for MM:SS.ss or SS.ss.
  - Optional fields include course, round, rank, age_group, source_screenshot, heat_lane, swimmer_name.

- Type Safety Mechanisms
  - Type hints define expected types for each field.
  - Defaults ensure safe initialization for optional fields.
  - Validation utilities enforce format correctness before persistence.

- Serialization Patterns
  - JSON storage uses list of dictionaries; each SwimEvent is serialized via to_dict().
  - Deserialization uses from_dict() to reconstruct instances.

- Example Instantiation and Workflows
  - From OCR extraction: UI constructs SwimEvent from extracted data and persists via DataStore.
  - Manual entry: UI collects inputs and creates SwimEvent, then saves.

- Data Transformation
  - Time normalization: time_to_seconds() converts MM:SS.ss or SS.ss to seconds for analytics.
  - Reverse conversion: seconds_to_time() formats seconds back to displayable time strings.

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
class DataStore {
+load_swim_events() SwimEvent[]
+save_swim_events(events) void
+add_swim_event(event) void
}
class Validation {
+validate_swim_event_data(data) Tuple
+validate_time_format(time_str) Tuple
+time_to_seconds(time_str) float
+seconds_to_time(seconds) string
}
SwimEvent --> DataStore : "serialized via to_dict()/from_dict()"
Validation --> SwimEvent : "validates fields"
```

**Diagram sources**
- [models.py:7-30](file://src/models.py#L7-L30)
- [storage.py:30-44](file://src/storage.py#L30-L44)
- [validation.py:75-102](file://src/validation.py#L75-L102)

**Section sources**
- [models.py:7-30](file://src/models.py#L7-L30)
- [validation.py:7-24](file://src/validation.py#L7-L24)
- [validation.py:26-60](file://src/validation.py#L26-L60)
- [validation.py:75-102](file://src/validation.py#L75-L102)
- [storage.py:30-44](file://src/storage.py#L30-L44)
- [app.py:97-113](file://app.py#L97-L113)

### BodyMetrics Model
- Structure and Relationships
  - BodyMetrics is a dataclass capturing anthropometric measurements.
  - Provides to_dict() and from_dict() for JSON serialization and deserialization.
  - Computed property bmi returns a derived metric based on height and weight.

- Field Definitions and Constraints
  - date: ISO date string.
  - height_cm, weight_kg, arm_span_cm: numeric values; defaults to zero.
  - notes: optional textual notes.
  - BMI computation requires positive height and weight; otherwise returns 0.0.

- Type Safety Mechanisms
  - Type hints ensure numeric types for height, weight, and arm span.
  - Defaults prevent uninitialized values.
  - BMI property guards against division by zero and invalid inputs.

- Serialization Patterns
  - Stored as list of dictionaries; BodyMetrics serialized via to_dict().
  - Deserialized via from_dict().

- Example Instantiation and Workflows
  - UI collects height, weight, arm span, and notes; constructs BodyMetrics and persists.

- Data Transformation
  - BMI is computed on demand; no persistent derived field is stored.

```mermaid
classDiagram
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
+load_body_metrics() BodyMetrics[]
+save_body_metrics(metrics) void
+add_body_metric(metric) void
}
BodyMetrics --> DataStore : "serialized via to_dict()/from_dict()"
```

**Diagram sources**
- [models.py:32-55](file://src/models.py#L32-L55)
- [storage.py:47-61](file://src/storage.py#L47-L61)

**Section sources**
- [models.py:32-55](file://src/models.py#L32-L55)
- [storage.py:47-61](file://src/storage.py#L47-L61)
- [app.py:185-194](file://app.py#L185-L194)

### Validation Utilities
- Time Format Validation
  - validate_time_format(): checks MM:SS.ss or SS.ss using regex patterns defined in config.
  - Returns a tuple of (is_valid, error_message).

- Numeric and Structural Validation
  - validate_swim_event_data(): ensures required fields are present and non-empty, validates time and splits.
  - Returns a tuple of (is_valid, error_messages).

- Conversion Utilities
  - time_to_seconds(): converts time string to total seconds.
  - seconds_to_time(): converts seconds to time string in MM:SS.ss or SS.ss.

- Integration
  - OCRService uses validate_swim_event_data() to validate extracted data.
  - UI pages rely on these utilities for robust ingestion.

```mermaid
flowchart TD
Start(["Validate Swim Event Data"]) --> CheckRequired["Check Required Fields"]
CheckRequired --> RequiredOK{"All Present?"}
RequiredOK --> |No| CollectMissing["Collect Missing Fields"]
RequiredOK --> |Yes| ValidateTime["Validate Time Format"]
ValidateTime --> TimeOK{"Valid?"}
TimeOK --> |No| AppendTimeError["Append Time Error"]
TimeOK --> |Yes| ValidateSplits["Validate Each Split"]
ValidateSplits --> SplitsOK{"All Valid?"}
SplitsOK --> |No| AppendSplitErrors["Append Split Errors"]
SplitsOK --> |Yes| Success["Return Success"]
AppendSplitErrors --> Success
AppendTimeError --> Success
CollectMissing --> Success
Success --> End(["Done"])
```

**Diagram sources**
- [validation.py:75-102](file://src/validation.py#L75-L102)
- [config.py:26-29](file://src/config.py#L26-L29)

**Section sources**
- [validation.py:7-24](file://src/validation.py#L7-L24)
- [validation.py:26-60](file://src/validation.py#L26-L60)
- [validation.py:62-73](file://src/validation.py#L62-L73)
- [validation.py:75-102](file://src/validation.py#L75-L102)
- [config.py:26-29](file://src/config.py#L26-L29)
- [ocr_service.py:107](file://src/ocr_service.py#L107)

### Storage Layer
- DataStore
  - Loads and saves SwimEvent and BodyMetrics collections as JSON arrays.
  - Uses to_dict() for serialization and from_dict() for deserialization.
  - Handles file creation and encoding; gracefully returns empty lists on errors.

- ScreenshotIndex
  - Manages screenshot metadata index as JSON.
  - Supports loading, saving, adding entries, listing, and removal by path.

- Persistence Patterns
  - Files are stored under the data/ directory as defined in config.
  - Ensures parent directories exist before writing.

```mermaid
sequenceDiagram
participant UI as "UI Page<br/>app.py"
participant DS as "DataStore<br/>src/storage.py"
participant FS as "File System<br/>data/*.json"
UI->>DS : "load_swim_events()"
DS->>FS : "open(swim_events.json)"
FS-->>DS : "JSON data or error"
DS-->>UI : "List[SwimEvent]"
UI->>DS : "save_swim_events(events)"
DS->>FS : "write JSON with indent"
FS-->>DS : "OK"
DS-->>UI : "None"
```

**Diagram sources**
- [storage.py:14-28](file://src/storage.py#L14-L28)
- [storage.py:30-44](file://src/storage.py#L30-L44)
- [storage.py:47-61](file://src/storage.py#L47-L61)

**Section sources**
- [storage.py:10-62](file://src/storage.py#L10-L62)
- [storage.py:64-107](file://src/storage.py#L64-L107)
- [config.py:10-14](file://src/config.py#L10-L14)

### Application Integration
- OCR Extraction and Validation
  - OCRService extracts structured data from screenshots and validates it using validate_swim_event_data().
  - Adds extraction confidence and error metadata to the result.

- UI Pages
  - Upload page: constructs SwimEvent from OCR output and persists.
  - Body Metrics page: constructs BodyMetrics from user inputs and persists.
  - Analytics page: loads SwimEvent data for visualization and analysis.
  - Data export/import: serializes/deserializes models for backup/restore.

```mermaid
sequenceDiagram
participant UI as "Upload Page<br/>app.py"
participant OCR as "OCRService<br/>src/ocr_service.py"
participant VAL as "Validation<br/>src/validation.py"
participant DS as "DataStore<br/>src/storage.py"
participant MOD as "SwimEvent<br/>src/models.py"
UI->>OCR : "extract_from_screenshot()"
OCR-->>UI : "Tuple(is_valid, data, message)"
UI->>VAL : "validate_swim_event_data(data)"
VAL-->>UI : "Tuple(is_valid, errors)"
UI->>MOD : "SwimEvent(**data)"
UI->>DS : "add_swim_event(event)"
DS-->>UI : "Success"
```

**Diagram sources**
- [app.py:97-113](file://app.py#L97-L113)
- [ocr_service.py:49-116](file://src/ocr_service.py#L49-L116)
- [validation.py:75-102](file://src/validation.py#L75-L102)
- [storage.py:30-44](file://src/storage.py#L30-L44)
- [models.py:24-29](file://src/models.py#L24-L29)

**Section sources**
- [app.py:97-113](file://app.py#L97-L113)
- [ocr_service.py:49-116](file://src/ocr_service.py#L49-L116)
- [validation.py:75-102](file://src/validation.py#L75-L102)
- [storage.py:30-44](file://src/storage.py#L30-L44)
- [models.py:24-29](file://src/models.py#L24-L29)

## Dependency Analysis
- SwimEvent depends on:
  - dataclasses (asdict) for serialization
  - typing (Optional, List) for type hints
  - datetime.date for type annotation (not used at runtime)
- BodyMetrics depends on:
  - dataclasses (asdict) for serialization
  - typing (Optional) for type hints
- Validation depends on:
  - re for regex patterns
  - config.TIME_FORMAT_MM_SS and TIME_FORMAT_SS
- Storage depends on:
  - json for serialization
  - pathlib.Path for file paths
  - models for type-aware serialization
  - config for file paths
- OCRService depends on:
  - validation for data validation
  - config for API settings
- App integrates:
  - models, storage, validation, and OCRService

```mermaid
graph LR
M["models.py"] --> S["storage.py"]
M --> V["validation.py"]
V --> C["config.py"]
O["ocr_service.py"] --> V
O --> C
A["app.py"] --> M
A --> S
A --> O
A --> V
```

**Diagram sources**
- [models.py:1-55](file://src/models.py#L1-L55)
- [validation.py:1-103](file://src/validation.py#L1-L103)
- [storage.py:1-107](file://src/storage.py#L1-L107)
- [config.py:1-29](file://src/config.py#L1-L29)
- [ocr_service.py:1-144](file://src/ocr_service.py#L1-L144)
- [app.py:1-447](file://app.py#L1-L447)

**Section sources**
- [models.py:1-55](file://src/models.py#L1-L55)
- [validation.py:1-103](file://src/validation.py#L1-L103)
- [storage.py:1-107](file://src/storage.py#L1-L107)
- [config.py:1-29](file://src/config.py#L1-L29)
- [ocr_service.py:1-144](file://src/ocr_service.py#L1-L144)
- [app.py:1-447](file://app.py#L1-L447)

## Performance Considerations
- Model instantiation is lightweight due to dataclasses and minimal logic.
- JSON serialization/deserialization is efficient for moderate-sized datasets.
- Regex-based validation is fast; consider caching compiled patterns if validating large batches.
- Time conversions are constant-time operations.
- Storage operations are I/O bound; batch writes when adding many records.

## Troubleshooting Guide
- Invalid time format
  - Symptom: Validation fails with time-related error messages.
  - Cause: time or splits not matching MM:SS.ss or SS.ss.
  - Resolution: Ensure inputs conform to expected formats; use seconds_to_time() for display.

- Missing required fields
  - Symptom: Validation reports missing required fields.
  - Cause: date, meet_name, stroke, distance, or time absent.
  - Resolution: Provide all required fields; ensure OCR extraction succeeded.

- Non-positive height/weight
  - Symptom: BMI equals 0.0.
  - Cause: height_cm or weight_kg non-positive.
  - Resolution: Enter positive values for height and weight.

- JSON decode errors
  - Symptom: Storage load returns empty list or errors.
  - Cause: corrupted or malformed JSON.
  - Resolution: Verify file integrity; re-export/import data.

- API key issues
  - Symptom: OCR extraction fails due to missing API key.
  - Cause: ALIBABA_CLOUD_API_KEY not set.
  - Resolution: Set environment variable before running the app.

**Section sources**
- [validation.py:7-24](file://src/validation.py#L7-L24)
- [validation.py:62-73](file://src/validation.py#L62-L73)
- [validation.py:75-102](file://src/validation.py#L75-L102)
- [models.py:48-55](file://src/models.py#L48-L55)
- [storage.py:14-28](file://src/storage.py#L14-L28)
- [ocr_service.py:55-119](file://src/ocr_service.py#L55-L119)
- [app.py:442-447](file://app.py#L442-L447)

## Conclusion
The data models for the Swimming Data Analysis Platform are designed around simplicity, type safety, and robust validation. SwimEvent captures race results and metadata with strong validation rules, while BodyMetrics tracks anthropometric data with computed BMI. The integration with validation utilities, JSON-based storage, and Streamlit UI ensures reliable ingestion, persistence, and analysis of swimming performance data.

## Appendices

### Field Reference Summary
- SwimEvent
  - date: str (ISO date)
  - meet_name: str
  - stroke: str (freestyle, backstroke, breaststroke, butterfly, IM)
  - distance: int (meters)
  - time: str (MM:SS.ss or SS.ss)
  - splits: List[str]
  - course: str (LC/SC)
  - round: str (heat/semifinal/final)
  - rank: int
  - age_group: str
  - source_screenshot: str
  - heat_lane: str
  - swimmer_name: str

- BodyMetrics
  - date: str (ISO date)
  - height_cm: float
  - weight_kg: float
  - arm_span_cm: float
  - notes: str
  - bmi: float (computed)

**Section sources**
- [models.py:7-30](file://src/models.py#L7-L30)
- [models.py:32-55](file://src/models.py#L32-L55)