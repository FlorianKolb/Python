import re
import os.path
import xml.dom.minidom
import xml.etree.ElementTree as ET

class Gedcom:
    inputGedcomFile = ''

    indiStartRegex = re.compile('\s*\d\s@(?<ID>.*)@\sINDI')
    familyStartRegex = re.compile('\s*\d\s@(?<ID>.*)@\sFAM')
    valueRegex = re.compile('\s*(?<NUMBER>\d)\s(?<CAPTURE>.*?)\s(?<VALUE>.*)')
    groupRegex = re.compile('\s*(?<NUMBER>\d)\s(?<CAPTURE>[A-Z|_]*)\Z')

    def __init__(self, inputGedcomFile):
        if (os.path.exists(inputGedcomFile)):
            self.inputGedcomFile = inputGedcomFile
        else:
            raise Exception('The input GEDCOM file \'' + inputGedcomFile + '\' does not exist!')

    def ToXml(self, xmlFileName):
        gedFile = open(self.inputGedcomFile, 'r')

        rootElement = ET.fromstring('<GedcomFile/>')
        
        for line in gedFile:
            if (self.valueRegex.match(line)):
                match = self.valueRegex.match(line)
                capture = match.group('CAPTURE')
                value = match.group('VALUE')

                childElement = ET.Element(capture)
                childElement.set('Content', value)

                rootElement.append(childElement)
        
        xmlTree = ET.ElementTree(rootElement)
        xmlTree.write(xmlFileName)

        #TODO: Pretty print xml
        #self.PrettyPrint(xmlFileName)

    def PrettyPrint(self, xmlFileName):
        doma = xml.dom.minidom.parse(xmlFileName)
        xmlElement = ET.fromstring(doma.toprettyxml())
        ET.ElementTree(xmlElement).write(xmlFileName)

try:
    reader = Gedcom('F:\export-BloodTree.ged')
    reader.ToXml('F:\\test.xml')
except Exception as ex:
    raw_input(ex.message)