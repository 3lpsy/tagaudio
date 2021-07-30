# tagaudio

This simple script leverages the mutagen library to add tags to audio files. While programs such as picard are great for accomplishing this, I could not find any CLI libraries that supported opus.

This script will work with any format mutagen supports. MP3 and WAV will probably not work, though it may be possible in the future to add alternative mechanisms for updating these files.

## Instructions

You will need mutagen installed [https://pypi.org/project/mutagen/](https://pypi.org/project/mutagen/). I may include a requirements.txt file later, but I just installed this via my package manager. You can use pip and (preferably) a venv/virtualenv if you wish. There are no other dependencies.

The program can target either a single file or a directory containing multiple files. If you wish to target nested directoiries, the script will prompt you for confirmation (to avoid accidentally tagging excessive files).

So if you wanted to update the 'artist' tag on a single file, you would run:

```
./tagaudio.py -t artist SuperCoolArtis path/to/file
```

The `-t`/`--tag` argument takes two values (the key and the value). It can be repeated multiple times for different tags.

If you don't want to be asked for confirmation before updating the file, simply use the `-c` switch to auto confirm.

## Usage

```
usage: tagaudio.py [-h] -t TAG TAG [-c] target

Tag files or directories

positional arguments:
  target                Individual file or directory to tag

optional arguments:
  -h, --help            show this help message and exit
  -t TAG TAG, --tag TAG TAG
                        Tag key/value to add (repeatable)
  -c, --confirm         auto confirm
```
