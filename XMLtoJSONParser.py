import xmltodict, json
import os

class XMLtoJSONParser():

    def __init__(self, corpusName):

        self.corpusName = corpusName
        self.nodesDict = {}
        self.nodesDict["nodes"] = []
        self.nodesDict["edges"] = []
        self.uniqueRelationNodes = set()

        self.DEFAULT_INFERENCE_NUMBER = 72
        self.DEFAULT_CONFLICT_NUMBER = 71

        self.DEFAULT_INFERENCE = "Default Inference"
        self.DEFAULT_CONFLICT = "Default Conflict"

        self.argSchemeDict = {
            "-":"72",
            "Default Inference":"72",
            "Default Conflict": "71",
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
            "Waste":"33"
        }

    def startParsing(self, xmlData):

        xmlNodes = xmlData["Annotation"]["Proposition"]

        for proposition in range(len(xmlNodes)):

            self.nodesDict["nodes"].append(

                {
                    "id": xmlNodes[proposition]["@id"],
                    "x": 1,
                    "y": 1,
                    "color": "b",
                    "text": xmlNodes[proposition]["text"],
                    "type": "I",
                    "scheme": "0",
                    "visible": True
                })

            listTyp = list().__class__

            if "Relation" in xmlNodes[proposition]:

                xmlNodeRelations = xmlNodes[proposition]["Relation"]

                if xmlNodes[proposition]["Relation"].__class__ == listTyp:

                    for relationIndex in range(len(xmlNodeRelations)):

                        self.createEdges(xmlNodeRelations[relationIndex], xmlNodes[proposition])
                else:

                    self.createEdges(xmlNodeRelations, xmlNodes[proposition])

        if "OriginalText" in xmlData["Annotation"].keys():

            self.nodesDict["participants"] = []
            self.nodesDict["analysis"] = {
                "txt":xmlData["Annotation"]["OriginalText"]
            }

        return self.nodesDict


    def createEdges(self, xmlNodeRelations, xmlNode):

        if xmlNodeRelations["@relationID"] not in self.uniqueRelationNodes:

            if xmlNodeRelations["@type"] == self.DEFAULT_CONFLICT:

                relationNodeColor = "r"
                type = "CA"

            else:
                relationNodeColor = "g"
                type = "RA"



            if xmlNodeRelations["@type"] in self.argSchemeDict.keys():
                schemeID = self.argSchemeDict[xmlNodeRelations["@type"]]

            else:
                schemeID = "72"

            self.nodesDict["nodes"].append(

            {
                "id": xmlNodeRelations["@relationID"],
                "x": 1,
                "y": 1,
                "color": relationNodeColor,
                "text": xmlNodeRelations["@type"],
                "type": type,
                "scheme": schemeID,
                "descriptors":{},
                "visible": True
            })

            self.uniqueRelationNodes.add(xmlNodeRelations["@relationID"])

            self.nodesDict["edges"].append(
            {

                "from": {
                       "id": xmlNodeRelations["@relationID"]
                   },
                   "to": {
                       "id": xmlNodeRelations["@partnerID"]
                   }

                }
            )

        self.nodesDict["edges"].append(

            {
                "from": {
                        "id": xmlNode["@id"]
                    },
                    "to": {
                        "id": xmlNodeRelations["@relationID"]
                    }
            }
        )


class main:

    inputdir = "outputCorpus"
    outputdir = "jsonOutput"
    corporaDirs = next(os.walk(inputdir))[1]

    for e, corpus in enumerate(corporaDirs):

        subdir = os.path.join(inputdir, corpus)

        for annotationFile in os.listdir(subdir):

            if annotationFile.endswith(".xml"):
                print("Parsing file:")
                print(os.path.join(subdir, annotationFile))

                annotationFilePath = os.path.join(subdir, annotationFile)

                corpusName = corpus

                converter = XMLtoJSONParser(corpusName)

                with open (annotationFilePath, "r") as myfile:
                    data = myfile.read()

                xmlData = xmltodict.parse(data)

                jsonDict = converter.startParsing(xmlData)

                jsonOutput = json.dumps(jsonDict, ensure_ascii=False)

                outputDirectory = "jsonOutput/"+corpusName+"/"

                if not os.path.exists(outputDirectory):
                    os.makedirs(outputDirectory)

                with open (outputDirectory +annotationFile +".json", "w") as jsonFile:
                    jsonFile.write(jsonOutput)
