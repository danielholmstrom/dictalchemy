Version 0.1.2.7
===============

* Bugfix for how fromdict handles `allow_pk` in combination with `exclude`

Version 0.1.2.6
===============

* Support for _AssociationList and _AssociationDict with asdict

Version 0.1.2.4
===============

* Fixed bug where follow arguments were modified instead of a copy of the arguments.
* Checking for list or dict when following relations instead of specific classes

Version 0.1.2.3
===============

* All extra keyword arguments to asdict are now passed on to followed relations.

Version 0.1.2.2
===============

* Using sqlalchemy.inspect to find model attributes
* Min sqlalchemy version set to 0.9.4
* New parameter `parent` for follow argument in `asdict`

Version 0.1.2.1
===============

* Additional keyword arguments allowed in `asdict`
* New parameter `method` in `asdict`


Version 0.1.2b3
===============

* Relationships with nullable foreign keys no longer raises an UnsupportedRelationError if the relation is None

Version 0.1.2b2
===============

* Support for dynamic relationships with asdict
