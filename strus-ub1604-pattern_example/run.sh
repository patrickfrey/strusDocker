#!/bin/sh

# Option -K or --tokens is important for the example rules in program.rul
# It tells to print also the basic tokens of patterns generated and in program.rul there are only such patterns defined
cat names.txt | ./createNameRules.pl > program.rul
# xml:
# strusPatternMatcher -K -m modstrus_analyzer_pattern -p program.rul data/ 
# text/plain:
strusPatternMatcher -C text/plain -g plain -F -K -m modstrus_analyzer_pattern -p program.rul inputlist.txt

# Remarks:
# - Loading patterns can last very long, for 2000 patterns about one minute.
#   Therefore the pattern matcher should be started with a directory as input.
#   With a directory as input it processes all files in that directory.
# - Use option -t <N> for running the program with multiple threads and options -O
#   and -o to redirect output and stderr to files.

