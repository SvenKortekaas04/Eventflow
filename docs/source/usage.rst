Advanced Usage
==============

Event Data
----------

In some cases, it may be helpful to provide an event with additional information to work with.

.. code-block:: python

    >>> bus.fire(event_type="...", data={})

.. note:: A ``dict`` is used as the format in which the data is stored.

You can then access the data through the `event` argument.

.. code-block:: python

    def func(event):
        data = event["data"]