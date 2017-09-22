import csv
import re
from lxml import etree

#from xml.etree import ElementTree as etree

class IBMCorpusParser:

    def __init__(self, corpusName):

        self.corpusName = corpusName
        self.DEFAULT_INFERENCE = "Default Inference"
        self.DEFAULT_CONFLICT = "Default Conflict"

        self.UNKOWN = "Unknown"
        self.UNKNOWN_NUMBER = "-"


    def startParsing(self, annotationFile):

        with open(annotationFile) as f:
            annotatedData = [line for line in csv.reader(f, dialect="excel-tab")]

        self.argumentDict = {}
        self.relationDict = {}

        currentArgumentID = 0
        currentConclusion = ""
        currentClaim = ""
        currentClaimID = 1
        currentPremiseID = 2

        for index, line in enumerate(annotatedData):

            conclusion = line[0]
            claim = line[1]
            premise = re.sub(r"]", '', re.sub(r"\[([A-Za-z_]+)", '', line[2]))

            if conclusion == currentConclusion:

                if claim == currentClaim:

                    self.addNewPremise(currentArgumentID, currentClaimID, currentPremiseID, premise)

                else :

                    currentClaimID += 4

                    self.addNewClaim(currentArgumentID, currentClaimID, claim)

                    self.addNewPremise(currentArgumentID, currentClaimID, currentPremiseID, premise)

                    currentClaim = claim

            else:

                if (index > 0):

                    currentArgumentID = currentArgumentID+4
                    currentClaimID += 4

                self.addNewArgument(currentArgumentID, conclusion)

                self.addNewClaim(currentArgumentID, currentClaimID, claim)

                self.addNewPremise(currentArgumentID, currentClaimID, currentPremiseID, premise)

                currentConclusion = conclusion
                currentClaim = claim

            currentPremiseID += 4

        xmlData = self.convertToPassauXML()

        return xmlData


    def addNewPremise(self, argumentID, claimID, premiseID, premise):

        self.argumentDict[argumentID][claimID][premiseID]={}
        self.argumentDict[argumentID][claimID][premiseID]["premiseText"] = premise

        self.relationDict[premiseID] = {}
        self.relationDict[premiseID]["type"]=self.DEFAULT_INFERENCE
        self.relationDict[premiseID]["label"] = "0"
        self.relationDict[premiseID]["from"]=premiseID
        self.relationDict[premiseID]["to"]=claimID
        self.relationDict[premiseID]["relationID"]=str(premiseID) + "-R-" + str(claimID)

    def addNewClaim(self, argumentID, claimID, claim):

        self.argumentDict[argumentID][claimID] = {}
        self.argumentDict[argumentID][claimID]["claimText"]=claim

        self.relationDict[claimID] = {}
        self.relationDict[claimID]["type"]=self.UNKOWN
        self.relationDict[claimID]["label"] = "2"
        self.relationDict[claimID]["from"]=claimID
        self.relationDict[claimID]["to"]=argumentID
        self.relationDict[claimID]["relationID"]=str(claimID) + "-R-" + str(argumentID)

    def addNewArgument(self, argumentID, conclusion):

        self.argumentDict[argumentID] = {}
        self.argumentDict[argumentID]["conclusionText"] = conclusion


    def convertToPassauXML(self):

        xmlData = list()

        for key in self.argumentDict.keys():

            root = etree.Element('Annotation')
            root.set("corpus", self.corpusName)

            proposition = etree.Element('Proposition')
            proposition.set("id", str(key))
            root.append(proposition)

            aduType = etree.Element('ADU')
            aduType.set("type", "conclusion")
            proposition.append(aduType)

            text = etree.Element('text')
            text.text = self.argumentDict[key]["conclusionText"]
            proposition.append(text)

            for claimKey in self.argumentDict[key].keys():

                if claimKey == "conclusionText":
                    continue
                else:

                    proposition = etree.Element('Proposition')
                    proposition.set("id", str(claimKey))
                    root.append(proposition)

                    aduType = etree.Element('ADU')
                    aduType.set("type", "claim")
                    proposition.append(aduType)

                    text = etree.Element('text')
                    text.text = self.argumentDict[key][claimKey]["claimText"]
                    proposition.append(text)

                    relation = etree.Element('Relation')
                    relation.set("relationID", self.relationDict[claimKey]["relationID"])
                    relation.set("type", self.relationDict[claimKey]["type"])
                    relation.set("typeBinary", self.relationDict[claimKey]["label"])
                    relation.set("partnerID", str(self.relationDict[claimKey]["to"]))
                    proposition.append(relation)

                    for premiseKey in self.argumentDict[key][claimKey].keys():

                         if premiseKey == "claimText":
                            continue

                         else:

                            proposition = etree.Element('Proposition')
                            proposition.set("id", str(premiseKey))
                            root.append(proposition)

                            aduType = etree.Element('ADU')
                            aduType.set("type", "premise")
                            proposition.append(aduType)

                            text = etree.Element('text')
                            text.text = self.argumentDict[key][claimKey][premiseKey]["premiseText"]
                            proposition.append(text)

                            relation = etree.Element('Relation')
                            relation.set("relationID", self.relationDict[premiseKey]["relationID"])
                            relation.set("type", self.relationDict[premiseKey]["type"])
                            relation.set("typeBinary", self.relationDict[premiseKey]["label"])
                            relation.set("partnerID", str(self.relationDict[premiseKey]["to"]))
                            proposition.append(relation)

            xmlData.append(etree.tostring(root, pretty_print=True))

        return xmlData
