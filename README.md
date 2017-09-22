# ArgumentationCorpusParser

This parser allows the user to parse certain argumentation corpora into a unified model and format. The parser supports the following corpora:

1. Any corpus from the AIF-DB (http://corpora.aifdb.org/) such as AraucariaDB, Microtext, RRD
2. The CE-EMNLP-15 corpus from the IBM Debating Technologies Datasets (https://www.research.ibm.com/haifa/dept/vst/debating_data.shtml)
3. Argument Annotated Essays (version 2) (https://www.ukp.tu-darmstadt.de/data/argumentation-mining/argument-annotated-essays-version-2/)

These are the steps for executing the parser:


1. Download the project.
2. Unpack the project to [your directory]
3. Copy the corpora you want to parse into the folder [your directory]/arguEParser/inputCorpora
   * Make sure each dataset is in a seperate folder (e.g. AraucariaDB, IBM, RRD, Microtext)
4. Run the "CorpusParserStanalone.py" with python [your directory]/arguEParser/CorpusParserStanalone.py
5. Find the output inside the outputCorpus directory.
