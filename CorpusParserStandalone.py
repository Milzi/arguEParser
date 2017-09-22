from arguEParser.Parsers import AIFParser as aif
from arguEParser.Parsers import IBMCorpusParser as ibm
from arguEParser.Parsers import BratParser as brat
import os


class main:

    inputdir = "inputCorpora"
    outputdir = "outputCorpus"
    corporaDirs = next(os.walk(inputdir))[1]

    for e, corpus in enumerate(corporaDirs):

        subdir = os.path.join(inputdir, corpus)

        if any(fname.endswith('.json') for fname in os.listdir(subdir)):

            IBM = False
            fileType = ".json"
            originalTextAvailable = True
            xmlParser = aif.AIFParser(corpus)
            outputDirectory = os.path.join(outputdir, corpus)

        elif all(fname.endswith('.txt') for fname in os.listdir(subdir)):

            print("läuft")

            IBM = True
            fileType = ".txt"
            originalTextAvailable = False
            xmlParser = ibm.IBMCorpusParser(corpus)
            outputDirectory = os.path.join(outputdir, corpus)


        elif any(fname.endswith('.ann') for fname in os.listdir(subdir)):

            IBM = False
            fileType = ".ann"
            originalTextAvailable = True
            xmlParser = brat.BratParser(corpus)
            outputDirectory = os.path.join(outputdir, corpus)

        else:
            continue

        if not os.path.exists(outputDirectory):
                os.makedirs(outputDirectory)

        for annotationFile in os.listdir(subdir):

            if annotationFile.endswith(fileType):

                annotationFilePath = os.path.join(subdir, annotationFile)

                print("Parsing file:")
                print(annotationFilePath)

                if originalTextAvailable:

                    originalTextFile = os.path.splitext(annotationFilePath)[0]+".txt"

                    xmlData = xmlParser.startParsing(annotationFilePath, originalTextFile)

                else:

                    xmlData = xmlParser.startParsing(annotationFilePath)

                if IBM:

                    for e, argumentation in enumerate(xmlData):
                        outputFileName = outputDirectory + "/"+ annotationFile + str(e)


                        with open(outputFileName +".xml", 'wb') as xmlOuput:
                            xmlOuput.write(argumentation)

                else:

                    outputFileName = outputDirectory +"/"+ annotationFile

                    with open(outputFileName +".xml", 'wb') as xmlOuput:
                        xmlOuput.write(xmlData)

                print("----Done----")
                continue

            else:
                continue
