#!/usr/bin/env python

import configparser
import datetime
import json
import logging
import os
import sys
import urllib
from collections import OrderedDict
from json.decoder import JSONDecodeError

import click
import requests
from learnosity_sdk.request import DataApi, Init
from pygments import formatters, highlight, lexers
from requests import Response

try:
    from trogon import tui
except ImportError:

    def tui():
        def decorator(f):
            return f

        return decorator


from ._version import __version__

# This is a public Learnosity Demos consumer
# XXX: never commit any other secret anywhere!
DEFAULT_CONSUMER_KEY = "yis0TYCu7U9V4o7M"
DEFAULT_CONSUMER_SECRET = "74c5fd430cf1242a527f6223aebd42d30464be22"

DEFAULT_API_ANNOTATIONS_URL = "https://annotations{region}{environment}.learnosity.com"
DEFAULT_API_ANNOTATIONS_VERSION = "latest"

DEFAULT_API_AUTHOR_URL = "https://authorapi{region}{environment}.learnosity.com"
DEFAULT_API_AUTHOR_VERSION = "latest"

DEFAULT_API_DATA_URL = "https://data{region}{environment}.learnosity.com"
DEFAULT_API_DATA_VERSION = "latest"

DEFAULT_API_EVENTS_URL = "https://events{region}{environment}.learnosity.com"
DEFAULT_API_EVENTS_VERSION = "latest"

DEFAULT_API_ITEMS_URL = "https://items{region}{environment}.learnosity.com"
DEFAULT_API_ITEMS_VERSION = "latest"

DEFAULT_API_QUESTIONS_URL = "https://questions{region}{environment}.learnosity.com"
DEFAULT_API_QUESTIONS_VERSION = "latest"

DEFAULT_API_REPORTS_URL = "https://reports{region}{environment}.learnosity.com"
DEFAULT_API_REPORTS_VERSION = "latest"

DOTDIR = os.path.expanduser("~") + "/.learnosity"
SHARED_CREDENTIALS_FILE = f"{DOTDIR}/credentials"
CONFIG_FILE = f"{DOTDIR}/config"

# TODO: use credentials from environment/file


class LrnCliException(click.ClickException):
    exit_code = 1
    logger = None

    def __init__(self, message, response=None):
        self.response = response
        if self.response:
            message += f"\nHTTP response: {self.response}"
        super().__init__(message)

    @classmethod
    def set_logger(cls, logger):
        cls.logger = logger

    def show(self):
        if self.logger:
            self.logger.error(self)
        else:
            click.ClickException.show(self)


