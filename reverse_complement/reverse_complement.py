import sys
from typing import BinaryIO, Iterator, Tuple


def parse_fasta(inp: BinaryIO) -> Iterator[Tuple[bytes, bytes]]:
    pass


def reverse_complement(inp: BinaryIO, outp: BinaryIO):
    translate_table = bytes.maketrans(
        b"ACGTUMRYKVHDB",
        b"TGCAAKYRMBDHV",
    )
    line_length = 80
    for name, sequence in parse_fasta(inp):
        translated = sequence.translate(translate_table)
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