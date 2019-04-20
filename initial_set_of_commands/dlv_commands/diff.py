import difflib
import re

def print_file(file, start_line, end_line):

    for i in range(start_line, end_line):
        print " " + file[i],

text1 = open("text1.txt").readlines()
text2 = open("text2.txt").readlines()

matches = difflib.SequenceMatcher(
    None, text1, text2).get_matching_blocks()

diff = difflib.unified_diff(text1, text2)

start_line = 0
end_line = 0
for line in diff:

    m0 = re.match(r'^@@ -(\d+),(\d+) +', line)
    if m0:
        end_line = int(m0.group(1)) - 1
        print_file(text1, start_line, end_line)
        start_line = end_line + int(m0.group(2))
    else:
        print line,

end_line = len(text1)
print_file(text1, start_line, end_line)
