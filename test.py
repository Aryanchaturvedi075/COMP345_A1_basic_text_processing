import re

# f = r"(?:\.\d+)?"
# grp = r"(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?"
# sgn = r"[+-−]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?"
# per = r"[+-−]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?%?"
# cur = r"[+-−]?[$€]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?[$€]?%?"                                                     ### Will match per, sgn, grp, gi, dec and int too
# opn = r"[+-−]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?[eE/^]?[+-−]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?"
# ocp = r"[+-−]?[$€]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?[eE/^]?[+-−]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?[$€]?%?"    ### Will match opn too 
# brc = r"[+-−]?\([+-−]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?\)"
# bcp = r"[+-−]?\([+-−]?[$€]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?[$€]?%?\)"                                           ### Will match brc too
# bop = r"[+-−]?[$€]?\([+-−]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?[eE/^]?[+-−]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?\)[$€]?%?"
# glm = r"(?:\d+[_.:/\-−])+\d+"
# svl = r"(?:[+-−]?\([+-−]?[$€]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?[$€]?%?\)[,;\-−])+[+-−]?\([+-−]?[$€]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?[$€]?%?\)"
# sdf = r"[@#]?\w+"
# sfw = r"\w+-\w+"
# efw = r"\S+"
# weg = r"[!#&'-/<=>@$€]+"
# rg4 = r"[%:;`~_,]"
# eww = r"[\"\(\)\*\+\.\?\[\\\]\^\{\|\}]+"
# efe = r"(https?://)|(www.)\S+"
# rwg = r"n?'[a-z]{1,2}"

s, c, p, op  = r"[+-−]?", r"[$€]?", r"%?", r"[eE/^*_:]?"
gi = r"\d{1,3}(?:,\d{3})+"
grp = r"(?:"+ gi +r"|\d+)(?:\.\d+)?"
sgn = s + grp
per = sgn + p
cur = s + c + grp + c + p
opn = sgn + op + sgn
ocp = s + c + grp + op + sgn + c + p
brc = s + r"\(" + sgn + r"\)"
bcp = s + r"\(" + cur + p + r"\)"
bop = s + c + r"\(" + opn + r"\)" + c + p
glm = r"(?:\d+[_.:/\-−]){2,}\d+"
svl = r"(?:" + bcp + r"[,;\-−])+" + bcp

patterns = [ svl, bop, glm, ocp, bcp, cur ]
patterns = [ glm, ocp ]

# s, c, p, op  = r"[+-−]?", r"[$€]?", r"%?", r"[eE/^*_:]?"
# gi = r"\d{1,3}(?:,\d{3})+"
# grp = r"(?:"+ gi +r"|\d+)(?:\.\d+)?"
# sgn = s + grp
# cur = s + c + grp + c + p
# opn = sgn + op + sgn
# bcp = s + r"\(" + cur + p + r"\)"


# patterns = [
#     r"(?:" + bcp + r"[,;\-−])+" + bcp ,
#     s + c + r"\(" + opn + r"\)" + c + p ,
#     r"(?:\d+[_.:/\-−]){2,}\d+" , 
#     s + c + grp + op + sgn + c + p ,
#     bcp ,
#     cur ,
# ]


# a function to tokenize text into words
def tokenize(text):
    combined_pattern = '|'.join(f'(?:{pattern})' for pattern in patterns)
    words = re.findall(combined_pattern, text.strip())
    return words

if __name__ == "__main__":
    test = r" 123 -42 1e6 1.23e-4 1_000_000 1,234,567 1,234.56 01/21/2024 13:45 13:45:45:45 (1)−(2.3)-(3);($4) 1-2-3 123.45 .45 50.5% 5+3 1/2 10^6 $123 €12,345,678 123$ 1.2.3.4.454.45 1_234 1:302"
    # test = r" 1.23e-4 50.5% 1_000_000  01/21/2024 1-2-3 13:45:45:45 1.2.3.4.454.45"
    # test = " 123,456,789 1,234.5677 1.23 123456.789 -1,234.5677 -1.23"
    # test = r" 1_000_000 01/21/2024 1−2−3 "
    debug = tokenize(test)
    print(test, debug)
