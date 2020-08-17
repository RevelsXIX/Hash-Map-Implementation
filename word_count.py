def top_words(source, number):
    """
    Takes a plain text file and counts the number of occurrences of case insensitive words.
    Returns the top `number` of words in a list of tuples of the form (word, count).

    Args:
        source: the file name containing the text
        number: the number of top results to return (e.g. 5 would return the 5 most common words)
    Returns:
        A list of tuples of the form (word, count), sorted by most common word. (e.g. [("a", 23), ("the", 20), ("it", 10)])
    """

    # keys = set()

    ht = HashMap(997, hash_function_1)

    # This block of code will read a file one word as a time and
    # put the word in `w`.
    with open(source) as f:
        for line in f:
            words = rgx.findall(line)
            for w in words:
                # lowercase all the words so they're uniform
                w = w.lower()
                # check if key already exists, if it does, update the value of the key
                # in the hash table, if not, add a new node at beginning of bucket.
                if ht.contains_key(w):
                    wValue = ht.get(w)
                    wValue += 1
                    ht.put(w, wValue)
                else:
                    ht.put(w, 1)
    # run helper function from hash_map.py
    hashedWords = ht.top_word_helper()
    newWordList = []
    # make a new list, create tuples from word node objects sent from hash map.
    for word in hashedWords:
        wordTuple = (word.key, word.value)
        newWordList.append(wordTuple)

    # sort list of words, slice list of words, return list of words
    sortWordList = sorted(newWordList, reverse=True, key=getValue)
    sortWordList = sortWordList[:number]

    return sortWordList


if __name__ == '__main__':
    print(top_words("alice.txt", 10))
