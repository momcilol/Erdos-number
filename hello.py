import lxml.etree as ET
from DataImport import DataImport




if __name__ == "__main__":
    data_file = "movies/tmdb_movies_data.csv"
    import_data = DataImport("bolt://localhost:7687", "neo4j", "password")
    import_data.open_sission()

    import_data.import_cooperations("dblp.xml", "dblp.dtd")

    # import_data.print_greeting("hello, world")
    
    import_data.close_session()
    import_data.close()
    print("\nThis is the end!")

