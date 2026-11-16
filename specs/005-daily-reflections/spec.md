# Feature Specification: Daily Reflections with AI-Augmented Content

**Feature Branch**: `005-daily-reflections`  
**Created**: November 30, 2025  
**Status**: Draft  
**Input**: User description: "Improve the value of the site by converting the daily readings feature into a daily reflection feature; this is where the true value of this site starts to come into being; the copying of the readings from usccb.org was just a milestone on the way to this reflections feature. Use the Anthropic LLM API to augment the readings, thus turning into a daily reflection with the following additions: for each reading, add a one-line synopsis presented in italics, generated from the Anthropic LLM API, just above the reading text; add a single reflection section after all the readings all the readings for the day; this generation should use all the readings as context as well as teaching from the Catholic Church, including questions for pondering, one or two relevant entries from the Catechism of the Catholic Church (CCC); add a relevant prayer to the top of the daily readings; the prayer should be found from some Catholic source (I would rather not have AI-generated prayers) and the source should be attributed with a link to the source's site; if it is a solemnity or other feast day, the prayer focus should follow that feast day, otherwise the prayer can focus on the Gospel reading; If it is a feast day, provide a brief synopsis of the feast; if the feast happens to be for a saint, provide a brief bio of the saint including time of birth, death, significant geographic locations, what the person did to become a saint, and a link to some Catholic site which gives more info about that saint."

## Clarifications

### Session 2025-11-30

- Q: When should the AI-augmented content (synopses, reflections) be generated for each day's readings? → A: Generate content each morning at 6am CT for just the current day's readings
- Q: Where should the system source authentic Catholic prayers from? → A: Multiple curated sources (USCCB, Vatican, Catholic Online, EWTN, Loyola Press) - choosing the most relevant prayer for that day
- Q: How should the system validate that AI-generated Catechism of the Catholic Church (CCC) paragraph references are valid and exist? → A: Use Vatican's official online CCC with paragraph range validation (CCC has 2865 paragraphs)
- Q: Since content is generated daily at 6am CT for the current day, should the system also support generating reflections for past dates if requested? → A: Yes, generate on-demand for historical dates
- Q: How should theological accuracy of AI-generated reflections be ensured before publication? → A: Automated validation only - Use carefully crafted AI prompts emphasizing orthodox Catholic teaching, with CCC validation as quality check
- Q: What cost constraints should be applied to AI API usage? → A: AI API costs must stay below $0.04 per daily reflection (estimated actual cost ~$0.02, providing 2x buffer for feast days and retries)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View Daily Reading with AI-Generated Synopsis (Priority: P1)

A Catholic user visits the daily readings page to prepare for Mass or for personal devotion. They see each Scripture reading prefaced with a one-line synopsis in italics that helps them quickly understand the key message, making the readings more accessible and easier to engage with.

**Why this priority**: This is the foundational enhancement that transforms static readings into reflective content. It provides immediate value by making Scripture more approachable for users at all levels of biblical knowledge.

**Independent Test**: Can be fully tested by visiting any daily readings page and verifying that each Scripture passage (First Reading, Responsorial Psalm, Second Reading, Gospel) has a one-line italicized synopsis immediately above it.

**Acceptance Scenarios**:

1. **Given** the user visits today's readings page after 6:00 AM CT, **When** they scroll through the page, **Then** they see a one-line synopsis in italics above each reading (First Reading, Psalm, Second Reading if applicable, and Gospel)
2. **Given** a reading contains complex theological language, **When** the synopsis is generated, **Then** it presents the core message in accessible, plain language
3. **Given** the AI text generation service is temporarily unavailable during the 6:00 AM CT scheduled generation, **When** the page is accessed, **Then** the readings still display without the synopsis and include a note that enhanced content is temporarily unavailable
4. **Given** the user requests a historical date's readings, **When** enhanced content doesn't exist yet, **Then** the system generates it on-demand

---

### User Story 2 - Read Integrated Daily Reflection (Priority: P2)

After reading all the Scripture passages, the user encounters a thoughtful reflection that weaves together all the day's readings with Catholic teaching. The reflection includes pondering questions and 1-2 relevant Catechism of the Catholic Church (CCC) references that deepen their understanding and invite personal prayer.

**Why this priority**: This is the heart of the feature's value proposition - transforming readings into a complete spiritual reflection experience. It requires the synopses (P1) to be in place for best user experience.

**Independent Test**: Can be tested by viewing any daily readings page and confirming a reflection section appears after all readings, containing synthesized insights from all readings, 2-3 pondering questions, and 1-2 CCC citations with paragraph numbers.

**Acceptance Scenarios**:

