"""from werkzeug contrib atom.py """
# Python 2


def implements_to_string(cls):
    cls.__unicode__ = cls.__str__
    cls.__str__ = lambda x: x.__unicode__().encode('utf-8')
    return cls


@implements_to_string
class AtomFeed(object):

    """A helper class that creates Atom feeds.

    :param title: the title of the feed. Required.
    :param title_type: the type attribute for the title element.  One of
                       ``'html'``, ``'text'`` or ``'xhtml'``.
    :param url: the url for the feed (not the url *of* the feed)
    :param id: a globally unique id for the feed.  Must be an URI.  If
               not present the `feed_url` is used, but one of both is
               required.
    :param updated: the time the feed was modified the last time.  Must
                    be a :class:`datetime.datetime` object.  If not
                    present the latest entry's `updated` is used.
                    Treated as UTC if naive datetime.
    :param feed_url: the URL to the feed.  Should be the URL that was
                     requested.
    :param author: the author of the feed.  Must be either a string (the
                   name) or a dict with name (required) and uri or
                   email (both optional).  Can be a list of (may be
                   mixed, too) strings and dicts, too, if there are
                   multiple authors. Required if not every entry has an
                   author element.
    :param icon: an icon for the feed.
    :param logo: a logo for the feed.
    :param rights: copyright information for the feed.
    :param rights_type: the type attribute for the rights element.  One of
                        ``'html'``, ``'text'`` or ``'xhtml'``.  Default is
                        ``'text'``.
    :param subtitle: a short description of the feed.
    :param subtitle_type: the type attribute for the subtitle element.
                          One of ``'text'``, ``'html'``, ``'text'``
                          or ``'xhtml'``.  Default is ``'text'``.
    :param links: additional links.  Must be a list of dictionaries with
                  href (required) and rel, type, hreflang, title, length
                  (all optional)
    :param generator: the software that generated this feed.  This must be
                      a tuple in the form ``(name, url, version)``.  If
                      you don't want to specify one of them, set the item
                      to `None`.
    :param entries: a list with the entries for the feed. Entries can also
                    be added later with :meth:`add`.

    For more information on the elements see
    http://www.atomenabled.org/developers/syndication/

    Everywhere where a list is demanded, any iterable can be used.
    """

    default_generator = ('Werkzeug', None, None)

    def __init__(self, title=None, entries=None, **kwargs):
        self.title = title
        self.title_type = kwargs.get('title_type', 'text')
        self.url = kwargs.get('url')
        self.feed_url = kwargs.get('feed_url', self.url)
        self.id = kwargs.get('id', self.feed_url)
        self.updated = kwargs.get('updated')
        self.author = kwargs.get('author', ())
        self.icon = kwargs.get('icon')
        self.logo = kwargs.get('logo')
        self.rights = kwargs.get('rights')
        self.rights_type = kwargs.get('rights_type')
        self.subtitle = kwargs.get('subtitle')
        self.subtitle_type = kwargs.get('subtitle_type', 'text')
        self.generator = kwargs.get('generator')
        if self.generator is None:
            self.generator = self.default_generator
        self.links = kwargs.get('links', [])
        self.entries = entries and list(entries) or []

        if not hasattr(self.author, '__iter__') \
           or isinstance(self.author, string_types + (dict,)):
            self.author = [self.author]
        for i, author in enumerate(self.author):
            if not isinstance(author, dict):
                self.author[i] = {'name': author}

        if not self.title:
            raise ValueError('title is required')
        if not self.id:
            raise ValueError('id is required')
        for author in self.author:
            if 'name' not in author:
                raise TypeError('author must contain at least a name')

    def add(self, *args, **kwargs):
        """Add a new entry to the feed.  This function can either be called
        with a :class:`FeedEntry` or some keyword and positional arguments
        that are forwarded to the :class:`FeedEntry` constructor.
        """
        if len(args) == 1 and not kwargs and isinstance(args[0], FeedEntry):
            self.entries.append(args[0])
        else:
            kwargs['feed_url'] = self.feed_url
            self.entries.append(FeedEntry(*args, **kwargs))

    def __repr__(self):
        return '<%s %r (%d entries)>' % (
            self.__class__.__name__,
            self.title,
            len(self.entries)
        )

    def generate(self):
        """Return a generator that yields pieces of XML."""
        # atom demands either an author element in every entry or a global one
        if not self.author:
            if False in map(lambda e: bool(e.author), self.entries):
                self.author = ({'name': 'Unknown author'},)

        if not self.updated:
            dates = sorted([entry.updated for entry in self.entries])
            self.updated = dates and dates[-1] or datetime.utcnow()

        yield u'<?xml version="1.0" encoding="utf-8"?>\n'
        yield u'<feed xmlns="http://www.w3.org/2005/Atom">\n'
        yield '  ' + _make_text_block('title', self.title, self.title_type)
        yield u'  <id>%s</id>\n' % escape(self.id)
        yield u'  <updated>%s</updated>\n' % format_iso8601(self.updated)
        if self.url:
            yield u'  <link href="%s" />\n' % escape(self.url)
        if self.feed_url:
            yield u'  <link href="%s" rel="self" />\n' % \
                escape(self.feed_url)
        for link in self.links:
            yield u'  <link %s/>\n' % ''.join('%s="%s" ' %
                                              (k, escape(link[k])) for k in link)
        for author in self.author:
            yield u'  <author>\n'
            yield u'    <name>%s</name>\n' % escape(author['name'])
            if 'uri' in author:
                yield u'    <uri>%s</uri>\n' % escape(author['uri'])
            if 'email' in author:
                yield '    <email>%s</email>\n' % escape(author['email'])
            yield '  </author>\n'
        if self.subtitle:
            yield '  ' + _make_text_block('subtitle', self.subtitle,
                                          self.subtitle_type)
        if self.icon:
            yield u'  <icon>%s</icon>\n' % escape(self.icon)
        if self.logo:
            yield u'  <logo>%s</logo>\n' % escape(self.logo)
        if self.rights:
            yield '  ' + _make_text_block('rights', self.rights,
                                          self.rights_type)
        generator_name, generator_url, generator_version = self.generator
        if generator_name or generator_url or generator_version:
            tmp = [u'  <generator']
            if generator_url:
                tmp.append(u' uri="%s"' % escape(generator_url))
            if generator_version:
                tmp.append(u' version="%s"' % escape(generator_version))
            tmp.append(u'>%s</generator>\n' % escape(generator_name))
            yield u''.join(tmp)
        for entry in self.entries:
            for line in entry.generate():
                yield u'  ' + line
        yield u'</feed>\n'

    def to_string(self):
        """Convert the feed into a string."""
        return u''.join(self.generate())

    def get_response(self):
        """Return a response object for the feed."""
        return BaseResponse(self.to_string(), mimetype='application/atom+xml')

    def __call__(self, environ, start_response):
        """Use the class as WSGI response object."""
        return self.get_response()(environ, start_response)

    def __str__(self):
        return self.to_string()


# Example
def atom_feed(request):
    feed = AtomFeed("My Blog", feed_url=request.url,
                    url=request.host_url,
                    subtitle="My example blog for a feed test.")

    for post in Post.query.limit(10).all():
        feed.add(post.title, post.body, content_type='html',
                 author=post.author, url=post.url, id=post.uid,
                 updated=post.last_update, published=post.pub_date)

    data = feed.to_string()

    return Response(data, mimetype='application/atom+xml')
