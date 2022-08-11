# The Computer Language Benchmarks Game
# https://salsa.debian.org/benchmarksgame-team/benchmarksgame/
#
# contributed by Ruben Vorderman

"""
This program reads a FASTA file from stdin and outputs a FASTA file to stdout
with all the sequences reverse complemented.
"""

import sys
from typing import BinaryIO, Iterator, List, Tuple


def parse_fasta(inp: BinaryIO) -> Iterator[Tuple[bytes, List[bytes]]]:
    """
    Create a generator from inp (a binary IO object) that yields
    names (bytes) and sequence parts (list of bytes objects)
    """
    # The rationale for parsing the sequences in lists of bytes rather than
    # singular bytes objects is that we can inverse the blocks individually
    # later. This is good for cache locality, memory usage and improves speed.
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
    # The translate function is implemented in C in Python and is therefore
    # the fastest method to complement sequences.
    letters = b"ACGTUMRYKVHDB"
    complmn = b"TGCAAKYRMBDHV"
    translate_table = bytes.maketrans(
        letters + letters.lower(),
        complmn + complmn,
    )
    # Writing chunks of sequence to output with a fixed line length is trickier
    # than using the whole sequence at once. b"\n".join(chunk_lines) does not
    # put a  newline at the last line, so we can save the offset and fill in
    # the remaining bytes with the next chunk
    line_length = 60
    for name, sequence_parts in parse_fasta(inp):
        outp.write(name)
        outp.write(b"\n")
        last_line_length = 0
        for part in reversed(sequence_parts):
            translated = part.translate(translate_table, b'\n')
            # [start:stop:step] -> using -1 as step creates a new reversed
            # bytes object. This is faster than reversing in place with a bytearray.
            rev = translated[::-1]
            offset = line_length - last_line_length
            fasta_lines = [rev[i:i + line_length]
                           for i in range(offset, len(rev), line_length)]
            last_line_length = len(fasta_lines[-1])
            outp.write(rev[:offset])  # Fill out remaining bytes on the line.
            outp.write(b"\n")
            outp.write(b"\n".join(fasta_lines))
        outp.write(b"\n")  # Terminate entire sequence with final newline.
    outp.flush()


if __name__ == "__main__":
    reverse_complement(sys.stdin.buffer, sys.stdout.buffer)
