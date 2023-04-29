from dfa import DFA,symmetric_difference

class Teacher:
    def __init__(self, dfa: DFA):
        self.dfa = dfa
    
    def member(self, w: str):
        return self.dfa.accept(w)
    
    def equiv(self, M: DFA):
        return symmetric_difference(self.dfa, M)
    
    def sigma(self):
        return list(self.dfa.d[self.dfa.q0].keys())

def __add_sufix(S: list,E: list, T: dict, e: str, teacher: Teacher):
    Sigma = teacher.sigma()
    E.append(e)
    for s in S:
        for a in Sigma:
            T[s+a+e] = teacher.member(s+a+e)

def __add_prefix(S: list,E: list, T: dict, s: str, teacher: Teacher):
    Sigma = teacher.sigma()
    S.append(s)
    for a in Sigma:
        for e in E:
            T[s + a + e] = teacher.member(s+a+e)

def __update_table_equiv(S: list,E: list, T: dict, u: str, teacher: Teacher):
    w = ''
    for x in u:
        w += x
        if w not in S:
            __add_prefix(S,E,T,w, teacher)

def __are__equal(s1: str, s2: str, E: list, T: dict):
    for e in E:
        if (T[s1+e] != T[s2+e]):
            return e
    return True

def __consistent(S: list,E: list, T:dict, Sigma: list):
    for s1 in S:
        for s2 in S:
            if s1 != s2 and __are__equal(s1,s2,E,T) == True:
                for a in Sigma:
                    e = __are__equal(s1 + a, s2 + a, E, T)
                    if e != True:
                        return a + e

def __closed(S: list,E: list, T:dict, Sigma: list):
    for s1 in S:
        for a in Sigma:
            is_in_S = False
            for s2 in S:
                if __are__equal(s1+a,s2,E,T) == True:
                    is_in_S = True
                    break
            if not is_in_S:
                return s1 + a

def __induct_DFA(S: list, E: list, T: dict, Sigma: list) -> DFA:
    i = 0
    q0 = 0
    Q = []
    F = {}
    d = {}
    for s in S:
        q = [T[s+e] for e in E]
        if q not in Q:
            Q.append(q)
            if T[s]:
                F[i] = q
            transitions = {}
            for a in Sigma:
                transitions[a] = [T[s+a+e] for e in E]
            d[i] = transitions
            i+= 1
    new_Q = list(range(len(Q)))
    for i in d:
        for a in d[i]:
            d[i][a] = Q.index(d[i][a])
    return DFA(new_Q,q0,list(F.keys()),d)


def learn(teacher: Teacher) -> DFA:
    S = []
    E = ['']
    T = {'': teacher.member('')}
    M = None
    __add_prefix(S,E,T, '', teacher)
    is_equiv = False
    while is_equiv != None:
        consistent = __consistent(S, E,T, teacher.sigma())
        closed = __closed(S, E,T, teacher.sigma())
        while consistent != None or closed != None:
            if consistent != None:
                __add_sufix(S,E,T,consistent,teacher)
            if closed != None:
                __add_prefix(S,E,T, closed, teacher)
            consistent = __consistent(S, E,T, teacher.sigma())
            closed = __closed(S, E,T, teacher.sigma())
        M = __induct_DFA(S,E,T,teacher.sigma())
        is_equiv = teacher.equiv(M)
        if is_equiv != None:
            __update_table_equiv(S,E,T,is_equiv,teacher)
    return M