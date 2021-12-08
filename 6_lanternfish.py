from concurrent.futures import ThreadPoolExecutor as Executor
from time import sleep

from advent_utils import read_input_file

def part_1():
    lanternfishes = parse_input(read_input_file("6_input.txt"))
    days = 256
    lanternfishes = pass_days_improved(lanternfishes, days)
    print(f"There would be {lanternfishes} lanternfishes after {days} days")

def part_2():
    lanternfishes = parse_input(read_input_file("6_input.txt"))
    days = 256
    lanternfishes = pass_days_mapreduce(lanternfishes, days, 1, False)
    print(f"There would be {lanternfishes} lanternfishes after {days} days")

def pass_days(lanternfishes: list, days: int, is_debug: bool = False) -> list:
    print(f"Initial state: {lanternfishes}")
    
    for day in range(days):
        num_new_fishes = 0

        for idx, fish in enumerate(lanternfishes):
            if fish == 0:
                lanternfishes[idx] = 6
                num_new_fishes += 1
            else:
                lanternfishes[idx] = fish - 1
        
        # Create new fishes
        for new_fish in range(num_new_fishes):
            lanternfishes.append(8)
        
        
        print(f"Day {day + 1} {':' + str(lanternfishes) if is_debug else ''}")
    
    return lanternfishes

def pass_days_improved(lanternfishes: list, days: int, is_debug: bool = False) -> list:
    print(f"Initial state: {lanternfishes}")
    
    fish_counter = {
        8: 0,
        7: 0,
        6: 0,
        5: 0,
        4: 0,
        3: 0,
        2: 0,
        1: 0,
        0: 0,
    }

    # Let's accelerate lookup by keeping count in a map
    for fish in lanternfishes:
        fish_counter[fish] += 1

    for day in range(days):

        new_fish_counter = {
            8: 0,
            7: 0,
            6: 0,
            5: 0,
            4: 0,
            3: 0,
            2: 0,
            1: 0,
            0: 0,
        }

        for timer in range(9):
            fish_count = fish_counter[timer]

            if timer == 0:
                new_fish_counter[8] += fish_count # Create new fishes
                new_fish_counter[6] += fish_count # Adults start again
                continue

            # Move the fish count to one timer level lower
            new_fish_counter[timer - 1] += fish_count
        
        # Prepare for a new day
        fish_counter = new_fish_counter
        
        print(f"Day {day + 1}")
    
    return sum(fish_counter.values())

def pass_days_mapreduce(lanternfishes: list,
                        days: int,
                        threads: int = 2,
                        is_debug: bool = False) -> list:
    print(f"Initial state: {lanternfishes}")
    result = []

    # Set up the futures and executor
    with Executor(max_workers=threads) as executor:
        futures = []
        split_data = split_list(lanternfishes, threads)

        for split_id, datum in enumerate(split_data):
            futures.append(executor.submit(lanternfish_mapper, datum, days, split_id))
        
        workers_not_done = 1

        while workers_not_done > 0:
            workers_not_done = 0

            for f in futures:
                workers_not_done += 1 if not f.done() else 0

            if is_debug:
                print(f"Waiting for {workers_not_done} workers..." if workers_not_done else "Done!")
        

        result = sum([fut.result() for fut in futures])
        
        return result

def lanternfish_mapper(fishes: list, days: int, worker_id: int = None) -> int:
    fish_counter = {
        8: 0,
        7: 0,
        6: 0,
        5: 0,
        4: 0,
        3: 0,
        2: 0,
        1: 0,
        0: 0,
    }

    # Let's accelerate lookup by keeping count in a map
    for fish in fishes:
        fish_counter[fish] += 1

    for day in range(days):

        new_fish_counter = {
            8: 0,
            7: 0,
            6: 0,
            5: 0,
            4: 0,
            3: 0,
            2: 0,
            1: 0,
            0: 0,
        }

        for timer in range(9):
            fish_count = fish_counter[timer]

            if timer == 0:
                new_fish_counter[8] += fish_count # Create new fishes
                new_fish_counter[6] += fish_count # Adults start again
                continue

            # Move the fish count to one timer level lower
            new_fish_counter[timer - 1] += fish_count
        
        # Prepare for a new day
        fish_counter = new_fish_counter
        
        print(f"Worker {worker_id} - Day {day + 1}")
    
    return sum(fish_counter.values())

def split_list(fishes: list, num_splits: int) -> list:
    step_size = len(fishes) // num_splits
    result = []
    
    for split_idx in range(0, len(fishes), step_size):
        result.append(fishes[split_idx: split_idx + step_size])
    
    return result


def parse_input(lines: list) -> list:
    result = []
    for l in lines:
        result.extend([int(num) for num in l.split(",") if num.isdigit()])
    return result

if __name__ == "__main__":
    part_2()
