input = open('2024/09/input.txt').read().strip()

def disk_map_to_disk(disk_map):
    is_file = True
    disk = []
    id = 0
    for char in disk_map:
        new_file = str(id) if is_file else '.'
        id = id + 1 if is_file else id
        for i in range(int(char)):
            disk.append(new_file)
        is_file = not is_file
    return disk

# naive implementation
def compress(disk):
    # start at the end of the disk
    for i in range(len(disk) - 1, 0, -1):
        file_id = disk[i]
        #print(f'file_id: {file_id}')
        new_index = disk.index('.')
        if new_index >= i: 
            break
        disk[i] = '.'
        disk[new_index] = file_id
        #print(''.join(disk))
    return disk

def checksum(disk):
    return sum(i * int(disk[i]) for i in range(disk.index('.')))

disk = disk_map_to_disk(input)
#print(disk)
#print(''.join(disk))    
compress(disk)
#print(''.join(disk))
print(checksum(disk))


