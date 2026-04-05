import os, subprocess

folder = r"C:\Users\malkh\.copaw\workspaces\default\mohamed-alkheder-website"
os.chdir(folder)

# Remove check.py if it exists
check = os.path.join(folder, "check.py")
if os.path.exists(check):
    os.remove(check)

# Stage and commit
print("--- git status ---")
subprocess.run(["git", "add", "-A"], check=True)
print("--- git commit ---")
subprocess.run([
    "git", "commit", "-m",
    "✨ Dynamic posts with tabs + Auto-sync workflow\n\n"
    "- index.html: fetches posts.json dynamically with 3 tabs\n"
    "- scripts/fetch_linkedin_posts.py: Apify scraper (token via GH Secret)\n"
    "- .github/workflows/linkedin-posts.yml: every 4 hours auto-sync\n"
    "- posts.json: latest data\n"
    "- Tab system: Latest / Top Engagement / Featured Comments"
], capture_output=True, text=True)

# Push to main
print("--- git push main ---")
subprocess.run(["git", "push", "origin", "main"], check=True, capture_output=True, text=True)
print("Pushed main!")

# Copy to gh-pages and push
print("--- Update gh-pages branch ---")
subprocess.run(["git", "checkout", "gh-pages"], capture_output=True, check=True, text=True)
# Remove everything from gh-pages, copy from main
import shutil
for item in os.listdir(folder):
    if item in ['.git', '.github', 'scripts']:
        continue
    p = os.path.join(folder, item)
    if os.path.isfile(p):
        os.remove(p)
    elif os.path.isdir(p):
        shutil.rmtree(p)

# Copy everything from main's working tree
subprocess.run(["git", "checkout", "main", "--", "."], capture_output=True, check=True, text=True)
subprocess.run(["git", "add", "-A"], capture_output=True, check=True, text=True)
subprocess.run(["git", "commit", "-m", "🔄 Sync: update site with dynamic posts and new JS"], capture_output=True, text=True)
print("--- git push gh-pages ---")
subprocess.run(["git", "push", "origin", "gh-pages"], capture_output=True, check=True, text=True)
print("Pushed gh-pages!")

# Switch back to main
subprocess.run(["git", "checkout", "main"], capture_output=True, check=True, text=True)
print("\n✅ DONE! Branches updated: main + gh-pages")
