## ADDED Requirements

### Requirement: Natural language questions about swimming data
The system SHALL accept natural language questions about Sunny's swimming data and provide accurate, data-backed answers.

#### Scenario: Ask about personal best
- **WHEN** a user asks "What is Sunny's fastest 100m freestyle time?"
- **THEN** the system retrieves and displays the personal best time with the meet date

#### Scenario: Ask about trends
- **WHEN** a user asks "How has Sunny's backstroke improved this year?"
- **THEN** the system analyzes backstroke times from the current year and describes the trend with specific data points

### Requirement: Question context awareness
The system SHALL maintain conversation context to support follow-up questions.

#### Scenario: Follow-up question
- **WHEN** a user asks "What about breaststroke?" after asking about freestyle
- **THEN** the system understands the context and compares breaststroke performance similarly

### Requirement: Data-backed answers with citations
The system SHALL include data citations in every answer.

#### Scenario: Answer with evidence
- **WHEN** a user asks "Is Sunny improving?"
- **THEN** the system answers with specific times from recent meets compared to earlier meets

### Requirement: Handle out-of-scope questions gracefully
The system SHALL decline to answer questions unrelated to Sunny's swimming data.

#### Scenario: Irrelevant question
- **WHEN** a user asks "What is the weather today?"
- **THEN** the system responds that it can only answer questions about Sunny's swimming data
