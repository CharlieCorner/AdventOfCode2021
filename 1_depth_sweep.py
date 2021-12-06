def part_1():
    total_increments = 0

    with open("1_input_case.txt") as fp:
        prev_val = None
        
        for line in fp.readlines():

            curr_val = int(line)
            
            if not prev_val:
                prev_val = curr_val
                continue

            if curr_val > prev_val:
                total_increments += 1
            
            prev_val = curr_val
    
    print(f"Total increments: {total_increments}")

def part_2():
    total_increments = 0
    lines = []

    with open("1_input_case.txt") as fp:
        lines = fp.readlines()
    
    prev_val = None
        
    for line_idx in range(0, len(lines) - 2):

        curr_val = int(lines[line_idx]) + int(lines[line_idx + 1]) + int(lines[line_idx + 2])
        
        if not prev_val:
            prev_val = curr_val
            #print(f"{curr_val} N/A - no previous sum")
            continue

        if curr_val > prev_val:
            total_increments += 1
            #print(f"{curr_val} increased")
        elif curr_val == prev_val:
            pass
            #print(f"{curr_val} no change")
        else:
            pass
            #print(f"{curr_val} decreased")
        
        prev_val = curr_val
    
    print(f"Total increments: {total_increments}")
    

if __name__ == "__main__":
    part_2()
