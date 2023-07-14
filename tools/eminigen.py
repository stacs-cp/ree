import random
inequa = [">=","<=",">","<","="]
operators = ["*","+","-","/"]   
recursionProb = 0.4
def spawnEssence():
    '''
    Really really basic Emini generator.
    Integer only
    arithmetics
    Recursive expression generation (more probability of recursion-> more depth)
    '''
    spec = ""
    index = 0
    variables = 0
    decision = 0

    lettingNum = random.randint(1,3)
    findsNum = random.randint(1,3)
    constraintsNum = random.randint(1,3)
    

    for l in range(lettingNum):
        variables +=1
        spec = addLetting(spec,variables)
        

    for f in range(findsNum):
        decision +=1
        spec = addFind(spec,decision)
        
    for c in range(constraintsNum):
        spec = addConstraint(spec,decision,variables)   
    
    return spec

def addLetting(spec,variables):
    spec += f"letting resource{variables} be {random.randint(1,20)} \n" 
    return spec

def addFind(spec,decision):
    spec += f"find Y{decision}: int(0..100) \n"    
    return spec

def addConstraint(spec,decision,variables):
    spec += f"such that \n  {expression(decision,variables)} \n "
    return spec
def expression(decision,variables):
    expression = f"Y{random.randint(1,decision)} {random.choice(inequa)} resource{binaryExpress(random.randint(1,variables))}\n"
    return expression
    
def binaryExpress(inputExp):
    exp = str(inputExp)
    if random.random() > recursionProb:
        exp += f' {random.choice(operators)} resource{str(binaryExpress(exp))}'
    return exp

print(spawnEssence())
