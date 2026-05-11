# Configuration Management

<cite>
**Referenced Files in This Document**
- [src/config.py](file://src/config.py)
- [app.py](file://app.py)
- [src/ocr_service.py](file://src/ocr_service.py)
- [src/storage.py](file://src/storage.py)
- [src/screenshot_manager.py](file://src/screenshot_manager.py)
- [src/validation.py](file://src/validation.py)
- [src/research_service.py](file://src/research_service.py)
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
This document describes the configuration management system of the Swimming Data Analysis Platform. It explains how environment variables are loaded, validated, and consumed across the application, including Alibaba Cloud API configuration, path configuration for data directories, and integration with external services. It also covers security considerations for API key management, validation mechanisms, and practical guidance for environment-specific setups.

## Project Structure
The configuration system is centralized in a dedicated module and consumed by services responsible for OCR, storage, research, and screenshot management. The main application integrates configuration visibility for user feedback.

```mermaid
graph TB
Config["src/config.py<br/>Environment variables and paths"]
App["app.py<br/>UI and runtime integration"]
OCR["src/ocr_service.py<br/>Alibaba Cloud client and validation"]
Storage["src/storage.py<br/>JSON persistence paths"]
Screenshots["src/screenshot_manager.py<br/>Screenshot storage paths"]
Research["src/research_service.py<br/>Research cache path"]
Validation["src/validation.py<br/>Time format regex"]
App --> Config
App --> OCR
OCR --> Config
Storage --> Config
Screenshots --> Config
Research --> Config
Validation --> Config
```

**Diagram sources**
- [src/config.py:1-29](file://src/config.py#L1-L29)
- [app.py:10-447](file://app.py#L10-L447)
- [src/ocr_service.py:1-144](file://src/ocr_service.py#L1-L144)
- [src/storage.py:1-107](file://src/storage.py#L1-L107)
- [src/screenshot_manager.py:1-136](file://src/screenshot_manager.py#L1-L136)
- [src/research_service.py:1-93](file://src/research_service.py#L1-L93)
- [src/validation.py:1-103](file://src/validation.py#L1-L103)

**Section sources**
- [src/config.py:1-29](file://src/config.py#L1-L29)
- [app.py:10-447](file://app.py#L10-L447)

## Core Components
- Environment variables and defaults:
  - ALIBABA_CLOUD_API_KEY: API key for Alibaba Cloud Model Studio. Defaults to empty string if not set.
  - ALIBABA_CLOUD_BASE_URL: Base URL for Alibaba Cloud compatible API. Defaults to a known endpoint.
  - QWEN_MODEL_NAME: Vision-language model identifier for OCR. Defaults to a specific model name.
  - QWEN_TEXT_MODEL_NAME: Text model identifier for Q&A. Defaults to a specific model name.
- Path configuration:
  - PROJECT_ROOT: Root directory derived from the configuration module location.
  - DATA_DIR: Local data directory under project root.
  - SCREENSHOTS_DIR: Directory for raw screenshot images.
  - EXTRACTED_DIR: Directory for extracted artifacts.
  - BODY_METRICS_FILE: JSON file storing body metrics.
  - SWIM_EVENTS_FILE: JSON file storing swim events.
  - SCREENSHOT_INDEX_FILE: JSON index of screenshot metadata.
  - RESEARCH_CACHE_FILE: JSON cache for research results.
- Time format regex:
  - TIME_FORMAT_MM_SS: Regex pattern for MM:SS.ss time format.
  - TIME_FORMAT_SS: Regex pattern for SS.ss time format.

These values are loaded via environment variables with sensible defaults and are used across OCR, storage, research, and UI layers.

**Section sources**
- [src/config.py:1-29](file://src/config.py#L1-L29)

## Architecture Overview
The configuration system follows a central initialization pattern:
- Environment variables are read once during module import.
- Paths are computed relative to the project root.
- Services import configuration constants and apply defaults transparently.
- The UI surfaces configuration status to the user.

```mermaid
sequenceDiagram
participant Env as "Environment"
participant Config as "src/config.py"
participant OCR as "src/ocr_service.py"
participant Storage as "src/storage.py"
participant Research as "src/research_service.py"
participant UI as "app.py"
Env-->>Config : "Read env vars"
Config-->>OCR : "Expose constants"
Config-->>Storage : "Expose constants"
Config-->>Research : "Expose constants"
Config-->>UI : "Expose constants"
UI->>UI : "Display API status"
OCR->>OCR : "Validate API key presence"
Storage->>Storage : "Ensure directories exist"
Research->>Research : "Load/save cache"
```

**Diagram sources**
- [src/config.py:1-29](file://src/config.py#L1-L29)
- [src/ocr_service.py:15-56](file://src/ocr_service.py#L15-L56)
- [src/storage.py:14-27](file://src/storage.py#L14-L27)
- [src/research_service.py:14-29](file://src/research_service.py#L14-L29)
- [app.py:441-446](file://app.py#L441-L446)

## Detailed Component Analysis

### Environment Variables and Defaults
- ALIBABA_CLOUD_API_KEY
  - Purpose: Authenticates requests to Alibaba Cloud Model Studio for OCR and Q&A.
  - Default: Empty string.
  - Consumption: Used to initialize the OpenAI-compatible client in OCRService and validated before making requests.
- ALIBABA_CLOUD_BASE_URL
  - Purpose: Specifies the base URL for Alibaba Cloud compatible API.
  - Default: A known compatible endpoint.
  - Consumption: Passed to the OpenAI client initialization.
- QWEN_MODEL_NAME
  - Purpose: Selects the vision-language model for OCR.
  - Default: A specific model name.
  - Consumption: Used by OCRService to specify the model.
- QWEN_TEXT_MODEL_NAME
  - Purpose: Selects the text model for Q&A.
  - Default: A specific model name.
  - Consumption: Used by Q&A services (not shown here) to select the appropriate model.

Validation and error handling:
- If ALIBABA_CLOUD_API_KEY is empty, OCRService returns a clear error indicating the missing configuration.
- The UI checks ALIBABA_CLOUD_API_KEY and displays a status indicator.

**Section sources**
- [src/config.py:20-24](file://src/config.py#L20-L24)
- [src/ocr_service.py:15-21](file://src/ocr_service.py#L15-L21)
- [src/ocr_service.py:55-56](file://src/ocr_service.py#L55-L56)
- [app.py:441-446](file://app.py#L441-L446)

### Path Configuration
- Computed paths:
  - PROJECT_ROOT: Derived from the configuration module’s parent directory.
  - DATA_DIR: Under project root.
  - SCREENSHOTS_DIR: Under data directory for raw images.
  - EXTRACTED_DIR: Under data directory for extracted artifacts.
  - BODY_METRICS_FILE: JSON under data directory.
  - SWIM_EVENTS_FILE: JSON under data directory.
  - SCREENSHOT_INDEX_FILE: JSON index under screenshots directory.
  - RESEARCH_CACHE_FILE: JSON cache under data directory.
- Directory creation:
  - SCREENSHOTS_DIR and EXTRACTED_DIR are ensured to exist at import time.

Usage across modules:
- Storage layer reads/writes JSON files using the configured paths.
- Screenshot manager organizes images under SCREENSHOTS_DIR with meet/date subfolders.
- Research service caches results under RESEARCH_CACHE_FILE.

**Section sources**
- [src/config.py:5-18](file://src/config.py#L5-L18)
- [src/storage.py:14-27](file://src/storage.py#L14-L27)
- [src/screenshot_manager.py:45-47](file://src/screenshot_manager.py#L45-L47)
- [src/research_service.py:14-29](file://src/research_service.py#L14-L29)

### API Endpoint Configuration for Alibaba Cloud
- The OCR service initializes an OpenAI-compatible client with:
  - api_key set to ALIBABA_CLOUD_API_KEY.
  - base_url set to ALIBABA_CLOUD_BASE_URL.
- The service uses QWEN_MODEL_NAME for vision-language OCR requests.
- The UI exposes a quick status indicator for API configuration.

```mermaid
sequenceDiagram
participant UI as "app.py"
participant OCR as "OCRService"
participant OpenAI as "OpenAI Client"
participant Cloud as "Alibaba Cloud API"
UI->>UI : "Check ALIBABA_CLOUD_API_KEY"
OCR->>OpenAI : "Initialize with api_key and base_url"
OCR->>Cloud : "chat.completions.create(model, messages)"
Cloud-->>OCR : "Structured JSON response"
OCR-->>UI : "Validation result and data"
```

**Diagram sources**
- [app.py:441-446](file://app.py#L441-L446)
- [src/ocr_service.py:15-86](file://src/ocr_service.py#L15-L86)
- [src/config.py:21-24](file://src/config.py#L21-L24)

**Section sources**
- [src/ocr_service.py:15-21](file://src/ocr_service.py#L15-L21)
- [src/ocr_service.py:59-86](file://src/ocr_service.py#L59-L86)
- [src/config.py:21-24](file://src/config.py#L21-L24)
- [app.py:441-446](file://app.py#L441-L446)

### Validation Mechanisms
- Time format validation:
  - TIME_FORMAT_MM_SS and TIME_FORMAT_SS are used to validate time strings in validation utilities.
  - The validator converts between time strings and seconds and enforces strict formats.
- OCR data validation:
  - After extracting JSON from OCR, the system validates required fields and time formats.
  - Errors are collected and returned alongside extracted data for transparency.

```mermaid
flowchart TD
Start(["OCR Extraction Complete"]) --> CheckKey["Check ALIBABA_CLOUD_API_KEY present"]
CheckKey --> |Missing| ReturnError["Return error: API key not configured"]
CheckKey --> |Present| ParseJSON["Parse JSON response"]
ParseJSON --> ValidJSON{"JSON parse success?"}
ValidJSON --> |No| ReturnParseError["Return parse error with raw content"]
ValidJSON --> |Yes| ValidateFields["Validate required fields and time formats"]
ValidateFields --> ValidData{"All validations pass?"}
ValidData --> |No| ReturnWithErrors["Return with validation errors"]
ValidData --> |Yes| ReturnSuccess["Return success with extracted data"]
```

**Diagram sources**
- [src/ocr_service.py:55-116](file://src/ocr_service.py#L55-L116)
- [src/validation.py:75-103](file://src/validation.py#L75-L103)
- [src/config.py:26-28](file://src/config.py#L26-L28)

**Section sources**
- [src/validation.py:7-23](file://src/validation.py#L7-L23)
- [src/validation.py:75-103](file://src/validation.py#L75-L103)
- [src/ocr_service.py:106-116](file://src/ocr_service.py#L106-L116)

### Security Considerations for API Key Management
- API keys are loaded from environment variables and should never be hardcoded.
- The UI warns if the key is not set, preventing accidental misuse.
- Recommendations:
  - Store ALIBABA_CLOUD_API_KEY in a secure environment variable provider or secrets manager.
  - Restrict access to deployment environments and CI/CD secrets.
  - Avoid committing secrets to version control; keep .env files out of the repository.
  - Rotate keys periodically and monitor usage.

**Section sources**
- [app.py:441-446](file://app.py#L441-L446)
- [README.md:22-25](file://README.md#L22-L25)

### Configuration Loading Patterns and Defaults
- Centralized import-time loading ensures consistent defaults across modules.
- Defaults are explicit and documented in the configuration module.
- Consumers import constants directly, avoiding duplication and ensuring uniform behavior.

**Section sources**
- [src/config.py:20-24](file://src/config.py#L20-L24)

### Environment-Specific Setups and Examples
- Typical setup:
  - Set ALIBABA_CLOUD_API_KEY to your Alibaba Cloud credential.
  - Optionally override ALIBABA_CLOUD_BASE_URL if using a proxy or alternate endpoint.
  - Optionally override QWEN_MODEL_NAME or QWEN_TEXT_MODEL_NAME for different models.
- Example commands (from project documentation):
  - Export the API key in your shell before running the application.
- Data directories:
  - All data is stored under the data/ directory, including screenshots, JSON datasets, and research cache.

**Section sources**
- [README.md:22-30](file://README.md#L22-L30)
- [src/config.py:5-18](file://src/config.py#L5-L18)

## Dependency Analysis
Configuration dependencies across modules are straightforward and centralized.

```mermaid
graph LR
Config["src/config.py"]
OCR["src/ocr_service.py"]
Storage["src/storage.py"]
Screenshots["src/screenshot_manager.py"]
Research["src/research_service.py"]
Validation["src/validation.py"]
App["app.py"]
Config --> OCR
Config --> Storage
Config --> Screenshots
Config --> Research
Config --> Validation
App --> Config
```

**Diagram sources**
- [src/config.py:1-29](file://src/config.py#L1-L29)
- [src/ocr_service.py:8](file://src/ocr_service.py#L8)
- [src/storage.py:7](file://src/storage.py#L7)
- [src/screenshot_manager.py:10](file://src/screenshot_manager.py#L10)
- [src/research_service.py:6](file://src/research_service.py#L6)
- [src/validation.py:4](file://src/validation.py#L4)
- [app.py:10](file://app.py#L10)

**Section sources**
- [src/config.py:1-29](file://src/config.py#L1-L29)

## Performance Considerations
- Environment variable lookup occurs at import time; this is negligible overhead.
- Path existence checks and JSON serialization are infrequent operations compared to OCR requests.
- Caching research results reduces network overhead for repeated queries.

[No sources needed since this section provides general guidance]

## Troubleshooting Guide
Common configuration issues and resolutions:
- Missing Alibaba Cloud API key:
  - Symptom: OCR extraction fails with a configuration error; UI shows a warning.
  - Resolution: Set ALIBABA_CLOUD_API_KEY in your environment and restart the application.
- Incorrect base URL:
  - Symptom: Network errors when calling the OCR service.
  - Resolution: Verify ALIBABA_CLOUD_BASE_URL points to a valid compatible endpoint.
- Time format errors:
  - Symptom: Validation errors for extracted times.
  - Resolution: Ensure times conform to MM:SS.ss or SS.ss formats.
- Data directory permissions:
  - Symptom: Failures saving JSON or images.
  - Resolution: Ensure write permissions to the data/ directory and its subdirectories.

Debugging techniques:
- Inspect ALIBABA_CLOUD_API_KEY availability in the UI status panel.
- Enable verbose logging in OCRService to capture request/response details.
- Validate time formats using the validation utilities.
- Confirm directory existence and permissions for data paths.

**Section sources**
- [src/ocr_service.py:55-56](file://src/ocr_service.py#L55-L56)
- [src/ocr_service.py:103-104](file://src/ocr_service.py#L103-L104)
- [app.py:441-446](file://app.py#L441-L446)
- [src/validation.py:1-103](file://src/validation.py#L1-L103)

## Conclusion
The configuration management system is intentionally minimal and robust. It centralizes environment variables and path definitions, applies sensible defaults, and exposes clear validation and error handling. By following the recommended security practices and environment-specific setup steps, teams can reliably operate the platform across diverse environments.

[No sources needed since this section summarizes without analyzing specific files]

## Appendices

### Environment Variables Reference
- ALIBABA_CLOUD_API_KEY
  - Type: String
  - Required: Yes (for OCR/Q&A)
  - Default: Empty string
  - Notes: Set via environment variable
- ALIBABA_CLOUD_BASE_URL
  - Type: String
  - Required: No
  - Default: Compatible API endpoint
  - Notes: Override for proxies/endpoints
- QWEN_MODEL_NAME
  - Type: String
  - Required: No
  - Default: Vision-language model identifier
  - Notes: OCR model selection
- QWEN_TEXT_MODEL_NAME
  - Type: String
  - Required: No
  - Default: Text model identifier
  - Notes: Q&A model selection

**Section sources**
- [src/config.py:20-24](file://src/config.py#L20-L24)
- [README.md:22-25](file://README.md#L22-L25)

### Data Directory Layout
- data/
  - body_metrics.json
  - swim_events.json
  - research_cache.json
  - screenshots/
    - index.json
    - Meet Name/
      - YYYY-MM-DD/
        - screenshot.png

**Section sources**
- [src/config.py:10-14](file://src/config.py#L10-L14)
- [src/config.py:16-18](file://src/config.py#L16-L18)
- [src/screenshot_manager.py:45-47](file://src/screenshot_manager.py#L45-L47)