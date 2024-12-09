input = open('2024/09/input.txt').read().strip() + '0'

def disk_map_to_disk(disk_map):
    is_file = True
    disk = []
    id = 0
    for char in disk_map:
        new_file = chr(id) if is_file else '􏿿'
        id = id + 1 if is_file else id
        for i in range(int(char)):
            disk.append(new_file)
        is_file = not is_file
    return disk

# disk_hash is a dictionary with keys as file_id and values are (start, end) tuples
def disk_map_to_disk_hash(disk_map):
    is_file = True
    disk = {}
    id = 0
    loc = 0
    for char in disk_map:
        end = loc + int(char) - 1
        if is_file:
            disk[id] = (loc, end)
            id = id + 1
        else:
            disk[-id] = (loc, end)
        loc = end + 1
        is_file = not is_file
    return disk

# first return is a list of files and second return is a list of dots
def disk_map_to_lists(disk_map):
    files = []
    dots = []
    id = 0
    for file_len, dot_len in zip(disk_map[::2], disk_map[1::2]):
        files.append(str(id) * int(file_len))
        #dots.append('􏿿' * int(dot_len))
        dots.append(int(dot_len))
        id += 1
    return files, dots

# naive implementation
def compress(disk):
    # start at the end of the disk
    for i in range(len(disk) - 1, 0, -1):
        file_id = disk[i]
        #print(f'file_id: {file_id}')
        new_index = disk.index('􏿿')
        if new_index >= i: 
            break
        disk[i] = '􏿿'
        disk[new_index] = file_id
        #print(''.join(disk))
    return disk

# naive again :(
def pt2(disk):
    # start at the end of the disk
    i = len(disk) - 1
    while i > 0:
        if disk[i] == '􏿿':
            i -= 1
            continue
        file_id = disk[i]
        file_len = 1
        while disk[i-file_len] == file_id:
            file_len += 1
        
        #print(f'file_id: {file_id}, file_len: {file_len}, index: {i}')

        # find an open place starting at the beginning
        open_size = 0
        j = 0
        while j <= i:
            if disk[j] == '􏿿':
                open_size += 1
            else:
                open_size = 0
            if open_size == file_len:
                # found a spot
                start_idx = j - file_len + 1
                #print(start_idx)
                #print(f'start_idx: {start_idx}, i: {i}, file_len: {file_len}')
                disk[start_idx:start_idx+file_len] = [file_id] * file_len
                disk[i+1-file_len:i+1] = ['􏿿'] * file_len
                #for k in range(file_len-1):
                #    disk[start_idx+k] = file_id
                #    disk[i+k] = '􏿿'
                #print(''.join(disk))

                break
            j += 1
            #print(f'j: {j}, i: {i}')
        i -= file_len
    return disk


def move(lst, old_index, new_index):
    lst.insert(new_index, lst.pop(old_index))

def compress_pt2(files, dots):
    # start at the end of the disk
    new_files = files.copy()
    new_dots = dots.copy()
    #print(''.join([x+''.join(['􏿿']*y) for x,y in zip(new_files, new_dots)]))
    while files:
        file = files.pop()
        # find the first dot that is >= the length of the file
        valid_indices = [dots.index(i) for i in range(len(file), 9) if i in dots]
        if valid_indices:
            dot_index = min(valid_indices)
            file_index = new_files.index(file)
            #print(f'file: {file}, dot_index: {dot_index}, file_index: {file_index}')
            move(new_files, new_files.index(file), dot_index+1)
            #move(new_dots, dot_index, len(new_dots))
            new_dots[dot_index] -= len(file)
            new_dots[file_index] += len(file)
        #print(''.join([x+''.join(['􏿿']*y) for x,y in zip(new_files, new_dots)]))
    #print(file)


def checksum(disk):
    #return sum(i * int(disk[i]) for i in range(disk.index('􏿿')))
    #disk = (''.join(disk)).replace('􏿿', '0')
    #return sum(i * int(disk[i]) for i in range(len(disk)))
    return sum(i * ord(disk[i]) for i in range(len(disk)) if disk[i] != '􏿿')



#files, dots = disk_map_to_lists(input)
#print(f'files: {files}')
#print(f'dots: {dots}')
#print(''.join([x+''.join(['􏿿']*y) for x,y in zip(files, dots)]))

#compress_pt2(files, dots)
#quit()


#print(ord('􏿿')); quit()
disk = disk_map_to_disk(input)
#print(''.join(disk))
pt2(disk)
#print(''.join(disk))
print(checksum(disk))
quit()

#print(disk)
#print(''.join(disk))    
print(checksum(compress(disk.copy())))
#print(''.join(disk))
print(checksum(disk))

disk_hash = disk_map_to_disk_hash(input)
print(disk_hash)
print(compress_pt2(disk_hash.copy()))