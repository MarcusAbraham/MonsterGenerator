import re
from pdfminer.high_level import extract_text
import string
import csv


def gather_index():
    monster_dict = {}
    with open('../resources/MonsterIndex.txt', 'r') as file:
        for line in file:
            line_parts = line.strip().split(',')
            monster_name = line_parts[0].strip()
            page_number = int(line_parts[1].strip())
            monster_dict[monster_name] = page_number

    return monster_dict


def gather_monsters():
    # Extract pdf and split into pages
    pdf_text = extract_text('../resources/MonsterManual.pdf')
    pages = pdf_text.split('\f')

    print(pages[32])


index_dict = gather_index()
print(index_dict)

gather_monsters()
