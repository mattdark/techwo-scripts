#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lxml import etree
import cairosvg
import json
from dates import dates

SVGNS = u"http://www.w3.org/2000/svg"

with open('../assets/invitation.svg', 'r') as mysvg:
    svg = mysvg.read()

utf8_parser = etree.XMLParser(encoding='utf-8')

xml_data = etree.fromstring(svg.encode('utf-8'), parser=utf8_parser)

find_name = etree.ETXPath("//{%s}tspan[@id='tspan5652']" % (SVGNS))
find_org = etree.ETXPath("//{%s}tspan[@id='tspan5656']" % (SVGNS))
find_fecha1 = etree.ETXPath("//{%s}tspan[@id='tspan839']" % (SVGNS))
find_fecha2 = etree.ETXPath("//{%s}tspan[@id='tspan878']" % (SVGNS))
find_fecha3 = etree.ETXPath("//{%s}tspan[@id='tspan880']" % (SVGNS))
find_fecha4 = etree.ETXPath("//{%s}tspan[@id='tspan882']" % (SVGNS))

ds = dates()

with open('../speakers/speakers.json') as data_file:
    data = json.load(data_file)

for i in range(2):
    id = data["speakers"][i]["id"]
    name = data["speakers"][i]["name"]
    org = data["speakers"][i]["org"]
    find_name(xml_data)[0].text = name
    find_org(xml_data)[0].text = org
    find_fecha1(xml_data)[0].text = ds[0]
    find_fecha2(xml_data)[0].text = ds[1]
    find_fecha3(xml_data)[0].text = ds[2]
    find_fecha4(xml_data)[0].text = ds[3]
    new_svg = etree.tostring(xml_data).decode('utf-8')
    svg_file = './invitations/' + id + '.svg'
    f = open(svg_file, 'w+')
    f.write(new_svg)
    f.close()
    pdf_file = './invitations/' + id + '.pdf'
    cairosvg.svg2pdf(url=svg_file, write_to=pdf_file)
