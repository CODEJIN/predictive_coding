import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

def Sub_Pronunciation_Generate(phoneme_String):
    return [phoneme_String[0:index] for index in range(1, len(phoneme_String))]

class Model:
    def __init__(self):
        self.Load_Data()
    def Load_Data(self, lexicon_File = "ELP_groupData.csv", additional_Lexicon_File = None):
        with open (lexicon_File, "r") as f:
            readLines = f.readlines()[1:]
        splited_ReadLine = [readLine.replace('"','').strip().split(",")[1:] for readLine in readLines]
        self.word_Index_Dict = {word.lower(): index for index, (word, _, _, _, _) in enumerate(splited_ReadLine)}
        self.pronunciation_Dict = {word.lower(): pronunciation for word, pronunciation, _, _, _ in splited_ReadLine}
        self.frequency_Dict = {word.lower(): float(frequency) * 0.05 + 0.1 for word, _, _, frequency, _ in splited_ReadLine}
        self.human_RT_Dict = {word.lower(): float(rt) for word, _, _, _, rt in splited_ReadLine}

        if not additional_Lexicon_File is None:
            with open (additional_Lexicon_File, "r") as f:
                readLines = f.readlines()[1:]
            splited_ReadLine = [readLine.replace('"','').strip().split(",")[1:] for readLine in readLines]

            self.word_Index_Dict.update({word.lower(): index for index, (word, _, _, _, _) in enumerate(splited_ReadLine)})
            self.pronunciation_Dict.update({word.lower(): pronunciation for word, pronunciation, _, _, _ in splited_ReadLine})
            self.frequency_Dict.update({word.lower(): float(frequency) * 0.05 + 0.1 for word, _, _, frequency, _ in splited_ReadLine})
            self.human_RT_Dict.update({word.lower(): float(rt) for word, _, _, _, rt in splited_ReadLine})

        self.phoneme_List = []
        for pronunciation in self.pronunciation_Dict.values():
            self.phoneme_List.extend(pronunciation)
        self.phoneme_List = list(set(self.phoneme_List))

    def Test(self, phoneme_String):
        probability_Dict = {}

        probability_Dict[-1] = {x:0.0 for x in self.phoneme_List}
        new_Candidate_Word_List = []
        for word in self.word_Index_Dict.keys():
            pronunciation = self.pronunciation_Dict[word]
            new_Candidate_Word_List.append(word)            
            for phoneme in self.phoneme_List:            
                if phoneme == pronunciation[0]:
                    probability_Dict[-1][phoneme] += 1 #self.frequency_Dict[word]
                    break
        sum_Frequency = np.sum([x for x in probability_Dict[-1].values()])
        probability_Dict[-1] = {phoneme: probability_Dict[-1][phoneme] / sum_Frequency for phoneme in self.phoneme_List}
        candidate_Word_List = new_Candidate_Word_List


        for index, (test_Phoneme, test_Sub_String) in enumerate(zip(phoneme_String, Sub_Pronunciation_Generate(phoneme_String))):    #c, ca, cas, cast            
            probability_Dict[index] = {x:0.0 for x in self.phoneme_List}
            new_Candidate_Word_List = []            
            for word in candidate_Word_List:
                pronunciation = self.pronunciation_Dict[word]                
                if len(pronunciation) > index + 1 and test_Phoneme == pronunciation[index]:
                    new_Candidate_Word_List.append(word)                
                    for phoneme in self.phoneme_List:
                        if len(pronunciation) > index + 1 and phoneme == pronunciation[index + 1]:
                            probability_Dict[index][phoneme] += 1 #self.frequency_Dict[word]
                            break
            sum_Frequency = np.sum([x for x in probability_Dict[index].values()])
            probability_Dict[index] = {phoneme: probability_Dict[index][phoneme] / sum_Frequency for phoneme in self.phoneme_List}            
            candidate_Word_List = new_Candidate_Word_List

        new_Fig = plt.figure(figsize=(7 * np.minimum(2, len(probability_Dict)), 3 * np.ceil(len(probability_Dict) / 2)))
        for index in sorted(probability_Dict.keys()):
            error = 0.0
            next_Phoneme = phoneme_String[index + 1]
            for predicted_Phoneme in self.phoneme_List:
                if predicted_Phoneme == next_Phoneme:
                    error += np.abs(1 - probability_Dict[index][predicted_Phoneme])
                else:
                    error += np.abs(0 - probability_Dict[index][predicted_Phoneme])
            probability_List = [probability_Dict[index][phoneme] for phoneme in self.phoneme_List]

            plt.subplot(int(np.ceil(len(probability_Dict) / 2)), np.minimum(2, len(probability_Dict)), index + 2)
            plt.bar(self.phoneme_List, probability_List)
            plt.title("Input: {}     Location: {}    Error: {}".format(phoneme_String, index, error))
            plt.draw()
        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    new_Model = Model()
    new_Model.Test("fOrmj@l@")
    input()