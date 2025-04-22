from src import *
import argparse

def main(n_player       = 6,
         player_names   = [],
         n_select       = 3,
         exclude_list   = []):
    
    # initialising pool
    wizard_dict = load_wizards(exclude_list=exclude_list)
    print('Wizard Selection Pool initialised excluding : ', *exclude_list)
    
    # initialising games
    GAME = game(n_player     = n_player, 
                player_names = player_names,
                n_select     = n_select,
                wizard_dict  = wizard_dict)
    
    while True:
        GAME.new_round()
        key_in = input("Press Enter for next round, type anything to quit: \n")
        if len(key_in)!=0: break
    
    return 

if __name__=='__main__':
    
    # receiving inputs
    parser = argparse.ArgumentParser()
    parser.add_argument('-np', '--n_player', 
                        type=int, default=6)
    parser.add_argument('-pn', '--player_names',
                        nargs='+', help="List of names", 
                        default=[])
    parser.add_argument('-ns', '--n_select', 
                        type=int, default=3)
    parser.add_argument('-ex', '--exclude_list', 
                        nargs='+', help="List of names",
                        default=[])
    args = parser.parse_args()

    main(n_player        = args.n_player,
         player_names    = args.player_names,
         n_select        = args.n_select,
         exclude_list    = args.exclude_list,)

