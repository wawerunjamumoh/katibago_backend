Entity

ArticleCase

---

Purpose

Defines how a reusable Case is adapted
for a specific Article.

---

Identity

id

---

Relationships

Article (1)

Case (1)

---

Business Fields

display_order

usage_type

is_required

---

System Fields

created_at

updated_at

---

Business Rules

Each ArticleCase links one Article to one Case.

Display order is unique within an Article.

Cases remain reusable.

ArticleCase never modifies Case content.

---

Does NOT own

Article

Case

LearningObjective

DecisionPoint

Choice

Feedback
