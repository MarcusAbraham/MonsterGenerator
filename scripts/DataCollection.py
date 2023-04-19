from pdfminer.high_level import extract_text


def gather_index():
    monster_dict = {}
    with open('../resources/MonsterIndex.txt', 'r') as file:
        for line in file:
            line_parts = line.strip().split(',')
            monster_name = line_parts[0].strip()
            page_number = int(line_parts[1].strip())
            monster_dict[monster_name] = page_number

    return monster_dict


def gather_monsters(index_dict):
    # Extract pdf and split into pages
    pdf_text = extract_text('../resources/MonsterManual.pdf')
    pages = pdf_text.split('\f')

    for monster_name, page_number in index_dict.items():
        # Check up to 10 pages before and after the monster's statblock page
        for page in range(page_number - 10, page_number + 10):
            if page < 0 or page >= len(pages):
                continue

            page_text = pages[page]
            # Look for headings with the same name in all capital letters
            if monster_name.upper() in page_text:
                start_index = page_text.find(monster_name.upper())
                end_index = page_text.find('\n\n', start_index)

                # Copy all text under the heading until the next capitalised heading
                monster_description = page_text[start_index:end_index].strip()
                print(f"{monster_name}: {monster_description}")
                break


index_dict = gather_index()
print(index_dict)

gather_monsters(index_dict)
