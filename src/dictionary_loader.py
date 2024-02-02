import json
import threading
from collections import OrderedDict


class DictionaryLoader:
    def __init__(self, dictionary_path, cache_size=10000,missing_log_path='missing_words.txt'):
        """
        Initializes the Dictionary Loader with a path to the .jsonl dictionary file,
        and sets up caching mechanisms and a file for logging missing words/prefixes.

        :param dictionary_path: Path to the .jsonl dictionary file.
        :param cache_size: Maximum number of dictionary entries to keep in cache.
        """
        self.dictionary_path = dictionary_path
        self.cache_size = cache_size
        self.cache = OrderedDict()  # Cache for frequently accessed dictionary entries
        self.missing_log_path = 'missing_words.txt'  # File to log missing words/prefixes
        self.missing_log_lock = threading.Lock()
    
    def load_dictionary_entry(self, prefix):
        """
        Loads the dictionary entry for a given prefix from the cache or the .jsonl file.
        Caches the entry if found, and logs to file if the prefix is missing.

        :param prefix: The prefix for which to load the dictionary entry.
        :return: Dictionary entry for the prefix or None if not found.
        """
        # Check if the entry is already in cache
        if prefix in self.cache:
            return self.cache[prefix]

        # Attempt to load the dictionary entry from the .jsonl file
        dictionary_entry = None
        with open(self.dictionary_path, 'r', encoding='utf-8') as file:
            for line in file:
                entry = json.loads(line)
                if prefix in entry:
                    dictionary_entry = entry[prefix]
                    self.cache_dictionary_entry(prefix, dictionary_entry)  # Cache the found entry
                    break
        
        if dictionary_entry is None:
            # If the entry is not found, log the missing word
            self.log_missing_word_or_prefix(prefix)
        
        return dictionary_entry
    
    def cache_dictionary_entry(self, prefix, dictionary_entry):
        """
        Caches a dictionary entry for a given prefix. If the cache exceeds the specified size,
        the least recently used entry is removed.

        :param prefix: The prefix of the dictionary entry to cache.
        :param dictionary_entry: The dictionary entry to cache.
        """
        # If the entry already exists, update it and move it to the end to mark it as recently used
        if prefix in self.cache:
            self.cache.move_to_end(prefix)
        self.cache[prefix] = dictionary_entry
        
        # Check if cache exceeds the specified size limit
        if len(self.cache) > self.cache_size:
            self.cache.popitem(last=False)  # Remove the least recently used entry (first inserted)


    
    def log_missing_word_or_prefix(self, word_or_prefix):
        """
        Logs a missing word or prefix to a file in a thread-safe manner.
        Creates the log directory if it does not exist.

        :param word_or_prefix: The missing word or prefix to log.
        """
        with self.missing_log_lock:
            with open(self.missing_log_path, 'a') as log_file:
                log_file.write(f"{word_or_prefix}\n")

    
    def get_translated_word(self, word):
        """
        Translates a word using the dictionary, leveraging cached entries for efficiency
        and logging any missing words or prefixes.

        :param word: The word to translate.
        :return: The translated word or the original word if a translation is not found.
        """
        prefix = word[:4]
        # Check if the prefix dictionary entry is in the cache
        if prefix in self.cache:
            prefix_dict = self.cache[prefix]
            # Check if the word is in the prefix dictionary
            if word in prefix_dict:
                return prefix_dict[word]
            else:
                self.log_missing_word_or_prefix(word)
        else:
            # Attempt to load the dictionary entry for the prefix if not in cache
            prefix_dict = self.load_dictionary_entry(prefix)
            if prefix_dict is not None:
                # If the word is in the newly loaded prefix dictionary
                if word in prefix_dict:
                    return prefix_dict[word]
                else:
                    self.log_missing_word_or_prefix(word)
            else:
                # Prefix not found in the dictionary
                self.log_missing_word_or_prefix(prefix)
        
        # Return the original word if no translation is found
        return word

    
    def preload_cache(self, prefixes):
        """
        Preloads cache with dictionary entries for a list of prefixes to minimize disk reads.

        :param prefixes: A list of prefixes to preload into the cache.
        """
        pass
