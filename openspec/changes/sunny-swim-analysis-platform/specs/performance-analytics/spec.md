## ADDED Requirements

### Requirement: Time progression trends by stroke
The system SHALL generate line charts showing time progression for each stroke type over time.

#### Scenario: View freestyle time trend
- **WHEN** a user selects "Freestyle" from the stroke filter
- **THEN** the system displays a line chart of 50m, 100m, and 200m freestyle times over time with trend lines

### Requirement: Age-adjusted performance analysis
The system SHALL calculate and display age-adjusted performance metrics.

#### Scenario: Compare performance at age 8 vs age 9
- **WHEN** a user views performance analytics
- **THEN** the system shows time improvements normalized by age group and distance

### Requirement: Stroke comparison radar chart
The system SHALL generate a radar chart comparing performance across all strokes.

#### Scenario: View stroke balance analysis
- **WHEN** a user navigates to the stroke comparison section
- **THEN** the system displays a radar chart comparing relative performance in freestyle, backstroke, breaststroke, and butterfly

### Requirement: Personal best tracking
The system SHALL maintain and display personal best times for each event.

#### Scenario: View personal bests
- **WHEN** a user opens the personal bests dashboard
- **THEN** the system displays the fastest time recorded for each stroke-distance combination with the date achieved
