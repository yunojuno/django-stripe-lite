CHANGELOG
=========

0.3.0 - 2022-12-13 (BREAKING)
-----------------------------

This version ensures the application can work under Django 4.1 by ensuring it
abides by newer default location for the AppConfig. The AppConfig was
previously defined in the `__init__.py` with the `default_app_config` parameter
but this was deprecated long ago in favour of placement in `apps.py`.

Because the `AppConfig` has moved, this change is listed as a breaking change
as some users may have explicitly defined the route to the `AppConfig` as part
of their Django Settings `INSTALLED_APPS` configuration. The fix is to simply
use the new location instead.

---

Version support for Django v2 and Python v3.7 has been deprecated. The official
support is now for Django v3.2->4.1.x and Python v3.8->3.10.
