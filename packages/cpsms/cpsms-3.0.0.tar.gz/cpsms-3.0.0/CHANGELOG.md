# 3.0.0

## New features

- Add support for getting the credit status from the gateway.

## Changes

- The `gateway_url` has been replaced by a `gateway_base_url`, as several
  endpoints at the gateway is now used, not only the endpoint for sending
  an SMS.
- Make minimum supported Python version 3.10. Things will probably still work
  with older versions as well.
- Change license from GPL3 to MIT.
- Relocate project from GitHub to git.data.coop
