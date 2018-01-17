import sys
import os
from preprocessors.nop import Nop
from preprocessors.token_processor import *
from comparators.winnowing import Winnowing

from util import Span
from compare import compare


def preprocess_and_fingerprint():
    _, ext = os.path.splitext(sys.argv[1])
    if ext == ".py":
        lang = "Python3"
    elif ext == ".c":
        lang = "C"
    preprocessor = TokenProcessor(
        lang,
        # StripWhitespace(),
        # StripComments(),
        # NormalizeIdentifiers(),
        # NormalizeStringLiterals(),
        # NormalizeNumericLiterals(),
        ExtractIdentifiers(),
        TokenPrinter(),
        Buffer(),
        TextPrinter()
    )
    comparator = Winnowing(12, 24)
    result = comparator.create_index(sys.argv[1], preprocessor)
    print(result)
    print(len(repr(result)))


def compare_two():
    def index(filename):
        preprocessor = Nop()
        comparator = Winnowing(16, 24)
        return comparator.create_index(filename, preprocessor)
    index1 = index(sys.argv[1])
    index2 = index(sys.argv[2])
    print(index1.compare(index2))


def similarities():
    directory = sys.argv[1]
    submissions = [f"{directory}/{d}/helpers.py"
                   for d in os.listdir(f"{directory}")
                   if os.path.isdir(f"{directory}/{d}")]
    results = compare("similarities/helpers.py", submissions)
    for i, result in enumerate(results[:8]):
        with open(f"{result.id1}/helpers.py", "r") as f:
            text1 = f.read()
        with open(f"{result.id2}/helpers.py", "r") as f:
            text2 = f.read()
        with open(f"out{i}a.txt", "w") as f:
            f.write(f"{result.id1}, ")
            f.write(f"{result.id2} (weight: {result.weight})\n\n")
            f.write(Span.highlight(result.spans1, text1))
        with open(f"out{i}b.txt", "w") as f:
            f.write(f"{result.id1}, ")
            f.write(f"{result.id2} (weight: {result.weight})\n\n")
            f.write(Span.highlight(result.spans2, text2))


if __name__ == "__main__":
    # preprocess_and_fingerprint()
    # compare_two()
    similarities()
