# Learnosity CLI tool (lrn-cli)

[![PyPI version](https://badge.fury.io/py/lrn-cli.svg)](https://pypi.org/project/lrn-cli/)
[![GitHub version](https://badge.fury.io/gh/Learnosity%2Flrn-cli.svg)](https://github.com/Learnosity/lrn-cli)

![lrn-cli logo](lrn-cli.png)

The `lrn-cli` tool allows the exchange of JSON payloads with the Learnosity APIs
without having to worry about signature generation.

*PLEASE NOTE*: This is experimental software, and is provided as-is. It is not
part of the Learnosity product offering that receives support.

In a nutshell, it can be used as follows:

    lrn-cli [--profile <PROFILE>|--consumer-key <KEY> --consumer-secret <SECRET>] [--region <REGION>]
		  --request-json '<REQUEST>' [--update|--set|--delete] \
		  <API> <ENDPOINT>

By default, the demonstration consumer credentials will be used if none are
specified.

If `--request-json` is not specified, the request will be read from
standard input, or an alternative JSON file can be provided through `--file`.

Documentation about all the options is available with the `--help` flag to both
the base tool, and each API.

    lrn-cli --help

## Getting started

### Setup

The simplest way to install, if you don't intend to develop, is via `pip3` (or
`pip`).

    pip3 install lrn-cli

If you intend to make changes to the codebase, you can get run from a clone of
the git repository.

    git clone git@github.com:Learnosity/lrn-cli
    cd lrn-cli
    make
    . .venv/lrn-cli/bin/activate

See at the end of this file for other development-related information.

#### Trogon UI

If you want to try out the Trogon UI, you will need to install the specific
dependencies with

    pip3 install lrn-cli[trogon]

You can then run it with

    lrn-cli tui

#### Docker

You can build a Docker image with

    make docker

You can then use the `lrn-cli-docker.sh` script to run from this image, with the
correct environment and mounts set up as needed.

There may not be complete feature parity for file-based interactions
(particularly with relative paths). Access to the current directory should work.

### Configuration

While most parameters (credentials, environment, version, region, ...) can be specified on
the command line, they can also be set as environment variables (`LRN_...` as
documented in the `--help` output of the main and sub-commands, if relevant).

lrn-cli also supports credentials and configuration files. By default, these are
`~/.learnosity/credentials` and `~/.learnosity/config` respectively. You may need to
create a `~/.learnosity` directory before creating these files.

Both are formatted as simple INI file, with sections in square brackets, and parameters
set within the section.  Those entries can be selected for use with either the
`--profile` command line option, or the `LRN_PROFILE` environment variable.

If the profile provided is not found, and keys not otherwise specified, `lrn-cli` will
default to the learnosity-demos consumer key.

#### Credentials file

The credentials file allows you to specify named consumer key and secret pairs.
By default, it is in `~/.learnosity/credentials`.

```ini
[default]
consumer_key=yis0TYCu7U9V4o7M
consumer_secret=74c5fd430cf1242a527f6223aebd42d30464be22

[some-other-consumer]
consumer_key=X
consumer_secret=Y

[staging]
consumer_key=X
consumer_secret=Y
```

#### Configuration file

The config file allows additional parameters to be specified, such as environment, region and
version. By default, it is in `~/.learnosity/config`.

```ini
[default]
region=au
version=v2020.2.LTS

[old-lts]
version=v2020.1.LTS
source_profile=default

[staging]
environment=staging
version=v2020.2.LTS

```

The `source_profile` allows to fetch a differently-named set of consumers
credentials.

### Action

The default action is GET. Different actions can be selected by using the
switches `--set`, `--update`, or `--delete`. These are mutually exclusive:
if more than one occurs, the last will be the effective action. (There is
a `--get` switch as well, though this is less useful, since GET is the default.)

## Examples

Getting the status of a session, passing the request from the command line arguments.

	$ API=data
	$ ENDPOINT=/sessions/statuses
	$ lrn-cli -l debug -R  '{ "limit": 1, "session_ids": ["4562ae00-0f59-6d3c-860b-74b7b5579b32"] }' ${API} ${ENDPOINT}
	2019-10-22 14:22:25,490 DEBUG:Using request JSON from command line argument
	2019-10-22 14:22:25,491 DEBUG:Sending GET request to https://data.learnosity.com/v1/sessions/statuses ...
	[
	 {
	  "user_id": "open_web_demo1",
	  "activity_id": "Demo Activity Id",
	  "num_attempted": 0,
	  "num_questions": 5,
	  "session_id": "4562ae00-0f59-6d3c-860b-74b7b5579b32",
	  "session_duration": 0,
	  "status": "Incomplete",
	  "dt_saved": "2019-10-21T23:48:31Z",
	  "dt_started": "2019-10-21T23:48:29Z",
	  "dt_completed": null
	 }
	]

Getting the last authored Item, passing the request from standard input.

	$ echo '{ "limit": 1 }' | lrn-cli -l debug data /itembank/items
	2019-10-22 14:24:07,108 DEBUG:Reading request json from <_io.TextIOWrapper name='<stdin>' mode='r' encoding='UTF-8'>...
	2019-10-22 14:24:07,108 DEBUG:Sending GET request to https://data.learnosity.com/v1/itembank/items ...
	[
	 {
	  "reference": "1de592c9-0af5-4a58-8d47-75c304ec654e",
	  "title": null,
	  "workflow": null,
	  "metadata": null,
	  "note": "",
	  "source": "",
	  "definition": {
	   "widgets": [
	    {
	     "reference": "10f24a41-64ad-4d08-ab44-cc7469e324ba",
	     "widget_type": "response"
	    },
	    {
	     "reference": "27093a4b-19cb-4517-9d47-557241577ec2",
	     "widget_type": "response"
	    }
	   ],
	   "template": "dynamic"
	  },
	  "description": "",
	  "status": "published",
	  "questions": [
	   {
	    "reference": "10f24a41-64ad-4d08-ab44-cc7469e324ba",
	    "type": "mcq"
	   },
	   {
	    "reference": "27093a4b-19cb-4517-9d47-557241577ec2",
	    "type": "mcq"
	   }
	  ],
	  "features": [],
	  "tags": {}
	 }
	]


## Development

A few handy dependencies to support development can be installed in the
virtualenv with

    make venv-dev

### Running Tests

Run `make test`.

### Creating a new release

Run `make release`.

This requires GNU-flavoured UNIX tools (particularly `gsed`). If these are not
the default on your system, you'll need to install them, e.g. for OS X,

    brew install gsed coreutils

### Deploying to PyPi

Releases are automatically pushed to PyPi when created in GitHub, using the
[Trusted Publishers](https://docs.pypi.org/trusted-publishers/) system.

Manualy releases can be triggered with `make dist-upload`, provided you have the
necessary PyPi permissions.
