"""A backend for playing music from a music cd.

This backend handles URIs starting with ``cdda:``.

See :ref:`music-from-cd-storage` for further instructions on using this
backend.

**Issues:**

https://github.com/mopidy/mopidy/issues?labels=Cd+backend

**Dependencies:**

- None

**Settings:**

- :attr:`mopidy.settings.CD_DEVICE`
"""

from __future__ import unicode_literals

# flake8: noqa
from .actor import CdBackend
