PART

Purpose:
Organize Articles within a Chapter while preserving
the distinction between constitutional Parts and
software-only grouping containers.

Identity:
id

Relationships:
Chapter 1 ──── * Part
Part 1 ──────── * Article

Business Fields:
title
display_order
part_type

part_type:
EXPLICIT
IMPLICIT

Business Rules:

1. A Part belongs to exactly one Chapter.
2. A Part has a unique display order within its Chapter.
3. An explicit Part represents an actual constitutional Part.
4. An implicit Part exists only to provide a consistent
   Chapter → Part → Article structure.
5. A Chapter without constitutional Parts may have one
   implicit Part.
6. An implicit Part should not be presented to learners
   as though it were an official constitutional Part.

Does NOT own:
Articles' educational content.
Learning objectives.
Cases.
Decision points.
Choices.
Feedback.
