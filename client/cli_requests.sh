wget --server-response \
    --output-document response.json \
    --header='Content-Type: application/json' \
    --post-data '{"songs": ["Panda"]}' \
    http://10.42.0.114:7777/api/recommend

cat response.json