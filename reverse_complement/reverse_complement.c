#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define INPUT_BUFFER_SIZE 8192
// Human genome chr1 is 250 million basepairs, so taking a 256 MB buffer seems reasonable.
#define SEQUENCE_BUFFER_INITIAL_SIZE 256 * 1024 * 1024

int fill_sequence_buffer(
    char **sequence_buffer_ptr, 
    size_t *sequence_buffer_size_ptr, 
    size_t *sequence_length_ptr,
    char *input_buffer,
    size_t input_buffer_length
) {
    size_t sequence_buffer_size = *sequence_buffer_size_ptr;
    size_t sequence_length = *sequence_length_ptr;
    if (sequence_length + input_buffer_length > sequence_buffer_size) {
        sequence_buffer_size *= 2;
        char *tmp = realloc(*sequence_buffer_ptr, sequence_buffer_size);
        
    }
}

int main() {
    char input_buffer[INPUT_BUFFER_SIZE];
    size_t sequence_buffer_size = SEQUENCE_BUFFER_INITIAL_SIZE;
    char *sequence_buffer = malloc(sequence_buffer_size); 
    if (sequence_buffer == NULL) {
        fprintf(stderr, "Could not allocate %d memory for sequence buffer", sequence_buffer_size);
        return 1;
    }

    size_t input_buffer_fill = fread(input_buffer, 1, INPUT_BUFFER_SIZE, stdin);
    if (input_buffer_fill == 0) {  //EOF
        return 0;
    }
    while (1) {
        char *end_of_name = memchr(input_buffer, '\n', input_buffer_fill);
        if (end_of_name == NULL) {
            fprintf(stderr, "Sequence names should be shorter than %d", INPUT_BUFFER_SIZE);
        }
    }
}