#!/usr/bin/env python
from bs4 import BeautifulSoup
import re
soup = BeautifulSoup(open('tests/fixtures/document.html', 'rb'), 'html.parser')

root = soup.body
section_types = ['section', 'article']
all_sections = root.find_all(section_types)

top_level_sections = []
for section in all_sections:
    parent_names = [parent.name for parent in section.parents]
    if not any(set(parent_names).intersection(section_types)):
        top_level_sections.append(section)

def outline(top_level_sections):
    document_outline = []

    for sect in top_level_sections:
        outlined_sect = {}
        outlined_sect['type'] = sect.name

        # get the section heading
        sect_heading = sect.find(re.compile('h[1-6]'))
        sect_content = sect.find_all('p')
        sect_sub_sections = sect.find_all(section_types)

        for parent in sect_heading.parents:
            if parent == sect:
                outlined_sect['heading'] = sect_heading
                break
            elif parent.name in section_types:
                break

        outlined_sect['content'] = []
        for paragraph in sect_content:
            for parent in paragraph.parents:
                if parent == sect:
                    outlined_sect['content'].append(paragraph)
                    break
                elif parent.name in section_types:
                    break

        outlined_sect['sections'] = []
        for sub_section in sect_sub_sections:
            for parent in sub_section.parents:
                if parent == sect:
                    outlined_sect['sections'].extend(outline([sub_section]))
                    break
                elif parent.name in section_types:
                    break

        document_outline.append(outlined_sect)

    return document_outline

o = outline(top_level_sections)
for i in o:
    print i
    print
'''
    for outline in document_outline:
        print outline['type']
        try:
            print outline['heading']

        except KeyError:
            print "NO HEADING"

        for p in outline['content']:
            print p

        for sub_section in outline['sections']:
            print sub_section.name
'''

