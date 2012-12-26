# Converts SQLAlchemy declarative models to dict

Currently this works with synonyms and simple relations-ships as one-to-many and many-to-many. Relationships will only be followed one level.

The only collection currently supported is sqlalchemy.orm.collections.InstrumentedList.

## License

iteralchemy is released under the MIT license.

## Examples

Mixin iterachlemy.IterableModel in a declarative class or use it as a base class for declarative\_base. Each class can have the following attibutes set:

* asdict\_exclude: List of properties that should be excluded by default(default empty)
* asdict\_exclude\_underscore: Exclude properties starting with an underscore(default True)

    >>> dict(user)
    {'id': 3, 'name': 'Gerald'}
    >>> user.asdict(exclude=['id'])
    {'name': 'Gerald'}
    >>> user.asdict(follow=['roles'])
    {'id': 3, 'name': 'Gerald', 'roles': [{'id': 'admin'}, {'id': 'user'}]}



See iteralchemy/test\_todict.py for more examples.

## TODO

* Write docs
* Support more collections
