Getting started
===============

Installation
------------

Python Version
^^^^^^^^^^^^^^

It's recommended to use the latest version of Python. Eventflow supports Python 3.6 and newer.

Dependencies
^^^^^^^^^^^^

Eventflow has no external dependencies.

Install Eventflow
^^^^^^^^^^^^^^^^^

You can get the latest development version from `Github <https://github.com/SvenKortekaas04/Eventflow>`_. After downloading and unpacking it, you can install it using::

$ pip install .

Basic Usage
-----------

Let's cover the basics before going more into detail. We'll start by creating a new instance of the `EventBus` class.

.. code-block:: python

    from eventflow import EventBus
    bus = EventBus()

You now have created a new instance of the `EventBus` class. Let's continue by adding a listener. We start by creating a function that acts as a listener.

.. code-block:: python

    def func(event):
        ...

.. note:: A function acting as a listener must have an `event` argument as the first positional argument.

To assign a function as a listener, you can use a decorator. It takes an event type as an argument, which is the event type to which the listener will be assigned.

.. code-block:: python

    @bus.listen(event_type="test")
    def func(event):
        ...

If you prefer to use a function you can use :py:meth:`eventflow.EventBus.add_listener`.

.. code-block:: python

    >>> bus.add_listener(event_type="...", listener=func)

Now you can get all listeners stored in the event bus.

.. code-block:: python

    >>> bus.listeners
    {"test": 2}

You can also remove listeners from the event bus if you no longer need them.

.. code-block:: python

    >>> bus.remove_listener(event_type="...", listener=func)

Finally, once listeners have been added to the event bus, you can trigger them by calling the event type.

.. code-block:: python

    >>> bus.fire(event_type="...")