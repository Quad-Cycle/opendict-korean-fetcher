from neo4j import GraphDatabase

class GraphDBGenerator:
    uri = 'bolt://localhost:7687'
    username = 'neo4j'
    password = '2019112073'
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

    def merge_node_with_relations(self, data):
        print("Making create nodes with relation queries...")
        result = []
        for word, hypernyms in data:
            for hypernym in hypernyms:
                result.append(
                    ("MERGE (a:Word{{name:'{}'}}) MERGE (b:Word{{name:'{}'}}) MERGE (a)-[:HYPERNYM]->(b)".format(word, hypernym))
                )
        print("Completed making create nodes with relation queries!")
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
        nodes_with_relation_queries =self.merge_node_with_relations(data)
        # 쿼리 실행 및 commit
        print("---------------------------------------")
        print("Running create nodes with relation transactions...")
        with self.driver.session() as session:
            with session.begin_transaction() as tx:
                for query in nodes_with_relation_queries:
                    tx.run(query)
                tx.commit()
        print("Commited all of create nodes with relation transactions!")
