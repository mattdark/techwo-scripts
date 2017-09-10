#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lxml import etree
import xlrd
import cairosvg
from PyPDF2 import PdfFileMerger

SVGNS = u"http://www.w3.org/2000/svg"

with open('./format/cert.svg', 'r') as mysvg:
    svg = mysvg.read() #.replace('\n', '')

utf8_parser = etree.XMLParser(encoding='utf-8')

xml_data = etree.fromstring(svg.encode('utf-8'), parser=utf8_parser)
# We search for element 'text' with id='tile_text' in SVG namespace
find_text = etree.ETXPath("//{%s}tspan[@id='tspan3951']" % (SVGNS))
# find_text(xml_data) returns a list
# [<Element {http://www.w3.org/2000/svg}text at 0x106185ab8>]
# take the 1st element from the list, replace the text

workbook = xlrd.open_workbook('./speakers/speakers.xls')
worksheet = workbook.sheet_by_name('Speakers')
merger = PdfFileMerger()
for x in range(1,3,1):
    id = str(int(worksheet.cell(x,0).value))
    name = ''
    for y in range(1,4,1):
        name += worksheet.cell(x, y).value
        name += ' '
    name.rstrip()
    find_text(xml_data)[0].text = name
    new_svg = etree.tostring(xml_data).decode('utf-8')
    svg_file = './speakers/' + id + '.svg'
    f = open(svg_file, 'w+')
    f.write(new_svg)
    f.close()
    pdf_file = './speakers/' + id + '.pdf'
    cairosvg.svg2pdf(url=svg_file, write_to=pdf_file)
    merger.append(open(pdf_file, 'rb'))

with open('./certificates/cert.pdf', 'wb') as fout:
    merger.write(fout)