1. **Given** the user has read all daily Scripture passages, **When** they continue scrolling, **Then** they encounter a "Daily Reflection" section that synthesizes themes from all readings
2. **Given** the reflection is generated, **When** the user reads it, **Then** it includes 2-3 questions for personal pondering that connect the readings to daily life
3. **Given** the reflection references Church teaching, **When** CCC entries are included, **Then** 1-2 specific paragraph numbers are cited with brief quotes or summaries
4. **Given** the reflection cites CCC paragraphs, **When** displayed, **Then** the paragraph numbers are formatted clearly (e.g., "CCC 2558" or "Catechism of the Catholic Church, paragraph 2558")

---

### User Story 3 - Begin with Relevant Prayer (Priority: P2)

When the user first arrives at the daily readings page, they encounter a relevant Catholic prayer at the top that sets a prayerful tone. If it's a feast day, the prayer reflects that feast; otherwise, it connects to the Gospel reading. The prayer includes attribution and a link to its Catholic source.

**Why this priority**: Prayer frames the spiritual encounter with Scripture, making the page a complete devotional experience rather than just informational content. It can function independently of other enhancements.

**Independent Test**: Can be tested by visiting the readings page on any date and verifying a prayer appears at the top with proper attribution and source link to a Catholic website.

**Acceptance Scenarios**:

1. **Given** the user visits the readings page on an ordinary weekday, **When** the page loads, **Then** a prayer relevant to the Gospel reading appears at the top with source attribution and link
2. **Given** the user visits the readings page on a feast day, **When** the page loads, **Then** a prayer specific to that feast day appears at the top with source attribution and link
3. **Given** a prayer is sourced from a Catholic site, **When** displayed, **Then** the prayer includes text such as "Source: [Source Name]" with a clickable link to the original page
4. **Given** no appropriate existing prayer can be found, **When** the page is generated, **Then** a default prayer appropriate to daily Scripture reading is used (e.g., traditional prayer before reading Scripture)

---

### User Story 4 - Learn About Feast Days and Saints (Priority: P3)

On days celebrating a feast or saint, the user sees a dedicated section explaining the feast or providing a biography of the saint (birth, death, geographic locations, path to sainthood, and link to more information on a Catholic site). This enriches their understanding of the liturgical calendar.

**Why this priority**: This adds valuable context but is supplementary to the core reading and reflection experience. It can be developed after the core reflection features.

**Independent Test**: Can be tested by viewing the readings page on a known feast day (e.g., feast of a saint) and confirming a biographical section appears with all required elements: birth/death dates, geographic info, why they're a saint, and an external link.

**Acceptance Scenarios**:

1. **Given** today is a feast day for a saint, **When** the user visits the readings page, **Then** they see a "About Today's Saint" section with birth/death dates, key geographic locations, significant deeds/virtues that led to canonization, and a link to a Catholic resource
2. **Given** today is a solemnity or feast that's not a saint (e.g., Holy Trinity), **When** the user visits the readings page, **Then** they see a brief synopsis explaining the theological significance of the feast
3. **Given** today is an ordinary weekday with no feast, **When** the user visits the readings page, **Then** no feast/saint section appears

---

### Edge Cases

- What happens when the AI text generation service request fails or times out during the 6:00 AM CT scheduled generation?
- How does the system handle a feast day where liturgical data is incomplete or unavailable?
- What if multiple saints or feasts are celebrated on the same day?
- How does the system handle readings that are unusually long or complex for synopsis generation?
- What happens if no appropriate sourced prayer can be found from any of the five curated Catholic sources (USCCB, Vatican, Catholic Online, EWTN, Loyola Press)?
- What if CCC paragraph references generated by the AI fall outside the valid range (1-2865)?
- How are quotes from prayers or saints properly attributed to avoid copyright issues?
- What happens if the scheduled 6:00 AM CT generation fails - should it retry, and when?
- How does the system handle on-demand historical date generation if the AI service is temporarily unavailable?
- What if prayer sources become unreachable or restructure their websites?
- What happens if AI API costs exceed the $0.04 per reflection limit due to unusually long readings or complex feast days?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST generate a one-line synopsis for each Scripture reading (First Reading, Responsorial Psalm, Second Reading when present, Gospel) using AI-powered text generation
- **FR-002**: System MUST display each reading synopsis in italics immediately above the corresponding Scripture text
- **FR-003**: System MUST generate a unified daily reflection after all readings that synthesizes themes from all the day's Scripture passages
- **FR-004**: Daily reflection MUST include 2-3 questions for personal pondering that connect readings to daily spiritual life
- **FR-005**: Daily reflection MUST include 1-2 specific citations from the Catechism of the Catholic Church (CCC) with paragraph numbers
- **FR-006**: System MUST display a relevant Catholic prayer at the top of the daily readings page, sourced from multiple curated Catholic sources (USCCB, Vatican, Catholic Online, EWTN, Loyola Press), selecting the most relevant prayer for each day
- **FR-007**: Prayer MUST include attribution text and a clickable link to the source Catholic website
- **FR-008**: On feast days, the prayer MUST be relevant to the feast being celebrated; on ordinary days, the prayer MUST relate to the Gospel reading
- **FR-009**: On feast days celebrating a saint, system MUST display a biographical section including: approximate birth/death dates, significant geographic locations, reasons for canonization, and a link to a reputable Catholic information source
- **FR-010**: On feast days that are not saint celebrations (e.g., solemnities), system MUST provide a brief synopsis explaining the theological significance
- **FR-011**: System MUST handle AI service unavailability gracefully by displaying readings without enhanced content and showing an appropriate message
- **FR-012**: System MUST validate CCC paragraph references against Vatican's official online CCC (paragraphs 1-2865) before including them
- **FR-013**: Generated content MUST respect Catholic doctrine and present Church teaching accurately through carefully crafted AI prompts emphasizing orthodox Catholic teaching
- **FR-014**: System MUST preserve all existing daily readings functionality while adding the reflection enhancements
- **FR-015**: System MUST store AI service credentials securely and not expose them in generated HTML or public repositories
- **FR-016**: System MUST generate AI-augmented content daily at 6:00 AM Central Time for the current day's readings
- **FR-017**: System MUST support on-demand generation of AI-augmented content for historical dates when requested
- **FR-018**: System MUST limit AI API costs to a maximum of $0.04 per daily reflection generation (input + output tokens combined)

