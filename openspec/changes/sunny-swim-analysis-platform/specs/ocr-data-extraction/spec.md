## ADDED Requirements

### Requirement: OCR extracts comprehensive structured swimming data from screenshots
The system SHALL use Alibaba Cloud Model Studio Service to extract comprehensive structured data including event name, stroke type, distance, total time, split times, course, round, rank, date, meet name, heat/lane information, and swimmer names from screenshots.

#### Scenario: Extract data from meet result screenshot
- **WHEN** a screenshot contains tabular meet results
- **THEN** the system extracts event names, swimmer names, total times, split times, course, round, rank, heat/lane info, and meet details into structured JSON

#### Scenario: Extract split times from detailed results
- **WHEN** a screenshot contains detailed results with per-lap or per-50m split times
- **THEN** the system extracts all split times and associates them with the corresponding event and total time

#### Scenario: Handle unsupported screenshot format
- **WHEN** a screenshot format is not recognized or OCR fails
- **THEN** the system flags the file for manual data entry and notifies the user

### Requirement: OCR accuracy confidence scoring
The system SHALL assign a confidence score to each extracted field.

#### Scenario: Low confidence extraction
- **WHEN** OCR extracts a time with confidence below 80%
- **THEN** the system highlights the field for user review and correction

### Requirement: Extracted data validation
The system SHALL validate extracted data against known swimming event formats.

#### Scenario: Invalid time format detected
- **WHEN** OCR extracts a time that does not match MM:SS.ss or SS.ss format
- **THEN** the system marks the field as invalid and prompts for correction
