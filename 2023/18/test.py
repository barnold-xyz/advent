def get_polygon_vertices(edges):
    # Start at the origin
    x, y = 0, 0
    vertices = [(x, y)]  # Initial vertex
    
    for edge in edges:
        direction, length = edge  # direction is 'U', 'D', 'L', or 'R', length is number of units
        
        if direction == 'U':  # Move up
            for i in range(1, length + 1):
                vertices.append((x, y + i))
            y += length
        elif direction == 'D':  # Move down
            for i in range(1, length + 1):
                vertices.append((x, y - i))
            y -= length
        elif direction == 'L':  # Move left
            for i in range(1, length + 1):
                vertices.append((x - i, y))
            x -= length
        elif direction == 'R':  # Move right
            for i in range(1, length + 1):
                vertices.append((x + i, y))
            x += length
    
    return vertices

# Toy Example: Move up 3 units, then move right, down, and left.
edges = [('U', 3), ('R', 1), ('D', 3), ('L', 1)]
vertices = get_polygon_vertices(edges)
print(vertices)
