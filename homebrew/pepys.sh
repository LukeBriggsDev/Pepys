/usr/libexec/path_helper -s;
export PATH=$PATH:/opt/homebrew/bin
echo $PATH;
export LANG="$(defaults read -g AppleLanguages | \
  sed '/"/!d;s/["[:space:]]//g;s/-/_/').UTF-8"
export HOMEBREW_CELLAR=$(brew --cellar)
$HOMEBREW_CELLAR/pepys/1.3.1/libexec/bin/python3 $HOMEBREW_CELLAR/pepys/1.3.1/lib/main/python/main.py