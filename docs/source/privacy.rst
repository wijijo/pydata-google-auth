Privacy
=======

This package is a `PyData project <https://pydata.org/>`_ and is subject to
the `NumFocus privacy policy <https://numfocus.org/privacy-policy>`_. Your
use of Google APIs with this module is subject to each API's respective
`terms of service <https://developers.google.com/terms/>`_.

Google account and user data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Accessing user data
~~~~~~~~~~~~~~~~~~~

The :mod:`pydata_google_auth` module accesses your Google user account, with
the list of `scopes
<https://developers.google.com/identity/protocols/googlescopes>`_ that you
specify. Depending on your specified list of scopes, the credentials returned
by this library may provide access to other user data, such as your email
address, Google Cloud Platform resources, Google Drive files, or Google
Sheets.

Storing user data
~~~~~~~~~~~~~~~~~

By default, your credentials are stored by the
:class:`pydata_google_auth.cache.READ_WRITE` class to a local file, such as
``~/.config/pydata``. All user data is stored on your local machine. **Use
caution when using this library on a shared machine**.

Sharing user data
~~~~~~~~~~~~~~~~~

The pydata-google-auth library only communicates with Google APIs. No user
data is shared with PyData, NumFocus, or any other servers.

Policies for application authors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Do not use the default client ID when using the pydata-google-auth library
from an application, library, or tool. Per the `Google User Data Policy
<https://developers.google.com/terms/api-services-user-data-policy>`_, your
application must accurately represent itself when authenticating to Google
API servcies.
