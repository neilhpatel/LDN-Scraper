import requests

def parseLink(link):
    r = requests.get(link)
    page_source = r.text
    page_source = page_source.split('\n')
    for element in page_source:
        i = 0
        if "<title>" in element:
            header = "<title>"
            bar = "|"
            title = element[element.index(header)+7:element.index(bar)]
            title = title.replace("&#039;", "\'")
            f = open(title, "w")
        if "cleanText" in element:
            string = element
            plug = "pluginVersion"
            txt = string[string.index("cleanText")+12:string.index(plug)-4]
            splits = txt.split()
            for split in splits:

                split = split.replace("\\r\\n", "")
                split = split.replace("\\r", "")
                split = split.replace("\\n", "")
                split = split.replace("\\u23f8", " ")
                split = split.replace("\\u23f", "")
                split = split.replace("\\u201c", "\"")
                split = split.replace("\\u201d", "\"")
                split = split.replace("\\u2019", "\'")
                split = split.replace("\\u2026", "... ")
                split = split.replace("\\u2018", "'")
                split = split.replace("\u00a0", " ")
                split = split.replace("\\u2014", " - ")

                f.write(split + " ")
                i = i + len(split + " ")
                if i > 100:
                    f.write("\n")
                    i = 0

    f.close()

if __name__ == "__main__":
    parseLink("https://www.lagrangenews.com/2023/06/02/troup-high-school-announces-new-principal/")
