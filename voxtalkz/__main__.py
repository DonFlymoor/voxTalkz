# __main__.py

from voxtalkz import *
import sys

def main():
    args = sys.argv
    debug = False
    if ("--debug") in args:
        args.remove("--debug")
        debug = True

    if ("--help" or "-h") in args:
        voxTalkz('', '').help()

    elif len(args) != 3:
        print("Expecting two arguments! Usage: voxtalkz [input file, output file] ")

    else:
        print(args)
        script = args[1]
        print(f"Using {script} as input file")
        try:
            open(script).close()
        except:
            print(f'No such file: {script}')
            script = False
        if script:
            filename = args[2]
            print(f"Outputting to {filename}")
            voxTalkz(script, filename, debug).ToSound()

if __name__ == "__main__":
	main()
