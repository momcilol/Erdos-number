import lxml.etree as ET
import time 

def out_dict_string(authors):
    l = len(authors)
    out_string = ""
    for i in range(l-1):
        for j in range(i+1,l):
            out_string += f"{authors[i]},{authors[j]}\n"

    return out_string


def print_to_csv(out_string):
    with open("dblp_authors.csv", "a", encoding="utf-8") as file:
        file.write(out_string)


ET.DTD(file="dblp.dtd")

with open("dblp.xml", 'rb') as file:
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
    out_string = ""
    authors = []
    start_time = time.time()
    previous_time = time.time()

    for event, elem in context:
        if not tag_open and event == "start" and elem.tag in cooperations:
            tag_open = True

        elif tag_open and event == "end" and elem.tag in cooperations:
            out_string += out_dict_string(authors)
            authors = []
            tag_open = False
            j = j + 1

            if j % 1000 == 0:
                print_to_csv(out_string)
                out_string = ""
                end_time = time.time()
                part_time = end_time - previous_time 
                previous_time = end_time
                print("Done: ", j, ", for: ", end_time - start_time, " s. Part time: ", part_time, "s")
                time_sleep = part_time / 10
                time.sleep(time_sleep)

        elif tag_open and event == "start" and elem.tag not in cooperations:
            if elem.tag == "author" and elem.text:
                authors.append(elem.text)
                

        elem.clear()


    end_time = time.time()
    print("Done all: ", j, ", for: ", end_time - start_time, "s")

