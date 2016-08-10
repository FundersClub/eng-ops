set -e
coverage run --concurrency multiprocessing --parallel-mode manage.py test --noinput
coverage combine
coverage report
# TODO: Set up coverage uploading
# bash <(curl -s https://codecov.io/bash) -t <token>
