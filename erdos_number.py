import DataAccess



def main():

    global db 
    db = DataAccess("bolt://localhost:7687","neo4j","password")
    print("""
          WELCOME TO "PATH TO ERDÖS" FINDER!!!

          If u want to search authors insert text like this:
          >> -a Milos Radovanovic
          and as a response you will get all authors that have both "Milos" and "Radovanovic" in their name.
          
          If you want to see all authors that have worked with some author, insert text like this:
          >> -c Milos Radovanovic 
          and as a response you will get all authors that "Milos Radovanovic" have worked with. 
          
          If you want to see "PATH TO ERDOS" of some author, insert text like this:
          >> -p Milos Radovanovic
          and as a response you will get shortest path (or multiple, if there is more than one) to the legendary mathematician "Paul Erdős"!
          """)

    while(True):
        input_string = input(">> ")
        tokens = input_string.split(" ", maxsplit=1)

        if len(tokens) < 2:
            print(f"You have only {len(tokens)} arguments, and 2 is minimum.")
            continue

        if tokens[0] != "-a" or tokens[0] != "-c" or tokens[0] != "-p":
            print(f"First argument can be either '-a' or '-c' or '-p'. Yours is '{tokens[0]}'")
            continue

        if tokens[0] == "-a":
            authors = db.find_author(tokens[1])
            if len(authors) == 0:
                print("There is no author with that or similar name...")
                continue

            print("I found those authors: ")
            for a in authors:
                print(a)
            
            continue

        if tokens[0] == "-c":
            colleagues = db.find_colleagues(tokens[1])
            if len(colleagues) == 0:
                print("There are no colleagues for this author...")
                continue

            print("I found those colleagues: ")
            for c in colleagues:
                print(c)
            
            continue

        if tokens[0] == "-p":
            paths = find_paths(tokens[1])
            if len(paths) == 0:
                print("There are no paths from this author to Paul Erdős")
    

def find_paths(author: str):
    pass


if __name__ == "__main__":
    main()