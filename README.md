# Sample Convert Tool for Qun mk2
Convert a wav file or folder (and subfolders) of wav sample(s) to 16bit 48kHz mono for the [Qun mk2 sampler](https://github.com/raspy135/Qun-mk2)

This is a variation of the script that is in the Qun git repo [here](https://github.com/raspy135/Qun-mk2/blob/main/scripts/wavconvert.py)

# Requirements:

[Python 3](https://www.python.org/downloads/) - Is a easy to learn programming language.

[SOX Command Line](https://linux.die.net/man/1/sox) - A tool for converting audio files via the command line.




# How to use:

You can run via command line like 
```
python3 wavconvert.py MyFolder
```

This will process all the wav files found in the folder **MyFolder** and save the new output in a folder called **output**


To get all the options try the following:

```
python3 wavconvert.py -h
```


```

usage: wavconvert.py [-h] --input INPUT [--output_dir OUTPUT_DIR] [--separate_channels] [--allmix] [--debug]

Wav file converter for Qun mk2 (requires sox). Converts wav files to 16bit 48kHz mono. Converts all files in a directory recursively.)

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         Input file name or directory. (Required) If input is a directory then all files in the directory are processed recursively. If input is a file then only that
                        file is processed. Only wav files are processed.
  --output_dir OUTPUT_DIR
                        Output folder name. (Defaults to folder named 'output')
  --separate_channels   Separate channels
  --allmix              Output mix and separated channels data
  --debug               Print debug messages

```