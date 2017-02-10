""" pyeloqua is a package of wrappers functions for interacting with Eloqua over Bulk API 2.0.
    Right now, they cover Contacts, Accounts, and Custom Data Objects."""

from .pyeloqua import Eloqua
from .bulk import Bulk
from .system_fields import ACTIVITY_FIELDS, CONTACT_SYSTEM_FIELDS, ACCOUNT_SYSTEM_FIELDS
