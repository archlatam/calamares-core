#!/bin/bash
set -e

files=$(git diff --name-only)

icons=""

for f in $files; do
  case "$f" in
  PKGBUILD | .SRCINFO) icons="${icons}📦" ;;
  *.rs) icons="${icons}🦀" ;;
  *.desktop) icons="${icons}🖥" ;;
  *.png | *.svg) icons="${icons}🎨" ;;
  *.sh) icons="${icons}🧩" ;;
  esac
done

echo "📂 Cambios:"
echo "$files"
echo

echo "✏️ Commit:"
read -r msg

git add -A
git commit -m "$icons $msg"
git push

echo
echo "✅ Done"
