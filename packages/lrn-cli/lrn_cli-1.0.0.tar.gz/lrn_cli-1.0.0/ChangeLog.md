# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [v1.0.0] - 2024-08-21
### Added
- Add trogon.tui support
- Add support to build Docker image and run from it

## [v0.0.6] - 2024-08-01
### Added
- Add --output-payload  option to output signed urlencoded HTTP requests paremeters to stdout
- Add --output-json  option to output signed JSON payloads to stdout
- Update build system to use the Python `build` module
- Add likely non-functional first attempt at Trusted Publishing GhA

### Fixed
- Bug when sending SET requests to api-data's sessions endpoint
- Bug where sending requests with `user` set would result in empty request being
    sent instead

### Changed
- Only read JSON from the terminal if `--file -` is specified

## [v0.0.5] - 2023-10-11
### Added
- End-to-end tests for the CLI command
- `version` command
- Better request dumping in debug mode
- Add `--output-payload` | `-O` option to return signed request

### Fixed
- Requests to API endpoints that don't expect a request payload
- Updated Python build system to use pyproject.toml
- Changed linter from Flake8 to Black
- Use `isort`

### Added

- Support for DELETE requests
- Workflow to run tests on PR triggers
- Support for Annotations API
- Support for Events API
- Support for `developer` version

### Fixed

- Pinned flake8 to a version that works with pytest-flake8

## [v0.0.4] - 2022-05-04

### Added

- Support for object pagination in SET/UPDATE requests

## [v0.0.3] - 2021-04-21

### Added

- Tests (lint and rudimentary doctest)
- Travis support
- More doc
- PR template

### Fixed

- Release-support code
- Bugs due to incorrect merge conflict resolution impacting all but api-data

## [v0.0.2] - 2021-04-20

- New PyPI release including actual code...

## [v0.0.1] - 2021-04-20
### Added

- This ChangeLog!
- lrn-cli: Support for api-author, api-items, api-questions and api-reports
- lrn-cli: Support for usrequest
- lrn-cli command
