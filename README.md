# Hash-Map-Implementation
Portfolio Project for Oregon State CS 261 Data Structures




There were two parts to this assignment. In the first part, I completed an implementation of a hash map. In the second part, I implemented a concordance program. 

Part 1: Hash Map
This hash map uses a hash table of buckets, each containing a linked list of hash links. Each hash link stores the key-value pair (string and integer in this case) and a pointer to the next link in the list. this program is titled hash_map.py    



Part 2: Concordance
The concordance program, word_count.py, imports the hash_map.py program, takes an input document, computes the number of times each word was used in the document, and returns the top X words and associated counts. I have chosen to have the program display the top 10 words and the associated counts in a list of tuples. Included in the repo is a text document of Alice in Wonderland as an example document.

 
