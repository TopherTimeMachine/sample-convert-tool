import sys
import time
import argparse
import os
import logging

parser = argparse.ArgumentParser(description = "Wav file converter for Qun mk2 (requires sox). Converts wav files to 16bit 48kHz mono. Converts all files in a directory recursively.)")

parser.add_argument("--input", type=str, required = True, help = "Input file name or directory. (Required) If input is a directory then all files in the directory are processed recursively. If input is a file then only that file is processed. Only wav files are processed. ")
parser.add_argument("--output_dir", type=str, required = False, help = "Output folder name. (Defaults to folder named 'output')")
parser.add_argument("--separate_channels", action="store_true", help = "Separate channels")
parser.add_argument("--allmix", action="store_true", help = "Output mix and separated channels data")
parser.add_argument("--debug", action = "store_true", help = "Print debug messages ")

args = parser.parse_args()
if args.allmix:
    args.separate_channels = True

if args.debug:
    logging.basicConfig(level = logging.DEBUG)
else:
    logging.basicConfig(level = logging.INFO)

base_name = os.path.basename(args.input)

if args.output_dir == None:    # if arg.output_dir does not exist then default to "output"
    args.output_dir = "output"

if args.output_dir[-1] != "/": # if output_dir does not end with a slash then add it
    args.output_dir = args.output_dir + "/"

# create output directory if it does not exist
if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)

# check if sox is installed
if os.system("which sox >/dev/null 2>&1") != 0:
    print("Sox is not installed. Please install sox and try again.");
    print("Linux: sudo apt-get install sox");
    print("Mac: brew install sox or brew install sox --with-flac");
    print("Windows: https://sourceforge.net/projects/sox/files/sox/")
    sys.exit(1)

# function to convert wav file to 16bit 48kHz mono. take input file name and output file name as arguments. and  args (separate channels, allmix)
# put quotes around the file names so that spaces in the file names are handled correctly.
# clean up filename to remove spaces and non-alphanumeric characters (except for the dot before the extension)
# options is what comes from the command line arguments. passed to this function so that it can be used here.
def convert_wav(root, infile, options):
    if infile.endswith(".wav"):
        logging.debug("file = " + infile)
        command_common = "sox \"" + os.path.join(root, infile) + "\" "
        common_option = " -r 48000 -b 16 -c 1 "
        command_ending = " >/dev/null 2>&1" # redirect stdout and stderr to /dev/null so that they are not displayed on the console
        outfile = infile
        # remove spaces and non-alphanumeric characters from the file name (except for the dot before the extension)
        outfile = "".join([c for c in outfile if c.isalpha() or c.isdigit() or c=='.' ]).rstrip()
        outputDir = options.output_dir

        #update the output_dir to include the last directory from the root
        outputDir = os.path.join(outputDir, os.path.basename(root))
        logging.debug("output_dir = " + outputDir)
        
        # create subdirectory if it does not exist
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)

        # add .wav extension if it is not there
        if not outfile.endswith(".wav"):
            outfile = outfile + ".wav"

        logging.debug("outfile = " + outfile)
        if options.separate_channels:
            command = command_common + common_option + "\"" + os.path.join(outputDir, "l_" + outfile) + "\" remix 1" + command_ending
            logging.debug(command)
            os.system(command)
            command = command_common + common_option + "\"" + os.path.join(outputDir, "r_" + outfile) + "\" remix 2" + command_ending
            logging.debug(command)
            os.system(command)
        if options.separate_channels == False or args.allmix:
            #mixdown
            command = command_common + common_option + "\"" + os.path.join(outputDir, outfile) + "\"" + command_ending
            logging.debug(command)
            os.system(command)
   

# if args.input is a directory then process all files in the directory. process only wav files. 
# process subdirectories recursively. 
if os.path.isdir(args.input):
    logging.debug("input is a directory")
    for root, dirs, files in os.walk(args.input):
        print('\nProcessing Folder: '+ root+ " ", end='', flush=True) # print the folder name being processed
        for file in files:
            print('.', end='' , flush=True)  # print a dot for each file processed
            convert_wav(root, file, args)
    print()

else:
    logging.debug("input is a file : "+ args.input)
    # get the file name without the path
    base_name = os.path.basename(args.input)
    # get root of the input file name
    root = os.path.dirname(args.input)
    # convert the file
    convert_wav(root, base_name, args)

print("Finished. Saved to " + args.output_dir + " directory")




