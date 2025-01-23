import re

file_path = '20000_tweets.txt'

f = open(file_path, "r", encoding='utf-8')

line_count = 1
top_tweets = []
for tweet in f:
#   print("### Tweet", line_count, "#####")
#   print(tweet)

  top_tweets.append(tweet)
  line_count += 1
  if line_count > 10:
    break
f.close()

patterns = [
    r"\d*[./]?\d+\s?[%$€]?" ,     # 12345 12.35 or 12/35 or 12.35% or 12.35$
    r"[@#]?\w+" ,
    r"\w+-\w+" ,
    r"\S+" ,
    r"[!#&'-/<=>@$]+" ,
    r"[%:;`~_,]" ,
    r"[\"\(\)\*\+\.\?\[\\\]\^\{\|\}]+" ,
    r"(https?://)|(www.)\S+" ,
    r"n?'[a-z]{1,2}" ,
    r"\d{1,3}(?:,\d{3})+ ?\$?"
]


p = r"%?"                    # Suffix
c = r"[$€]?"                 # Prefix or Suffix
f = r"(.\d+)?"               # Suffix 
s = r"[+-−]?"                # Prefix    

i = s + r"\d+"
d = s + r"\d*.\d+"                  # 1.234 1234.454
g = r"\d{1,3}(?:,\d{3})+" + f       # 1,234,234.5678                            Numeric Grouping

## Resolve
b = s + r"\(?" + g + r"\)?"         # -(1,234) (12345678) (10^2)


# k = s + r"\d{1,3}(?:,\d{3})+" + f + p          # Groupings are subject to signs, %, and currency symbols, and decimal points (DONE!)      -1,234.5678% or -1,234.56$ -€234,456,456.98

experimental = [
   b ,                              # (123) -(123) -(-123)                      Negative, brackets
   d + p ,                          # +12.3, -123, −12.3, 123                   Negative, Decimal, Percentage
   d + r"[eE/^-−]" + i + p ,        # 10e46, 10E-46 -10\46, 10^46, 10-46        Negative, Decimal, Scientific, Fractions, Exponents, Hyphen, Percentage
   s + r"[$€]?\d+[$€%]?" ,          # $123, -€123, −123.45$, 123.45, -123%      Negative, Currency, Percentage ###Fix this

   r"(\d[.:/_])+\d" ,               # 1.234.4 3/5/2 1234_4_3 1,234:3:5              General Delimiters
   r"(" + b + r"[,;-])+\d" ,        # 1,234.6,4 2;-(-3,330);5.3;57 (1,514.2)-1,234-4        Negative, brackets, decimals, Comma-Semicolon-Hyphen separated lists
]

r"(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?"


r"[+-−]?\(?\d{1,3}(?:,\d{3})+(.\d+)?\)?"                                        # Decimals but no grouping

i
r"[+-−]?\d*.\d+%?"                                                              # Decimals but not bases
r"[+-−]?\d*.\d+[eE/^-−][+-−]?\d+%?"
r"[+-−]?[$€]?\d+[$€%]?"
r"(?:\d[.:/_])+\d"
r"([+-−]?\(?\d{1,3}(?:,\d{3})+(.\d+)?\)?[,;-])+\d"

# g1 = r"\b(?:\d{1,3}(?:,\d{3})*(?:\.\d+)?)\b"               It does lazy matching, so put the complex expression first 
# g2 = r"\b(?:\d+(?:\.\d+)?)\b"                              (?:) is a non-capturing group, use this to ensure it works correctly
# g1 = r"\b(?:\d{1,3}(?:,\d{3})+"+ f + r")\b"
# g2 = r"\b(?:\d+" + f + r")\b"
# group = f"{g1}|{g2}"

s = r"[+-−]?"
f = r"(?:\.\d+)?"
g1 = r"\d{1,3}(?:,\d{3})+"
g2 = r"\d+"
group = f"(?:{g1}|{g2}){f}"     # --> achieving grouping # 1,234,567.89 123.45 123,456 12
neg = s+group                       # --> achieving negative # -1,234,567.89 -123.45 -123,456 -12
percent = neg+r"%?"                  # --> achieving percentage # -1,234,567.89% -123.45% -123,456% -12%
print(group)


# a function to tokenize text into words
def tokenize(text):
    search_ptrn = '|'.join(patterns)
    # words = re.findall(search_ptrn, text.strip())
    words = re.findall(neg, text.strip())
    return words

# for i in experimental:
#     print(i)

# test = r" 1 -123,123% 432,654,567$ -€45,809"
# test = r" 1235 12.35 12/35 12.3 % 12.3 $"
# test = r" 123.4 123/5 123.456.789 123/456/789 123,45 123 123 1 234 -123 -123.45 $123 €123.45 123% 123.45% 1.23e5 1,234,567 1/2"
# test = r" 123 -42 1e6 1.23e-4 1_000_000 1,234,567 1.234,56 01/21/2024 13:45 1,2,3 1-2-3 123.45 .45 50.5% 5+3 1/2 10^6 10² $123 €123,45 123$  "
test = " 123,456,789 1,234.5677 1.23 123456.789 -1,234.5677 -1.23"
debug = tokenize(test)
print(test, debug)

# tokenized_top_tweets = [tokenize(tweet) for tweet in top_tweets]
# for tokenized_tweet in tokenized_top_tweets:
#   print(tokenized_tweet)