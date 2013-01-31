# Add asdict() and fromdict() methods to SQLAlchemy declarative models

dictutils add the helpers asdict() and fromdict() to SQLAlchemy declarative models. Currently documentations is lacking and the API is under development.

Currently this works with synonyms and simple relations-ships as one-to-many and many-to-many. Relationships can be followed in many levels.

The only collection currently supported is sqlalchemy.orm.collections.InstrumentedList.

## Status

No release, no version. This code should not be trusted. In pip there are versions but they should not be trusted until the final 0.1 relase.

## Usage

### DictableModel

Mixin dictalchemy.DictableModel in a declarative class or use it as a base class for declarative\_base. Each class can have the following attibutes set:

* dictalchemy\_exclude: List of properties that should be excluded by default(default empty)
* dictalchemy\_exclude\_underscore: Exclude properties starting with an underscore(default True)
* dictalchemy\_include: List of properties that should be included by default(default empty)
* dictalchemy\_fromdict\_allow\_pk: If True the primary key may be updated with fromdict()

## make\_class\_dictable()

This method can be run on existing classes to make them dictable.

## Examples

### Using asdict

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

### Using fromdict

```
>>> from iteralchemy import make_class_dictable
>>> make_class_dictable(Base)
>>> user = session.query(User).first()
>>> dict(user)
{'id': 3, 'name': 'Gerald'}
>>> user.fromdict({'name': 'Gerald the Great'})
>>> dict(user)
{'name': 'Gerald the Great'}
>>> dict(user, follow=['address'])
{'name': 'Gerald the Great', 'address': {'street': None}}
>>> user.fromdict({'address': {'street': 'Main street'})
>>> dict(user, follow=['address'])
{'name': 'Gerald the Great', 'address': {'street': 'Main street'}}
```

See dictalchemy/test\_asdict.py and dictalchemy/\_test\_asdict for more examples.


## License

dictalchemy is released under the MIT license.


## TODO

* Write better docs
* Settle on the API
* Support more collections
