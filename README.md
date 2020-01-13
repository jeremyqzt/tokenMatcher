# TokenMatcher
This program is a simple application to scan through a codebase (requires ctags) and then matches each function name to a line with a special token. The comparision is based on an offset which can be provided using -p option.

Possible uses for the application is to scan through a code base for per-function documentation, it will report if something is missing.

After finishing the comparision, lines missing the token are printed. Utilize a redirect (i.e. > or >> ) if a file output is required. 

# Usage
python tokMatch.py -p 1 -t ".c" -r 'some token' /path/to/files

# Testing
Tested briefly with python 2.7 and 3.5
