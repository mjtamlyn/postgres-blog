Title: Arrays merged
Date: 2014-05-23
Category: Blog
Tags: django, postgres, kickstarter
Slug: arrays-merged
Author: Marc Tamlyn
Summary: Arrays are merged, what next?

Good news everyone! `ArrayField` has been merged into django master. This
will not be backported to the upcoming 1.7 release, but it will now be in 1.8.
You can read the
[documentation](https://docs.djangoproject.com/en/dev/ref/contrib/postgres/).
Let us know if you find any errors!

There are two notable areas which still need to be addressed with arrays, but
the patch was large enough to review and merge without those as well. The first
is improving its behaviour in the admin. I would like to provide an admin
widget which uses the normal admin widgets for each field, starting with a
given number but also being extended to arbitrary size by an "add" button on
the page. This extension is rather difficult to implement at present because of
most of the django admin widgets are not easily constructible from javascript.
In order to do this well, a fairly significant overhaul of how the Django admin
renders widgets such as the date/time widget and makes them interactive is
needed.

The second area is indexing. While `db_index=True` will work on an
``ArrayField``, it will create a btree index which is only useful for equality
in this case. The correct index type is a `gist` index, but there is no way to
tell Django this is what I need. This will require a refactoring of
`spatial_index` in `contrib.gis` as well, and fits nicely within the work on
custom indexes.

I think my next area to work on will be uuid fields, with larger primary key
fields coming out as a corrollary. The interest here will be in supporting
making fields other than `AutoField` be "auto" fields - using `RETURNING` to
allow the database to calculate their values and return them.

For those interested, slides from my talk at DjangoConEurope are [available
online](https://speakerdeck.com/mjtamlyn/the-future-of-postgresql-in-django).
