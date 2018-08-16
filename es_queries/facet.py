#POST /projectfinder/_search
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


#POST /projectfinder/_search
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


#GET /projectfinder/_search
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