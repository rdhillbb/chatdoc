curl -X POST http://localhost:8050/ingestlocalweb/ \
     -H "Content-Type: application/json" \
     -d '{"request": "upload", "filedrawer": "GARLIC", "filename": "https://downloads.hindawi.com/journals/tswj/2021/8817288.pdf"}'

