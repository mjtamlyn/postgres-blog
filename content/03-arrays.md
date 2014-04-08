Title: Fields of fields
Date: 2014-04-08
Category: Blog
Tags: django, postgres, kickstarter
Slug: arrays
Author: Marc Tamlyn
Summary: Lists of data in a single field

I'm sure you will all be pleased to hear that some progress is being made with
the project! The bulk of the work will be done over the summer months, but I am
hoping to have a couple of the more interesting new field types done before
[DjangoConEU](http://2014.djangocon.eu/) in May. (Speaking of DjangoConEU - I
will be speaking in more detail there about this project, if you haven't booked
your tickets yet you should totally do so - it'll be a great event!)

There is now a "work in progress" [pull
request](https://github.com/django/django/pull/2485) available on github for
array fields. Comment is very welcome! An array field allows you to store lists
of data in a single field. It's like the big brother of Django's
[`CommaSeparatedIntegerField`](https://docs.djangoproject.com/en/dev/ref/models/fields/#commaseparatedintegerfield`),
but it supports most other field types underneath.

The only restriction on the field type is that we do not support any related
field type - `ForeignKey` or `ManyToMany`. I should not need to explain why the
latter is illogical, but in the case of the former it's worth pointing out the
reasoning why. In short, Postgres does not allow the use of `REFERENCES` in
array field declarations, so you could build an array of foreign key data, but
it would not have referential integrity. As this is a promise of the
`ForeignKey`, we cannot support `ArrayField(ForeignKey())`. This is an
unfortunate restriction as many of the "natural" use cases for arrays would
reference other objects, and one which I hope to lift in the future if Postgres
support improves. You can of course emulate this with
`ArrayField(IntegerField())` but this is at your own risk!

Aside from their utility for storing list-like data without the requirement for
another table, Postgres array fields can also be queried in a number of ways.
Taking as an example a dice-based guessing game where we have an `Attempt` model
which stores the attempts to guess the rolled number, the following queries are
all valid:

    :::python
    Attempt.objects.filter(guesses=[1])  # only one guess, value 1
    Attempt.objects.filter(guesses__0=1)  # first guess is 1
    Attempt.objects.filter(guesses__0_1=[1, 2])  # first guess 1, second guess 2
    Attempt.objects.filter(guesses__len__lt=3)  # less than 3 guesses
    Attempt.objects.filter(guesses__contains=[1])  # at least one guess is 1
    Attempt.objects.filter(guesses__overlap=[1, 2])  # at least one guess is either 1 or 2
    Attempt.objects.filter(guesses__contained_by=[1, 2])  # guesses include only 1 and 2

As with other non-text based fields in Django, at the moment array fields still
support a number of other lookups which cast the value to text. Personally I
consider this to be somewhat misleading at the moment and am considering
removing support for them. This is perhaps part of a wider question though - is
it logical that a `DateField` supports `__istartswith` (probably not) but is it
logical that it supports `__startswith=200` as an alternative to the upcoming
(postgres specific) `__decade=2000`? My instinct is that we should introduce a
`__text` transform which is available on all data types and casts to text,
allowing these filters. This could be done with a deprecation path. I'm
interested to hear your views!

The next step is to build a couple of form fields for arrays, one being a
simple CharField taking a `delimiter` with a delimiter to split on, and the
other being a more complex Javascript enabled field for the admin which allows
a nicer interface. Perhaps we could also include a version of this without the
javascript that has a similar API to formsets. After that I just need to write
complete documentation and we can merge it in!

## A note on JSON support

The Postgres team have recently merged support for a `jsonb` datatype - binary
stored JSON. It is quite likely that I will delay JSON support until Postgres
9.4 is out and only support the `jsonb` data type. There are several reasons
for this, the most significant being that the current `json` data type is
severly limited in its implementation, lacking even an equality operator. This
means that some parts of Django annotation code generate invalid queries (see
[this report](https://github.com/bradjasper/django-jsonfield/issues/55)) and
also means that a `__exact` lookup has to be forbidden. To handle all these
edge cases properly in Django would result in a huge amount of complexity, and
the benefits you gain over just storing json in a text field are actually quite
limited. 9.4 is due out towards the end of this year, so as a result JSON
fields are likely to only feature in the 1.8 release.

## Sponsors page updated

The [sponsors page](/pages/sponsors.html) has been updated with images and
links for all the major sponsors. Go and check out all the great companies and
individuals who have supported this project.
