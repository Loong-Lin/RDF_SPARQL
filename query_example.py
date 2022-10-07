from rdflib import Graph
import pandas as pd
import json
file_path = "test_data/myPC.rdf"
# file_path = "test_data/card2.ttl"
# Create a Graph, pare in Internet data
# source_url = "http://www.w3.org/People/Berners-Lee/card"
# source_url = "http://dbpedia.org/sparql"
g = Graph().parse(file_path)

g.serialize(destination=file_path, encoding='utf-8', format='xml')
# Query the data in g using SPARQL
# This query returns the 'name' of all ``foaf:Person`` instances
q = """
    PREFIX foaf2: <http://xmlns.com/foaf/0.1/>

    SELECT ?name
    WHERE {
        ?p rdf:type foaf2:Person .
        ?p foaf2:name ?name .
    }
"""

q2 = """

    SELECT distinct ?name
    WHERE {
        [] a ?name .
    }
"""
q3 = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT distinct *
    WHERE {
        ?name rdfs:label "A211223"@en 
    }
"""

q4 = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT distinct ?name ?label
    WHERE {
        ?name a <http://www.w3.org/2002/07/owl#Class> .
        ?name rdfs:label ?label
    }
"""

res = g.query(q4)
# result = res.serialize(encoding='utf-8', format='json').decode('utf-8')
# result = res.serialize(encoding='utf-8', format='txt').decode('utf-8')
print("res len: ", len(res))
result = res.serialize(encoding='utf-8', format='json').decode('utf-8')
result = json.loads(result)
result_table = pd.json_normalize(result["results"]["bindings"])
columns = list(result_table.columns)  # 获取列标题
print("shape: ", type(result_table), result_table.shape)
print(result_table)
# Apply the query to the graph and iterate through results

