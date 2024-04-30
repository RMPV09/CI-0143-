import csv
import hashlib
import pprint
import multiprocessing
import time

def compute_sha256(word):
    sha256_hash = hashlib.sha256(word.encode()).hexdigest()
    return sha256_hash

# Single Thread Version

# def search_for_one_word_key(hashed_password):
#     for line in text_data:
#         word = line.strip()
#         computed_hashed_password = compute_sha256(word)
#         if (computed_hashed_password == hashed_password):
#             return word

# def search_for_two_word_key(hashed_password):
#     for i in range(len(text_data)):
#         for j in range(len(text_data)):
#             concatenated_word = f"{text_data[i]}{text_data[j]}"
#             computed_hashed_password = compute_sha256(concatenated_word)
#             if (computed_hashed_password == hashed_password):
#                 return concatenated_word

# def search_for_three_word_key(hashed_password):
#     for i in range(len(text_data)):
#         for j in range(len(text_data)):
#             for k in range(len(text_data)):
#                 triple_concatenated_word = f"{text_data[i]}{text_data[j]}{text_data[k]}\n"
#                 computed_hashed_password = compute_sha256(triple_concatenated_word)
#                 if (computed_hashed_password == hashed_password):
#                     return triple_concatenated_word

# One Word
def process_lines(hashed_password, text_lines, start, end, result_queue):
    for line in text_lines[start:end]:
        word = line.strip()
        computed_hashed_password = compute_sha256(word)
        if computed_hashed_password == hashed_password:
            result_queue.put(word)
            return word

def search_for_one_word_key(hashed_password):
    num_processes = multiprocessing.cpu_count()  # Get the number of CPU cores
    result_queue = multiprocessing.Queue()

    chunk_size = len(text_data) // num_processes
    processes = []

    for i in range(num_processes):
        start = i * chunk_size
        end = start + chunk_size if i < num_processes - 1 else len(text_data)
        process = multiprocessing.Process(target=process_lines, args=(hashed_password, text_data, start, end, result_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    # Collect results from the result queue
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())
    return results

# Two Words
def process_combinations(hashed_password, text_data, start, end, result_queue):
    for i in range(start, end):
        for j in range(len(text_data)):
            concatenated_word = f"{text_data[i]}{text_data[j]}"
            computed_hashed_password = compute_sha256(concatenated_word)
            if computed_hashed_password == hashed_password:
                result_queue.put(concatenated_word)
                return concatenated_word

def search_for_two_word_key(hashed_password):
    num_processes = multiprocessing.cpu_count()  # Get the number of CPU cores
    result_queue = multiprocessing.Queue()

    chunk_size = len(text_data) // num_processes
    processes = []

    for i in range(num_processes):
        start = i * chunk_size
        end = start + chunk_size if i < num_processes - 1 else len(text_data)
        process = multiprocessing.Process(target=process_combinations, args=(hashed_password, text_data, start, end, result_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    # Collect results from the result queue
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())

    return results

# Three words
def process_permutations(hashed_password, text_data, start, end, result_queue):
    for i in range(start, end):
        for j in range(len(text_data)):
            for k in range(len(text_data)):
                triple_concatenated_word = f"{text_data[i]}{text_data[j]}{text_data[k]}\n"
                computed_hashed_password = compute_sha256(triple_concatenated_word)
                if computed_hashed_password == hashed_password:
                    result_queue.put(triple_concatenated_word)
                    return triple_concatenated_word

def search_for_three_word_key(hashed_password):
    num_processes = multiprocessing.cpu_count()  # Get the number of CPU cores
    result_queue = multiprocessing.Queue()

    chunk_size = len(text_data) // num_processes
    processes = []

    for i in range(num_processes):
        start = i * chunk_size
        end = start + chunk_size if i < num_processes - 1 else len(text_data)
        process = multiprocessing.Process(target=process_permutations, args=(hashed_password, text_data, start, end, result_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    # Collect results from the result queue
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())

    return results

if __name__ == "__main__":
    text_data = ""
    # Read the text file and store its contents in a list
    with open('words.txt', 'r') as textfile:
        text_data = textfile.readlines()

    # Open the CSV file
    with open('user.csv', newline='') as csvfile:
        dictionary = {}
        row_count = 0
        # Create a CSV reader object
        reader = csv.reader(csvfile)
        next(reader)  # This skips the first row
        print("***************Checking one word passwords***************")
        start_time = time.time()
        for row in reader:
            # Access the second column (index 1 since indexing starts from 0)
            hashed_password = row[1]
            original_word = str(search_for_one_word_key(hashed_password))
            if (original_word and len(original_word) != 2):
                print("Found!", original_word)
                dictionary[original_word] = hashed_password
            row_count+=1 
        elapsed_time = time.time() - start_time
        print("Elapsed time:", elapsed_time, "seconds")


        if row_count != len(dictionary):
            csvfile.seek(0)
            next(reader)  # Skip the first row again
            print("***************Checking two words passwords***************")
            start_time = time.time()
            for row in reader:
                hashed_password = row[1]
                if hashed_password not in dictionary.values():
                    original_word = str(search_for_two_word_key(hashed_password))
                    if (original_word and len(original_word) != 2):
                        print("Found!", original_word)
                        dictionary[original_word] = hashed_password
            elapsed_time = time.time() - start_time
            print("Elapsed time:", elapsed_time, "seconds")
            
            if row_count != len(dictionary):
                csvfile.seek(0)
                next(reader)  # Skip the first row again
                print("***************Checking three words passwords***************")
                start_time = time.time()
                for row in reader:
                    hashed_password = row[1]
                    if hashed_password not in dictionary.values():
                        original_word = str(search_for_three_word_key(hashed_password))
                    if (original_word and len(original_word) != 2):
                            print("Found!", original_word)
                            dictionary[original_word] = hashed_password
                elapsed_time = time.time() - start_time
                print("Elapsed time:", elapsed_time, "seconds")
        if row_count != len(dictionary):
            print("There has been an error")
        else:
            print("It allright")

        pprint.pprint(dictionary)

