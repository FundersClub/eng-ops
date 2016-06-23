if ! [ -e .git ]; then
    echo "Please run this from repo root directory"
    exit 1
fi

cd .git/hooks
for i in pre-commit post-checkout; do
    rm -fv $i
    ln -sv ../../tools/hooks/$i
done
