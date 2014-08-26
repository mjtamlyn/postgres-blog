Title: Converting database representations
Date: 2014-08-26
Category: Blog
Tags: django, postgres, kickstarter
Slug: from-db-value
Author: Marc Tamlyn
Summary: UUID and Duration preparatory work

I would like to start with an apology for the quietness on this blog recently,
work has been going on though a little slower than I would like as my personal
life has been getting in the way of doing any work. Over the last six weeks
things have improved and there are two exciting new fields in the pipeline.

## New fields on the way

There are 90% finished patches for
[UUIDField](https://github.com/django/django/pull/2923) and
[DurationField](https://github.com/django/django/pull/2995). These fields both
have long standing accepted tickets to be introduced as general django fields,
not specific to PostgreSQL. On PostgreSQL, they will natively use the `uuid`
and `interval` data types, and on other databases the will use `char(32)` and
`bigint` respectively. The initial patches used the metaclass `SubfieldBase`
provided by Django, but this has some significant issues. As a result, changes
have been needed in the ORM to handle database-python conversions when loading
from the database.

## The status quo

### Database backends

Not all database drivers return all field types in the same format. Psycopg2 is
generally pretty well behaved, but mysql, oracle and sqlite all have some
idiosyncrasies about certain fields, usually relating to dates, decimals or
booleans. Furthermore, sometimes these only happened when aggregates were
involved. There were two hooks provided to deal with these, firstly
`Query.convert_values` calling `DatabaseOperations.convert_values`, which was
called by aggregates code, and secondly the optional method
`SQLCompiler.resolve_columns` which was called during normal queryset
evaluation if present. On oracle and in gis, `SQLCompiler.resolve_columns`
invoked `Query.convert_values` which in turn invoked
`DatabaseOperations.convert_values`.

This change based on whether `SQLCompiler.resolve_columns` existed or not
caused at least [ticket 21565](https://code.djangoproject.com/ticket/21565).

### Custom fields
Django provides a metaclass called SubfieldBase, which basically means that
that field will have its `to_python()` method called whenever a value is
assigned to the model, including when it is loaded from the database. This
really is an abuse of `to_python()` whose primary purpose is to convert strings
from serialisation and forms into the relevant python object. It also provided
no way to change the behaviour based on the backend, but crucially was not
called by aggregation or `values()` calls. ([ticket
14462](https://code.djangoproject.com/ticket/14462))

### Proposed changes
The new proposed code allows backends and fields to provide converter functions
to transform the value from the database to the model layer. DatabaseBackend
converters are run first and for internal types will normalise the values. A
custom field can then convert the resulting object again if needs be. This code
is run in an efficient manner and the same way in all parts of the ORM -
queries, aggregates, `.values()`, `.dates()` etc. Due to changes in the
signatures and for performance reasons, all the hooks have changed. The new API
is summarized below:

#### "Private" API
- `SQLCompiler.get_converters(fields)`
- `SQLCompiler.apply_converters(row, converters)`

#### "Semi-Private" API
- `DatabaseOperations.get_db_converters(internal_type)` - returns a list of
    backend converter functions `convert(value, field)`
- `Field.get_db_converters(connection)` - returns a list of field converter
    functions `convert(value, field)`

#### Public API
- `Field.from_db_value(value, connection)` - public documented hook to replace
    SubfieldBase.

## A note on gis
This has a 147 line negative diff in `contrib.gis`, removing a bunch of
duplicated code, an entire compiler module for mysql, `GeoValuesQuerySet`, and
custom code in `SQLDateCompiler`. Overall it is a pretty substantial cleanup
and the proposed API is nicely overridable by the gis compiler.

## Comments
The proposed changes are available as a [pull
request](https://github.com/django/django/pull/3047) for comment, and there is
also a [thread on
Django-Dev](https://groups.google.com/forum/#!msg/django-developers/0nauqFFwscU/ykXvUTkxW0wJ)
