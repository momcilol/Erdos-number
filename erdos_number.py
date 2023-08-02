from DataAccess import DataAccess
from time import time
from types import FunctionType




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
          
    If you want to see "PATH TO ERDÖS" of some author, you have three choises:
    1. Using Breadth First Search (BFS):
    >> -bfs Milos Radovanovic
    2. Using Iterative Deepening Search(IDS):
    >> -ids Milos Radovanovic
    3. Using Bidirectional Breadth First Search (BBFS)
    >> -bbfs Milos Radovanovic
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

        if tokens[0] != "-a" and tokens[0] != "-c" and tokens[0] != "-bfs" and tokens[0] != "-ids" and tokens[0] != "-bbfs":
            print(f"First argument can be either '-a' or '-c' or '-bfs' or '-ids' or '-bbfs'. Your is '{tokens[0]}'")
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

        if tokens[0] == "-bfs":
            search(tokens[1], find_paths_bfs)
            continue
            
        if tokens[0] == "-ids":
            search(tokens[1], find_paths_ids)
            continue

        if tokens[0] == "-bbfs":
            search(tokens[1], find_paths_bbfs)
            continue
        

def search(author: str, fun: FunctionType):
    if not db.check_author(author):
        print("There is no author with that name...")
        return

    start_time = time()
    paths = fun(author)
    print(f"Execution time: {time() - start_time}")
    if len(paths) == 0:
        print(f"There are no paths from {author} to {erdos_name}")
        return

    print(f"Erdös number of {author} is {len(paths[0])-1}")
    print("Paths:")
    for i in range(len(paths)):
        print(f"{i+1}."," - ".join(paths[i]))


def find_paths_ids(author: str):
    i = 0
    while True:
        result = limited_dfs(author, i, [author])
        if result == None:
            return [[]]
        if result != [[]]:
            return result
        i += 1


def limited_dfs(author: str, i: int, visited):
    if i == 0:
        if author == erdos_name:
            return [[erdos_name]]
        else:
            return [[]]
        
    paths = []
    colleagues = db.find_colleagues(author)
    to_visit = [c for c in colleagues if c not in visited]
    if to_visit == []:
        return None
    else:
        empty_list = False
        full_list = False
        for coll in to_visit:
            subpaths = limited_dfs(coll, i-1, visited + [coll])
            if subpaths == None:
                continue
            if subpaths == [[]]:
                empty_list = True
                continue
            
            paths.extend([[author] + sub for sub in subpaths])
            full_list = True

    if full_list:
        return paths
    
    if empty_list:
        return [[]]
    
    return None

def find_paths_bfs(author: str):
    if author == erdos_name:
        return [[erdos_name]]

    # Mapa je strukture {<element>: {"level": <broj>, "parents": [<parent1>, ...]}}
    path_map = {}
    path_map[author] = {"level": 0, "parents": []}
    queue = []
    queue.append([author])
    queue.append([])
    i = 0
    j = 0
    path_exists = False

    while True:
        
        colleagues = db.find_colleagues(queue[i][j])
        if not path_exists:
            for coll in colleagues:
                if coll == erdos_name:
                    path_map[erdos_name] = {"level": i+1, "parents": [queue[i][j]]}
                    path_exists = True
                    break

                #Check if coll is in that level in queue or above (smaller index), making sure we don't go backward
                if coll not in path_map:
                    queue[i+1].append(coll)
                    path_map[coll] = {"level": i+1, "parents": [queue[i][j]]}
                elif path_map[coll]["level"] == i+1:
                    path_map[coll]["parents"].append(queue[i][j])
        else:
            for coll in colleagues:
                if coll == erdos_name:
                    path_map[erdos_name]["parents"].append(queue[i][j])
                    break

        j += 1

        if j >= len(queue[i]):
            j = 0
            i += 1
            queue.append([])
            if path_exists or len(queue[i]) == 0:
                break


    if not path_exists:
        return []       
    
    
    paths = dfs_paths(erdos_name, author, path_map)
    path_map = {}
    return paths


def dfs_paths(curr: str, author: str, map: dict):
    if curr == author:
        return [[author]]
    
    parents = map[curr]["parents"]

    paths = []
    for v in parents:
        paths.extend([a + [curr] for a in dfs_paths(v, author, map)])
    
    return paths


def find_paths_bbfs(author: str):
    if author == erdos_name:
        return [[erdos_name]]

    # path_map_bbfs sadrzi dve mape: 0 - polazi od authora, 1 - polazi od erdosa
    # Mapa je strukture {<element>: {"level": <broj>, "parents": [<parent1>, ...]}}
    path_map_bbfs = ({},{})
    path_map_bbfs[0][author] = {"level": 0, "parents": []}
    path_map_bbfs[1][erdos_name] = {"level": 0, "parents": []}

    # Isto vazi i za queue
    queue = ([[author],[]],[[erdos_name],[]])

    path_exists = False

    k = 0
    i = 0


    while True:
        for j in range(len(queue[k][i])):
            colleagues = db.find_colleagues(queue[k][i][j])
            if not path_exists:
                for coll in colleagues:
                    if not path_exists:
                        if coll in path_map_bbfs[(k+1)%2]:
                            path_map_bbfs[k][coll] = {"level": i+1, "parents": [queue[k][i][j]]}
                            path_exists = True
                            continue

                        #Check if coll is in that level in queue or above (smaller index), making sure we don't go backward
                        if coll not in path_map_bbfs[k]:
                            queue[k][i+1].append(coll)
                            path_map_bbfs[k][coll] = {"level": i+1, "parents": [queue[k][i][j]]}
                        elif path_map_bbfs[k][coll]["level"] == i+1:
                            path_map_bbfs[k][coll]["parents"].append(queue[k][i][j])
                    else:
                        if coll in path_map_bbfs[(k+1)%2]:
                            if coll not in path_map_bbfs[k]:
                                path_map_bbfs[k][coll] = {"level": i+1, "parents": [queue[k][i][j]]}
                            else:
                                path_map_bbfs[k][coll]["parents"].append(queue[k][i][j])
            else:
                for coll in colleagues:
                    if coll in path_map_bbfs[(k+1)%2]:
                            if coll not in path_map_bbfs[k]:
                                path_map_bbfs[k][coll] = {"level": i+1, "parents": [queue[k][i][j]]}
                            else:
                                path_map_bbfs[k][coll]["parents"].append(queue[k][i][j])

        if path_exists or len(queue[k][i+1]) == 0:
            break

        queue[k].append([])
        i += (k+1) // 2
        k = (k+1) % 2
    
    if not path_exists:
        return [[]]
        
    paths = []
    intersection = [key for key in path_map_bbfs[0].keys() & path_map_bbfs[1].keys()]
    
    for k in intersection:
        paths_author = [path[:-1] for path in dfs_paths(k,author,path_map_bbfs[0])]
        paths_erdos = [path[-2::-1] for path in dfs_paths(k, erdos_name, path_map_bbfs[1])]
        
        for pa in paths_author:
            for pe in paths_erdos:
                paths.append(pa + [k] + pe)
    
    return paths


if __name__ == "__main__":
    main()