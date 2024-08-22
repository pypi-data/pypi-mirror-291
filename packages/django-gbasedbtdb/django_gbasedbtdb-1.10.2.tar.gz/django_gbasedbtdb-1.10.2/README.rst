Django GBasedbtDB
==================

A database driver for Django to connect to an GBase 8s database via pyodbc.

**Some limitations**:

- Does not support default values
- GBase 8s automatically creates indexes on foreign keys, but Django attempts to do that
  manually; the current implementation here just attempts to catch the error on index
  creation. It may unintentionally catch other index creation errors where the index
  already exists.


Configure local environment
---------------------------

The following environment variables should exist:

GBASEDBTDIR
    The path to the GBase 8s client install directory

GBASEDBTSERVER
    The name of the GBase 8s service to which we need to connect

GBASEDBTSQLHOSTS
    The path to the ``sqlhosts`` file that the GBase 8s driver should use

LD_LIBRARY_PATH
    The path(s) to the various GBase 8s library files: Usually
    ``$GBASEDBTDIR/lib:$GBASEDBTDIR/lib/cli:$GBASEDBTDIR/lib/esql``

DB_LOCALE
    In case of ``Database locale information mismatch.`` error during connection,
    you should specify your database locale, e.g. ``DB_LOCALE=en_US.8859-15``

You will also need to add an entry within your ``sqlhosts`` file for each remote/local GBase 8s 
server connection in the following format::

    <GBASEDBT_SERVER_NAME>    onsoctcp     <GBASEDBT_HOST_NAME>    <GBASEDBT_SERVICE_NAME>

For example::

    dev    onsoctcp    localhost    9088

You may alternatively use a symbolic name in that line in place of the port number, typically ``sqlexec`` and
then configure the port number in the ``/etc/services`` file::

    sqlexec    9088/tcp


Configure settings.py
---------------------

Django’s settings.py uses the following to connect to an GBase 8s database:

.. code-block:: python

    'default': {
        'ENGINE': 'django_gbasedbtdb',
        'NAME': 'myproject',
        'SERVER': 'dbtserver',
        'USER' : 'testuser',
        'PASSWORD': 'passw0rd',
        'OPTIONS': {
            'DRIVER': '/path/to/iclit09b.so'. # Or iclit09b.dylib on macOS
            'CPTIMEOUT': 120,
            'CONN_TIMEOUT': 120,
            'ISOLATION_LEVEL': 'READ_UNCOMMITTED',
            'LOCK_MODE_WAIT': 0,
            'VALIDATE_CONNECTION': True,
        },
        'CONNECTION_RETRY': {
            'MAX_ATTEMPTS': 10,
        },
        'TEST': {
            'NAME': 'myproject',
            'CREATE_DB': False
        }
    }

CPTIMEOUT
    This will set connection pooling timeout.
    Possible values::

        0 - Turn off connection pooling
        nn - timeout set nn seconds

CONN_TIMEOUT
    This will set timeout for operations on connections (connection, ??closing??, we're not sure).
    Possible values::

        0 - Default timeout to the database (which could mean no timeout)
        nn - timeout set nn seconds

ISOLATION_LEVEL
    This will set database isolation level at connection level
    Possible values::

        READ_COMMITED
        READ_UNCOMMITTED
        SERIALIZABLE

LOCK_MODE_WAIT
    This will set database LOCK MODE WAIT at connection level
    Application can use this property to override the default server
    process for accessing a locked row or table.
    The default value is 0 (do not wait for the lock).
    Possible values::

        -1 - WAIT until the lock is released.
        0 - DO NOT WAIT, end the operation, and return with error.
        nn - WAIT for nn seconds for the lock to be released.

VALIDATE_CONNECTION
    Whether existing connections should be validated at the start of the request. Defaults to
    `False`.

VALIDATION_INTERVAL
    How often in seconds to revalidate connections if `VALIDATE_CONNECTION` is enabled. Defaults to
    `300` (5 minutes).

VALIDATION_QUERY
    Query used to validate whether a connection is usable. Defaults to
    `"SELECT 1 FROM dual"`.

CONNECTION_RETRY
    When opening a new connection to the database, automatically retry up to ``MAX_ATTEMPTS`` times
    in the case of errors. Only error codes in ``ERRORS`` will trigger a retry. The wait time
    between retries is calculated using an exponential backoff with jitter formula::

        random_between(WAIT_MIN, min(WAIT_MAX, WAIT_MULTIPLIER * WAIT_EXP_BASE ** (attempt - 1)))

    Defaults (wait times are in milliseconds)::

        MAX_ATTEMPTS: 1  # this implies no retries
        WAIT_MIN: 0
        WAIT_MAX: 1000
        WAIT_MULTIPLIER: 25
        WAIT_EXP_BASE: 2
        ERRORS: ['-908', '-930', '-27001']

    Each of these settings can be overridden in the ``CONNECTION_RETRY`` section of the database
    configuration in ``settings.py``. For example::

        DATABASES = {
           'default': {
               'ENGINE': 'django_gbasedbtdb',
               'CONNECTION_RETRY': {
                   'MAX_ATTEMPTS': 10,
                   'WAIT_MIN': 0,
                   'WAIT_MAX': 500,
               },
               # ...
            },
         }

    The error codes that are retried by default correspond to the following errors:

    * ``-908 Attempt to connect to database server (servername) failed``
    * ``-930 Cannot connect to database server servername``
    * ``-27001 Read error occurred during connection attempt``

    These errors are often seen when the database server is too busy, too many clients are
    attempting to connect at the same time or a network firewall has chopped the connection.


.. note:
    The ``DRIVER`` option is optional, default locations will be used per platform if it is not provided.

.. note:
    The ``TEST`` option sets test parametes.  Use ``NAME`` to override the name of the test database
    and set ``CREATE_DB`` to ``False`` to prevent Django from attempting to create a new test
    database.


Testing against an GBase 8s Database
------------------------------------

Due to a bug in the GBase 8s ODBC driver, it is not currently possible to run Django tests normally. Specifically, it is not possible for Django to create a test database. As such, you will need to do it manually. By default Django will attempt to create a database with a name equal to the default database name with a ``test_`` prefix. e.g. if you database name is ``my_database``, the test database name would be ``test_my_database``.  This can be overridden with the ``NAME`` option under ``TEST``.

To prevent Django from attempting to create a test database, set the ``CREATE_DB`` option
under ``TEST`` to ``False``: see 'Configure settings.py' above.

You can follow the steps above, in the section on using GBase 8s locally with Docker to create a test database. Then when running the test you can tell Django to re-use an existing database, rather than trying to create a new one with the ``-k`` parameter:

.. code-block:: bash

    ./manage.py test -k


For django_gbasedbtdb Developers
--------------------------------

To run the django_gbasedbtdb test suite, you need to set the GBASEDBTDIR environment variable, and the tests
expect an GBase 8s database at host "gbase01". Change that host in `test/conftest.py` if you need to.
Then run the test suite with:

    tox

This will run the tests under Django 2 and 3.


Release History
---------------

Version 1.10.2

- Add datatypes support

Version 1.10.1  

- Fork from django_informixdb  
- Fix 'unsupported column type -114'
