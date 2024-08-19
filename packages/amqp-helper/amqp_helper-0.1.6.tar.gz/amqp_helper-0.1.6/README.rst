================
amqp_helper
================

Introduction
=============

:code:`amqp_helper` aims to be a simple Helper library to configure AMQP communication for use with :code:`aio-pika`
To achieve this goal this Library provides the :code:`AMQPConfig` class.

This package also provides a log handler to send logs to an AMQP Broker. You can use it via the class :code:`AMQPLogHandler`

Installation
==============

:code:`amqp_helper` can be installed in multiple ways. The easiest Solution is to install it with :code:`pip`.

via pip
---------

.. code-block:: bash

    python3 -m pip install amqp-helper


from source
------------

.. code-block:: bash

    git clone https://github.com/bad-microservices/amqp_helper.git
    cd amqp_helper
    python3 -m pip install .

Example
========

.. code-block:: python

    import asyncio
    from amqp_helper import AMQPConfig
    from aio_pika import connect_robust

    amqp_config = AMQPConfig(username="test",password="testpw",vhost="testvhost")

    async def main():

        connection = await connect_robust(**amqp_config.aio_pika())

        # do some amqp stuff

    if __name__ == "__main__":
        asyncio.run(main())

Example RPC over AMQP
======================

Server code
------------
The Server code is quite simple

.. code-block:: python

    import asyncio
    from amqp_helper import AMQPConfig, AMQPService, new_amqp_func

    amqp_config = AMQPConfig(username="test",password="testpw",vhost="testvhost")

    async def testfunc(throw_value_error = False,throw_key_error = False, throw_exception = False*args, **kwargs):
        if throw_value_error:
            raise ValueError()
        if throw_key_error:
            raise KeyError()
        if throw_exception:
            raise Exception()

        return {"result": "sync stuff"}

    rpc_fun = new_amqp_func("test1", test1234)


    @rpc_fun.exception_handler(ValueError, KeyError)
    async def handle_value_error(*args, **kwargs):
        retrun "got ValueError or KeyError"

    @rpc_fun.exception_handler(Exception)
    async def handle_value_error(*args, **kwargs):
        return "got Exception"

    async def main():

        service = await AMQPService().connect(amqp_config)
        await service.register_function(rpc_fun)

        await service.serve()

        # do some amqp stuff

    if __name__ == "__main__":
        asyncio.run(main())


Client
------------

.. code-block:: python

    import asyncio
    from amqp_helper import AMQPConfig, AMQPClient

    amqp_config = AMQPConfig(username="test",password="testpw",vhost="testvhost")

    async def main():

        client = await AMQPClient().connect(amqp_config)

        print(await client.call(None,"test1"))

    if __name__ == "__main__":
        asyncio.run(main())


Logging to AMQP
================

if we want to log to an AMQP Topic we can do it with the following example code.

.. code-block:: python

    import logging
    from amqp_helper import AMQPLogHandler

    log_cfg = AMQPConfig(username="test",password="testpw",vhost="testvhost")

    handler = AMQPLogHandler(amqp_config=log_cfg, exchange_name="amqp.topic")

    root_logger= logging.getLogger()
    root_logger.addHandler(handler)

    root_logger.info("test log message")

