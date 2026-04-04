#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
محمد الخضر — LinkedIn Posts Auto-Sync
يسحب آخر منشوراتك من LinkedIn ويحدث posts.json تلقائياً

⚙️ يعمل داخل GitHub Actions — الـ API Token يُدرَج كـ Secret

⚠️ تحذير أمني: لا ترفع هذا الملف علنًا بدون حذف الـ Token!
   استخدم GitHub Secrets بدلاً من ذلك.
"""
import os, sys, json, hashlib
from datetime import datetime, timezone

try:
    import urllib.request
    import urllib.error
except ImportError:
    print("❌ urllib غير متوفر")
    sys.exit(1)

# ===== CONFIG =====
# في GitHub Actions: هذا المتغير يُدرَج من الـ Secrets
APIFY_TOKEN = os.environ.get("APIFY_TOKEN", "")
LINKEDIN_USERNAME = "mohamedalkhederb2bsales"
MAX_POSTS = 20
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "posts.json")

# قائمة بـ Actors المجانيين على Apify التي تسحب منشورات LinkedIn
# نجرّبهم بالترتيب — أول واحد ينجح نستخدمه
SCRAPER_OPTIONS = [
    {
        "actor": "apify/linkedin-profile-scraper",
        "payload": {"usernames": ["mohamedalkhederb2bsales"], "maxPosts": MAX_POSTS}
    },
    {
        "actor": "drobnikj/linkedin-post-scraper",
        "payload": {"searchUrl": "https://www.linkedin.com/in/mohamedalkhederb2bsales/recent-activity/all/", "maxItems": MAX_POSTS}
    },
]

def fetch_with_retry(url, payload, token, retries=2):
    """استدعاء Apify مع إعادة المحاولة."""
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "replace")[:200]
            print(f"⚠️ المحاولة {attempt+1} — HTTP {e.code}: {msg}")
            if e.code == 401:
                print("❌ الـ Token غير صحيح!")
                return None
        except urllib.error.URLError as e:
            print(f"⚠️ المحاولة {attempt+1} — URLError: {e}")
        except Exception as e:
            print(f"⚠️ المحاولة {attempt+1} — خطأ: {e}")
    return None

def extract_dataset(actor_response):
    """استخراج بيانات المنشورات من ردّ Apify."""
    if not actor_response or not isinstance(actor_response, dict):
        return None
    # Apify يرجع run info — نتحقق من حالة التشغيل
    dataset_id = actor_response.get("defaultDatasetId", "")
    run_id = actor_response.get("id", "")
    status = actor_response.get("status", "")
    
    if status == "SUCCEEDED" and dataset_id:
        # نجيب البيانات الفعلية من الـ Dataset
        url = "https://api.apify.com/v2/datasets/{}/items?token={}".format(dataset_id, APIFY_TOKEN)
        req = urllib.request.Request(url)
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read())
        except Exception as e:
            print(f"❌ فشل في قراءة الـ Dataset: {e}")
    
    return None

def transform_post(raw):
    """تحويل بيانات المنشور من Apify إلى صيغة العرض."""
    text = (raw.get("text", "") or "").strip()
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    text = "\n".join(lines)
    
    media = raw.get("postImageUrl") or raw.get("postMediaUrl") or ""
    posted = raw.get("postedOn", "")
    reactions = int(raw.get("numOfReactions", 0) or 0)
    comments = int(raw.get("numOfComments", 0) or 0)
    reposts = int(raw.get("numOfReshares", 0) or 0)
    engagement = reactions + comments * 2 + reposts * 3
    
    return {
        "id": hashlib.md5(text[:100].encode()).hexdigest()[:8],
        "text": text,
        "summary": text[:200] + ("..." if len(text) > 200 else ""),
        "reactions": reactions,
        "comments": comments,
        "reposts": reposts,
        "engagement_score": engagement,
        "date": posted,
        "media": media,
        "url": raw.get("postUrl", "https://www.linkedin.com/in/{}/".format(LINKEDIN_USERNAME)),
        "platform": "LinkedIn"
    }

def main():
    if not APIFY_TOKEN:
        print("⚠️ لا يوجد APIFY_TOKEN — يتم تخطي السحب")
        print("   لإضافة المنشورات تلقائياً: أضف APIFY_TOKEN كـ GitHub Secret")
        return

    print("🔍 جاري سحب المنشورات من LinkedIn...")
    all_data = []
    
    for i, scraper in enumerate(SCRAPER_OPTIONS):
        actor_id = scraper["actor"]
        print(f"  تجربة: {actor_id} ({i+1}/{len(SCRAPER_OPTIONS)})")
        
        actor_url = "https://api.apify.com/v2/acts/{}/run-sync?token={}".format(actor_id, APIFY_TOKEN)
        run_response = fetch_with_retry(actor_url, scraper["payload"], APIFY_TOKEN)
        
        if run_response:
            data = extract_dataset(run_response)
            if data and isinstance(data, list) and len(data) > 0:
                all_data = data
                print(f"✅ نجح: {actor_id}")
                break
            elif run_response and isinstance(run_response, list) and len(run_response) > 0:
                all_data = run_response
                print(f"✅ نجح (بيانات مباشرة): {actor_id}")
                break
    
    if not all_data:
        print("❨ لم يتم استخراج أي بيانات — تحقق من أن لديك صلاحيات على actor مجاني ⚠️")
        return
    
    posts = [transform_post(r) for r in all_data if (r.get("text", "") or "").strip()]
    posts.sort(key=lambda p: p.get("date", ""), reverse=True)
    
    # إزالة المكررات
    ids_seen, unique_posts = set(), []
    for p in posts:
        if p["id"] not in ids_seen:
            ids_seen.add(p["id"])
            unique_posts.append(p)
    
    result = {
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "total_posts": len(unique_posts),
        "source": "LinkedIn (Auto-Synced)",
        "posts": unique_posts
    }
    
    # حفظ المنشورات اليدوية اللي مو في الـ feed
    manual_posts = []
    try:
        with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
            existing = json.load(f)
        synced_ids = {p["id"] for p in unique_posts}
        for p in existing.get("posts", []):
            if p.get("id") not in synced_ids and p.get("source") == "manual":
                manual_posts.append(p)
    except FileNotFoundError:
        pass
    
    result["posts"].extend(manual_posts)
    
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print("✅ تم حفظ {} منشور | {}".format(len(unique_posts), result["last_updated"]))
    if unique_posts:
        print("📌 آخر منشور: {}...".format(unique_posts[0]["summary"][:60]))

if __name__ == "__main__":
    main()
