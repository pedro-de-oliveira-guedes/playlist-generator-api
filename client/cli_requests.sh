wget --server-response \
    --output-document response.json \
    --header='Content-Type: application/json' \
    --post-data '{"songs": ["Panda"]}' \
    http://10.43.113.159:52055/api/recommend

cat response.json
