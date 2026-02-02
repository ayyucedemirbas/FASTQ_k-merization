import sys
import gzip
from collections import defaultdict
import json

def get_kmers(sequence, k, stride=1):
    n = len(sequence)
    if n < k:
        return

    for i in range(0, n - k + 1, stride):
        yield sequence[i : i + k]

def stream_fastq_kmers(filepath, k=6):
    try:
        open_func = gzip.open if filepath.endswith('.gz') else open
        
        with open_func(filepath, 'rt') as f:
            for i, line in enumerate(f):
                if i % 4 == 1:
                    seq = line.strip()
                    for kmer in get_kmers(seq, k):
                        yield kmer
                        
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def build_vocab_and_tokenize(kmer_stream):
    vocab = defaultdict(lambda: len(vocab))
    tokenized_data = []
    
    for kmer in kmer_stream:
        token_id = vocab[kmer] 
        tokenized_data.append(token_id)
        
    return tokenized_data, dict(vocab)

def save_outputs(tokens, vocabulary, token_file="tokens.txt", vocab_file="vocab.json"):
    print(f"Saving {len(tokens)} tokens to '{token_file}'...")
    with open(token_file, "w") as f:
        f.write(" ".join(map(str, tokens)))
        
    print(f"Saving vocabulary ({len(vocabulary)} k-mers) to '{vocab_file}'...")
    with open(vocab_file, "w") as f:
        json.dump(vocabulary, f, indent=4)

fastq_file = "sample.fastq"

K_SIZE = 4
    
print(f"Extracting {K_SIZE}-mers from {fastq_file}...")
    
#kmer_generator = stream_fastq_kmers(fastq_file, k=K_SIZE)
    
#for i, token in enumerate(kmer_generator):
    #if i >= 10: break
    #print(f"Token {i+1}: {token}")

integers, vocabulary = build_vocab_and_tokenize(stream_fastq_kmers("sample.fastq", k=4))

save_outputs(integers, vocabulary)
    