@tui()
@click.group()
@click.option(
    "--consumer-key",
    "-k",
    help=f"API key for desired consumer, defaults to {DEFAULT_CONSUMER_KEY}",
    default=None,
    envvar="LRN_CONSUMER_KEY",
    show_envvar=True,
)
@click.option(
    "--consumer-secret",
    "-S",
    help=f"Secret associated with the consumer key, defaults to {DEFAULT_CONSUMER_SECRET}",
    default=None,
    envvar="LRN_CONSUMER_SECRET",
    show_envvar=True,
)
# Requests
@click.option("--file", "-f", type=click.File("r"), help="File containing the JSON request.", default=None)
@click.option("--file-is-usrequest", is_flag=True, default=False, help="Use the file as a usrequest")
@click.option(
    "--request-json", "-R", "request_json", help="JSON body of the request to send", metavar="JSON", default=None
)
@click.option(
    "--usrequest-json", "-U", "usrequest_json", help="JSON body of the usrequest to send", metavar="JSON", default=None
)
@click.option(
    "--output-payload",
    "-O",
    "output_mode",
    flag_value="http",
    help="Output signed and urlencoded HTTP payload to stdout rather than sending to server",
)
@click.option("--output-json", "-J", "output_mode", flag_value="json", help="Output signed JSON request")
@click.option("--get", "-g", "action", flag_value="get", default=True, help="Send a GET request [default]")
@click.option("--set", "-s", "action", flag_value="set", default=False, help="Send a SET request")
@click.option("--update", "-u", "action", flag_value="update", default=False, help="Send an UPDATE request")
@click.option("--delete", "-D", "action", flag_value="delete", default=False, help="Send a DELETE request")
@click.option("--dump-meta", "-m", is_flag=True, default=False, help="output meta object to stderr")
@click.option("--domain", "-d", help="Domain to use for web API requests", default="localhost")
# Environment
@click.option("--region", "-r", help="API region to target", envvar="LRN_REGION", show_envvar=True)
@click.option("--environment", "-e", help="API environment to target", envvar="LRN_ENVIRONMENT", show_envvar=True)
@click.option("--version", "-v", help="API version to target", envvar="LRN_VERSION", show_envvar=True)
# Configuration
@click.option(
    "--shared-credentials-file",
    "-c",
    type=click.File("r"),
    help=f"Credentials file to use for profiles definition, defaults to {SHARED_CREDENTIALS_FILE}",
    default=None,
    envvar="LRN_SHARED_CREDENTIALS_FILE",
    show_envvar=True,
)
@click.option(
    "--config-file",
    "-C",
    type=click.File("r"),
    help=f"Configuration file to use for profiles definition, defaults to {CONFIG_FILE}",
    default=None,
    envvar="LRN_CONFIG_FILE",
    show_envvar=True,
)
@click.option(
    "--profile",
    "-p",
    help="Profile to use (provides default consumer key and secret from the credentials, "
    "as well as environment and region from the config)",
    envvar="LRN_PROFILE",
    show_envvar=True,
)
# Logging
@click.option("--log-level", "-l", default="info", help="log level")
@click.option("--requests-log-level", "-L", default="warning", help="log level for the HTTP requests")
@click.pass_context
def cli(
    ctx,
    consumer_key,
    consumer_secret,
    file,
    file_is_usrequest=False,
    request_json=None,
    usrequest_json=None,
    output_mode=False,
    dump_meta=False,
    domain="localhost",
    environment=None,
    region=None,
    version=None,
    profile=None,
    shared_credentials_file=None,
    config_file=None,
    log_level="info",
    requests_log_level="warning",
    action="get",
):
    """Prepare and send requests to Learnosity APIs

    If neither --file nor --request-json are specified, the request will be read from STDIN.
    An empty input will be defaulted to `{}`, with a warning.
    """

    ctx.ensure_object(dict)

    ctx.obj["consumer_key"] = consumer_key
    ctx.obj["consumer_secret"] = consumer_secret

    if file_is_usrequest:
        ctx.obj["usrequest_file"] = file
    else:
        ctx.obj["request_file"] = file
    ctx.obj["output_mode"] = output_mode
    ctx.obj["request_json"] = request_json
    ctx.obj["usrequest_json"] = usrequest_json
    ctx.obj["action"] = action
    ctx.obj["dump_meta"] = dump_meta
    ctx.obj["domain"] = domain

    ctx.obj["region"] = region
    ctx.obj["environment"] = environment
    ctx.obj["version"] = version

    ctx.obj["shared_credentials_file"] = shared_credentials_file
    ctx.obj["config_file"] = config_file
    ctx.obj["profile"] = profile

    logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=log_level.upper())

    requests_logger = logging.getLogger("urllib3")
    requests_logger.setLevel(requests_log_level.upper())
    requests_logger.propagate = True

    logger = logging.getLogger()
    LrnCliException.set_logger(logger)
    ctx.obj["logger"] = logger


@cli.command()
def version():
    """Show lrn-cli version information"""
    click.echo(f"lrn-cli v{__version__}")


@cli.command()
@click.argument("endpoint_url")
@click.pass_context
def annotations(ctx, endpoint_url):
    """Make a request to Annotations API.

    The endpoint_url can be:

    - a full URL: https://annotations.learnosity.com/v2023.2.LTS/annotations

    - a REST path, with or without version:

      - /developer/annotations

      - /annotations

    Examples:

        lrn-cli -R '{"group_id":"a91faa6e-8bd2-4365-872d-f644f1f41853"}' annotations annotations
    """
    response, meta = _get_api_response(
        ctx, "annotations", endpoint_url, DEFAULT_API_ANNOTATIONS_URL, DEFAULT_API_ANNOTATIONS_VERSION
    )

    _output_response(response, meta, ctx.obj["dump_meta"])

    if not meta["status"]:
        ctx.exit(1)


