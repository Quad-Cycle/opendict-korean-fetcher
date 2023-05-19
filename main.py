import odk
from neo4j import GraphDatabase
import sys

uri = 'bolt://localhost:7687'
username = 'neo4j'
password = '2019112073'
database_name = 'word-hypernyms'
driver = GraphDatabase.driver(uri, auth=(username, password), database=database_name)

files = ['resources/1146510_150000.xml', 'resources/1146510_50000.xml', 'resources/1146510_500000.xml', 'resources/1146510_400000.xml', 'resources/1146510_800000.xml', 'resources/1146510_900000.xml', 'resources/1146510_1168166.xml', 'resources/1146510_1050000.xml', 'resources/1146510_1150000.xml', 'resources/1146510_200000.xml', 'resources/1146510_300000.xml', 'resources/1146510_750000.xml', 'resources/1146510_650000.xml', 'resources/1146510_600000.xml', 'resources/1146510_700000.xml', 'resources/1146510_350000.xml', 'resources/1146510_250000.xml', 'resources/1146510_1100000.xml', 'resources/1146510_1000000.xml', 'resources/1146510_950000.xml', 'resources/1146510_850000.xml', 'resources/1146510_450000.xml', 'resources/1146510_550000.xml', 'resources/1146510_100000.xml']

od = odk.ODKReader()
data = od.get_data_by_file_reader('resources/1146510_100000.xml')

def make_create_node_queries(data):
    print("Making create node queries...")
    result = []
    for word, hypernyms in data:
        result.append(
            ("CREATE (item:Word{{name:'{}', hypernyms:{}}}) RETURN item".format(word, hypernyms))
        )
    print("Completed making create node queries!")
    return result

def make_create_relation_queries(data):
    print("Making create relation queries...")
    result = []
    for word, hypernyms in data:
        result.append(
            ("MATCH (a{{name:'{}'}}) MATCH (b{{name:'{}'}})".format(hypernyms[0], word) + 
             "CREATE (a) <- [r:hypernym] - (b) RETURN a, r, b")
        )
    print("Completed making create relation queries!")
    return result

def create_nodes(data):
    # 입력된 단어 데이터로 create 쿼리 집합 생성
    node_queries = make_create_node_queries(data)
    # 쿼리 실행 및 commit
    print("---------------------------------------")
    print("Running create node transactions...")
    with driver.session() as session:
        with session.begin_transaction() as tx:
            for query in node_queries:
                tx.run(query)
            tx.commit()
    print("Commited all of create node transactions!")

def create_relations(data):
    # 입력된 데이터 간의 관계를 추가하는 create edge 쿼리 집합 생성
    relation_queries = make_create_relation_queries(data)
    # 쿼리 실행 및 commit
    print("---------------------------------------")
    print("Running create relation transactions...")
    with driver.session() as session:
        with session.begin_transaction() as tx:
            for query in relation_queries:
                tx.run(query)
            tx.commit()
    print("Commited all of create relation transactions!")

create_nodes(data)
print()
# create_relations(data)
