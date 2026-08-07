# LearningObjective Contract

## Purpose

Represents one measurable learning outcome within an Article.

A Learning Objective defines what a learner should know,
understand, or be able to do after completing the lesson.

---

## Ownership

LearningObjective owns:

- learning statement
- cognitive level
- display order

LearningObjective does NOT own:

- Articles
- Cases
- Decision Points
- Choices
- Feedback
- Safety Shields

---

## Relationships

Article (1)
      │
      │
      ▼
LearningObjective (*)

Every Learning Objective belongs to exactly one Article.

Every Article should contain at least two Learning Objectives.

---

## Business Rules

• Statement cannot be empty.

• Statement must describe an observable learning outcome.

• Display order must be unique within an Article.

• Cognitive level must be one of the supported levels.

---

## Future Extension

Learning Objectives may later be linked to:

- learner mastery
- adaptive learning
- AI tutoring
- analytics