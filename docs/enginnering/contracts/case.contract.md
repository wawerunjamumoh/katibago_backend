Entity
------

Case

Purpose
-------

Provide realistic, reusable Kenyan scenarios that help learners apply constitutional principles in context.

Responsibilities
----------------

• Establish a believable real-world situation.
• Present a constitutional dilemma.
• Remain legally neutral.
• Serve as the foundation for learner interaction through DecisionPoints.
• Be reusable across multiple Articles.

Identity
--------

• id

Relationships
-------------

• One Case can appear in many Articles (through ArticleCase).
• One Case can contain many DecisionPoints.

Business Fields
---------------

• case_title
• summary
• story

System Fields
-------------

• created_at
• updated_at

Business Rules
--------------

• Every Case must have a title.
• Every Case must contain a complete narrative.
• Cases must not reveal the correct legal answer.
• Cases should remain reusable and independent of any single Article.

Does NOT Own
------------

• Article
• LearningObjective
• DecisionPoint outcomes
• CitizenExplanation
• SafetyShield
