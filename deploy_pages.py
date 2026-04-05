import os, subprocess, shutil

folder = r"C:\Users\malkh\.copaw\workspaces\default\mohamed-alkheder-website"
os.chdir(folder)

# Clean up helper files
for f in ["check.py", "build_final.py", "push_all.py"]:
    p = os.path.join(folder, f)
    if os.path.exists(p): os.remove(p)

# Step 1: commit the cleanup
subprocess.run(["git", "add", "-A"], capture_output=True)
subprocess.run(["git", "commit", "-m", "Clean up helper files"], capture_output=True, text=True)
subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)

# Step 2: checkout gh-pages, copy main content, push
subprocess.run(["git", "checkout", "gh-pages"], capture_output=True)
# Remove old site files
for item in os.listdir(folder):
    if item in ['.git', '.github', 'scripts', 'memory']:
        continue
    p = os.path.join(folder, item)
    if os.path.isfile(p): os.remove(p)
    elif os.path.isdir(p): shutil.rmtree(p)

# Copy from main
subprocess.run(["git", "checkout", "main", "--", "index.html",
                "posts.json", "profile.jpg", "style.css"],
               capture_output=True)

subprocess.run(["git", "add", "-A"], capture_output=True)
subprocess.run(["git", "commit", "-m", "Sync: dynamic posts with tabs"], capture_output=True, text=True)
subprocess.run(["git", "push", "origin", "gh-pages"], capture_output=True, text=True)

# Back to main
subprocess.run(["git", "checkout", "main"], capture_output=True)
print("Done! Both main + gh-pages updated")
