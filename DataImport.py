from neo4j import GraphDatabase 
import lxml.etree as ET
import time
import os

class DataImport:


    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        

    def close(self):
        self.driver.close()


    def open_sission(self):
        self.session = self.driver.session()


    def close_session(self):
        self.session.close()


    def import_cooperations(self, xml, dtd):
        ET.DTD(file=dtd)

        with open(xml, 'rb') as file:
            context = ET.iterparse(file, events=("end", "start"), load_dtd=True)

            context = iter(context)

            cooperations = [
                "article", 
                "inproceedings",
                "proceedings", 
                "book", 
                "incollection", 
                "phdthesis", 
                "mastersthesis", 
                "www", 
                "person", 
                "data"
            ]

            j = 0
            tag_open = False
            dict = {}
            start_time = time.time()
            previous_time = time.time()

            for event, elem in context:
                if not tag_open and event == "start" and elem.tag in cooperations:
                    dict["tag"] = elem.tag
                    dict["authors"] = []
                    tag_open = True

                elif tag_open and event == "end" and elem.tag in cooperations:
                    # print("Cooperation: ", dict)
                    cooperation_result = self.session.execute_write(self._create_and_return_cooperation, dict)
                    # print(cooperation_result, "\n")
                    dict = {}
                    tag_open = False
                    j = j + 1

                    if j % 1000 == 0:
                        end_time = time.time()
                        part_time = end_time - previous_time 
                        previous_time = end_time
                        print("Done: ", j, ", for: ", end_time - start_time, " s. Part time: ", part_time, "s")
                        time_sleep = part_time / 10
                        time.sleep(time_sleep)

                elif tag_open and event == "start" and elem.tag not in cooperations:
                    if elem.tag == "author" and elem.text:
                        dict["authors"].append(elem.text)
                    if elem.tag == "title":
                        if elem.text:
                            dict["title"] = elem.text
                        else: 
                            dict["title"] = ""

                elem.clear()


            end_time = time.time()
            print("Done all: ", j, ", for: ", start_time - end_time, "s")


    def print_greeting(self, message):
        greeting = self.session.execute_write(self._create_and_return_greeting, message)
        print(greeting)


    @staticmethod
    def _create_and_return_cooperation(tx, dict):
        result = tx.run(""" 
            MERGE (cooperation: Cooperation: $tag {title : $title})
            FOREACH (
                auth IN $authors| 
                MERGE (author:Author {name : auth})
                MERGE (author)-[:WORKED_ON]->(cooperation)
            )
            RETURN cooperation
        """.replace("$tag", dict["tag"].capitalize()), 
            title=dict["title"],
            authors=dict["authors"]
        )
        return result.single()[0]


    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]

