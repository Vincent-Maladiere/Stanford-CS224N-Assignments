from bs4 import BeautifulSoup
import json
import urllib.request
import argparse

parser = argparse.ArgumentParser()


def main(url):
    #url = "https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1214/assignments/a1_preview/exploring_word_vectors.html"
    response = urllib.request.urlopen(url)
    #  for local html file
    # response = open("/Users/note/jupyter/notebook.html")
    text = response.read()

    soup = BeautifulSoup(text, 'lxml')
    # see some of the html
    print(soup.div)
    dictionary = {'nbformat': 4, 'nbformat_minor': 1, 'cells': [], 'metadata': {}}
    for d in soup.findAll("div"):
        if 'class' in d.attrs.keys():
            for clas in d.attrs["class"]:
                if clas in ["text_cell_render", "input_area"]:
                    # code cell
                    if clas == "input_area":
                        cell = {}
                        cell['metadata'] = {}
                        cell['outputs'] = []
                        cell['source'] = [d.get_text()]
                        cell['execution_count'] = None
                        cell['cell_type'] = 'code'
                        dictionary['cells'].append(cell)

                    else:
                        cell = {}
                        cell['metadata'] = {}

                        cell['source'] = [d.decode_contents()]
                        cell['cell_type'] = 'markdown'
                        dictionary['cells'].append(cell)
    file_name = "_".join(url.split("/")[-2:]) + ".ipynb"
    open(file_name, 'w').write(json.dumps(dictionary))


if __name__ == "__main__":

    parser.add_argument("-u", "--url", required=True)
    args = parser.parse_args()

    main(args.url)