@cli.command()
@click.argument("endpoint_url")
@click.pass_context
def author(ctx, endpoint_url):
    """Make a request to Author API.

    The endpoint_url can be:

    - a full URL: https://authorapi.learnosity.com/v2020.2.LTS/itembank/itemlist

    - a REST path, with or without version:

      - /developer/itembank/itemlist

      - itembank/itemlist

    Examples:

        lrn-cli -R '{ "mode": "itemlist", "user": { "id": "lrn-cli user" } }' author itembank/itemlist

    NOTE: The request needs to be an empty string, not an empty JSON object.

    """
    response, meta = _get_api_response(ctx, "author", endpoint_url, DEFAULT_API_AUTHOR_URL, DEFAULT_API_AUTHOR_VERSION)

    _output_response(response, meta, ctx.obj["dump_meta"])

    if not meta["status"]:
        ctx.exit(1)


@cli.command()
@click.argument("endpoint_url")
@click.option("--limit", "-l", "limit", help="Maximum `limit` of object to request at once")
@click.option(
    "--reference", "-r", "references", help="`reference` to request (can be used multiple times", multiple=True
)
@click.option(
    "--recurse", "-R", "do_recurse", is_flag=True, default=False, help="Automatically recurse using the next token"
)
@click.option(
    "--page-size",
    "-P",
    "page_size",
    default=50,
    type=int,
    help="Split out main data arrays into multiple pages when SETting",
)
@click.pass_context
def data(ctx, endpoint_url, references=None, limit=None, do_recurse=False, page_size=None):
    """Make a request to Data API.

    The endpoint_url can be:

    - a full URL: https://data.learnosity.com/v1/itembank/items

    - a REST path, with or without version:

      - /v1/itembank/items

      - itembank/items

    Example:

        lrn-cli -R '{}' data itembank/items -l 1

    """
    ctx.ensure_object(dict)
    logger = ctx.obj["logger"]

    consumer_key, consumer_secret, version, region, environment = _get_profile(ctx, DEFAULT_API_DATA_VERSION)

    action = ctx.obj["action"]
    data_request = _get_request(ctx)
    if not data_request:
        data_request = {}
    endpoint_url = _build_endpoint_url(endpoint_url, DEFAULT_API_DATA_URL, version, region, environment)

    if len(references) > 0:
        if "references" in data_request:
            logger.warning("Overriding `references` in request with `--references` from the command line")
        data_request["references"] = references
    if limit:
        if "limit" in data_request:
            logger.warning("Overriding `limit` in request with `--limit` from the command line")
        data_request["limit"] = limit

    if do_recurse and action not in ["get"]:
        logger.warning(f"Recursion not available for action {action}")

    data_attribute = endpoint_url.split("/")[-1]

    # Sessions submission doesn't use the same format as other requests
    if data_attribute == "sessions":
        data_attribute = "data"

    output_mode = ctx.obj["output_mode"]
    try:
        r = _send_json_request(
            endpoint_url,
            consumer_key,
            consumer_secret,
            data_request,
            action,
            logger,
            do_recurse,
            page_size,
            data_attribute,
            output_mode,
        )
    except Exception as e:
        raise LrnCliException(f"Exception sending JSON request to {endpoint_url}:  {e}")

    if output_mode:
        ctx.exit(0)

    response = _validate_response(r, ctx, url=endpoint_url)
    if response is None:
        return False

    data = response.get("data")
    meta = response.get("meta")

    _output_response(data, meta, ctx.obj["dump_meta"])

    if not response["meta"]["status"]:
        ctx.exit(1)


