data = open("2023/15/input.txt").read().strip().split(',')

boxes = {}

def hash(str):
    h = 0
    for c in str: 
        h += ord(c) 
        h *= 17
        h = h % 256
    return h

print(hash('HASH'))
print(sum([hash(d) for d in data]))

def run_inst(str):
    label, op, focal_len = str.partition('=') if '=' in str else str.partition('-')
    box_add(label, focal_len) if op == '=' else box_remove(label)

def box_remove(label):
    h = hash(label)
    if h in boxes:
        boxes[h] = [(l, f) for l, f in boxes[h] if l != label]
        if not boxes[h]:  # Remove the key if the list is empty
            del boxes[h]

def box_add(label, focal_len):
    h = hash(label)
    if h in boxes:
        if any(l == label for l, f in boxes[h]):
            # Replace with new focal length if label exists
            boxes[h] = [(l, focal_len) if l == label else (l, f) for l, f in boxes[h]]
        else:
            boxes[h].append((label, focal_len))
    else:
        boxes[h] = [(label, focal_len)]

def box_print():
    for box_num, pairs in sorted(boxes.items()):
        print(f'{box_num}: {pairs}')

def box_score():
    return sum((int(box_num) + 1) * (slot + 1) * int(focal_len) 
               for box_num, pairs in boxes.items() 
               for slot, (label, focal_len) in enumerate(pairs))

def debug_inst(str):
    print(str)
    run_inst(str)
    box_print()

[run_inst(d) for d in data]
box_print()
print(box_score())