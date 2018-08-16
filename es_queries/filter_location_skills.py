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


#multiple skills search with multiple location filter
#GET /projectfinder/_search
{
    "query": {
        "bool": {
            "must": [
                {"match": {
                  "skills": {
                  "query": "[Python, Django, java]",
                  "operator": "and"
                }}},
                {"match": {
                  "location": {
                  "query": "[Münster, Berlin, Bonn]",
                  "operator": "or"
                }}}
            ]
        }
    }
    ,
  "aggs": {
    "Location": {
      "terms": {
        "field": "location.keyword",
        "size": 10
     
      }
    },
    "Skills": {
      "terms": {
        "field": "skills.keyword",
        "size": 10
      }
    }
  }
}