@cli.command()
@click.argument("endpoint_url")
@click.option("--user-id", "-u", required=True, help="`user_id` (to use in the security packet)")
@click.pass_context
def events(ctx, endpoint_url, user_id):
    """Make a request to Events API.

    The endpoint_url can be:

    - a full URL: https://events.learnosity.com/v2023.2.LTS/authenticate

    - a REST path, with or without version:

      - /developer/authenticate

      - /authenticate

    Example:

        lrn-cli -R '{}' events authenticate -u 'test'

    """
    response, meta = _get_api_response(
        ctx, "events", endpoint_url, DEFAULT_API_EVENTS_URL, DEFAULT_API_EVENTS_VERSION, user_id
    )

    _output_response(response, meta, ctx.obj["dump_meta"])

    if not meta["status"]:
        ctx.exit(1)


@cli.command()
@click.argument("endpoint_url")
@click.pass_context
def items(ctx, endpoint_url):
    """ Make a request to Items API.

    The endpoint_url can be:

    - a full URL: https://items.learnosity.com/v2021.1.LTS/activity

    - a REST path, with or without version:

      - /developer/activity

      - activity

    Example:

        \b
        lrn-cli -m \\
            -R '{ "user_id": "lrn-cli",
                  "activity_id": "lrn-cli_example",
                  "session_id": "e0fa16e3-e763-4125-8708-60c04251de47",
                  "rendering_type": "assess",
                  "items": [ "item_1" ],
                  "name": "lrn-cli example"
                }' \\
             items activity

    """
    response, meta = _get_api_response(ctx, "items", endpoint_url, DEFAULT_API_ITEMS_URL, DEFAULT_API_ITEMS_VERSION)

    _output_response(response, meta, ctx.obj["dump_meta"])

    if not meta["status"]:
        ctx.exit(1)


@cli.command()
@click.argument("endpoint_url")
@click.option("--user-id", "-u", required=True, help="`user_id` (to use in the security packet)")
@click.pass_context
def questions(ctx, endpoint_url, user_id):
    """ Make a request to Questions API.

    The endpoint_url can be:

    - a full URL: https://questions.learnosity.com/v2021.1.LTS/questionresponses

    - a REST path, with or without version:

      - /developer/questionresponses

      - questionresponses

    Note that requests to this API need to go through the `usrequest`, and require a `user_id`

    Example:

        \b
        lrn-cli -m \\
            -R '{}' \\
            -U '{ "questionResponseIds":
                  [ "0034_demo-user_04c389f8-a306-4f11-b259-105dc4c6932d_f167c24c98ea6415d9a7b227714f491d"]
                }' \\
            questions questionresponses -u demo-user

    """
    response, meta = _get_api_response(
        ctx, "questions", endpoint_url, DEFAULT_API_QUESTIONS_URL, DEFAULT_API_QUESTIONS_VERSION, user_id
    )

    _output_response(response, meta, ctx.obj["dump_meta"])

    if not meta["status"]:
        ctx.exit(1)


@cli.command()
@click.argument("endpoint_url")
@click.pass_context
def reports(ctx, endpoint_url):
    """ Make a request to Reports API.

    The endpoint_url can be:

    - a full URL: https://reports.learnosity.com/v2020.2.LTS/init

    - a REST path, with or without version:

      - /developer/init

      - init

    Example:

        \b
        lrn-cli \\
            -R '{
                "reports": [
                    {
                        "user_id": "demo_student",
                        "session_id": "6e15d841-e6f0-419f-9fa5-eac62b7b102b",
                        "id": "session-detail-by-item",
                        "type": "session-detail-by-item"
                    }
                ]
            }' \\
            reports init

    """
    response, meta = _get_api_response(
        ctx, "reports", endpoint_url, DEFAULT_API_REPORTS_URL, DEFAULT_API_REPORTS_VERSION
    )

    _output_response(response, meta, ctx.obj["dump_meta"])

    if not meta["status"]:
        ctx.exit(1)


