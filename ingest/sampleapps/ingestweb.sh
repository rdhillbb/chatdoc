curl -X POST http://localhost:8050/ingestlocalweb/ \
     -H "Content-Type: application/json" \
     -d '{"request": "upload", "filedrawer": "Garlic", "filename": "https://www.webmd.com/vitamins/ai/ingredientmono-300/garlic"}'
curl -X POST http://localhost:8050/ingestlocalweb/ \
     -H "Content-Type: application/json" \
     -d '{"request": "upload", "filedrawer": "TESTLA", "filename": "/Users/randolphhill/Downloads/tesla_report.pdf"}'

