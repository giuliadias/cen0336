#!/usr/bin/env python3
# 6. Create a new function that computes and returns the reverse complement
#    of a sequence
#
#    - It will take a DNA sequence without spaces and no header as an argument
#      and return the reverse complement, with no spaces and no header.
#    - example `revComp_sequence = get_reverse_complement(dna)`


import sys


# global variable private to this class
NUCLEOTIDE_COMPLEMENT = str.maketrans(
    'acgturyswkmbdhvnACGTURYSWKMBDHVN',
    'tgcaayrwsmkvhdbnTGCAAYRWSMKVHDBN'
)
        
def wrap(maybe_linear_sequence, width=None):
    """
    Input: (Required) A linear sequence string without any existing newline 
           characters.
           (Optional) An integer `width` argument to specify the maximum
           line length to wrap the sequence flush to.
       
    Returns: A string of the input sequence, but with newline characters
           at fixed intervals specified by the `width` keyword argument.
    """

    # If the input sequence has newlines in it, we can quickly "delete" them
    # by replacing them with empty string "characters":
    linear_sequence = maybe_linear_sequence.replace('\n','')
    
    if width is None:
        # Set the default width of each line to be the max integer size of
        # your machine (typically either 2**(64-1) on 64-bit machines or
        # 2**(32-1) on 32-bit machines) by convention.
        width = sys.maxsize
        
    wrapped_sequence = ''
    linear_sequence_length = len(linear_sequence)  # pre-calc it
    for offset in range(0, linear_sequence_length, width):
        # Our function iterated over each sequence, jumping every `width`
        # nucleotides along the string. This is effectively like a sliding-
        # window approach, where windows do not overlap. The left coordinate
        # of the window is `offset`, the right coordinate is `offset+width`
        if offset+width < linear_sequence_length:
            # then the sliding window sits completely within the sequence:
            # Iter 1:
            # +---------+
            #    Iter 2: +---------+
            #               Iter 3: +---------+
            # ===================================   Sequence
            wrapped_sequence += linear_sequence[offset:(offset+width)] + "\n"
        else:
            # then the sliding window projects off the end of the sequence
            # and we need to bound the window to the end of the string.
            # Also, we don't want to add the newline to the last line
            #                          Iter 4: +---------+
            # ===================================   Sequence
            wrapped_sequence += linear_sequence[offset:linear_sequence_length]

    return wrapped_sequence

def gc_content(sequence):
    gc_chars = set('GCgc')
    gc_count = 0
    for nt in sequence:
        if nt in gc_chars:
            gc_count += 1
            
    return float(gc_count) / len(sequence)

def reverse_complement(sequence):
    """
    Return the reverse complemented sequence of the inputted sequence.
    """
    # Do it all in one go:
    # 1. `sequences[::-1]` reverses the string, which creates another string
    # 2. `string.translate(NUCLEOTIDE_COMPLEMENT)` complements the sequence 
    #    string and outputs another string, which gets returned
    return sequence[::-1].translate(NUCLEOTIDE_COMPLEMENT)

# If someone (accidentally?) tries to import this script, the following code
# would get executed, which is not what we want. Writing the following line
# protects against this because `__name__` will be assigned the module name
# and not "__main__" as it is if this script is executed as a script:
if __name__ == "__main__":
    fasta_infile = open(sys.argv[1], 'r')
    line_width = int(sys.argv[2])

    sequence = ''
    defline = [None,'']  # store ID and description in a list
    fasta_outfile = sys.stdout
    for line in fasta_infile:
        # FASTA files are allowed to have blank lines between sequence
        # records, and older versions of FASTA spec allowed for comment
        # lines starting with ';'. Skip these lines.
        if line.isspace() or \
           line.startswith(';'):
            continue

        # remove leading and trailing whitespace from the line
        line = line.strip()
        
        if line.startswith('>'):  # FASTA defline
            if len(sequence) > 0:
                # If we are parsing our first FASTA record, `sequence` will
                # still be an empty string (as initialized) and evaluate to
                # False, if we are parsing any other record, then we exec
                # the following code on the previously-seen record, then
                # re-initialize our variables for the current record.
                defline[0] += '-revcomp'
                fasta_outfile.write(">{0} %GC={1:.3f}\n{2}\n".format(
                    ' '.join(defline),
                    100.0 * gc_content(sequence),
                    wrap(reverse_complement(sequence), width=line_width)))
                sequence = ''

            # A split character of `None` means any whitespace.
            # `split()` can be told to split the first N instances of the
            # specified split character. Split on only the first whitespace
            # below (as descriptions may contain whitespaces)
            defline = line.lstrip('>').split(None, 1)

        else:
            sequence += line

    if len(sequence) > 0:
        defline[0] += '-revcomp'        
        fasta_outfile.write(">{0} %GC={1:.3f}\n{2}\n".format(
            ' '.join(defline),
            100.0 * gc_content(sequence),
            wrap(reverse_complement(sequence), width=line_width)))

    fasta_outfile.close()  # always be sure to close your output files!


    
