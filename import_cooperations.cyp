CREATE CONSTRAINT IF NOT EXISTS FOR (a:Author) REQUIRE a.name IS UNIQUE;
CREATE TEXT INDEX IF NOT EXISTS FOR (a:Author) ON (a.name);

:auto LOAD CSV WITH HEADERS FROM "file:///dblp_authors.csv" AS line 
WITH line
CALL {
    WITH line
    
    MERGE (a:Author {name: line.author1})
    MERGE (b:Author {name: line.author2})
    MERGE (a)-[:WORKED_WITH]-(b)
} IN TRANSACTIONS;