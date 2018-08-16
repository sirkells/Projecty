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