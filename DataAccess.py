from neo4j import GraphDatabase


class DataAccess:
    _find_author_template = """
    MATCH (a:Author) $where_clause RETURN a.name
"""
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self._find_author_template

    def close_session(self):
        self.session.close()

    
    def find_colleagues(self, author):
        result = self.driver.execute_query(""" 
            MATCH (:Author {name: $author})-[:WORKED_WITH]-(n:Author)
            RETURN n.name
        """, author=author, database_= "neo4j")
        colleagues = [r.value() for r in result[0]]
        # print(colleagues)
        return colleagues

    
    def find_author(self, author_name: str):
        substrings = author_name.split(" ")
        sub_dict = {f"name{i}":substrings[i] for i in range(len(substrings))}
        if len(substrings) == 0:
            return None
        
        sub_list = []
        where_clause = "WHERE "
        for i in range(len(substrings)):
            sub_list.append(f"TOLOWER(a.name) CONTAINS TOLOWER($name{i})")

        where_clause += " AND ".join(sub_list)
        query = DataAccess._find_author_template.replace("$where_clause", where_clause)
        result = self.driver.execute_query(query,parameters_=sub_dict)
        authors = [r.value() for r in result[0]]
        # print(authors)
        return authors


    def check_author(self, author: str) -> bool:
        result = self.driver.execute_query("MATCH (n:Author {name: $author}) RETURN n.name", author=author)
        authors = [r.value() for r in result[0]]
        # print(authors)
        return len(authors) == 1
   
    def create_and_return_greeting(self, message):
        result = self.driver.execute_query("""
                        CREATE (a:Greeting)
                        SET a.message = $message
                        RETURN a.message
                        """, message=message)
        print(result[0][0].value())


if __name__ == "__main__":
    db = DataAccess("bolt://localhost:7687","neo4j","password")
    # db.find_colleagues("Neki tamo levi")
    # db.find_author("Paul Erd")
    # db.create_and_return_greeting("Hello World!!!")
    db.check_author("Milos Radovanovic")