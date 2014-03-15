Title: Making a start
Date: 2014-03-15
Category: Blog
Tags: django, postgres, kickstarter
Slug: where-to-start
Author: Marc Tamlyn
Summary: Funding has been secured, so where do we start?

The last month has been amazing for me. It feels like the whole Django
community has got behind this project and is looking forwards to it. An
enormous thank you to everyone who has contributed to the project. I am still
gathering together the details of the sponsors, but you can see a "raw" list on
[this site](/pages/sponsors.html). In particular, I'd like to thank the DSF,
Django stars, Judicata and Tangent Labs for their particularly generous
donations, but without all of you, none of what I'm about to do would be
possible.

I've made a start writing some code. Easily one of the most popular features is
hstore. For those who might not be familiar, a postgres hstore is a bit like a
simple dictionary in a column - it contains a mapping of strings to strings.
They are one dimensional and completely free form - there is no guarantee about
which keys might exist. They are a really great way to add a small amount of
unstructured data to a model without making schema changes. You might be
tempted to just use json for this sort of functionality, but unless you need
the nested structures, hstore is much more powerful for querying and indexing.

The problem with hstore is that it requires an extension. This is pretty
straightforwards for a production database - just type `CREATE EXTENSION
hstore` at the prompt in that database once (before creating the tables) and
you're good to go. Where it becomes a problem for us is in testing - the newly
created test database does not have the `hstore` extension. It would also be
nice if you didn't have to log on to your shell and run the `CREATE EXTENSION`
directly, it was just created if you have a model using hstore.

There are a few possible ways to acheive this using the new migrations
framework. The first (for which there is a [proposed
patch](https://github.com/django/django/pull/2266)) is to extend
`Field.db_parameters()` to allow it to return some `pre_create_sql`, which will
be run every time a field of this type is created (either by adding a model
using the field, or by adding a field of this type to an already existing
model). This means the sql might be run many times and needs to be coded
defensively - that is use `CREATE EXTENSION IF NOT EXISTS`. Whilst this patch
works, it introduces potentially a large number of unnecessary SQL statements
run against the database, and it also has no way to remove any extension if it
is no longer needed.

An alternative is to create an initial migration in the postgres app which will
create all the necessary extensions that might be needed for all parts of the
app. This has a major drawback which is that it would create extensions even if
the project does not use that part of the code. As some extensions could
conceivably only for for some versions of PostgreSQL, these migrations might
not even work for all users.

Another alternative is to introduce a new concept called an `Extension` which
would be tracked by the autodetector for migrations. I'm going to try to create
a concrete patch for this to see how complex it is, but the idea does have some
usage outside of postgres as a means of allowing certain models or field types
to require custom functions to be created in the database, something which all
the supported databases have.

This is going to take some time to get right, so in the mean time I'm going to
make a start on array fields. They're possibly my favourite feature in the
entire project and something I know I have half a dozen concrete use cases for.
One of the most interesting things about them is that they can be created for
almost any django field type (with the notable exception of
`ManyToManyField`!), so there's a lot of possible edge cases, especially in the
admin widget. It will also be the first core field to have dynamic custom
lookups - a syntax along the lines of `.filter(myarray__0=17)`.

First things first however is the get the beta of 1.7 out of the door and get
the branch away for master. This will then allow me to start merging new
features into Django master. As always, community help with reviewing
prereleases of Django is enormously beneficial for the core team, so please do
go and download the new versions and test them out - there are loads of awesome
new features in 1.7!
