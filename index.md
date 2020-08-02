# IronStrataReliquary

## What

Python class for interacting with PAN-OS API

## How

Create a new `IronStrataReliquary`, where `strata_interface` is the name of your Strata appliance:
`strata_interface = IronStrataReliquary(args.verbosity, args.k, args.u, args.p, args.api_endpoint)`
From there, it's possible to perform get and post invocations. Example:
`strata_interface.do_api_get_opcmd_key(strata_interface.query_get_globalprotect_summary_v9`

## Why

Toil tasks such as routing changes should be automatically validated, e.g.

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
