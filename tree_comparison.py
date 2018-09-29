import numpy as np
import matplotlib.pyplot as plt

def compareTwoTrees(tree1, tree2, show=False):
    '''
    compare two trees

    Args:
        tree1 (tree Obj): first tree to compare.
        tree2 (tree Obj): second tree to compare.
        show (bool): true prints the span matix

    Returns:
        float: inter-annotator agreement
    '''
    spanMatrix1, AnswerIDs1 = spanMatrix(tree1)
    spanMatrix2, AnswerIDs2 = spanMatrix(tree2)
    
    assert spanMatrix1.size == spanMatrix2.size, "The two tree obj do not have the same number of leaf nodes"
    
    if show:
        print(tree1)
        _printSpanMatrix(spanMatrix1, AnswerIDs1, title="Spanmatrix Tree1")
        print(tree2)
        _printSpanMatrix(spanMatrix2, AnswerIDs2, title="Spanmatrix Tree2")
    
    return _interAnnotatorAgreement(spanMatrix1, spanMatrix2)


    
def _printSpanMatrix(spanMatrix, AssertionIDs, title="Spanmatrix"):
    '''
    print on span matrix using pyplot

    Args:
        spanMatrix (np.matrix): spanmatrix
        AssertionIDs (List<str>): List of the Answer IDs (mostly [A1,...,An])
        title (str): title of the table
    '''
    fig, ax = plt.subplots()
    ax.axis('off')
    ax.axis('tight')
    
    ax.table(cellText=spanMatrix,
                      rowLabels=AssertionIDs,
                      colLabels=AssertionIDs,
                      loc='bottom')
    fig.tight_layout()
    fig.suptitle(title)
    plt.show()



def _interAnnotatorAgreement(spanMatrix1, spanMatrix2):
    '''
    compute confusion matrix and call the function to calculate k coefficient of agreement

    Args:
        spanMatrix1 (np.matrix): first spanmatrix
        spanMatrix2 (np.matrix): second spanmatrix

    Returns:
        float: inter-annotator agreement
    '''
    confusionMatrix = np.zeros((2,2))
    
    for row1, row2 in zip(spanMatrix1, spanMatrix2):
        for cell1, cell2 in zip(row1, row2):
            if not np.isnan(cell1) and not np.isnan(cell2):
                confusionMatrix[(int(cell1),int(cell2))] += 1
    
    return _computeK(confusionMatrix)
    

def _getExpectedAgreement(confusionMatrix):
    annotator1 = confusionMatrix.sum(axis=1)/confusionMatrix.sum()
    annotator2 = confusionMatrix.sum(axis=0)/confusionMatrix.sum()
    return np.multiply(annotator1, annotator2).sum()

def _getActualAgreement(confusionMatrix):
    return (confusionMatrix[1,1] + confusionMatrix[0,0]) / confusionMatrix.sum()

def _computeK(confusionMatrix):
    ExpectedAgreement = _getExpectedAgreement(confusionMatrix)     
    ActualAgreement = _getActualAgreement(confusionMatrix)
    
    K = (ActualAgreement - ExpectedAgreement)/(1 - ExpectedAgreement)
    return K

def spanMatrix(tree):
    '''
    compute spanmatrix for a QUD-tree

    Args:
        tree (tree Obj): tree obj to get the spanmatrix from

    Returns:
        matrix: spanmatrix
        AssertionIDs: List of the Answer IDs (mostly [A1,...,An])
    '''
    orderedLeaveNodes = [leave.tag for leave in tree.leaves()]
    AnswerIDs = ["A" + str(number) for number in range(1,len(orderedLeaveNodes)+1)]
    lengths = len(orderedLeaveNodes)
    
    matrix = np.empty((lengths, lengths))
    matrix.fill(np.nan)
    
    iu1 = np.triu_indices(lengths)
    matrix[iu1] = 0
    
    for nodeid in tree.nodes:
        if not tree.get_node(nodeid).is_leaf():
            leaves = [orderedLeaveNodes.index(leave.tag) for leave in tree.leaves(nodeid)]
            matrix[min(leaves), max(leaves)] = 1
    
    return matrix, AnswerIDs