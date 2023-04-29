class DFA:

    def __init__(self, Q: list, q0, F: list, d: dict):
        self.Q = Q
        self.q0 = q0
        self.F = F
        self.d = d
    
    def accept(self, w: str) -> bool:
        """
        Args:
            w (str): the input string

        Returns:
            bool: True if w is in L(M); False otherwise.
        """
        state = self.q0
        for x in w:
            state = self.d[state][x]
        return (state in self.F)
    

def __symmetric_difference(dfa1: DFA, dfa2: DFA, q0_1, q0_2, Q: dict)->str:
    if (q0_1 in dfa1.F) != (q0_2 in dfa2.F):
        return ""
    Q[(q0_1, q0_2)] = True
    Sigma = list(dfa1.d[dfa1.q0].keys())
    for a in Sigma:
        q1 = dfa1.d[q0_1][a]
        q2 = dfa2.d[q0_2][a]
        if (q1,q2) not in Q:
            s = __symmetric_difference(dfa1,dfa2, q1, q2, Q)
            if s != None:
                return a+s
    return None

def symmetric_difference(dfa1: DFA, dfa2: DFA) -> str:
    """
    Args:
        dfa1 (DFA):
        dfa2 (DFA):
    Returns:
        str: String in the symmetric difference of the automatons. None if the automatons are equivalent
    """
    return __symmetric_difference(dfa1, dfa2, dfa1.q0, dfa2.q0, {})
    