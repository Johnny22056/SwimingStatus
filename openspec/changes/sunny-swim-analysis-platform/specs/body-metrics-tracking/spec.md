## ADDED Requirements

### Requirement: Manual input of body metrics
The system SHALL provide a form for inputting body metrics including height, weight, arm span, and date of measurement.

#### Scenario: Add new body metrics entry
- **WHEN** a user submits body metrics through the input form
- **THEN** the system stores the data in `data/body_metrics.json` with a timestamp

### Requirement: Body metrics history visualization
The system SHALL display body metrics history as line charts showing progression over time.

#### Scenario: View body metrics trends
- **WHEN** a user navigates to the body metrics section
- **THEN** the system displays charts for height, weight, and arm span over time

### Requirement: BMI and growth percentile calculation
The system SHALL calculate BMI and estimate growth percentiles based on age and gender.

#### Scenario: Calculate BMI for a measurement
- **WHEN** a new body metric entry includes height and weight
- **THEN** the system calculates and displays BMI alongside historical BMI values
