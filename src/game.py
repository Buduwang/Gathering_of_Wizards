import random
from .character import character

class game():
    
    def __init__(self, n_player     : int, 
                       player_names : list,
                       n_select     : int,
                       wizard_dict  : dict):
        
        self.n_player       = n_player
        self.player_names   = player_names
        self.n_select       = n_select
        self.wizard_dict    = wizard_dict
        self.n_wizard       = len(self.wizard_dict)

        self.rule1 = "-"*100
        self.rule2 = "="*100

        if len(self.player_names) != self.n_player:
            for i in range(self.n_player):
                self.player_names.append('Player %i'%(i+1))

        print('Game ready with %i players: '%(self.n_player), ", ".join(self.player_names))
        print('Each player have %i wizard options out of a pool with %i wizards. \n'%(self.n_select, self.n_wizard))
        print(self.rule2, '\n\n')

        return None

    def new_round(self):

        selected_index = random.sample(range(self.n_wizard), 
                                       self.n_player*self.n_select)
        
        for i in range(self.n_player):

            # Colour	Code
            # Black	30
            # Red	31
            # Green	32
            # Yellow	33
            # Blue	34
            # Magenta	35
            # Cyan	36
            # White	37
            # Reset	0

            # print(self.rule2)
            # print(self.player_names[i])
            print("\033[33m%s\033[0m"%(self.rule2))
            print("\033[1;32m%s\033[0m"%(self.player_names[i]))
            for j in range(self.n_select):
                print(self.rule1)
                character(wizard_dict=self.wizard_dict,
                          index=selected_index[i*self.n_select+j]).print()
            # print(self.rule2, '\n\n')
            print("\033[33m%s\033[0m \n\n"%(self.rule2))

        return None

