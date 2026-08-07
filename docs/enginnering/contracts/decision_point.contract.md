Entity
------

DecisionPoint

Purpose
-------

Represent a decision moment within a Case where the learner selects one of several predefined actions.

Questions it answers
--------------------

Where in this Case should the learner make a decision?

Responsibilities
----------------

• Represent one decision moment.
• Group related Choices.
• Maintain the order of decisions within a Case.
• Coordinate the learner's progression through the story.

Identity
--------

id

Relationships
-------------

Belongs to one Case.

Owns many Choices.

Business Fields
---------------

display_order

(Optional)
instruction
