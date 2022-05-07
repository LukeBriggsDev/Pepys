source "$HOME"/.zshrc
export HOMEBREW_CELLAR=$(brew --cellar)
export LANG="$(defaults read -g AppleLanguages | \
  sed '/"/!d;s/["[:space:]]//g;s/-/_/').UTF-8"
$HOMEBREW_CELLAR/pepys/1.5.4/libexec/bin/python3 $HOMEBREW_CELLAR/pepys/1.5.4/lib/main/python/main.py