import csv

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

    # Initialize CSV writer
    with open('../resources/GatheredDescriptions.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Monster Name', 'Description'])

        for monster_name, page_number in index_dict.items():
            # Check up to 10 pages before and after the page number
            for i in range(page_number - 10, page_number + 11):
                if i < 0 or i >= len(pages):
                    continue

                # Find the heading with the monster name in all capital letters
                page_lines = pages[i].strip().split('\n')
                for j in range(len(page_lines)):
                    line = page_lines[j]
                    if line.strip().upper() == monster_name.upper():
                        # Found the heading, so extract the description until the next heading
                        description_lines = []
                        for k in range(j + 1, len(page_lines)):
                            next_line = page_lines[k]
                            if next_line.strip().isupper():
                                break
                            description_lines.append(next_line.strip())

                            # Check if the description is empty or if the first word after the monster name is in the list of size words
                            if not description_lines or description_lines[0].replace("  ", " ").split()[0] in ['Tiny',
                                                                                                               'Small',
                                                                                                               'Medium',
                                                                                                               'Large',
                                                                                                               'Huge',
                                                                                                               'Gargantuan']:
                                break

                        description = ' '.join(description_lines)
                        # description = description.replace("  ", " ")  # Replace double spaces with single spaces
                        writer.writerow([monster_name, description])
                        break


index_dict = gather_index()
print(index_dict)

gather_monsters(index_dict)
print("Csv printed!")