def _get_profile(ctx, default_version=None):
    """
    Returns profile information based on CLI option and config:
    * consumer_key,
    * consumer_secret,
    * version,
    * region,
    * environment
    """
    logger = ctx.obj["logger"]
    profile_name = ctx.obj["profile"]

    # Changed in version 3.6: With the acceptance of PEP 468, order is retained for keyword
    # arguments passed to the OrderedDict constructor and its update() method.
    profile_params = OrderedDict(
        # credentials
        consumer_key=DEFAULT_CONSUMER_KEY,
        consumer_secret=DEFAULT_CONSUMER_SECRET,
        # config
        version=default_version,
        region="",
        environment="",
    )

    if profile_name:
        shared_credentials_file = ctx.obj["shared_credentials_file"]
        if not shared_credentials_file:
            shared_credentials_file = open(SHARED_CREDENTIALS_FILE, "r")
        credentials = configparser.ConfigParser()
        credentials.read_file(shared_credentials_file)

        if not ctx.obj["config_file"]:
            try:
                ctx.obj["config_file"] = open(CONFIG_FILE, "r")
            except FileNotFoundError:
                logger.debug(f"Config file not found: {CONFIG_FILE}")
        config_file = ctx.obj["config_file"]

        # look for profile in config
        if config_file:
            config = configparser.ConfigParser()
            config.read_file(config_file)

            if profile_name not in config:
                logger.debug(f"Profile {profile_name} not found in config {config_file.name}")
            else:
                for key in ["version", "region", "environment"]:
                    if key in config[profile_name]:
                        profile_params[key] = config[profile_name][key]
                # XXX: limited source_profile support: only allow to share credentials for now
                if "source_profile" in config[profile_name]:
                    profile_name = config[profile_name]["source_profile"]

        if profile_name not in credentials:
            logger.warning(
                f"Profile {profile_name} not found in credentials file {shared_credentials_file.name}, "
                "using learnosity-demos credentials..."
            )
        else:
            for key in ["consumer_key", "consumer_secret"]:
                if key in credentials[profile_name]:
                    profile_params[key] = credentials[profile_name][key]

    # override everything with CLI/env config
    for key in profile_params.keys():
        if ctx.obj[key]:
            profile_params[key] = ctx.obj[key]

    return profile_params.values()


def _get_request(ctx, field="request"):
    request = None
    request_file = field + "_file"
    file = None
    if request_file in ctx.obj:
        file = ctx.obj[request_file]
    logger = ctx.obj["logger"]
    request_json = ctx.obj[field + "_json"]

    if request_json is not None:
        logger.debug(f"Using {field} JSON from command line argument")
        try:
            return json.loads(request_json)
        except JSONDecodeError as e:
            logger.warning(f"Invalid JSON ({e}), using empty {field}")

    elif file is not None:
        if file.isatty():
            # Make sure the user is aware they need to enter something
            logger.info(f"Reading {field} JSON from {file}...")
        else:
            logger.debug(f"Reading {field} JSON from {file}...")

        try:
            request = json.load(file)
        except JSONDecodeError as e:
            logger.warning(f"Invalid JSON ({e}), using empty {field}")

    return request


def _add_user(request):
    if "user" in request:
        return request

    request["user"] = {
        "id": "lrn-cli",
        "firstname": "Learnosity",
        "lastname": "CLI",
        "email": "lrn-cli@learnosity.com",
    }

    return request


def _build_endpoint_url(endpoint_url, default_url, version, region="", environment=""):
    if region:
        region = f"-{region}"
    if environment not in ["", "prod", "production"]:
        environment = f".{environment}"

    if not endpoint_url.startswith("http"):
        if not endpoint_url.startswith("/"):  # Prepend leading / if missing
            endpoint_url = f"/{endpoint_url}"
        if (
            not endpoint_url.startswith("/v")
            and not endpoint_url.startswith("/latest")
            and not endpoint_url.startswith("/developer")
        ):  # API version
            endpoint_url = f"/{version}{endpoint_url}"

        endpoint_url = default_url.format(region=region, environment=environment) + endpoint_url
    return endpoint_url


