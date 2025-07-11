#!/usr/bin/env python
from acdh_tei_pyutils.tei import TeiReader, ET
from sys import argv
NS_TEI = "http://www.tei-c.org/ns/1.0"

input_files = argv[1:]
    
def extract_title_a(document):
    title = "Title A"
    return title

def extract_title_s(document):
    title = "Title S"
    return title

def extract_title_j(document):
    title = "Die Neue Freie Presse"
    return title
            
for document_file in input_files:
    document = TeiReader(document_file)
    titles = {
        "j": extract_title_j(document),
        "a":  extract_title_a(document),
        "s": extract_title_s(document)
    }
    titlestmt = document.any_xpath("//tei:fileDesc/tei:titleStmt")[0]
    title_elements = titlestmt.xpath("./tei:title", namespaces={"tei": NS_TEI})
    
    if not  [t for t in title_elements if t.get("level") == "j"]:
        title_j = ET.Element(f"{{{NS_TEI}}}title", level="j")
        title_elements[-1].tail = "\n            "
        title_elements[-1].addnext(title_j)
        title_elements.append(title_j)
        title_elements[-1].tail = "\n            "
  
    for title in title_elements:
        level = title.get("level")
        print(level)
        title.text = titles[level]
        print(title.text)
    
    document.tree_to_file("out.xml")
