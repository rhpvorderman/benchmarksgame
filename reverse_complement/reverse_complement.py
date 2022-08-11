import sys
from typing import BinaryIO, Iterator, Tuple


def parse_fasta(inp: BinaryIO) -> Iterator[Tuple[bytes, bytes]]:
    block_size = 64 * 1024
    name_index = 0
    block = inp.read(block_size)
    while True:
        name_end = block.find(b"\n", name_index)
        if name_end == -1:
            name_part = block[name_index:]
            block = inp.read(block_size)
            if block == b"":
                return
            name = name_part + block[:name_end]
        else:
            name = block[name_index: name_end]
        seq_parts = []
        while True:
            name_index = block.find(b">", name_end)
            if name_index == -1:
                seq_parts.append(block[name_end:])
                block = inp.read(block_size)
                if block == b"":
                    yield name, b"".join(seq_parts)
                    return
                name_end = 0
                continue
            if seq_parts:
                seq_parts.append(block[:name_index])
                yield name, b"".join(seq_parts)
                break
            yield name, block[name_end: name_index]
            break


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
        outp.write(b"\n")
        outp.write(b"\n".join(fasta_lines))
        outp.write(b"\n")
    outp.flush()


def main():
    reverse_complement(sys.stdin.buffer, sys.stdout.buffer)


if __name__ == "__main__":
    main()