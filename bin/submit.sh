tar \
  --disable-copyfile \
  --exclude '*__pycache__*' \
  -czvf submit.tar.gz \
  bin \
  insta485 \
  package-lock.json \
  package.json \
  setup.py sql \
  webpack.config.js \
  deployed_index.html \
  deployed_index.log \
  deployed_bundle.js \
  deployed_bundle.log