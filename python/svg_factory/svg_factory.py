import os

from lxml import etree, html
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

from examples.svg_factory.primitives import Circle


class SVGFactory:

    def __init__(self, templates_dir, build_dir):
        self.templates_dir = templates_dir
        self.build_dir = build_dir
        self.rows = []

    def make_circle(self, cx, cy, r, fill):
        return Circle(cx, cy, r, fill, self.templates_dir)

    def build(self):
        template = self._read_template()
        svg = self._get_svg()
        result = template.format(tmp=svg)
        return result

    def _get_svg(self):
        rows = '\n'.join([row.svg() for row in self.rows])
        svg = '<svg>{}</svg>'.format(rows)
        return svg

    def save_html(self, filename):
        builded_html = self.build()
        docroot = html.fromstring(builded_html)
        result = etree.tostring(docroot, encoding='utf-8', pretty_print=True)
        path = os.path.join(self.build_dir, filename)
        with open(path, 'wb') as file:
            file.write(result)

    def save_png(self, filename):
        # drawing = svg2rlg("file.svg")
        # renderPDF.drawToFile(drawing, "file.pdf")
        svg = self._get_svg()
        tmp_svg = os.path.join(self.build_dir, 'tmp.svg')
        with open(tmp_svg, 'w') as file:
            file.write(svg)

        drawing = svg2rlg(tmp_svg)
        # renderPM.drawToFile(drawing, filename)
        tmp_pdf = os.path.join(self.build_dir, 'tmp.pdf')
        renderPDF.drawToFile(drawing, tmp_pdf)

    def add(self, obj):
        self.rows.append(obj)

    def _read_template(self):
        tmp_path = os.path.join(self.templates_dir, 'template.html')
        with open(tmp_path, 'r') as file:
            result = '\n'.join(file.readlines())
        return result
