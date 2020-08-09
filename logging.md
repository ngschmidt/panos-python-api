# Logging Schema

[Back to Home Page]<https://ngschmidt.github.io/panos-python-api/>

## Errors

Defined as an event that cannot be escaped from, the program should close (or rollback) to prevent impact.

### Error Breakdown

#### Preemptive Validation

* E0001: URL Validation Error

#### API Execution Errors

* E1000: Connection Timeout
* E1001: XML to Dictionary Conversion Error
* E1002: Unhandled Requests Library Exception
* EAxxx: HTTP Translated Error

#### Conversion Errors

* E2000: XML Parsing Error
* E2001: XML Conversion Error

#### File Errors

## Warnings

Defined as a negative result, but one that *should* not have unintended side effects.

### Warning Breakdown
