#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lxml import etree
import xlrd
import cairosvg
from dates import dates

SVGNS = u"http://www.w3.org/2000/svg"

with open('./format/invitation.svg', 'r') as mysvg:
    svg = mysvg.read() #.replace('\n', '')

utf8_parser = etree.XMLParser(encoding='utf-8')

xml_data = etree.fromstring(svg.encode('utf-8'), parser=utf8_parser)

find_name = etree.ETXPath("//{%s}tspan[@id='tspan5652']" % (SVGNS))
find_org = etree.ETXPath("//{%s}tspan[@id='tspan5656']" % (SVGNS))
find_fecha1 = etree.ETXPath("//{%s}tspan[@id='tspan839']" % (SVGNS))
find_fecha2 = etree.ETXPath("//{%s}tspan[@id='tspan878']" % (SVGNS))
find_fecha3 = etree.ETXPath("//{%s}tspan[@id='tspan880']" % (SVGNS))
find_fecha4 = etree.ETXPath("//{%s}tspan[@id='tspan882']" % (SVGNS))

ds = dates()

workbook = xlrd.open_workbook('./speakers/speakers.xls')
worksheet = workbook.sheet_by_name('Speakers')

for x in range(1,3,1):
    id = str(int(worksheet.cell(x,0).value))
    name = ''
    for y in range(1,4,1):
        name += worksheet.cell(x, y).value
        name += ' '
    name.rstrip()
    org = worksheet.cell(x,4).value
    find_name(xml_data)[0].text = name
    find_org(xml_data)[0].text = org
    find_fecha1(xml_data)[0].text = ds[0]
    find_fecha2(xml_data)[0].text = ds[1]
    find_fecha3(xml_data)[0].text = ds[2]
    find_fecha4(xml_data)[0].text = ds[3]
    new_svg = etree.tostring(xml_data).decode('utf-8')
    svg_file = './speakers/' + id + '.svg'
    f = open(svg_file, 'w+')
    f.write(new_svg)
    f.close()
    pdf_file = './speakers/' + id + '.pdf'
    cairosvg.svg2pdf(url=svg_file, write_to=pdf_file)
