'''
Markov model
'''

class Markov():
    ''''
    Class that builds a Markov model for text capitalization based the
    initial text provided. See the constructor method for details
    on attributes.
    '''
    def __init__(self, text):
        '''
        Construct a Markov model using the statistics of string "text"
        
        Inputs:
            text (list of lists of str): text to build a Markov model around
        '''
        self.case_pattern = {}
        self.count_cases(text)
        self.prob_model = {}
        self.probability()
        
    def count_cases(self, text):
        '''
        '''
        for sequence in text:
            i = 0
            n = len(sequence)
            while n > 1:
                word = sequence[i]
                next_word = sequence[i+1]
                # check current case
                case = self.check_case(word[:2])
                # check next case
                next_case = self.check_case(next_word[:2])
                i += 1
                n -= 1
                if next_case == 'Special Character':
                    continue
                self.case_pattern[case] = self.case_pattern.get(case, {})
                self.case_pattern[case][next_case] = self.case_pattern[case].get(next_case, 0) + 1

                
    def check_case(self, word):
        if word.islower():
            case = 'All Lower'
        elif word.isupper():
            case = 'All Upper'
        elif not word.isalpha():
            case = 'Special Character'
        else:
            case = 'Title'
        return case
    
    def probability(self):
        for case, counts in self.case_pattern.items():
            self.prob_model[case] = self.prob_model.get(case, {})
            counts_sum = sum(counts.values())
            for next_case, cnt in counts.items():
                self.prob_model[case][next_case] = cnt / counts_sum