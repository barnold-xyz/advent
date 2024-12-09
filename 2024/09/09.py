input = open('2024/09/input.txt').read().strip() + '0'

EMPTY = '􏿿'

def disk_map_to_disk(disk_map):
    is_file = True
    disk = []
    id = 0
    for char in disk_map:
        new_file = chr(id) if is_file else EMPTY
        id = id + 1 if is_file else id
        for i in range(int(char)):
            disk.append(new_file)
        is_file = not is_file
    return disk

# naive implementation
def compress(disk):
    for i in range(len(disk) - 1, 0, -1):
        file_id = disk[i]
        new_index = disk.index(EMPTY)
        if new_index >= i: 
            break
        disk[i] = EMPTY
        disk[new_index] = file_id
    return disk

# naive again :(
def pt2(disk):
    i = len(disk) - 1
    while i > 0:
        if disk[i] == EMPTY:
            i -= 1
            continue
        file_id = disk[i]
        file_len = 1
        while disk[i-file_len] == file_id:
            file_len += 1
        
        # find an open place starting at the beginning
        open_size = 0
        j = 0
        while j <= i:
            if disk[j] == EMPTY:
                open_size += 1
            else:
                open_size = 0
            if open_size == file_len:
                # found a spot
                start_idx = j - file_len + 1
                disk[start_idx:start_idx+file_len] = [file_id] * file_len
                disk[i+1-file_len:i+1] = [EMPTY] * file_len
                break
            j += 1
        i -= file_len
    return disk

def checksum(disk):
    return sum(i * ord(disk[i]) for i in range(len(disk)) if disk[i] != EMPTY)

disk = disk_map_to_disk(input)
print(checksum(compress(disk.copy())))
print(checksum(pt2(disk.copy())))