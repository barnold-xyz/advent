from functools import cmp_to_key

[rule_list, pages_list] = [x.split('\n') for x in open("2024/05/input.txt").read().split('\n\n')]
rule_list = [x.split('|') for x in rule_list]
pages_list = [x.split(',') for x in pages_list]

# rules will be a dict from the page to the list of pages that must come after it if they are present
rules = {first: [] for first, _ in rule_list}
[rules[first].append(second) for first, second in rule_list]

# naiive rule check
def check_order(pages):
    return all(not (second in pages and pages.index(page) > pages.index(second)) 
               for page in set(pages).intersection(rules.keys()) 
               for second in rules[page])

def middle_page(pages):
    return int(pages[len(pages) // 2])

def compare_pages(p1, p2):
    if p2 in rules.get(p1, []): return -1
    if p1 in rules.get(p2, []): return 1
    return 0
    
pages_in_order = [check_order(pages) for pages in pages_list]

print(sum(middle_page(pages) for pages, in_order in zip(pages_list, pages_in_order) if in_order))
print(sum(middle_page(sorted(pages, key=cmp_to_key(compare_pages))) for pages, in_order in zip(pages_list, pages_in_order) if not in_order))
