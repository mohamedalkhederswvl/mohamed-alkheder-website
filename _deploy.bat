pushd "C:\Users\malkh\.copaw\workspaces\default\mohamed-alkheder-website"
del /q /f deploy_pages.py 2>nul
git checkout gh-pages
REM Remove old files
del /q /f index.html 2>nul
del /q /f posts.json 2>nul
del /q /f profile.jpg 2>nul
del /q /f style.css 2>nul
REM Get fresh files from main
git checkout main -- index.html posts.json profile.jpg style.css
git add -A
git commit -m "Sync: dynamic posts with tabs"
git push origin gh-pages
git checkout main
echo DONE
