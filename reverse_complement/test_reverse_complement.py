import io
import sys

from reverse_complement import reverse_complement

if __name__ == "__main__":
    with open("revcomp-input.txt", "rb") as inp:
        outp = io.BytesIO()
        reverse_complement(inp, outp)
    with open("revcomp-output.txt", "rb") as testf:
        correct = testf.read()
        if outp.getvalue() == correct:
            print("Sucess!")
        else:
            print("Failure!")
            sys.exit(1)
