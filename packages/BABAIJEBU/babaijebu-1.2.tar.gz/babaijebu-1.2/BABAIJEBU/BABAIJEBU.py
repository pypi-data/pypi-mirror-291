import random as rnd
class Baba_ijebu:
    def __init__(self, trial_number=3 ):
        """
            Baba Ijebu is a game that allows it users to guess a random number from 0-10 setting thier trial number optionaly  
            Args:
                trial_number: int

            Attributes: 
                trial_number: set theb numbers of trials to guess the random number 
        """
        self.trial_number= trial_number
    def play_baba_ijebu(self):
        gen_ran = int(rnd.random()*11)    
        start = 1
        while(start < self.trial_number):
                
            userInput = int(input("Guess a random Number from 0-10.....  "))

            if(gen_ran != userInput):
                start += 1
                # print(gen_ran)
                print(gen_ran)
            else:
                start = self.trial_number
                
                print("Congratulation this is the random Number {} ".format(userInput))


# set_number = Baba_ijebu(trial_number=8)
# set_number.play_baba_ijebu()

