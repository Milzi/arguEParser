import re
from lxml import etree


class BratParser:

    def __init__(self, argumentTopic):

        self.corpusName=argumentTopic

        self.ARGUMENTATIVE_UNIT = 'T'
        self.ARGUMENTATIVE_RELATION = 'R'
        self.ARGUMENTATIVE_TOP_LEVEL_RELATION = 'A'
        self.CON_STANCE = 'Against'
        self.PRO_STANCE = "For"

        self.DEFAULT_INFERENCE = "Default Inference"
        self.DEFAULT_CONFLICT = "Default Conflict"

        self.argSchemeDict = {
            "Analogy":"1",
            "Arbitrary Verbal Classification":"59",
            "Bias":"2",
            "Causal Slippery Slope":"2",
            "Cause To Effect":"4",
            "Circumstantial Ad Hominem":"5",
            "Commitment":"6",
            "Correlation To Cause":"7",
            "Dilemma":"9",
            "Direct Ad Hominem":"10",
            "Established Rule":"61",
            "Ethotic":"12",
            "Evidence To Hypothesis":"13",
            "Example":"14",
            "Exceptional Case":"62",
            "Expert Opinion":"15",
            "Falsification Of Hypothesis":"16",
            "Fear Appeal":"17",
            "Full Slippery Slope":"18",
            "Gradualism":"63",
            "Ignorance":"19",
            "Inconsistent Commitment":"20",
            "Negative Consequences":"22",
            "Popular Opinion":"23",
            "Popular Practice":"25",
            "Position To Know":"26",
            "Positive Consequences":"27",
            "Practical Reasoning":"28",
            "Precedent Slippery Slope":"29",
            "Sign":"30",
            "Vague Verbal Classification":"60",
            "Verbal Classification":"31",
            "Verbal Slippery Slope":"32",
            "Waste":"33",
            "Fairness":"999"
        }
    def startParsing(self, annotationFile, textFile):

        with open(annotationFile) as f:
            bratInput = f.readlines()

        with open(textFile) as tf:
            originalText = tf.readlines()

        self.argumentDict={}
        self.relationDict={}

        # filling the argumentDict dictionary
        self.parseBratInput(bratInput)

        root = etree.Element('Annotation')
        root.set("corpus", self.corpusName)

        for key in self.argumentDict.keys():

            proposition = etree.Element('Proposition')
            proposition.set("id", str(key))
            root.append(proposition)

            aduType = etree.Element('ADU')
            aduType.set("type", "conclusion")
            proposition.append(aduType)

            text = etree.Element('text')
            text.text = self.argumentDict[key]["conclusionText"]
            proposition.append(text)

            textPosition = etree.Element('TextPosition')
            textPosition.set("start", self.argumentDict[key]["positionStart"])
            textPosition.set("end", self.argumentDict[key]["positionEnd"])
            proposition.append(textPosition)

            for propositionKey in self.argumentDict[key].keys():

                if propositionKey[0] == self.ARGUMENTATIVE_UNIT:

                    proposition = etree.Element('Proposition')
                    proposition.set("id", str(propositionKey))
                    root.append(proposition)

                    aduType = etree.Element('ADU')

                    aduType.set("type", self.argumentDict[key][propositionKey]["type"])
                    proposition.append(aduType)

                    text = etree.Element('text')
                    text.text = self.argumentDict[key][propositionKey]["text"]
                    proposition.append(text)

                    textPosition = etree.Element('TextPosition')
                    textPosition.set("start", self.argumentDict[key][propositionKey]["positionStart"])
                    textPosition.set("end", self.argumentDict[key][propositionKey]["positionEnd"])
                    proposition.append(textPosition)

                    for relationKey in self.relationDict.keys():

                        if (propositionKey == self.relationDict[relationKey]["from"]):

                            relation = etree.Element('Relation')
                            relation.set("relationID", self.relationDict[relationKey]["relationID"])
                            relation.set("type", self.relationDict[relationKey]["type"])
                            relation.set("typeBinary", self.relationDict[relationKey]["label"])
                            relation.set("partnerID", self.relationDict[relationKey]["to"])
                            proposition.append(relation)

        originalTextNode = etree.Element('OriginalText')
        originalTextNode.text = "".join(originalText)
        root.append(originalTextNode)

        xmlData = etree.tostring(root, pretty_print=True)

        return xmlData

    def parseBratInput(self, bratInput):

        rdfTupelDict= {}
        rdfTupels = []
        conclusion = ""
        relation=""
        schemeNumber=71
        issue = ""


        conclusionKey = "T0"

        for line in bratInput:

            wordsInLine = line.split()

            # find conclusion of the argument first
            if wordsInLine[1] == "conclusion" or wordsInLine[1] == "MajorClaim":

                self.argumentDict[wordsInLine[0]] = {}
                self.argumentDict[wordsInLine[0]]["conclusionText"] = ' '.join(word for word in wordsInLine[4:])
                self.argumentDict[wordsInLine[0]]["positionStart"] = wordsInLine[2]
                self.argumentDict[wordsInLine[0]]["positionEnd"] = wordsInLine[3]
                conclusionKey = wordsInLine[0]
                break

        for line in bratInput:

            wordsInLine = line.split()

            if (wordsInLine[0][0] == self.ARGUMENTATIVE_UNIT and wordsInLine[1] != "conclusion" and wordsInLine[1] != "MajorClaim"):

                # add claim or premise
                self.argumentDict[conclusionKey][wordsInLine[0]] = {}

                self.argumentDict[conclusionKey][wordsInLine[0]]["text"]= ' '.join(word for word in wordsInLine[4:])

                self.argumentDict[conclusionKey][wordsInLine[0]]["type"]= wordsInLine[1].lower()

                self.argumentDict[conclusionKey][wordsInLine[0]]["positionStart"] = wordsInLine[2]

                self.argumentDict[conclusionKey][wordsInLine[0]]["positionEnd"] = wordsInLine[3]

            elif (wordsInLine[0][0] == self.ARGUMENTATIVE_RELATION):

                self.relationDict[wordsInLine[0]] = {}

                if wordsInLine[1] == "support" or wordsInLine[1] == "supports":

                    schemeName = self.DEFAULT_INFERENCE

                    relationID = wordsInLine[3][5:]+schemeName

                    label = "0"

                elif wordsInLine[1] == "attack" or wordsInLine[1] == "attacks":

                    schemeName = self.DEFAULT_CONFLICT

                    relationID = "R" + wordsInLine[3][5:] + "-" + wordsInLine[2][5:]

                    label = "1"

                else:

                    schemeName  = " ".join(re.findall('[A-Z][^A-Z]*', wordsInLine[1]))

                    schemeNumber = self.argSchemeDict[schemeName]

                    label = "0"

                self.relationDict[wordsInLine[0]]["relationID"]=wordsInLine[3][5:]+schemeName

                self.relationDict[wordsInLine[0]]["type"]=schemeName

                self.relationDict[wordsInLine[0]]["label"]=label

                self.relationDict[wordsInLine[0]]["from"]=wordsInLine[2][5:]

                self.relationDict[wordsInLine[0]]["to"]=wordsInLine[3][5:]

            elif (wordsInLine[0][0] == self.ARGUMENTATIVE_TOP_LEVEL_RELATION):


                if wordsInLine[3] == self.PRO_STANCE:

                    self.relationDict[wordsInLine[0]] = {}

                    self.relationDict[wordsInLine[0]]["type"]=self.DEFAULT_INFERENCE

                    self.relationDict[wordsInLine[0]]["label"] = "0"

                    self.relationDict[wordsInLine[0]]["relationID"]="R" + wordsInLine[2] +"-" + conclusionKey

                    self.relationDict[wordsInLine[0]]["from"]=wordsInLine[2]

                    self.relationDict[wordsInLine[0]]["to"]=conclusionKey

                elif wordsInLine[3] == self.CON_STANCE:

                    self.relationDict[wordsInLine[0]] = {}

                    self.relationDict[wordsInLine[0]]["type"]=self.DEFAULT_CONFLICT

                    self.relationDict[wordsInLine[0]]["label"] = "1"

                    self.relationDict[wordsInLine[0]]["relationID"]="R" + wordsInLine[2] + conclusionKey

                    self.relationDict[wordsInLine[0]]["from"]=wordsInLine[2]

                    self.relationDict[wordsInLine[0]]["to"]=conclusionKey
