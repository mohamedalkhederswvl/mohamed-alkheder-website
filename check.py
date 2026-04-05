import json
with open("index.html","r",encoding="utf-8") as f:
    t = f.read()
print("Lines:", t.count("\n"))
print("Has fetch:", "fetch(" in t)
print("Has tabs:", "post-tab" in t)
print("Ends OK:", t.strip().endswith("</html>"))
