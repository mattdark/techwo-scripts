#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lxml import etree
import xlrd
import cairosvg
import json
from PyPDF2 import PdfFileMerger

SVGNS = u"http://www.w3.org/2000/svg"

with open('../assets/cert.svg', 'r') as mysvg:
    svg = mysvg.read()

utf8_parser = etree.XMLParser(encoding='utf-8')

xml_data = etree.fromstring(svg.encode('utf-8'), parser=utf8_parser)
find_text = etree.ETXPath("//{%s}tspan[@id='tspan3951']" % (SVGNS))

merger = PdfFileMerger()

with open('./speakers/speakers.json') as data_file:
    data = json.load(data_file)

for i in range(2):
    id = data["speakers"][i]["id"]
    name = data["speakers"][i]["name"]
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
