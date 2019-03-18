import difflib
text1 = open("init.py").readlines()
text2 = open("init-2.py").readlines()

matches = difflib.SequenceMatcher(
    None, text1, text2).get_matching_blocks()

diff = difflib.unified_diff(text1, text2)

for line in diff:
    print line,
    # print(str(match.a) + " " + str(match.size))
