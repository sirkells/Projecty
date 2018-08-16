#GET /projectfinder/_search
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