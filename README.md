notmuch-neomutt
===============

Convenience tool for searching email with [Notmuch][] and displaying the
results using [NeoMutt][].

Usage is similar to [notmuch-search(1)][].

```
usage: notmuch-neomutt [-h] [--showcmd | --showurl | --showquery] [-R] [+R]
                       [--limit number] [-t {default,messages,m,threads,t}]
                       [--query {infix,sexp}] [--neomutt-exe path]
                       [--neomutt-help] [--neomutt-args ...]
                       [search-term ...]

Construct a notmuch:// URL from a notmuch-search(1) query, then open it with
neomutt.

positional arguments:
  search-term

options:
  -h, --help            show this help message and exit
  --showcmd             show the command only
  --showurl             show the mailbox URL only
  --showquery           show the query only
  -R, --read-only       open mailbox in read-only mode
  +R, --read-write      open mailbox in read-write mode
  --limit number        restricts the number of messages/threads in the result
  -t {default,messages,m,threads,t}, --type {default,messages,m,threads,t}
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

```console
$ notmuch neomutt --showcmd 'subject:"Test message"'
neomutt -f 'notmuch:///home/user/Maildir?query=subject%3A%22Test%20message%22'
```

#### Showing just the URL:

```console
$ notmuch neomutt --showurl 'subject:"Test message"' --limit 100 -tt
notmuch:///home/user/Maildir?query=subject%3A%22Test%20message%22&type=threads&limit=100
```

#### S-expression queries (see [notmuch-sexp-queries(7)][]):

```console
$ notmuch neomutt --showcmd --query=sexp '(and (from test@example.com) (subject "Test message"))'
neomutt -f 'notmuch:///home/user/Maildir?query=sexp%3A%22%28and%20%28from%20test%40example.com%29%20%28subject%20%22%22Test%20message%22%22%29%29%22'
```

#### Read-only mode:

```console
$ notmuch neomutt --showcmd -R 'subject:"Test message"'
neomutt -R -f 'notmuch:///home/user/Maildir?query=subject%3A%22Test%20message%22'
```

#### Configuring read-only mode by default:

```console
$ notmuch config set neomutt.read_only true

$ notmuch neomutt --showcmd 'subject:"Test message"'
neomutt -R -f 'notmuch:///home/user/Maildir?query=subject%3A%22Test%20message%22'
```

#### Read-write mode when configured read-only by default:

```console
$ notmuch config get neomutt.read_only
true

$ notmuch neomutt --showcmd +R 'subject:"Test message"'
neomutt -f 'notmuch:///home/user/Maildir?query=subject%3A%22Test%20message%22'
```

## See also

* [NeoMutt homepage][NeoMutt]
* [Notmuch homepage][Notmuch]
* [notmuch:// virtual mailbox feature for NeoMutt][notmuch:// URL]
* [notmuch-search manpage][notmuch-search(1)]
* [notmuch-search-terms manpage][notmuch-search-terms(7)]
* [notmuch s-expression queries manpage][notmuch-sexp-queries(7)]

<!-- References -->

[NeoMutt]: <https://neomutt.org/> "The NeoMutt Project"

[Notmuch]: <https://notmuchmail.org/> "Notmuch -- Just an email system"

[notmuch:// URL]: <https://neomutt.org/feature/notmuch> "Notmuch Feature - NeoMutt"

[notmuch-search(1)]: <https://notmuchmail.org/manpages/notmuch-search-1/> "notmuch-search - search for messages matching the given search terms"

[notmuch-search-terms(7)]: <https://notmuchmail.org/manpages/notmuch-search-terms-7/> "notmuch-search-terms - syntax for notmuch queries"

[notmuch-sexp-queries(7)]: <https://notmuchmail.org/manpages/notmuch-sexp-queries-7/> "notmuch-sexp-queries - s-expression syntax for notmuch queries"
