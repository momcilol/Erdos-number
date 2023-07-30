from DataAccess import DataAccess
from time import time




def main():
    global erdos_name
    erdos_name = "Paul Erdös"
    global db 
    db = DataAccess("bolt://localhost:7687","neo4j","password")

    message = """
    WELCOME TO "PATH TO ERDÖS" FINDER!!!
    
    If u want to search authors insert text like this:
    >> -a Milos Radovanovic
    and as a response you will get all authors that have both "Milos" and "Radovanovic" in their name.
          
    If you want to see all authors that have worked with some author, insert text like this:
    >> -c Milos Radovanovic 
    and as a response you will get all authors that "Milos Radovanovic" have worked with. 
          
    If you want to see "PATH TO ERDOS" of some author, insert text like this:
    >> -p Milos Radovanovic
    and as a response you will get shortest path (or multiple, if there is more than one) to the legendary mathematician "Paul Erdös"!

    For exit type:
    >> exit

    To print again this welcome message type:
    >> welcome
    """

    print(message)

    while(True):
        input_string = input(">> ")
        tokens = input_string.split(" ", maxsplit=1)

        if len(tokens) == 0:
            print("Try again...")
            continue

        
        if len(tokens) == 1:
            if tokens[0] == "exit":
                break

            if tokens[0] == "welcome":
                print(message)
                continue

            print(f"You have only 1 arguments, and 2 is needed.")
            continue

        if tokens[0] != "-a" and tokens[0] != "-c" and tokens[0] != "-p":
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
            if not db.check_author(tokens[1]):
                print("There is no author with that name...")
                continue

            colleagues = db.find_colleagues(tokens[1])
            if len(colleagues) == 0:
                print(f"There are no colleagues for {tokens[1]}...")
                continue

            print("I found those colleagues: ")
            for c in colleagues:
                print(c)
            
            continue

        if tokens[0] == "-p":
            if not db.check_author(tokens[1]):
                print("There is no author with that name...")
                continue

            start_time = time()
            paths = find_paths(tokens[1])
            print(f"Execution time: {time() - start_time}")
            if len(paths) == 0:
                print(f"There are no paths from {tokens[1]} to {erdos_name}")
                continue

            print(f"Erdös number of {tokens[1]} is {len(paths[0])-1}")
            print("Paths:")
            for i in range(len(paths)):
                print(f"{i+1}."," - ".join(paths[i]))
            

def find_paths(author: str):
    if author == erdos_name:
        return [[erdos_name]]

    global path_map
    path_map = []
    queue = []
    queue.append([author])
    queue.append([])
    j = 0
    path_exists = False

    while True:
        
        colleagues = db.find_colleagues(queue[-2][j])
        if not path_exists:
            for coll in colleagues:
                if coll == erdos_name:
                    path_map.append((coll, queue[-2][j]))
                    path_exists = True
                    break
                #Check if coll is in that level in queue or above (smaller index), making sure we don't go backward
                level_ab = False
                #Check if coll is in last level, that is currentlly filling
                level_l = False
            
                for level in queue[:-1]:
                    if coll in level:
                        level_ab = True
                        break
                    
                if not level_ab and coll in queue[-1]:
                    level_l = True

                if not level_ab:
                    path_map.append((coll, queue[-2][j]))
                    if not level_l:
                        queue[-1].append(coll)
        else:
            for coll in colleagues:
                if coll == erdos_name:
                    path_map.append((coll, queue[-2][j]))
                    break

        j += 1

        if j >= len(queue[-2]):
            j = 0
            queue.append([])
            if path_exists or len(queue[-2]) == 0:
                break


    if not path_exists:
        return []       
    
    
    paths = dfs_paths(erdos_name, author)
    path_map = []
    return paths


def dfs_paths(curr: str, author: str):
    if curr == author:
        return [[author]]
    
    parents = [v for (k, v) in path_map if k == curr]

    paths = []
    for v in parents:
        paths.extend([a + [curr] for a in dfs_paths(v, author)])
    
    return paths


if __name__ == "__main__":
    main()