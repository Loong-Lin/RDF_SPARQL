import mkwikidata

query = """
SELECT DISTINCT ?cityLabel ?population ?gps
WHERE
{
  ?city wdt:P31/wdt:P279* wd:Q515 .
  ?city wdt:P1082 ?population .
  ?city wdt:P625 ?gps .
  SERVICE wikibase:label {
    bd:serviceParam wikibase:language "en" .
  }
}
ORDER BY DESC(?population) LIMIT 5
"""
query_result = mkwikidata.run_query(query, params={})
print("query_result type: ", type(query_result))
print("query_result: ", query_result)
query_result = query_result['results']['bindings']
print(type(query_result), len(query_result))

