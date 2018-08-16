#exact phrase search with location filter
#GET /projectfinder/_search
{
    "query": {
        "bool": {
            "must": [
                {"match": {"skills": "Python"}}
            ],
            "filter": {
              "term": {
                "location": "köln"
              }
            }
        }
    }
}
