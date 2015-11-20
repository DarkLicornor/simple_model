simple_model
============

As the name says, this is a very simple model framework. It can be used for data
validation and (de-)serialization.

Installation
------------

Install with pip::

    $ pip install --user simple_model

Usage
-----

Examples::

    >>> from simple_model import Model, Attribute

    >>> class Data(Model):
    ...     name = Attribute(str)
    ...     some_value = Attribute(str, nullable=True)
    ...     another_value = Attribute(int, fallback=0)

    >>> Data(name = 'test', some_value = None, another_value = 12).__attributes__()
    { 'name': 'test', 'some_value': None, 'another_value': 12 }

    >>> Data(name = 'test', _allow_missing=True).__attributes__()
    { 'name': 'test', 'some_value': None, 'another_value': 0 }

    >>> Data(name = 'test', unknown_value = True, _allow_missing=True, _allow_unknown=True).__attributes__()
    { 'name': 'test', 'some_value': None, 'another_value': 0 }

    >>> init_dict = {'name': 'test', 'some_value': 'val', 'another_value': 3}
    >>> Data(**init_dict)
    { 'name': 'test', 'some_value': 'val', 'another_value': 3 }

Initializing with unknown or missing attributes while not specifying to allow
them will result in a *TypeError*.

The default behaviour for missing/unknown attributes can be changed::

    >>> class Data(Model):
    ...     __allow_unknown__ = True
    ...     __allow_missing__ = True

Serialization can be achieved easily, for example::

    >>> import json
    >>> def serialize(model):
    ...     return json.dumps(model.__attributes__())

    >>> def deserialize(string):
    ...     return Data(**json.loads(string))

Tests
-----

To run the tests use tox::

    $ tox

Or run py.test manually (not recommended, needs simple_module installed)::

    $ py.test .