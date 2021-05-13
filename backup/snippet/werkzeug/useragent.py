"""user agent 解析."""
import re


class UserAgentParser(object):

    """A simple user agent parser.  Used by the `UserAgent`."""

    platforms = (
        ('cros', 'chromeos'),
        ('iphone|ios', 'iphone'),
        ('ipad', 'ipad'),
        (r'darwin|mac|os\s*x', 'macos'),
        ('win', 'windows'),
        (r'android', 'android'),
        ('netbsd', 'netbsd'),
        ('openbsd', 'openbsd'),
        ('freebsd', 'freebsd'),
        ('dragonfly', 'dragonflybsd'),
        ('(sun|i86)os', 'solaris'),
        (r'x11|lin(\b|ux)?', 'linux'),
        (r'nintendo\s+wii', 'wii'),
        ('irix', 'irix'),
        ('hp-?ux', 'hpux'),
        ('aix', 'aix'),
        ('sco|unix_sv', 'sco'),
        ('bsd', 'bsd'),
        ('amiga', 'amiga'),
        ('blackberry|playbook', 'blackberry'),
        ('symbian', 'symbian')
    )
    browsers = (
        ('googlebot', 'google'),
        ('msnbot', 'msn'),
        ('yahoo', 'yahoo'),
        ('ask jeeves', 'ask'),
        (r'aol|america\s+online\s+browser', 'aol'),
        ('opera', 'opera'),
        ('chrome', 'chrome'),
        ('seamonkey', 'seamonkey'),
        ('firefox|firebird|phoenix|iceweasel', 'firefox'),
        ('galeon', 'galeon'),
        ('safari|version', 'safari'),
        ('webkit', 'webkit'),
        ('camino', 'camino'),
        ('konqueror', 'konqueror'),
        ('k-meleon', 'kmeleon'),
        ('netscape', 'netscape'),
        (r'msie|microsoft\s+internet\s+explorer|trident/.+? rv:', 'msie'),
        ('lynx', 'lynx'),
        ('links', 'links'),
        ('Baiduspider', 'baidu'),
        ('bingbot', 'bing'),
        ('mozilla', 'mozilla')
    )

    _browser_version_re = r'(?:%s)[/\sa-z(]*(\d+[.\da-z]+)?(?i)'
    _language_re = re.compile(
        r'(?:;\s*|\s+)(\b\w{2}\b(?:-\b\w{2}\b)?)\s*;|'
        r'(?:\(|\[|;)\s*(\b\w{2}\b(?:-\b\w{2}\b)?)\s*(?:\]|\)|;)'
    )

    def __init__(self):
        self.platforms = [(b, re.compile(a, re.I)) for a, b in self.platforms]
        self.browsers = [(b, re.compile(self._browser_version_re % a))
                         for a, b in self.browsers]

    def __call__(self, user_agent):
        for platform, regex in self.platforms:
            match = regex.search(user_agent)
            if match is not None:
                break
        else:
            platform = None
        for browser, regex in self.browsers:
            match = regex.search(user_agent)
            if match is not None:
                version = match.group(1)
                break
        else:
            browser = version = None
        match = self._language_re.search(user_agent)
        if match is not None:
            language = match.group(1) or match.group(2)
        else:
            language = None
        return platform, browser, version, language


if __name__ == '__main__':
    ua = UserAgentParser()
    import sys
    uastr = ''.join(sys.argv[1:])
    print(ua(uastr))
