"""Caching implementations for reading and writing user credentials."""

import json
import logging
import os
import os.path

import google.oauth2.credentials


logger = logging.getLogger(__name__)


_DIRNAME = "pydata"
_FILENAME = "pydata_google_credentials.json"


def _get_default_credentials_path(credentials_dirname, credentials_filename):
    """
    Gets the default path to the Google user credentials

    Returns
    -------
    str
        Path to the Google user credentials
    """
    if os.name == "nt":
        config_path = os.environ["APPDATA"]
    else:
        config_path = os.path.join(os.path.expanduser("~"), ".config")

    config_path = os.path.join(config_path, credentials_dirname)

    # Create a pydata directory in an application-specific hidden
    # user folder on the operating system.
    if not os.path.exists(config_path):
        os.makedirs(config_path)

    return os.path.join(config_path, credentials_filename)


def _load_user_credentials_from_info(credentials_json):
    return google.oauth2.credentials.Credentials(
        token=credentials_json.get("access_token"),
        refresh_token=credentials_json.get("refresh_token"),
        id_token=credentials_json.get("id_token"),
        token_uri=credentials_json.get("token_uri"),
        client_id=credentials_json.get("client_id"),
        client_secret=credentials_json.get("client_secret"),
        scopes=credentials_json.get("scopes"),
    )


def _load_user_credentials_from_file(credentials_path):
    """
    Loads user account credentials from a local file.

    Parameters
    ----------
    None

    Returns
    -------
    - GoogleCredentials,
        If the credentials can loaded. The retrieved credentials should
        also have access to the project (project_id) on BigQuery.
    - OR None,
        If credentials can not be loaded from a file. Or, the retrieved
        credentials do not have access to the project (project_id)
        on BigQuery.
    """
    try:
        with open(credentials_path) as credentials_file:
            credentials_json = json.load(credentials_file)
    except (IOError, ValueError) as exc:
        logger.debug(
            "Error loading credentials from {}: {}".format(credentials_path, str(exc))
        )
        return None

    return _load_user_credentials_from_info(credentials_json)


def _save_user_account_credentials(credentials, credentials_path):
    """
    Saves user account credentials to a local file.
    """
    try:
        with open(credentials_path, "w") as credentials_file:
            credentials_json = {
                "refresh_token": credentials.refresh_token,
                "id_token": credentials.id_token,
                "token_uri": credentials.token_uri,
                "client_id": credentials.client_id,
                "client_secret": credentials.client_secret,
                "scopes": credentials.scopes,
            }
            json.dump(credentials_json, credentials_file)
    except IOError:
        logger.warning("Unable to save credentials.")


class CredentialsCache(object):
    """
    Shared base class for crentials classes.

    This class also functions as a noop implementation of a credentials class.
    """

    def load(self):
        """
        Load credentials from disk.

        Does nothing in this base class.

        Returns
        -------
        google.oauth2.credentials.Credentials, optional
            Returns user account credentials loaded from disk or ``None`` if no
            credentials could be found.
        """
        pass

    def save(self, credentials):
        """
        Write credentials to disk.

        Does nothing in this base class.

        Parameters
        ----------
        credentials : google.oauth2.credentials.Credentials
            User credentials to save to disk.
        """
        pass


class ReadWriteCredentialsCache(CredentialsCache):
    """
    A :class:`~pydata_google_auth.cache.CredentialsCache` which writes to
    disk and reads cached credentials from disk.

    Parameters
    ----------
    dirname : str, optional
        Name of directory to write credentials to. This directory is created
        within the ``.config`` subdirectory of the ``HOME`` (``APPDATA`` on
        Windows) directory.
    filename : str, optional
        Name of the credentials file within the credentials directory.
    """

    def __init__(self, dirname=_DIRNAME, filename=_FILENAME):
        super(ReadWriteCredentialsCache, self).__init__()
        self._path = _get_default_credentials_path(_DIRNAME, _FILENAME)

    def load(self):
        """
        Load credentials from disk.

        Returns
        -------
        google.oauth2.credentials.Credentials, optional
            Returns user account credentials loaded from disk or ``None`` if no
            credentials could be found.
        """
        return _load_user_credentials_from_file(self._path)

    def save(self, credentials):
        """
        Write credentials to disk.

        Parameters
        ----------
        credentials : google.oauth2.credentials.Credentials
            User credentials to save to disk.
        """
        _save_user_account_credentials(credentials, self._path)


class WriteOnlyCredentialsCache(CredentialsCache):
    """
    A :class:`~pydata_google_auth.cache.CredentialsCache` which writes to
    disk, but doesn't read from disk.

    Use this class to reauthorize against Google APIs and cache your
    credentials for later.

    Parameters
    ----------
    dirname : str, optional
        Name of directory to write credentials to. This directory is created
        within the ``.config`` subdirectory of the ``HOME`` (``APPDATA`` on
        Windows) directory.
    filename : str, optional
        Name of the credentials file within the credentials directory.
    """

    def __init__(self, dirname=_DIRNAME, filename=_FILENAME):
        super(WriteOnlyCredentialsCache, self).__init__()
        self._path = _get_default_credentials_path(_DIRNAME, _FILENAME)

    def save(self, credentials):
        """
        Write credentials to disk.

        Parameters
        ----------
        credentials : google.oauth2.credentials.Credentials
            User credentials to save to disk.
        """
        _save_user_account_credentials(credentials, self._path)


NOOP = CredentialsCache()
"""
Noop impmentation of credentials cache.

This cache always reauthorizes and never save credentials to disk.
Recommended for shared machines.
"""

READ_WRITE = ReadWriteCredentialsCache()
"""
Write credentials to disk and read cached credentials from disk.
"""

REAUTH = WriteOnlyCredentialsCache()
"""
Write credentials to disk. Never read cached credentials from disk.

Use this to reauthenticate and refresh the cached credentials.
"""