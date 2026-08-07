Entity
------

DecisionPoint

Purpose
-------

Present a constitutional dilemma that requires learners to reason before making a decision.

Questions it answers
--------------------

What decision should the learner make?

Responsibilities
----------------

• Pause the story.
• Present a dilemma.
• Encourage reasoning.
• Lead to multiple Choices.

Identity
--------

id

Relationships
-------------

Case (Many → One)

Choice (One → Many)

Business Fields
---------------

decision_prompt

display_order

System Fields
-------------

created_at

updated_at

Business Rules
--------------

Must belong to one Case.

Must contain at least two Choices.

Display order must be unique within a Case.

Must not reveal the correct answer.

Does NOT own
------------

Case

Choice outcomes

Feedback

Citizen Explanation

Safety Shield
