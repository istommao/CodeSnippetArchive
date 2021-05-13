import os
import time
import hashlib

from datetime import datetime
from uuid import uuid4

import six

from django.db import models
from django.conf import settings
from django.utils.deconstruct import deconstructible


def generate_image_filename(origin_filename):
    ext = origin_filename.split('.')[-1]

    salt = '{}{}'.format(time.time(), uuid4().hex)
    hash_md5 = hashlib.md5(salt.encode())

    file_prefix = hash_md5.hexdigest()
    return '{}.{}'.format(file_prefix, ext)


@deconstructible    # pylint: disable=R0903
class PathAndRename(object):
    """Path and rename."""

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, origin_filename):
        filename = generate_image_filename(origin_filename)

        datestr = datetime.today().strftime('%Y%m%d')
        fullpath = os.path.join(self.path, datestr)

        abspath = os.path.join(settings.MEDIA_ROOT, fullpath)
        if not os.path.exists(abspath):
            os.makedirs(abspath)

        return os.path.join(fullpath, filename)
