"""Translate archival Excel text while preserving every sheet, formula and format."""
import html
import re
import zipfile
import xml.etree.ElementTree as ET
from localization import RU, chunks, translate

TEXT = re.compile(r'(?<=>)[^<]+(?=<)')
ATTR = re.compile(r'([\w:.-]+)="([^"]*)"')
FORMULA = re.compile(r'<(?:[\w.-]+:)?(?:f|definedName)(?:\s[^>]*)?>$')


def workbook_strings(path):
    with zipfile.ZipFile(path) as archive:
        for name in archive.namelist():
            if not name.endswith('.xml'): continue
            xml = archive.read(name).decode('utf-8')
            for match in TEXT.finditer(xml):
                if not FORMULA.search(xml[:match.start()]):yield from chunks(html.unescape(match.group()))
            for match in ATTR.finditer(xml): yield from chunks(html.unescape(match.group(2)))


def translate_workbook(source, destination, dictionary):
    with zipfile.ZipFile(source) as original:
        names=[s.attrib['name'] for s in ET.fromstring(original.read('xl/workbook.xml')).findall('{*}sheets/{*}sheet')]
    renamed={name:translate(name,dictionary) for name in names}
    assert len(set(renamed.values()))==len(names) and all(len(v)<=31 for v in renamed.values())
    def references(value):
        for old,new in renamed.items():value=value.replace("'"+old+"'!", "'"+new+"'!")
        return value
    def text(match):
        original = html.unescape(match.group())
        if FORMULA.search(match.string[:match.start()]):return html.escape(references(original),quote=False)
        return html.escape(translate(original, dictionary), quote=False) if RU.search(original) or original.strip() in dictionary else match.group()
    def attribute(match):
        original = html.unescape(match.group(2))
        if not RU.search(original): return match.group()
        if match.group(1)=='location':return 'location="'+html.escape(references(original),quote=True)+'"'
        return match.group(1) + '="' + html.escape(translate(original, dictionary), quote=True) + '"'
    with zipfile.ZipFile(source) as original, zipfile.ZipFile(destination, 'w') as localized:
        for entry in original.infolist():
            body = original.read(entry.filename)
            if entry.filename.endswith('.xml'):
                xml = body.decode('utf-8')
                body = ATTR.sub(attribute, TEXT.sub(text, xml)).encode('utf-8')
            localized.writestr(entry, body)
