import spacy

questionWords = set(["what", "why", "when", "how", "who"])
otherWords = set(["we", "it", "problem", "solution", "argument"])

def getUnknownNouns(qudQuestion, priviousText, underneathText, nlp):
       
    QuestionDoc = nlp(qudQuestion)
    TextDoc = nlp(priviousText)
    
    QuestionNouns = set([chunk.root.lemma_ for chunk in QuestionDoc.noun_chunks])
    TextNouns = set([chunk.root.lemma_ for chunk in TextDoc.noun_chunks])
    
    UnknownNouns = QuestionNouns - TextNouns - questionWords - otherWords
    
    if priviousText != "" and qudQuestion[0] != "[":
        if UnknownNouns != set():
            print("===========")
            print(priviousText)
            print()
            print(qudQuestion)
            print()
            print(underneathText)
            print()
            print(UnknownNouns)

        return len(UnknownNouns)
    
    else:
        return 100

def getUnknownVerbs(qudQuestion, priviousText, underneathText, nlp):
    QuestionDoc = nlp(qudQuestion)
    TextDoc = nlp(priviousText)
    
    QuestionVerbs = set([token.lemma_ for token in QuestionDoc if token.pos_ == "VERB" and not token.tag_ in ["MD", "BES", "HVS"]and not token.lemma_ in ["be", "do", "have"]])
    
    TextVerbs = set([token.lemma_ for token in TextDoc if token.pos_ == "VERB" and not token.tag_ in ["MD", "BES", "HVS"] and not token.lemma_ in ["be", "do", "have"]])
    UnknownVerbs = QuestionVerbs - TextVerbs 
    
    if priviousText != "" and qudQuestion[0] != "[":
        if UnknownVerbs != set():
            print("===========")
            print(priviousText)
            print()
            print(qudQuestion)
            print()
            print(underneathText)
            print()
            print(UnknownVerbs)

        return len(UnknownVerbs)
    
    else:
        return 100