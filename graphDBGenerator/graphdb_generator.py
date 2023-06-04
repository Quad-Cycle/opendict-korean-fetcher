from neo4j import GraphDatabase
import time
from tqdm import tqdm
from collections import defaultdict

class GraphDBGenerator:
    uri = 'bolt://localhost:7687'
    username = 'neo4j'
    password = '00000000'
    database_name = 'word-hypernyms'
    driver = GraphDatabase.driver(uri, auth=(username, password), database=database_name)

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

    def merge_node_with_relations_queries(self, data):
        print("Making create nodes with relation queries...")
        result = []
        for word, hypernyms in data:
            for hypernym in hypernyms:
                result.append(
                    ("MERGE (a:Word{{name:'{}'}}) MERGE (b:Word{{name:'{}'}}) MERGE (a)-[:HYPERNYM]->(b)".format(word, hypernym))
                )
        print("Completed making create nodes with relation queries!")
        return result

    def search_HYPERNYM_queries(self, input_word):
        print("Making search queries...")
        result = ("match (a:Word{{name:'{}'}}) - [r:HYPERNYM] -> (b:Word) return b.name as hypernym".format(input_word))
        print("Completed making search queries!")
        return result

    def create_nodes(self, data):
        # 입력된 단어 데이터로 create 쿼리 집합 생성
        node_queries = self.make_create_node_queries(data)
        # 쿼리 실행 및 commit
        print("---------------------------------------")
        print("Running create node transactions...")
        with self.driver.session() as session:
            with session.begin_transaction() as tx:
                for query in node_queries:
                    tx.run(query)
                tx.commit()
        print("Commited all of create node transactions!")

    def create_relations(self, data):
        # 입력된 데이터 간의 관계를 추가하는 create edge 쿼리 집합 생성
        relation_queries =self.make_create_relation_queries(data)
        # 쿼리 실행 및 commit
        print("---------------------------------------")
        print("Running create relation transactions...")
        with self.driver.session() as session:
            with session.begin_transaction() as tx:
                for query in relation_queries:
                    tx.run(query)
                tx.commit()
        print("Commited all of create relation transactions!")

    def create_nodes_with_relations(self, data):
        # 데이터와 관계를 생성하면서 노드 중복 방지하는 쿼리 집합 생성
        nodes_with_relation_queries = self.merge_node_with_relations_queries(data)
        # 쿼리 실행 및 commit
        print("---------------------------------------")
        print("Running create nodes with relation transactions...")
        with self.driver.session() as session:
            with session.begin_transaction() as tx:
                for query in tqdm(nodes_with_relation_queries):
                    tx.run(query)
                tx.commit()
        print("Commited all of create nodes with relation transactions!")

    def search_HYPERNYM(self, input_word_list):
        search_queries = []
        for input_word in input_word_list:
            search_queries.append(self.search_HYPERNYM_queries(input_word))
        print("---------------------------------------")
        print("Running search nodes with relation transactions...")
        with self.driver.session() as session:
            start = time.time()
            results = defaultdict() # 조회된 모든 상위어와 등장 횟수가 기록된 딕셔너리
            for query in search_queries:
                query_result = session.run(query)
                for record in query_result:
                    hypernym = record['hypernym']
                    if hypernym:
                        results[hypernym] = results.get(hypernym, 0)+1 # 상위어 등장 횟수 +1
            end = time.time()
            # 등장 횟수 내림차순으로 정렬 후 출력
            print(sorted(results.items(), key=lambda item: item[1], reverse=True))
            print(f"{end - start:.7f} sec")
