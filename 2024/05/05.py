[rule_list, pages_list] = [x.split('\n') for x in open("2024/05/input.txt").read().split('\n\n')]
rule_list = [x.split('|') for x in rule_list]
pages_list = [x.split(',') for x in pages_list]

# rules will be a dict from the page to the list of pages that must come after it if they are present
rules = {}
for first, second in rule_list:
    if first not in rules:
        rules[first] = []
    rules[first].append(second)

# naiive rule check
def check_order(pages):
    # throw an error if there are duplicate pages
    if len(pages) != len(set(pages)):
        print(f'Duplicate pages: {pages}')
    for page in pages:
        if rules.get(page) is not None:
            for second in rules[page]:
                if second in pages:
                    if pages.index(page) > pages.index(second):
                        return False
    return True

def middle_page(pages):
    return int(pages[len(pages) // 2])

def part1():
    pages_in_order = [check_order(pages) for pages in pages_list] 
    return sum(middle_page(pages) for pages, in_order in zip(pages_list, pages_in_order) if in_order)

print(part1())