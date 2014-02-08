#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Marc Tamlyn'
SITENAME = 'Improved PostgreSQL support for Django'
SITEURL = 'http://postgres.mjtamlyn.co.uk/'

TIMEZONE = 'Europe/London'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

# Blogroll
LINKS = (
    ('Django', 'http://djangoproject.org/'),
)

# Social widget
SOCIAL = (
    ('Twitter', 'http://twitter.com/mjtamlyn'),
    ('Github', 'http://github.com/mjtamlyn'),
)

DEFAULT_PAGINATION = 10
