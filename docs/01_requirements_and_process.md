# 1. Requirements and Process Model

## Functional requirements
FR1 Register a user (name, unique email, role). FR2 Create events of kind seminar/workshop/concert with default fee and capacity limits. FR3 List events. FR4 Register a user for an event; reject duplicates and full events. FR5 Price depends on role/date (student 20% off, early bird 15%). FR6 Charge payment for paid events. FR7 Send a confirmation e-mail after registration. FR8 View registrations of an event. FR9 Persist all data in SQLite.

## Non-functional requirements
NFR1 Extensibility: new event kinds/pricing/notifiers without editing existing code. NFR2 Testability: >=85% coverage, external dependencies mockable. NFR3 Reliability: failed payment stores nothing. NFR4 Usability: simple web form + Swagger docs. NFR5 Maintainability: CI on every PR.

## User stories
- As a student, I want to register for a workshop so that I get a seat at a discount.
- As an organizer, I want to create an event with a capacity so that it cannot be overbooked.
- As a student, I want a confirmation e-mail so that I know my payment succeeded.
- As a developer, I want API docs so that I can integrate quickly.

## Prototype / mock-up (ASCII, redraw in Figma/draw.io for the report)
```
+----------------------------------------+
| Campus Events                          |
| * Git 101 (workshop, 2027-03-01, cap 40)|
| Add event: [title][kind v][date][cap][Create] |
+----------------------------------------+
```

## Process model: Incremental (Agile-style, weekly increments)
Justification: requirements were clear but the module count was high, so each module (users -> events -> registration -> payment -> notifications) was delivered and tested as one increment. Rejected: Waterfall (late feedback, no working software until the end).