def _get_api_response(ctx, api, endpoint_url, default_url, default_version, user_id=None):
    ctx.ensure_object(dict)
    logger = ctx.obj["logger"]
    domain = ctx.obj["domain"]

    consumer_key, consumer_secret, version, region, environment = _get_profile(ctx, default_version)

    api_request = _get_request(ctx)
    api_usrequest = _get_request(ctx, "usrequest")
    # XXX: This may not be relevant to all APIs, but it's fine as long as it doesn't break.
    if api_request:
        api_request = _add_user(api_request)
    endpoint_url = _build_endpoint_url(endpoint_url, default_url, version, region, environment)
    action = ctx.obj["action"]
    output_mode = ctx.obj["output_mode"]

    try:
        r = _send_www_encoded_request(
            api,
            endpoint_url,
            consumer_key,
            consumer_secret,
            logger,
            api_request,
            action,
            api_usrequest,
            user_id,
            domain,
            output_mode,
        )
    except requests.RequestException as e:
        raise LrnCliException(f"Exception sending Web request to {endpoint_url}: {e}")

    if output_mode:
        ctx.exit(0)

    response = _validate_response(r, ctx)
    if response is None:
        return False

    return response["data"], response["meta"]


def _send_www_encoded_request(
    api,
    endpoint_url,
    consumer_key,
    consumer_secret,
    logger,
    request=None,
    action="get",
    usrequest=None,
    user_id=None,
    domain="localhost",
    output_mode=None,
):
    if request is None and api == "questions":
        request = {}

    security = _make_security_packet(consumer_key, consumer_secret, user_id, domain)

    init = Init(api, security, consumer_secret, request)
    security["signature"] = init.generate_signature()

    # XXX: some hacks for the signed data to match
    if api == "items":
        # api-items lifts the the user_id from the request into the security object
        if "user_id" not in security and "user_id" in request:
            security["user_id"] = request["user_id"]

    form = {
        "action": action,
        "security": json.dumps(security),
    }

    if request:
        form["request"] = init.generate_request_string()
    if usrequest:
        form["usrequest"] = json.dumps(usrequest)

    if _handle_output_mode(output_mode, form):
        return

    logger.debug(f"Sending request to {endpoint_url}: {form}")

    return requests.post(endpoint_url, data=form)


def _send_json_request(
    endpoint_url,
    consumer_key,
    consumer_secret,
    request,
    action,
    logger,
    do_recurse=False,
    page_size=None,
    data_attribute="data",
    output_mode=False,
):
    data_api = DataApi()

    security = _make_security_packet(consumer_key, consumer_secret)

    payload = {
        "action": action,
        "request": request,
        "security": security,
    }
    logger.debug(f"Sending request to {endpoint_url}: {payload}")

    if output_mode:
        init = Init("data", security, consumer_secret, request)
        payload = init.generate()
    if _handle_output_mode(output_mode, payload):
        return

    if do_recurse and action in ["get"]:
        meta = {
            "_comment": "fake meta recreated by lrn-cli for failing initial recursive request",
            "status": "false",
        }
        data = None
        logger.debug("Iterating through pages of data...")

        for i, r_iter in enumerate(data_api.request_iter(endpoint_url, security, consumer_secret, request, action)):
            meta = r_iter["meta"]
            new_data = r_iter["data"]
            data = _merge_returned_data(data, new_data)
            logger.debug(f"Got page {i} with {len(new_data)} new objects")

        meta["records"] = len(data)
        r = {
            "meta": meta,
            "data": data,
        }

    elif page_size and action in ["set", "update"]:
        meta = {
            "_comment": "fake meta recreated by lrn-cli for failing initial paginated request",
            "status": "false",
        }
        data = None
        logger.debug(f"Sending `{data_attribute}` array as multiple pages of {page_size} objects ...")

        for i, data_page in enumerate(_paginate(request[data_attribute], page_size)):
            logger.debug(f"Sending page {i} ...")
            request[data_attribute] = data_page
            r = data_api.request(endpoint_url, security, consumer_secret, request, action)
            # XXX We don't want to pass the context so far down... but we want some validation/JSON
            response = _validate_response(r, url=endpoint_url)
            meta = response.get("meta")
            new_data = response.get("data")
            data = _merge_returned_data(data, new_data)

        meta["records"] = len(data)
        r = {
            "meta": meta,
            "data": data,
        }

    else:
        r = data_api.request(endpoint_url, security, consumer_secret, request, action)

    return r


