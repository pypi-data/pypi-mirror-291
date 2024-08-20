import ctypes
import os
import platform
import bisect

# Determine the correct shared library file based on the OS and architecture
system = platform.system()
arch, _ = platform.architecture()

if system == "Windows":
    if arch == "32bit":
        lib_path = os.path.abspath(r"./lib/rdrand32.dll")
        c_uint_type = ctypes.c_uint32
    else:
        lib_path = os.path.abspath(r"./lib/rdrand64.dll")
        c_uint_type = ctypes.c_uint64
elif system == "Linux":
    if arch == "32bit":
        lib_path = os.path.abspath(r"./lib/librdrand.so")
        c_uint_type = ctypes.c_uint32
    else:
        lib_path = os.path.abspath(r"./lib/librdrand64.so")
        c_uint_type = ctypes.c_uint64
else:
    raise RuntimeError("Unsupported operating system")



#Get just the number from the architecture
archN = int(arch[:2])


# Load the shared library
lib = ctypes.CDLL(lib_path)

# Define the argument and return types
lib.get_random_number.argtypes = [ctypes.POINTER(c_uint_type)]
lib.get_random_number.restype = ctypes.c_int

def getRDRAND():
    rand = c_uint_type()
    result = lib.get_random_number(ctypes.byref(rand))
    if result == 1:
        return rand.value
    else:
        raise RuntimeError("Failed to generate random number")

def random():
    '''
    Generates a random number between 0 and 1
    :return: A random number between 0 and 1
    '''
    return getRDRAND() / (2**archN - 1)

def randrange(start = 0, stop = 1, step=1):
    '''
    Return a randomly selected element from range(start, stop, step).
    :param start: Initial value of the range
    :param stop: Last value of the range
    :param step: Step of the range
    :return: A random number between start and stop with the specified step
    '''



    return start + step * (getRDRAND() % ((stop - start) // step + 1))

def randint(a=0, b=1):
    '''
    Return a random integer N such that a <= N <= b.
    :param a: Initial value of the range
    :param b: Last value of the range
    :return: A random number between a and b
    '''

    if a > b:
        raise ValueError("Invalid range parameters")

    return a + getRDRAND() % (b - a + 1)

def choice(seq):
    '''
    Return a random element from the non-empty sequence seq.
    :param seq: Sequence of elements
    :return: A random element from the sequence
    '''

    if not seq:
        raise ValueError("Empty sequence")

    return seq[getRDRAND() % len(seq)]

def shuffle(seq):
    '''
    Shuffle the sequence seq in place.
    :param seq: Sequence to shuffle
    :return: None
    '''

    if not seq:
        raise ValueError("Empty sequence")

    for i in range(len(seq) - 1, 0, -1):
        j = getRDRAND() % (i + 1)
        seq[i], seq[j] = seq[j], seq[i]
        
def getrandbits(k=8):
    '''
    Returns a Python integer with k random bits.
    :param k: Number of bits to generate
    :return: A random number with k bits
    '''

    if k <= 0:
        raise ValueError("Number of bits must be greater than 0")

    num_bytes = (k + 7) // 8  # Calculate the number of bytes needed
    random_bits = 0
    for _ in range(num_bytes):
        random_bits = (random_bits << 8) | getRDRAND()
    return random_bits & ((1 << k) - 1)


def choices(population, weights=None, cum_weights=None, k=1, repetitions=True):
    '''
    Return a list of k elements chosen from the population with optional weights.
    :param population: List of elements to choose from
    :param weights: Optional list of weights corresponding to the population elements
    :param cum_weights: Optional cumulative weights
    :param k: Number of elements to choose
    :param repetitions: If True, repetitions are allowed. If False, repetitions are not allowed.
    :return: A list of k elements chosen from the population
    '''
    if not population:
        raise ValueError("Population cannot be empty")
    if k <= 0:
        raise ValueError("Number of elements to choose must be greater than zero")
    if cum_weights is None:
        if weights is None:
            total = len(population)
            cum_weights = [i + 1 for i in range(total)]
        else:
            cum_weights = []
            cumulative_sum = 0
            for weight in weights:
                cumulative_sum += weight
                cum_weights.append(cumulative_sum)
    total = cum_weights[-1]

    if repetitions:
        return [population[bisect.bisect(cum_weights, random() * total)] for _ in range(k)]
    else:
        if k > len(population):
            raise ValueError("Number of elements to choose cannot be greater than the population size")
        chosen = set()
        result = []
        while len(result) < k:
            choice = population[bisect.bisect(cum_weights, random() * total)]
            if choice not in chosen:
                chosen.add(choice)
                result.append(choice)
        return result

def sample(population, k=1):
    '''
    Return a k length list of unique elements chosen from the population sequence or set.
    :param population: List of elements to choose from
    :param k: Number of elements to choose
    :return: A list of k unique elements chosen from the population
    '''

    if k > len(population):
        raise ValueError("Sample size cannot be greater than the population size")

    return choices(population=population, k=k, repetitions=False)


def uniform(a=0, b=1):
    '''
    Get a random float between a and b
    :param a: Initial value of the range
    :param b: Last value of the range
    :return: A random number between a and b
    '''

    if a > b:
        raise ValueError("a must be less than or equal to b")

    return a + (b - a) * random()

def triangular(low, high, mode):
    '''
    Get a random number between low and high with the specified mode
    :param low: Initial value of the range
    :param high: Last value of the range
    :param mode: Mode of the range
    :return: A random number between low and high with the specified mode
    '''
    if not (low <= mode <= high):
        raise ValueError("Mode must be between low and high")

    u = random()
    if u < (mode - low) / (high - low):
        return low + ((high - low) * (mode - low) * u) ** 0.5
    else:
        return high - ((high - low) * (high - mode) * (1 - u)) ** 0.5