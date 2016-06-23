REPO_ROOT=$(pwd)
REQUIREMENTS="requirements.txt"
VIRTUALENVWRAPPER_PATH="/usr/local/bin/virtualenvwrapper.sh"

DJANGO_PROJECT_NAME="eng-ops"

# install git hooks
./tools/hooks/install.sh

# setup virtualenv
if [ -f $VIRTUALENVWRAPPER_PATH ]; then
    . $VIRTUALENVWRAPPER_PATH
fi
mkvirtualenv $DJANGO_PROJECT_NAME &&
pip install -r $REPO_ROOT/$REQUIREMENTS

cdsitepackages  # defined by virtualenvwrapper
if [ ! -e _virtualenv_path_extensions.pth ]; then
    # _virtualenv_path_extensions.pth has custom PYTHONPATH paths,
    # created by add2virtualenv
    add2virtualenv $REPO_ROOT $REPO_ROOT/external-apps $REPO_ROOT/external-libs
    echo cd $REPO_ROOT >> ~/.virtualenvs/$DJANGO_PROJECT_NAME/bin/postactivate
fi
cd -  # go back to the previous directory (before cdsitepackages)
