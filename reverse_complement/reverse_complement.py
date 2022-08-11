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
                    yield name, seq_parts
                    return
                name_end = 0
                continue
            seq_parts.append(block[name_end:name_index])
            yield name, seq_parts
            break


def reverse_complement(inp: BinaryIO, outp: BinaryIO):
    letters = b"ACGTUMRYKVHDB"
    complmn = b"TGCAAKYRMBDHV"
    translate_table = bytes.maketrans(
        letters + letters.lower(),
        complmn + complmn,
    )
    line_length = 60
    last_line_length = 0
    for name, sequence_parts in parse_fasta(inp):
        outp.write(name)
        outp.write(b"\n")
        for part in reversed(sequence_parts):
            translated = part.translate(translate_table, b'\n')
            rev = translated[::-1]
            offset = line_length - last_line_length
            fasta_lines = [rev[i:i + line_length]
                           for i in range(offset, len(rev), line_length)]
            last_line_length = len(fasta_lines[-1])
            outp.write(rev[:offset])
            outp.write(b"\n")
            outp.write(b"\n".join(fasta_lines))
    outp.flush()


def main():
    reverse_complement(sys.stdin.buffer, sys.stdout.buffer)


if __name__ == "__main__":
    main()