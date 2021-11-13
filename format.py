import json

ans = []

with open("outputs/part_3_output.json", 'r') as f:
    ans = json.load(f)

print(ans['objective'])