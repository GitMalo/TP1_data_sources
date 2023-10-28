import time
from collections import Counter
import matplotlib.pyplot as plt

# measure execution time
def execution_time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        return execution_time
    return wrapper

# dictionary implementation
@execution_time_decorator
def count_words_with_dict(text):
    words = text.split()
    word_count = {}
    for word in words:
        word = word.lower()
        word_count[word] = word_count.get(word, 0) + 1
    return word_count

# counter implementation
@execution_time_decorator
def count_words_with_counter(text):
    words = text.split()
    word_count = Counter(words)
    return word_count

with open("t8.shakespeare.txt", "r") as file:
    shakespeare_text = file.read()

execution_times_dict = []
execution_times_counter = []

for _ in range(100):
    execution_time_dict = count_words_with_dict(shakespeare_text)
    execution_times_dict.append(execution_time_dict)
    execution_time_counter = count_words_with_counter(shakespeare_text)
    execution_times_counter.append(execution_time_counter)

# Plot the graph
plt.plot(execution_times_dict, label='Dictionary Implementation', alpha=0.5)
plt.plot(execution_times_counter, label='Counter Implementation', alpha=0.5)
plt.legend()
plt.xlabel('Execution Time (seconds)')
plt.ylabel('Frequency')
plt.show()