### Dependencies and Assumptions

- **Dependency**: Access to an AI text generation service for creating synopses and reflections (user preference: Anthropic Claude API)
- **Dependency**: Access to multiple curated Catholic prayer sources: USCCB, Vatican, Catholic Online, EWTN, and Loyola Press websites
- **Dependency**: Liturgical calendar data to identify feast days, solemnities, and saint celebrations
- **Dependency**: Vatican's official online Catechism of the Catholic Church (CCC) for paragraph validation (2865 total paragraphs)
- **Dependency**: Saint biographical information from reputable Catholic sources
- **Dependency**: Scheduled task execution capability to run daily generation at 6:00 AM Central Time
- **Assumption**: AI-generated reflection content will use carefully crafted prompts emphasizing orthodox Catholic teaching, with CCC validation serving as the primary quality check (no manual review required)
- **Assumption**: The curated Catholic prayer sources will have sufficient content to cover all liturgical seasons and major feast days
- **Assumption**: The existing USCCB daily readings data will continue to be available and structured consistently
- **Assumption**: On-demand generation for historical dates will complete within acceptable response time for user requests
- **Assumption**: AI API pricing remains stable at approximately current rates (Anthropic Claude 3.5 Sonnet: $3/M input tokens, $15/M output tokens), allowing typical daily reflections to cost ~$0.02 with a $0.04 limit providing adequate buffer

### Key Entities

- **Daily Reading Content**: Comprises the Scripture passages (First Reading, Psalm, Second Reading, Gospel) from the Catholic Lectionary, augmented with AI-generated synopses
- **AI-Generated Synopsis**: A one-line summary for each individual Scripture reading, displayed in italics above the reading text
- **Daily Reflection**: A unified reflection synthesizing all readings, including pondering questions and CCC references
- **Sourced Prayer**: An existing Catholic prayer with attribution and source link, selected based on liturgical calendar (feast day or Gospel theme)
- **Feast Day Information**: Includes type (saint, solemnity, etc.), saint biography when applicable (dates, locations, canonization reasons), and link to Catholic resource
- **Liturgical Calendar Data**: Information about the current day's liturgical celebration, used to determine feast days, solemnities, and ordinary time

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Each daily readings page displays at least 3 Scripture readings (First Reading, Psalm, Gospel) with AI-generated synopses in italics above each reading
- **SC-002**: Daily reflection section includes 2-3 specific pondering questions and cites 1-2 valid CCC paragraph numbers (validated against paragraphs 1-2865) on every generated page
- **SC-003**: 100% of daily readings pages include a sourced prayer at the top with visible attribution and functional link to one of the five curated Catholic sources (USCCB, Vatican, Catholic Online, EWTN, Loyola Press)
- **SC-004**: On feast days celebrating saints (approximately 15-20% of days in liturgical year), biographical information appears with all required elements (dates, locations, canonization reasons, external link)
- **SC-005**: System successfully generates AI-augmented content by 6:00 AM Central Time each day, and gracefully handles AI service failures by displaying basic readings with appropriate messaging
- **SC-006**: Generated reflection content maintains theological accuracy through carefully crafted AI prompts emphasizing orthodox Catholic teaching, requiring zero corrections for doctrinal errors in the first month of operation
- **SC-007**: On-demand historical date generation completes successfully when requested, providing the same quality of enhanced content as scheduled daily generation
- **SC-008**: AI API costs remain at or below $0.04 per daily reflection for 95% of generated reflections over a 30-day period
