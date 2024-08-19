from time import perf_counter
from colorama import Fore


def time_decorator(func):
    def wrapper(*args, **kwargs):
        begin_time = perf_counter()
        output = func(*args, **kwargs)
        end_time = perf_counter() - begin_time
        print(f"{Fore.BLUE}[Execution Time]{Fore.RESET} {func.__name__}: {end_time:,.1f}s")
        return output
    return wrapper
