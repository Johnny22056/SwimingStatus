## ADDED Requirements

### Requirement: Screenshots are stored in an organized folder structure
The system SHALL store uploaded screenshots in a folder hierarchy organized by meet and date.

#### Scenario: Upload a new screenshot
- **WHEN** a user uploads a screenshot file
- **THEN** the system saves it to `data/screenshots/<meet-name>/<date>/` with the original filename

### Requirement: Duplicate screenshot detection
The system SHALL detect and prevent duplicate screenshot uploads based on filename and checksum.

#### Scenario: Upload duplicate screenshot
- **WHEN** a user uploads a screenshot that already exists in the storage
- **THEN** the system warns the user and does not overwrite the existing file without explicit confirmation

### Requirement: Screenshot metadata tracking
The system SHALL maintain a metadata file for each screenshot recording upload date, original filename, and associated meet.

#### Scenario: Track screenshot metadata
- **WHEN** a screenshot is successfully stored
- **THEN** the system records its metadata in `data/screenshots/index.json`
