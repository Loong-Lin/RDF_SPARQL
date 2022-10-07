import pandas as pd
from rdflib import Graph
import json


def query_data(sparql_query, file_path):
    """
    Query the rdf file with the given query string and return the results as a pandas Dataframe.
    """
    g = Graph().parse(file_path)
    query_res = g.query(sparql_query)
    result = query_res.serialize(encoding='utf-8', format='json')
    result = json.loads(result)
    print("result: \n", result["results"]["bindings"])
    return pd.json_normalize(result["results"]["bindings"])


def formate_data(result_table):
    """

    :param result_table: type is pandas.core.frame.DataFrame
    :return: pandas.core.frame.DataFrame
    """
    columns = list(result_table.columns)  # 获取列标题
    print("shape: ", type(result_table), result_table.shape)

    # print("head: \n", result_table.head())  # Viewing the first 5 lines
    new_colums = list()
    for item in columns:
        if item.endswith('.value'):
            new_colums.append(item)

    simple_table = result_table[new_colums]
    simple_table = simple_table.rename(columns=lambda col: col.replace(".value", ""))
    print("simple_table:\n ", simple_table)
    return simple_table


query = """
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>

    SELECT ?link ?name
    WHERE {
        ?link rdf:type foaf:Person .
        ?link foaf:nick ?name .
    }
    """


rdf_file_path = 'test_data/card.rdf'
result_ = query_data(query, rdf_file_path)
formate_data(result_)