def _merge_returned_data(data, new_data):
    """
    >>> _merge_returned_data(None, ['bob'])
    ['bob']
    >>> _merge_returned_data(None, {'bob': 'bla'})
    {'bob': 'bla'}
    >>> _merge_returned_data(['bib'], ['bob'])
    ['bib', 'bob']

    >>> _merge_returned_data(None, {'bob': 'bla'})
    {'bob': 'bla'}
    >>> _merge_returned_data({'bib': 'blu'}, {'bob': 'bla'})
    {'bib': 'blu', 'bob': 'bla'}

    >>> _merge_returned_data(1, 2)
    Traceback (most recent call last):
    ...
    TypeError: Unexpected return data type: not list or dict
    >>> _merge_returned_data({'bib': 'blu'}, ['bob'])
    Traceback (most recent call last):
    ...
    TypeError: data and new_data have different types
    >>> _merge_returned_data(['bib'], {'bob': 'bla'})
    Traceback (most recent call last):
    ...
    TypeError: data and new_data have different types
    """
    if data is None:
        data = new_data
    elif type(data) != type(new_data):
        raise TypeError("data and new_data have different types")
    elif type(data) is list:
        data += new_data
    elif type(data) is dict:
        data.update(new_data)
    else:
        raise TypeError("Unexpected return data type: not list or dict")
    return data


def _paginate(data: list, page_size: int):
    """
    >>> _paginate([1], 0)
    [[1]]
    >>> _paginate([1], 2)
    [[1]]
    >>> _paginate([1,2,3], 2)
    [[1, 2], [3]]
    """
    if page_size == 0:
        return [data]
    pages = [data[i : i + page_size] for i in range(0, len(data), page_size)]
    return pages


def _make_security_packet(consumer_key, consumer_secret, user_id=None, domain="localhost"):
    """
    >>> s = _make_security_packet('consumer_key', 'consumer_secret', 'user_id', 'domain')  # doctest: +ELLIPSIS
    >>> s['consumer_key'] == 'consumer_key'
    True
    >>> s['domain'] == 'domain'
    True
    >>> s['user_id'] == 'user_id'
    True
    >>> type(s['timestamp']) is str
    True
    """

    security = {
        "consumer_key": consumer_key,
        "domain": domain,
        "timestamp": datetime.datetime.utcnow().strftime("%Y%m%d-%H%M"),
    }

    if user_id:
        security["user_id"] = user_id

    return security


def _validate_response(r, ctx=None, url=None):
    logger = logging
    if ctx and ctx.obj:
        logger = ctx.obj["logger"]

    try:
        response = _decode_response(r, logger)
    except Exception as e:
        raise LrnCliException(f"Exception decoding response: {e}", response=r.text)

    if not url:
        url = r.url

    if not response["meta"]["status"]:
        logger.error(f"Incorrect status for request to {url}: {response['meta']['message']}")

    return response


def _decode_response(response, logger):
    if type(response) == Response:
        if response.status_code > 299:
            logger.error(
                "Error %d sending request to %s: %s"
                %
                # TODO: try to extract an error message from r.json()
                (response.status_code, response.url, response.text)
            )
        response = response.json()
    return response


def _handle_output_mode(output_mode: str, payload: dict) -> bool:
    if output_mode == "http":
        for k in payload:
            if type(payload[k]) == dict:
                payload[k] = json.dumps(payload[k])
        print(urllib.parse.urlencode(payload))
        return True
    elif output_mode == "json":
        for k in payload:
            try:
                parsed = json.loads(payload[k])
                payload[k] = parsed
            except:
                pass
        _output_json(payload)
        return True
    return False


def _output_response(response, meta, dump_meta=False):
    if dump_meta and meta:
        _output_json(meta, sys.stderr)
    _output_json(response)


def _output_json(data, stream=None):
    colorise = True
    if stream is None:
        stream = sys.stdout
    if not stream.isatty():
        colorise = False

    outJson = json.dumps(data, indent=True)
    if colorise:
        outJson = highlight(outJson, lexers.JsonLexer(), formatters.TerminalFormatter())
    stream.write(outJson + "\n")
