#use this for user skills and projects skills matching. save skills as a string of words and put it in the search query
GET /projectfinder/itproject/_search
{
  "query": {
    "multi_match": {
      "query": "pyhon",
      "fields": ["description", "title", "skills.keyword^2"]
    }
  }
}
###########################################
DELETE /projectfinder
GET _cat/indices?v

GET /projectfinder/_search
{
  "query": {
    "multi_match": {
      "query": "java sq",
      "fields": ["description", "title", "skills.keyword^2"],
      "fuzziness" : "AUTO",
      "prefix_length" : 2
    }
  }
}


GET /projectfinder/_search
{
    "query" : {
        "constant_score" : { 
            "filter" : {
                "term" : { 
                    "title" : "python developer"
                }
            }
        }
    }
}

#exact phrase search with location filter
GET /projectfinder/_search
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


#exact phrase search with location filter
GET /projectfinder/_search
{
    "query": {
        "bool": {
            "must": [
                {"match": {
                  "skills": {
                  "query": "[Python, Django]",
                  "operator": "and"
                }}}
            ],
            "filter": {
              "terms": {
                "location.keyword": ["Münster", "Berlin"]
              }
            }
        }
    }
}

#prefered multiple skills and location
GET /projectfinder/_search
{
    "query": {
        "bool": {
            "must": [
                {"match": {
                  "skills": {
                  "query": "[SAP]",
                  "operator": "and"
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

#multiple skills search with multiple location filter
GET /projectfinder/_search
{
    "query": {
        "bool": {
            "must": [
                {"match": {
                  "skills": {
                  "query": "[Data]",
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

#exact phrase search with location filter
GET /projectfinder/_search
{
    "query": {
        "bool": {
            "should": [
                {"match": {
                  "skills": {
                  "query": "[Python, Django, Javascript]",
                  "operator": "and"
                }}}
            ]
            
        }
    }
}

GET /projectfinder/_search
{
  "query": {
    "match": {
      "_all": {
        "query": "java developer",
        "operator": "and"
      },
      "location": {
        "query": "köln"
      }
    }
  }
}



GET /projectfinder/_search
{
    "query": {
        "constant_score" : {
            "filter" : {
                 "bool" : {
                    "must" : [
                        { "term" : { "skills" : "Python Developer" } }, 
                        { "term" : { "location" : "Köln" } } 
                    ]
                }
            }
        }
    }
}

GET /projectfinder/_search
{
    "dis_max": {
        "queries": [
            { "match": { "title": "python developer" }},
            { "match": { "location":  "köln" }}
        ]
    }
}

GET /projectfinder/_search
{
  "query": {
    "term": {
      "exact_value": "Köln" 
    }
  }
}


GET /projectfinder/_search
{
  "sort": [
    {
      "filter_date_post": {
        "order": "desc"
      }
    },
    "_score"
  ]
}
GET /projectfinder/_search
{
  "query": {
    "multi_match": {
      "query": "jva",
      "operator": "or",
      "zero_terms_query": "all",
      "fields": ["description", "title", "skills"]
    }
  }
}

GET /projectfinder/_search
{
  "query": {
        "bool": {
            "should": [
             
                {"match": {
                  "location": "Köln"
                }},
                {"match": {
                  "location": "Bonn "
                }}
            ]
           
            
            
        }                                                                        
  },
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

POST /projectfinder/_search
{
  "query": {
   "bool": {
     "must": [
      {
        "match": {
          "skills": {
          "query": "['Python','C', 'Django']"
          }
        }
      }
    ],
      "filter" : {
                "terms" : { 
                    "location" : ["bonn", "köln"]
                }
            }
        
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
POST /projectfinder/_search
{ 
  "query" : {
        "constant_score" : {
            "filter" : {
                "terms" : { 
                    "location" : ["bonn", "köln"]
                }
            }
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
PUT /projectmanager
{
    "settings": {
        "number_of_shards": 1, 
        "analysis": {
            "filter": {
                "autocomplete_filter": { 
                    "type":     "edge_ngram",
                    "min_gram": 2,
                    "max_gram": 20
                }
            },
            "analyzer": {
                "autocomplete": {
                    "type":      "custom",
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "autocomplete_filter" 
                    ]
                }
            }
        }
    }
}

GET /projectfinder_opt/_analyze
{
  "analyzer": "autocomplete",
  "text": "python"
}

PUT /projectmanager/_mapping/itproject
{
  "itproject": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "autocomplete"
      },
      "description": {
        "type": "text"
      }
    }
  }
}

GET _mapping