import sys
import os

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    print("This is the main routine.")
    print("It should do something interesting.")
    is_option = False
    commands = []
    option_key_pair = {}
    key = None
    #import pudb
    #pudb.set_trace()
    for arg in range(0,len(args)):
        if args[arg].startswith('--') is True:
            is_option = True

        if is_option == True:
            if args[arg].startswith('--') is True:
                key = args[arg]
                option_key_pair[key] = []
            else:
                if key != None:
                    option_key_pair[key].append(args[arg])
        else:
            commands.append(args[arg])

    if os.path.abspath('.') not in sys.path:
        sys.path.append(os.path.abspath('.'))


    from devicefarmtool.utils import utility
    utility(commands,option_key_pair)

    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do.

if __name__ == "__main__":
    main()