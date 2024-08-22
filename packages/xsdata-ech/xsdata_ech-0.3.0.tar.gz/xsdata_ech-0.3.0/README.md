eCH xsdata dataclasses
======================

Provides [xsdata](https://xsdata.readthedocs.io) dataclasses for swiss
e-government standards defined by [eCH](https://ech.ch).


! JSON deserialization might return wrong classes, if they have the same structure.

Tests
-----

Run the tests

    pip install .[test]
    tox

Releasing
---------

Make sure, all recent changes are in HISTORY.md. Then bump the version:

    pip install .[dev]
    bump2version {major|minor|patch}
    git push && git push --tags

Then create a new release on GitHub using the new tag.

Update definitions
------------------

Generate files

    pip install .[dev]
    xsdata generate xxx.xsd

Then move the files and fix the imports.