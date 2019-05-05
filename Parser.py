class Term:
    def __init__(self, operator, parameters=None):
        self.parameters = parameters
        self.operator = operator

        
    def represent_term(self):
        rep_tree = []
        rep_tree += [self.operator]
        if self.parameters is not None:
         for p in self.parameters:
             if p is not None:
              rep_tree += "("
              rep_tree += p.represent_term()
              rep_tree += ")"
            
        return rep_tree

class Parser:
    def __init__(self):
        pass
    def create_term(self, formula):
        if len(formula) > 3:
            if formula[:2] == "Or":
                formula = formula[3:len(formula) -1]
                operator = "Or"
            if formula[:3] == "And":
                formula = formula[4:len(formula) -1]
                operator = "And"
            if formula[:3] == "Not":
                formula = formula[4:len(formula) -1]
                operator = "Not"
            if formula[:4] == "Impl":
                formula = formula[5:len(formula) -1]
                operator = "Impl"
            if formula[:6] == "BiImpl":
                formula = formula[7:len(formula) -1]
                operator = "BiImpl"
            closed = True
            leftparameter = ""
            rightparameter = ""
            for i in range(0, len(formula)):
             if formula[i] == "(":
              closed = False
             elif formula[i]  == ")":
              closed = True
             if formula[i] == "," and closed:
                 rightparameter = formula[i:len(formula)]
                 break
             leftparameter += formula[i]
            leftparameterterm = self.create_term(leftparameter) #recursion
            rightparameterterm = self.create_term(rightparameter) #reursion
            term = Term(operator, [leftparameterterm, rightparameterterm])
            return term
        else:
            term = Term(formula,[])
            return term

    def replace_implication (self, term):
        if term.operator is not "Impl":
            return term
        else:
            new_parameters = [Term ("Not", [term.parameters[0]])]
            new_parameters += term.parameters[1:]
            replaced = Term("Or", new_parameters
            return replaced

    def replace_biimplication(self, term):
        if term.operator is not "BiImpl":
            return term
        else:
            subterm1 = Term("Or", [term[0], Term("Not", [term[1]])])
            subterm2 = Term("Or", [term[1], Term("Not", [term[0]])])
            replaced = Term("And", [subterm1, subterm2])
            return replaced

    def de_Morgan(self,term):
        replaced = term
        if term.operator is "Not":
            if term.parameters[0].operator == "Or":
                replaced = Term("And", [Term("Not", [term.parameters[0].parameters[0]]), Term("Not", [term.parameters[0].parameters[1]])])
            if term.parameters[0].operator == "And":
                replaced = Term("Or", [Term("Not", [term.parameters[0].parameters[0]]), Term("Not", [term.parameters[0].parameters[1]])])
            if term.parameters[0].operator == "Not":
                if term.parameters[0].parameters[0].parameters == None:
                    replaced = Term(term.parameters[0].parameters[0].operator)
                else:
                    replaced = Term(term.parameters[0].parameters[0].operator, parameters[0].parameters[0].parameters)
        return replaced

    def isClause(self,term):
        operators =("Or", "And", "Not", "Impl", "BiImpl")
        if term.operator not in operators:
            return True
        elif term.operator == "Not":
            if term.parameters[0].operator not in operators:
             return True
        elif term.operator == "Or":
            res = (isClause(term.parameters[0]) and isClause(term.parameters[1]))
            return res
        else:
            return False

    def apply_DistributiveLaw(self, term):
        if  term.operator is not "Or":
            return term
        else:
            if term.parameters[0].operator is not "And" or term.parameters[0].operator is not "And":
                return term
            parameter0 = Term("Or", [term.parameters[0], term.parameters[1].parameters[0]])
            parameter1 = Term("Or", [term.parameters[0], term.parameters[1].parameters[1]])
            return Term("And", [parameter0, parameter1])

    def convert_to_CNF(self, term):
        if term.operator == "Or":
            if self.isClause(term.parameters[0]) and self.isClause(term.parameters[1]):
                return term
            else:
                parameter0 = self.convert_to_CNF(self, term.parameters[0])
                parameter1 = self.convert_to_CNF(self, term.parameters[1])
                result = Term("Or", [parameter0, parameter1])
                result = self.apply_DistributiveLaw(result)
                return result
        elif term.operator == "Impl":
            parameter0 = self.convert_to_CNF(self, term.parameters[0])
            parameter1 = self.convert_to_CNF(self, term.parameters[1])
            result = Term("Impl", [parameter0, parameter1])
            result = self.replace_implication(result)
            return result
        elif term.operator == "BiImpl":
            parameter0 = self.convert_to_CNF(self, term.parameters[0])
            parameter1 = self.convert_to_CNF(self, term.parameters[1])
            result = Term("BiImpl", [parameter0, parameter1])
            result = self.replace_biimplication(result)
            return result
        elif term.operator == "And":
            if self.isClause(term.parameters[0]) and self.isClause(term.parameters[1]):
                return term
            else:
                parameter0 = self.convert_to_CNF(self, term.parameters[0])
                parameter1 = self.convert_to_CNF(self, term.parameters[1])
                result = Term("And", [parameter0, parameter1])
                return result
        else:
            return term




x= 1
#Raftek Test