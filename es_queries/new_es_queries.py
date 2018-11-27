#GET _cat/indices
#PUT itproject_clean
#DELETE itproject_clean
#DELETE projectfinder
#DELETE mongodb_meta

#GET projectfinder/itproject_clean/_mapping

#GET /projectfinder/itproject_clean/_search
{
    "query": {
        "bool": {
            "must": [
                {"match": {"bereich.group": "Development"}}
            ],
            "filter": {
              "term": {
                "region.bundesland.keyword": "Hessen"
              }
            }
        }
    }
}

#GET /projectfinder/itproject_clean/_search
{
    "query": {
        "bool": {
            "must": [
                {"match": {"bereich.group_type": "Business Intelligence"}}
            ]
        }
    }
}
#GET /projectfinder/itproject_clean/_search
{
  "query": {
        "bool": {
            "must": [
                {"match": {"bereich.group": "Infrastructure"}}
            ]
        }
    },
  "aggs": {
    "Category Filter": {
      "terms": {
        
        "field": "bereich.group_type.keyword",
        "size": 10
      }
    },
    "Region Filter": {
      "terms": {
        "field": "region.bundesland.keyword",
        "size": 10
      }
    },
    "Skill Filter": {
      "terms": {
        "field": "bereich.skill.keyword",
        "size": 10
      }
    }
  }
}

#GET /projectfinder/itproject_clean/_search
{
  "size": 0,
  "aggs" : {
    "messages" : {
      "filters" : {
        "filters" : {
          "Group" :   { "match" : { "bereich.group" : "Development"   }},
          "Mobile" : { "match" : { "bereich.group_type" : "Mobile" }}
        }
      }
    }
  }
}
#search with facet filters
#GET projectfinder/itproject_clean/_search
{
  "size": 10,
  "query": {
    "multi_match": {
      "query": "data science",
      "operator": "and",
      "fields": [
        "title^4",
        "description"
      ],
      "fuzziness": "AUTO",
      "prefix_length": 2
    }
  },
  "aggs": {
    "Group": {
      "terms": {
        "field": "bereich.group.keyword",
        "size": 10
      }
    },
    "Group Type": {
      "terms": {
        "field": "bereich.group_type.keyword",
        "size": 10
      }
    },
    "Group Stack": {
      "terms": {
        "field": "bereich.group_type_stack.keyword",
        "size": 10
      }
    },
    "Skill Filter": {
      "terms": {
        "field": "bereich.skill.keyword",
        "size": 10
      }
    },
    "Region Filter": {
      "terms": {
        "field": "region.bundesland.keyword",
        "size": 10
      }
    }
  }
}


#PUT /projectfinder
{
  "settings": {
    "number_of_shards": 1,
    "analysis": {
      "filter": {
        "autocomplete_filter": {
          "type": "edge_ngram",
          "min_gram": 2,
          "max_gram": 20
        }
      },
      "analyzer": {
        "autocomplete": {
          "type": "custom",
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

#PUT /projectfinder/_mapping/itproject
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



#PUT projectfinder
{
  "settings": {
    "number_of_shards": 5,
    "analysis": {
      "filter": {
        "autocomplete_filter": {
          "type": "edge_ngram",
          "min_gram": 2,
          "max_gram": 20
        }
      },
      "analyzer": {
        "autocomplete": {
          "type": "custom",
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



#PUT projectfinder/_mapping/itproject_clean
{
  "itproject_clean": { 
               "properties": { 
                   "title": { 
                       "type": "text",
                       "analyzer": "autocomplete"
                   },
                   "description": {
                       "type":  "text"
                   },
                   "bereich": {
                       "type":  "keyword"
                   },
                   "region": {
                       "type":  "keyword"
                   }
               }
           }
}

#PUT projectfinder/_mapping/itproject
{
  "itproject": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "autocomplete"
      },
      "description": {
        "type": "text"
      },
      "bereich": {
        "type": "keyword"
      },
      "region": {
        "type": "keyword"
      }
    }
  }
}


#GET /projectfinder/itproject_clean/_search
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


#GET projectfinder/_search
#GET projectfinder/itproject_clean/_search
{
  "query": {
    "multi_match": {
      "query": "Hessen",
      "fields": ["region.stadt"],
      "fuzziness" : "AUTO",
      "prefix_length" : 2
    }
  }
}
#DELETE projects






