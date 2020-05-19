# django-stripe-lite

Allow a light-touch Django integration with Stripe; we handle Stripe webhook
security + logging while allowing your project to take care of the business
logic.

## Tests

#### Running tests

The tests themselves use `pytest` as the test runner. If you have installed the `poetry` evironment, you can run them:

```bash
$ poetry run pytest
```

or

```bash
$ poetry shell
(django_stripe) $ pytest
```

The full suite is controlled by `tox`, which contains a set of environments that will format (`fmt`), lint, and test against all supported Python + Django version combinations.

```bash
$ tox
```

#### CI

CI is handled by GitHub Actions. See the `.github/workflows` folder.
