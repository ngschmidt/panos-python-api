# IronStrataReliquary

## Synopsis

Provide an API interation library compatible with PAN-OS XML API

## To use these examples

Create a new `IronStrataReliquary`:

`strata_interface = IronStrataReliquary(args.verbosity, args.k, args.u, args.p, args.api_endpoint)`

From there, it's possible to perform get and post invocations.

## Tested Platforms

- PAN-OS 9.0
- PAN-OS 9.1
- PAN-OS 10.0

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
