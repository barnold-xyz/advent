from anytree import Node, RenderTree

data = [line.strip().split('\n') for line in open('2022/07/input.txt').read().split('$ ') if line]

def print_tree(root):
    for pre, _, node in RenderTree(root):
        print(f"{pre}{node.name} (value={node.data['size']})")

root = Node('/', data={'size': 0})
curNode = root
for cmd, *results in data:
    if cmd == 'ls':
        [Node(name, parent=curNode, data={'size': 0 if size == 'dir' else int(size)}) 
         for size, name in (r.split(' ') for r in results)]
    else:
        _, dest = cmd.split(' ')
        if dest == '..':
            curNode = curNode.parent
        elif dest == '/':
            curNode = root
        else:
            curNode = next(c for c in curNode.children if c.name == dest)

def get_size(node):
    return node.data['size'] + sum(get_size(child) for child in node.children)
    
print('part 1:', sum(get_size(node) for node in root.descendants if node.data['size'] == 0 and get_size(node) <= 100000))

total_space = 70000000
space_needed = 30000000
space_used = get_size(root)
min_to_delete = space_used - total_space + space_needed
print('part 2:', min(get_size(node) for node in root.descendants if node.data['size'] == 0 and get_size(node) >= min_to_delete))

quit()
