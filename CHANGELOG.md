# CHANGELOG

All changes to this project will be documented in this file.

## 0.7.0 - 2024-03-19 (BREAKING)

Add support for Django 5.2 and update dependency requirements:

- Added support for Django 5.2
- Deprecated support for Django versions before 4.2
- Updated minimum Python version requirement to 3.10
- Updated ruff configuration to use modern syntax
- Updated GitHub Actions workflow to only test Django main branch with Python 3.12

### Breaking Changes
- Minimum Python version is now 3.10
- Minimum Django version is now 4.2
- Removed support for Python 3.8 and 3.9
- Removed support for Django 3.2, 4.0, and 4.1

## 0.6.0 - 2023-11-11

Add support for Django 5.0, Python 3.12

## 0.5.0 - 2022-12-13

Upgrade our dependency on Stripe from vs 2.x to 5.x

## 0.4.1 - 2022-12-13

Fix the 0.4.0 release; somehow the apps.py code got reverted before merge and we
did not notice. This ensures the AppConfig can be found by Django 4.1.

## 0.4.0 - 2022-12-13 (BREAKING)

This version ensures the application can work under Django 4.1 by ensuring it
abides by newer default location for the AppConfig. The AppConfig was previously
defined in the `__init__.py` with the `default_app_config` parameter but this was
deprecated long ago in favour of placement in `apps.py`.

Because the `AppConfig` has moved, this change is listed as a breaking change as
some users may have explicitly defined the route to the `AppConfig` as part of
their Django Settings `INSTALLED_APPS` configuration. The fix is to simply use
the new location instead.

---

Version support for Django v2 -> 3.1 and Python v3.7 has been deprecated. The
official support is now for Django v3.2->4.1.x and Python v3.8->3.11.
