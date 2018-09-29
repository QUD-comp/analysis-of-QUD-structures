import spacy
import pandas as pd

def getQuestions(tree):
    questions = []
    priviousTexts = []
    underneathTexts = []
    qudStacks = []
    for node in tree.all_nodes():
        if not node.is_leaf():
            assert node.tag[-1] =='?', "Node Text is not a question: " + node.tag
            
            underneathleaves = [leaf for leaf in tree.leaves(node.identifier)]
            underneathleaves.sort(key=lambda x: x.identifier)
            underneathTexts.append(" ".join([leaf.tag for leaf in underneathleaves]))
            priviousLeaves = [leaf for leaf in tree.leaves() if leaf.identifier < node.identifier]
            priviousLeaves.sort(key=lambda x: x.identifier)
            priviousTexts.append(" ".join([leaf.tag for leaf in priviousLeaves]))
            qudStacks.append(getQUDStack(tree, node))
            
            questions.append(node.tag)
            
    return questions, underneathTexts, priviousTexts, qudStacks



def getQuestionType(question, nlp):
    doc = nlp(question)
    if doc.text == "What is the way things are?":
        return "Big Question"
    
    if doc[:2].text == "What about":
        return "What about"
    if doc[0].pos_ == "VERB":
        print(question)
        return "Yes/No"
    return doc[0].text

def getQUDStack(tree, node):
    stack = [node]
    while not tree.parent(node.identifier) == None:
        parent = tree.parent(node.identifier)
        stack.append(parent)
        node=parent

    return [question.tag for question in stack]

def createQuestionDF(tree):
    nlp = spacy.load('en')
    questions, underneathTexts, priviousTexts,qudStacks = getQuestions(tree)
    newQuestionDF = pd.DataFrame()
    newQuestionDF["question"] = questions
    newQuestionDF["underneathTexts"] = underneathTexts
    newQuestionDF["priviousTexts"] = priviousTexts
    newQuestionDF["qudStack"] = qudStacks
    newQuestionDF["span"] = [len(underneathText) for underneathText in underneathTexts]
    newQuestionDF["type"] = [getQuestionType(question, nlp) for question in newQuestionDF["question"]]
    return newQuestionDF