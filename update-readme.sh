#!/bin/bash
# dlitz 2022
set -eu

if ! command -v mdsh >/dev/null 2>&1 ; then
    echo >&2 "mdsh not found."
    echo >&2 "Try 'cargo install mdsh'"
    echo >&2 "See also: https://github.com/zimbatm/mdsh"
    exit 2
fi

tmpdir=$(mktemp -d)

test -d "$tmpdir"

cat >"$tmpdir/config" <<EOF
[database]
path=$tmpdir
mail_root=/home/user/Maildir
EOF

export COLUMNS=80
export NOTMUCH_CONFIG="$tmpdir/config"

set +e
mdsh
rc=$?
rm "$tmpdir/config"
rmdir "$tmpdir"
exit "$rc"
