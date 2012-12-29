# Converts SQLAlchemy declarative models to dict

Currently this works with synonyms and simple relations-ships as one-to-many and many-to-many. Relationships can be followed in many levels.

The only collection currently supported is sqlalchemy.orm.collections.InstrumentedList.

## Status

No release, no version. This code should not be trusted.

## Usage

### DictableModel

Mixin dictalchemy.DictableModel in a declarative class or use it as a base class for declarative\_base. Each class can have the following attibutes set:

* asdict\_exclude: List of properties that should be excluded by default(default empty)
* asdict\_exclude\_underscore: Exclude properties starting with an underscore(default True)

## make\_class\_iterable()

This method can be run on existing classes to make them iterable.

## Examples

```
>>> from iteralchemy import make_class_dictable
>>> make_class_dictable(Base)
>>> user = session.query(User).first()
>>> dict(user)
{'id': 3, 'name': 'Gerald'}
>>> user.asdict(exclude=['id'])
{'name': 'Gerald'}
>>> user.asdict(follow=['roles'])
{'id': 3, 'name': 'Gerald', 'roles': [{'id': 1, 'name': 'admin'}, {'id': 2, 'name': 'user'}]}
>>> user.asdict(follow={'roles': {'exclude': ['id']})
{'id': 3, 'name': 'Gerald', 'roles': [{'name': 'admin'}, {'name': 'user'}]}
>>> user.asdict(follow={'roles': {'exclude': ['id'], 'follow': ['group']})
{'id': 3, 'name': 'Gerald', 'roles': [{'name': 'admin', 'group': {'id': 1, 'name': 'admin'}}, {'name': 'user', 'group': {'id': 2, 'name': 'user'}}]}
```

See dictalchemy/test\_asdict.py for more examples.

## License

dictalchemy is released under the MIT license.


## TODO

* Write docs
* Support more collections
