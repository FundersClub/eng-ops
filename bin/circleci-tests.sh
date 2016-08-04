set -e
run --concurrency multiprocessing --parallel-mode manage.py test --skip-migrations --noinput --split-to-bins=$CIRCLE_NODE_TOTAL --test-bin=$CIRCLE_NODE_INDEX --parallel 2
# TODO: Set up coverage tracking
# coverage combine
# coverage report
# bash <(curl -s https://codecov.io/bash) -t <token>
