Title: A wild Kickstarter appears!
Date: 2014-02-08
Category: Django postgres
Tags: django, postgres, kickstarter
Slug: launch
Author: Marc Tamlyn
Summary: Because the Django pony and the Postgres elephant could be better friends.

I love Django. I also love PostgreSQL.

I've been fortunate enough to hear Craig Kersteins and Christophe Pettus talk
several times about how wonderful Postgres is. I've come away from Django
conferences filled with enthusiasm for the promised land of database
specificity, of semi-flexible schemas using hstore, of array fields, of json in
my database, of full text search and functional indexes and materialized views
and… all the other wonderful features offered by Postgres.

Then I go looking for third party packages to use these features. The state of
hstore is pretty good - I can install the `django-hstore` package, add a model
and a custom manager to my model and everything works, even the admin. The API
for filtering is pretty good, I get some interesting atomic operations to
update keys via the custom manager, and there's even an interesting subclass
which extends the API to reference other model instances as the values. It's
not all perfect - the API could be more natural in some places (e.g.
`.filter(data__mykey=value)` rather than `.filter(data__contains({'mykey':
'value'})` - but we are pretty much there.

What about arrays? Well according to django packages there are [several
different implementations](https://www.djangopackages.com/grids/g/arrayfield/),
none of which have Python3 support, none of which are currently actively
developed, and most of which don't even have documentation. Alternatively,
there's [djorm-ext-pgarray](https://github.com/niwibe/djorm-ext-pgarray) which
is better, but it still requires me to understand how to use array fields in
SQL - I need to know what `@>` means, using `SqlExpression` objects in
`.where()` clauses to build my queries. I need to know the postgres name for
the underlying database field I want to use. That's not the ORM I love.

Now, I do not wish to appear too harsh on the developers of these pacakges and
others. Django has in no way helped them make it easy to provide nice APIs. The
custom field syntax is quite limited, only really allowing you to change the
mapping between the database structure and the python structure, and changing
the `db_type` to modify creation. This gets a lot better in Django 1.7 as we
now have [custom lookups and
transforms](https://docs.djangoproject.com/en/dev/ref/models/custom-lookups/),
although they currently only work in `.filter()` clauses. In particular, I'd
like to thank [Andrey Antukh](https://github.com/niwibe) for his work on the
`pg-ext-*` collection of packages, which have working implementations of most
of the features I wish to build directly into Django.

That said, we can do better. Several people I've worked with, who I consider to
be very good Django developers, have absolutely no idea how to go about
constructing complex SQL queries by hand. Ask what the difference is between
a left and a right outer join and you'll just get a blank expression. Whilst
it's easy to be snarky about this and claim it's a failing in their education,
I prefer to see it as a huge compliment for the power of the Django ORM. These
people have managed to write numerous successful websites with the database at
the core of the functionality, without knowing how to interact with their
database directly. I would like the more advanced postgres features to have the
same ease of use.

Whilst in Warsaw at the wonderful [Django Circus](http://2013.djangocon.eu/)
conference last summer, I chatted a bit to members of the core team about this
concept, and the general state of postgres support in the community. There was
agreement that it was not ideal, and we could do better. The idea formed in my
head that we could build first class support for these features into Django
itself, with the understanding that using database specific functionality is
perfectly reasonable (if not required) for any large site.

So I've decided to do something about it. The core team and the DSF have given
their backing for me to do exactly that - build first class support for
PostgreSQL specific features into Django. This will be as a new contrib module
- `django.contrib.postgres`. This is not a small undertaking I can write in an
odd evening or weekend. I'm going to need your help to allow me to spend enough
time on it to make it good. To that end, and inspired by Andrew Godwin's
[success with
migrations](www.kickstarter.com/projects/andrewgodwin/schema-migrations-for-django),
I'm launching a Kickstarter hopefully at some point in the next week. The
initial aim is to ensure that most Postgres data types have a good Django
equivalent, and for full text search to be possible. With more funding, I'll
also make date based queries much more powerful, add dozens of postgres
specific functions as custom transforms and lookups, and add support for custom
indexes and views. It will take time to build all of this, but I'm confident at
least some features will land for Django 1.8, with most of the rest in Django
1.9.

For reference, this is what I currently consider as the list of things each
field will need to be considered fully supported:

- The field implementation itself, with appropriate keyword arguments to
  provide the same level of expression as the raw SQL equivalent
- Support for "standard" filters such as `__contains`, `__lt` etc if
  appropriate
- Support for appropriate custom filtering methods specific to the data type
- A usable, javascript-free form field
- Where appropriate, a cleverer custom widget for use in the admin
- Extensive tests for each field covering field creation and modification via
  migrations, all allowable query constructs and validation
- Documentation for the model field and form field, complete with examples and
  comments on possible use cases.

Thanks for reading, and I hope you are as excited by this project as I am!
