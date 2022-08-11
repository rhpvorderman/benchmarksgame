import sys
from typing import BinaryIO, Iterator, Tuple


def parse_fasta(inp: BinaryIO) -> Iterator[Tuple[bytes, bytes]]:
    name = next(inp)
    lines = []
    for line in inp:
        if line.startswith(b">"):
            yield name, b"".join(lines)
            name = line
            lines = []
            continue
        lines.append(line)
    yield name, b"".join(lines)


def reverse_complement(inp: BinaryIO, outp: BinaryIO):
    letters = b"ACGTUMRYKVHDB"
    complmn = b"TGCAAKYRMBDHV"
    translate_table = bytes.maketrans(
        letters + letters.lower(),
        complmn + complmn,
    )
    line_length = 60
    for name, sequence in parse_fasta(inp):
        translated = sequence.translate(translate_table, b'\n')
        reversed = translated[::-1]
        fasta_lines = [reversed[i:i+line_length]
                       for i in range(0, len(reversed), line_length)]
        outp.write(name)
        outp.write(b"\n".join(fasta_lines))
        outp.write(b"\n")
    outp.flush()


def main():
    reverse_complement(sys.stdin.buffer, sys.stdout.buffer)


if __name__ == "__main__":
    main()