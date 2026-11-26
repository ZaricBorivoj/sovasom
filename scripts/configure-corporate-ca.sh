#!/usr/bin/env bash
# Persist corporate CA settings without changing unrelated zsh configuration.
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 || ${1:-} == --help ]]; then
  echo "Usage: bash $0 PEM_BUNDLE [ZSHRC_PATH]"
  echo 'Defaults to ${ZDOTDIR:-$HOME}/.zshrc. Open a new terminal after setup.'
  [[ ${1:-} == --help ]] && exit 0
  exit 2
fi

bundle=$1
profile=${2:-${ZDOTDIR:-$HOME}/.zshrc}
if [[ ! -f "$bundle" || ! -r "$bundle" ]] ||
   ! grep -q -- '-----BEGIN CERTIFICATE-----' "$bundle" ||
   ! grep -q -- '-----END CERTIFICATE-----' "$bundle"; then
  echo 'Provide a readable PEM certificate bundle from your IT team.' >&2
  exit 1
fi
bundle="$(cd -- "$(dirname -- "$bundle")" && pwd -P)/$(basename -- "$bundle")"

start='# >>> sovasom corporate CA >>>'
end='# <<< sovasom corporate CA <<<'
temporary=$(mktemp)
trap 'rm -f -- "$temporary"' EXIT

# Validate marker structure before touching the profile. Append the replacement
# block last so older exports elsewhere in the profile cannot override it.
if [[ -e "$profile" ]]; then
  if ! awk -v start="$start" -v end="$end" '
    $0 == start { if (seen++ || inside) exit 1; inside=1; next }
    $0 == end { if (!inside) exit 1; inside=0; next }
    !inside { print }
    END { if (inside) exit 1 }
  ' "$profile" > "$temporary"; then
    echo 'The corporate CA block is malformed; repair its markers and retry.' >&2
    exit 1
  fi
fi
{
  printf '%s\n' "$start"
  for key in AWS_CA_BUNDLE SSL_CERT_FILE CURL_CA_BUNDLE REQUESTS_CA_BUNDLE NODE_EXTRA_CA_CERTS; do
    printf 'export %s=%q\n' "$key" "$bundle"
  done
  printf '%s\n' "$end"
} >> "$temporary"

mkdir -p -- "$(dirname -- "$profile")"
if [[ -f "$profile" ]] && cmp -s "$temporary" "$profile"; then
  echo 'Corporate CA settings are already up to date.'
else
  # Writing through the existing path preserves dotfile symlinks and permissions.
  cat "$temporary" > "$profile"
  echo "Installed corporate CA settings in $profile."
fi
echo 'Open a new terminal to load the settings automatically.'
