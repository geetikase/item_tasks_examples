from collections import Counter
import json
import sys

def count_words(wordlist_filepath):
    with open(wordlist_filepath, 'r') as wordfile:
        words = [word.strip() for word in wordfile.readlines()]  
        from collections import Counter
        c = Counter(words)
        return c

if len(sys.argv) == 1:
    # When called with no args, print the task specs.
    with open('wordcount/spec.json', 'r') as spec:
        print(json.dumps(json.loads(spec.read()), indent=4))
else:
    task_name = sys.argv[1]
    if task_name == 'wordcount':
        # Expects an input file path, and an output file path.
        wordlist_filepath, wordcount_filepath = sys.argv[2:4]
        c = count_words(wordlist_filepath)
        with open(wordcount_filepath, 'w') as wordcountfile:
            wordcountfile.write('\n'.join(['%s: %s' % (word, count) for word, count in c.items()]))
    elif task_name == 'topwordcount':
        # Expects an input file path, a number of most frequent words, and an output file path.
        wordlist_filepath, top_n, wordcount_filepath = sys.argv[2:5]
        top_n = int(top_n)
        c = count_words(wordlist_filepath)
        with open(wordcount_filepath, 'w') as wordcountfile:
            wordcountfile.write('\n'.join(['%s: %s' % (word, count) for word, count in c.most_common(top_n)]))
    else:
        sys.stderr.write('Task "%s" not found.\n' % (task_name,))
