# Converts SQLAlchemy declarative models to dict

Currently this works with synonyms and simple relations-ships as one-to-many and many-to-many. Relationships will only be followed one level.

The only collection currently supported is sqlalchemy.orm.collections.InstrumentedList.

## Status

No release, no version. This code should not be trusted.

## Usage

Mixin iterachlemy.IterableModel in a declarative class or use it as a base class for declarative\_base. Each class can have the following attibutes set:

* asdict\_exclude: List of properties that should be excluded by default(default empty)
* asdict\_exclude\_underscore: Exclude properties starting with an underscore(default True)

## Examples

```
>>> dict(user)
{'id': 3, 'name': 'Gerald'}
>>> user.asdict(exclude=['id'])
{'name': 'Gerald'}
>>> user.asdict(follow=['roles'])
{'id': 3, 'name': 'Gerald', 'roles': [{'id': 1, 'name': 'admin'}, {'id': 2, 'name': 'user'}]}
>>> user.asdict(follow={'roles': {'exclude': ['id']})
{'id': 3, 'name': 'Gerald', 'roles': [{'name': 'admin'}, {'name': 'user'}]}
```

See iteralchemy/test\_asdict.py for more examples.

## License

iteralchemy is released under the MIT license.


## TODO

* Write docs
* Support more collections
