# https://github.com/pyenv/pyenv-virtualenv
# brew install pyenv-virtualenv
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

source project
if [ "$1" == "setup" ]; then
  pyenv virtualenv "$PROJECT_PYTHON_VERSION" "$PROJECT_NAME"
  pyenv activate "$PROJECT_NAME"
  pyenv local "$PROJECT_NAME"
  pip install --upgrade pip
  pip install pip-tools
elif [ "$1" == "remove" ]; then
  pyenv uninstall "$PROJECT_NAME"
elif [ "$1" == "compile" ]; then
  pyenv activate "$PROJECT_NAME"
  pip-compile --upgrade requirements.in
elif [ "$1" == "install" ]; then
  pyenv activate "$PROJECT_NAME"
  pip install --upgrade pip
  pip install -r requirements.txt
else
  echo "Usage: $0 setup | remove | compile | install"
fi
