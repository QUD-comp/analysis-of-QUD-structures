import spacy

questionWords = set(["what", "why", "when", "how", "who"])
otherWords = set(["we", "it", "problem", "solution", "argument"])

def getGivenNouns(qudQuestion, priviousText, underneathText, nlp):
       
    QuestionDoc = nlp(qudQuestion)
    TextDoc = nlp(priviousText)
    
    QuestionNouns = set([chunk.root.lemma_ for chunk in QuestionDoc.noun_chunks])
    TextNouns = set([chunk.root.lemma_ for chunk in TextDoc.noun_chunks])
    
    GivenNouns = TextNouns.intersection(QuestionNouns)
    
    return len(GivenNouns), GivenNouns
        

def getGivenVerbs(qudQuestion, priviousText, underneathText, nlp):
    QuestionDoc = nlp(qudQuestion)
    TextDoc = nlp(priviousText)
    
    QuestionVerbs = set([token.lemma_ for token in QuestionDoc if token.pos_ == "VERB" and not token.tag_ in ["MD", "BES", "HVS"]and not token.lemma_ in ["be", "do", "have"]])
    
    TextVerbs = set([token.lemma_ for token in TextDoc if token.pos_ == "VERB" and not token.tag_ in ["MD", "BES", "HVS"] and not token.lemma_ in ["be", "do", "have"]])
    GivenVerbs = QuestionVerbs.intersection(TextVerbs)
    
    return len(GivenVerbs), GivenVerbs