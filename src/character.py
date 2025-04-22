# retrieve a single character
class character():

    def __init__(self, wizard_dict:dict, index:int):

        wizard_entry        = list(wizard_dict.items())[index]
        self.wizard_name    = wizard_entry[0]
        self.wizard_power   = wizard_entry[1]

        return None

    def print(self):

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

        print("\033[31m%s : \033[0m"%(self.wizard_name))
        for power_name,power_explanation in self.wizard_power.items():
            print('    \033[36m%s : \033[0m%s'%(power_name, power_explanation))
        # print("\033[36m%s\033[0m"%(self.player_names[i]))
        
        return None