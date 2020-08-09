# IronStrataReliquary

## What

Python class for interacting with PAN-OS API

- [Logging Practices](./logging.html)
- [Unit Testing](unit-testing.html)

## How

Create a new `IronStrataReliquary`, where `strata_interface` is the name of your Strata appliance:

```python
strata_interface = IronStrataReliquary(args.verbosity, args.k, args.u, args.p, args.api_endpoint)
```

From there, it's possible to perform get and post invocations. Example:

```python
strata_interface.do_api_get_opcmd_key(strata_interface.query_get_globalprotect_summary_v9
```

## Why

Object-based API invocation is useful from a programmatic standpoint, because the module import saves hundreds of lines of redundant coding.

The objective of this project is to develop and maintain API invocations for routine usage in PAN-OS. Each saved invocation is annotated with the PAN-OS version it was added in, to help determine if any changes are made between versions.

- Maintaining a self-testing 3rd party class of API invocations with a pipeline will provide deprecation notice if used with a test bed.
- Toil tasks such as routing changes should be automatically validated.
- Automated monitoring via REST and XML APIs will be more comprehensive than with SNMP.

### Dependencies

- Python 3.
- Django Core. Required for URL/URI Validation and parsing.
- Requests. You can't really make API calls without it.
- xmltodict. Required to process API responses
- JSON

## TODO

- Moved to project board

## Authors

- *Nick Schmidt*
