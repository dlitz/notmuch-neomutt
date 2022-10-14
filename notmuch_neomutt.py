#!/usr/bin/env python3
# dlitz 2022

from subprocess import run, check_output
from urllib.parse import urlsplit, urljoin, urlencode, quote as urlquote
from pathlib import PurePath, Path
from argparse import Action, ArgumentParser, SUPPRESS, REMAINDER
import os
import sys
import json
import shlex

# exit codes from <sysexits.h>
EX_USAGE = 64
EX_CONFIG = 78


class ConfigurationError(Exception):
    "raised on configuration error (message will be shown without backtrace)"


def get_default_neomutt_exe():
    return os.environ.get("NOTMUCH_NEOMUTT_EXE", "neomutt")


def parse_args(parser):
    parser.description = """
    Launch neomutt(1) to view the results of a notmuch-search(1) query.
    """
    parser.allow_abbrev = False
    parser.prefix_chars = "-+"
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--showcmd", action="store_true", help="show the command only")
    g.add_argument("--showurl", action="store_true", help="show the mailbox URL only")
    g.add_argument("--showquery", action="store_true", help="show the query only")
    parser.add_argument(
        "-R",
        "--read-only",
        dest="read_only",
        action="store_true",
        default=None,
        help="open mailbox in read-only mode",
    )
    parser.add_argument(
        "+R",
        "--read-write",
        dest="read_only",
        action="store_false",
        help="open mailbox in read-write mode",
    )
    parser.add_argument(
        "--limit",
        metavar="number",
        type=int,
        help="restricts the number of messages/threads in the result",
    )
    parser.add_argument(
        "-t",
        "--type",
        choices=("messages", "m", "threads", "t"),
        default=None,
        help="""
            reads only matching messages, or whole threads (default: use
            NeoMutt configuration)
        """,
    )
    parser.add_argument(
        "--query",
        dest="query_type",
        choices=("infix", "sexp"),
        default="infix",
        help="notmuch query type (default: %(default)s)",
    )
    parser.add_argument("search_terms", metavar="search-term", nargs="*")
    parser.add_argument(
        "--neomutt-exe",
        metavar="path",
        default=get_default_neomutt_exe(),
        help="""neomutt executable to invoke (default: 'neomutt', or value of
        the NOTMUCH_NEOMUTT_EXE environment variable)""",
    )
    parser.add_argument("--neomutt-help", action="store_true", help="show neomutt help")
    parser.add_argument(
        "--neomutt-args",
        nargs=REMAINDER,
        action="extend",
        default=[],
        help="remaining arguments to be passed to neomutt",
    )

    parser.epilog = """
    Read-only mode configurable via
    `notmuch config set neomutt.read_only true`.
    """

    args, remaining_args = parser.parse_known_args()
    args.neomutt_args += remaining_args
    args.type = {'m': 'messages', 't': 'threads', None: None}[args.type]
    if args.read_only is None:
        args.read_only = get_notmuch_config_bool("neomutt.read_only")
    return args


def get_notmuch_config(item):
    return check_output(["notmuch", "config", "get", item], text=True).rstrip()


def get_notmuch_config_bool(item, nullable=True):
    rawval = get_notmuch_config(item)
    if not rawval:
        if nullable:
            return None
        else:
            raise ConfigurationError(f"config item required: {item}")
    bool_map = {"true": True, "false": False, "yes": True, "no": False}
    result = bool_map.get(rawval.lower(), None)
    if result is None:
        raise ConfigurationError(f"config item not a valid boolean: { {item: rawval} }")
    return result


def get_notmuch_mail_root():
    setting = "database.mail_root"
    mail_root = get_notmuch_config(setting)
    # database.mail_root is resolved relative to the user's home directory
    mail_root_path = Path("~").expanduser() / mail_root
    return mail_root_path


def notmuch_infix_quote_string(s):
    escaped = s.replace('"', '""')
    return f'"{escaped}"'


def notmuch_sexp_quote_string(s):
    escaped = s.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def showcmd(cmd):
    # print(f"{parser.prog}: debug: {args=!r}", file=sys.stderr)
    print(shlex.join(cmd))


def query_urlencode(dict_):
    return urlencode(dict_, quote_via=urlquote)


def main():
    parser = ArgumentParser()
    try:
        args = parse_args(parser)

        if args.neomutt_help:
            cmd = [args.neomutt_exe, "-h"]
            # --neomutt-help may be combined with --showcmd
            if args.showcmd:
                showcmd(cmd)
                return
            os.execvp(cmd[0], cmd)

        # Construct the query
        if not args.search_terms:
            parser.exit(
                EX_USAGE, f"Error: {parser.prog} requires at least one search term.\n"
            )
        query = " ".join(args.search_terms)
        if args.query_type == "sexp":
            query = f"sexp:{notmuch_infix_quote_string(query)}"

        if args.showquery:
            print(query)
            return

        # Construct the mailbox URL
        mail_root = get_notmuch_mail_root()
        qs = {'query': query}
        if args.type is not None:
            qs['type'] = args.type
        if args.limit is not None:
            qs['limit'] = args.limit
        u = urlsplit("notmuch:///")
        u = u._replace(path="//" + urlquote(str(mail_root)))
        u = u._replace(query=query_urlencode(qs))
        mailbox_url = u.geturl()

        if args.showurl:
            print(mailbox_url)
            return

        # Construct the command-line
        cmd = [args.neomutt_exe]
        if args.read_only:
            cmd.append("-R")
        cmd += ["-f", mailbox_url]
        cmd += args.neomutt_args

        if args.showcmd:
            showcmd(cmd)
            return

        os.execvp(cmd[0], cmd)

    except ConfigurationError as exc:
        parser.exit(EX_CONFIG, message=f"{parser.prog}: {str(exc)}\n")


if __name__ == "__main__":
    main()
