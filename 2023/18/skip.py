#https://topaz.github.io/paste/#XQAAAQCWAQAAAAAAAAA4GwhH7u5OdXNRlPeIKYn01V1xhpyceJIwtT5HvB9jA7zH7F67Rry3WbFjXXlg+rj3O3Pcr0jV1/vTXP/7jdZNkrMTQPkbSnuvlXFjzrTfvX3Ir+VxA2REBE39YUc3u64mdAog36DTi6Cd3mk6MAP8HSDqMVD0qJWDIkT/T1frVVjq6Vwl5B9bhr/EfMYhQ76SVYOJ6B7nLXSvqLGiHL5rPpGvcRdh0YoH1xiJatTkING88zdpuFObWwPvuD4cTrcfh/S8kGfa8HfqLQ2orimQG0QsuKI0HONFCDJETbWr//xp3YC3FDnfyWQt6ckdQnNJ6Oha4P/4frRL
plan = list(map(str.split, open('2023/18/input.txt')))

dirs = {'R': (1,0), 'D': (0,1), 'L': (-1,0), 'U': (0,-1),
        '0': (1,0), '1': (0,1), '2': (-1,0), '3': (0,-1)}

def f(steps, pos=0, ans=1):
    for (x,y), n in steps:
        pos += x*n
        ans += y*n * pos + n/2

    return int(ans)

print(f((dirs[d],    int(s))          for d,s,_ in plan),
      f((dirs[c[7]], int(c[2:7], 16)) for _,_,c in plan))