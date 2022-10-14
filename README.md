<!-- Code blocks generated using 'update-readme.sh' -->
notmuch-neomutt
===============

A command-line helper script for viewing the results of a [Notmuch][] search
using [NeoMutt][].

It works by constructing a [notmuch:// URL][] and then passing it on the
neomutt command-line.

## Installation

    pip install git+https://github.com/dlitz/notmuch-neomutt

## Usage

Usage is similar to [notmuch-search(1)][].

`$ notmuch-neomutt --help`
```
usage: notmuch-neomutt [-h]
                       [--showcmd | --showurl | --showurl-strict | --showquery]
                       [-R] [+R] [--limit number] [-t {messages,m,threads,t}]
                       [--query {infix,sexp}] [--neomutt-exe path]
                       [--neomutt-help] [--neomutt-args ...]
                       [search-term ...]

Launch neomutt(1) to view the results of a notmuch-search(1) query.

positional arguments:
  search-term

options:
  -h, --help            show this help message and exit
  --showcmd             show the command only
  --showurl             show the mailbox URL only
  --showurl-strict      show the mailbox URL only (strict URL-encoding)
  --showquery           show the query only
  -R, --read-only       open mailbox in read-only mode
  +R, --read-write      open mailbox in read-write mode
  --limit number        restricts the number of messages/threads in the result
  -t {messages,m,threads,t}, --type {messages,m,threads,t}
                        reads only matching messages, or whole threads
                        (default: use NeoMutt configuration)
  --query {infix,sexp}  notmuch query type (default: infix)
  --neomutt-exe path    neomutt executable to invoke (default: 'neomutt', or
                        value of the NOTMUCH_NEOMUTT_EXE environment variable)
  --neomutt-help        show neomutt help
  --neomutt-args ...    remaining arguments to be passed to neomutt

Read-only mode configurable via `notmuch config set neomutt.read_only true`.
```

## Examples

Omit `--showcmd` to open neomutt instead of displaying the command.

#### Showing the command:

`$ notmuch neomutt --showcmd 'subject:"Test message"'`
```
neomutt -f 'notmuch:///home/user/Maildir?query=subject:"Test message"'
```

#### Showing just the URL:

`$ notmuch neomutt --showurl 'subject:"Test message"' --limit 100 -tt`
```
notmuch:///home/user/Maildir?query=subject:"Test message"&type=threads&limit=100
```

#### Showing just the URL (strict URI syntax):

`$ notmuch neomutt --showurl-strict 'subject:"Test message"' --limit 100 -tt`
```
notmuch:///home/user/Maildir?query=subject%3A%22Test%20message%22&type=threads&limit=100
```

#### S-expression queries (see [notmuch-sexp-queries(7)][]):

`$ notmuch neomutt --showcmd --query=sexp '(and (from test@example.com) (subject "Test message"))'`
```
neomutt -f 'notmuch:///home/user/Maildir?query=sexp:"(and (from test%40example.com) (subject ""Test message""))"'
```

#### Read-only mode:

`$ notmuch neomutt --showcmd -R 'subject:"Test message"'`
```
neomutt -R -f 'notmuch:///home/user/Maildir?query=subject:"Test message"'
```

#### Configuring read-only mode by default:

`$ notmuch config set neomutt.read_only true; notmuch neomutt --showcmd 'subject:"Test message"'`
```
neomutt -R -f 'notmuch:///home/user/Maildir?query=subject:"Test message"'
```

#### Read-write mode when configured read-only by default:

`$ notmuch config get neomutt.read_only ; notmuch neomutt --showcmd +R 'subject:"Test message"'`
```
true
neomutt -f 'notmuch:///home/user/Maildir?query=subject:"Test message"'
```

## See also

* [NeoMutt homepage][NeoMutt]
* [Notmuch homepage][Notmuch]
* [notmuch:// virtual mailbox feature for NeoMutt][notmuch:// URL]
* [notmuch-search manpage][notmuch-search(1)]
* [notmuch-search-terms manpage][notmuch-search-terms(7)]
* [notmuch s-expression queries manpage][notmuch-sexp-queries(7)]

## License

[> LICENSE](LICENSE)
<!-- BEGIN mdsh -->
MIT License

Copyright (c) 2022 Darsey Litzenberger

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
<!-- END mdsh -->

<!-- References -->

[NeoMutt]: <https://neomutt.org/> "The NeoMutt Project"

[Notmuch]: <https://notmuchmail.org/> "Notmuch -- Just an email system"

[notmuch:// URL]: <https://neomutt.org/feature/notmuch> "Notmuch Feature - NeoMutt"

[notmuch-search(1)]: <https://notmuchmail.org/manpages/notmuch-search-1/> "notmuch-search - search for messages matching the given search terms"

[notmuch-search-terms(7)]: <https://notmuchmail.org/manpages/notmuch-search-terms-7/> "notmuch-search-terms - syntax for notmuch queries"

[notmuch-sexp-queries(7)]: <https://notmuchmail.org/manpages/notmuch-sexp-queries-7/> "notmuch-sexp-queries - s-expression syntax for notmuch queries"
