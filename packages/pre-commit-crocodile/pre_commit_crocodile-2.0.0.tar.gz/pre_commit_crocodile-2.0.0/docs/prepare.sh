#!/bin/sh

# Configurations
set -e

# Variables
docs_path=$(cd "$(dirname "${BASH_SOURCE:-${0}}")" && pwd -P)
root_path="${docs_path%/*}"

# Prepare cache
rm -f "${docs_path}/.cache/*.md"
mkdir -p "${docs_path}/.cache/"
cp -rfv "${docs_path}/"*.md "${docs_path}/.cache/"

# Export index
cp -f "${root_path}/README.md" "${docs_path}/.cache/index.md"
sed -i '/Documentation:/{ N; d; }' "${docs_path}/.cache/index.md"

# Export commits
{
  echo ''
  echo '---'
  echo ''
  cz info | sed \
    -e '1{ /^$/d }' \
    -e '/^</,$ { /^</ { s/^/```powershell\n/ }; ${ s/^/```/ } }' \
    -e 's/^\([A-Za-z0-9 ]\{1,\}\): /**\1:** /g' \
    -e "s/ '\([A-Za-z0-9:!]\{1,\}\)' / \`\1\` /g" \
    -e "s/ \([A-Za-z0-9]\{1,\}\):\([ ,]\)/ \`\1:\`\2/g" \
    -e 's/^\([^#]\{1,\}\)$/\1  /g'
  echo ''
  echo '---'
  echo ''
  echo '## Commit example'
  echo ''
  echo '```ruby'
  cz example
  echo '```'
} >>"${docs_path}/.cache/commits.md"

# Export configurations/commitizen
{
  echo ''
  echo '---'
  echo ''
  echo '## Commitizen configurations'
  echo ''
  echo '**Sources / .cz.yaml:**'
  echo ''
  echo '```yaml'
  cat "${root_path}/.cz.yaml"
  echo '```'
} >>"${docs_path}/.cache/commitizen.md"

# Export configurations/pre-commit
{
  echo ''
  echo '---'
  echo ''
  echo '## Commitizen configurations'
  echo ''
  echo '**Sources / .pre-commit-config.yaml:**'
  echo ''
  echo '```yaml'
  cat "${root_path}/.pre-commit-config.yaml"
  echo '```'
} >>"${docs_path}/.cache/pre-commit.md"

# Export about/changelog
mkdir -p "${docs_path}/.cache/about/"
cp -f "${root_path}/CHANGELOG.md" "${docs_path}/.cache/about/changelog.md"

# Export about/license
{
  echo '# License'
  echo ''
  echo '---'
  echo ''
  cat "${root_path}/LICENSE"
} >"${docs_path}/.cache/about/license.md"

# Show cache
echo ' '
ls -laR "${docs_path}/.cache/"
echo ' '
