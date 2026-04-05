# -*- coding: utf-8 -*-
"""
Complete rebuild — index.html with dynamic LinkedIn posts from JSON
"""
import json

html = r'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>محمد الخضر | خبير مبيعات B2B</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800;900&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
        :root {
            --primary: #0A1628;
            --accent: #C8A44E;
            --accent-light: #E8D48B;
            --glass: rgba(255,255,255,0.04);
            --glass-border: rgba(255,255,255,0.08);
            --text: #F0EDE6;
            --text-muted: #8A8A8A;
            --gradient-1: linear-gradient(135deg, #C8A44E, #E8D48B);
        }
        html { scroll-behavior: smooth; font-size: 16px; }
        body {
            font-family: 'Tajawal', sans-serif;
            background: var(--primary);
            color: var(--text);
            overflow-x: hidden;
            position: relative;
        }
        body::before {
            content: '';
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background:
                radial-gradient(ellipse at 20% 20%, rgba(200,164,78,0.08) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 80%, rgba(200,164,78,0.05) 0%, transparent 50%);
            pointer-events: none;
            z-index: 0;
        }

        /* ---- Navbar ---- */
        #navbar {
            position: fixed; top: 0; right: 0; left: 0;
            display: flex; align-items: center; justify-content: space-between;
            padding: 1.2rem 5%;
            z-index: 1000;
            transition: background 0.3s, box-shadow 0.3s;
        }
        #navbar.scrolled {
            background: rgba(10,22,40,0.95);
            backdrop-filter: blur(12px);
            box-shadow: 0 2px 20px rgba(0,0,0,0.3);
        }
        .nav-logo {
            font-size: 1.3rem; font-weight: 800;
            background: var(--gradient-1);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .nav-links { display: flex; gap: 2rem; list-style: none; align-items: center; }
        .nav-links a {
            color: var(--text-muted); text-decoration: none; font-size: 0.95rem;
            font-weight: 500; transition: color 0.3s; position: relative;
        }
        .nav-links a::after {
            content: ''; position: absolute; bottom: -4px; right: 0;
            width: 0; height: 2px; background: var(--accent); transition: width 0.3s ease;
        }
        .nav-links a:hover { color: var(--accent); }
        .nav-links a:hover::after { width: 100%; }
        .nav-cta {
            padding: 0.6rem 1.8rem; border-radius: 50px; background: var(--gradient-1); color: var(--primary);
            font-weight: 700; font-size: 0.9rem; border: none; cursor: pointer; transition: transform 0.3s, box-shadow 0.3s;
        }
        .nav-cta:hover { transform: translateY(-2px); box-shadow: 0 8px 30px rgba(200,164,78,0.3); }
        .menu-toggle { display: none; flex-direction: column; gap: 5px; cursor: pointer; z-index: 1001; }
        .menu-toggle span { width: 28px; height: 2px; background: var(--text); transition: 0.3s; }

        /* ---- Hero ---- */
        .hero {
            min-height: 100vh; display: flex; align-items: center; justify-content: center;
            text-align: center; padding: 8rem 5% 4rem; position: relative;
        }
        .hero-badge {
            display: inline-flex; align-items: center; padding: 0.7rem 1.5rem;
            border-radius: 50px; background: var(--glass); border: 1px solid var(--glass-border);
            margin-bottom: 2rem; font-size: 0.9rem; color: var(--accent);
            backdrop-filter: blur(10px); font-weight: 500;
        }
        .badge-dot {
            width: 8px; height: 8px; border-radius: 50%; background: var(--accent);
            margin-left: 8px; animation: pulse 2s infinite;
        }
        @keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:0.3; } }
        .hero h1 {
            font-size: clamp(2.5rem, 6vw, 4.2rem); font-weight: 900;
            line-height: 1.2; margin-bottom: 1rem;
        }
        .hero h1 .accent { background: var(--gradient-1); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .hero-subtitle {
            font-size: clamp(1rem, 2.5vw, 1.3rem); color: var(--text-muted);
            max-width: 680px; margin: 0 auto 3rem;
        }
        .hero-btns { display: flex; gap: 1.2rem; justify-content: center; flex-wrap: wrap; }
        .btn-primary {
            padding: 1rem 2.5rem; border-radius: 50px; background: var(--gradient-1);
            color: var(--primary); font-weight: 700; font-size: 1rem;
            text-decoration: none; transition: transform 0.3s, box-shadow 0.3s; display: inline-block;
        }
        .btn-primary:hover { transform: translateY(-3px); box-shadow: 0 12px 40px rgba(200,164,78,0.35); }
        .btn-outline {
            padding: 1rem 2.5rem; border-radius: 50px; border: 2px solid var(--accent);
            color: var(--accent); font-weight: 700; font-size: 1rem; text-decoration: none;
            transition: all 0.3s; display: inline-block; background: transparent;
        }
        .btn-outline:hover { background: var(--accent); color: var(--primary); }

        /* ---- Stats ---- */
        .stats-section { padding: 2rem 5% 6rem; }
        .stats-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem; max-width: 1200px; margin: 0 auto;
        }
        .stat-card {
            text-align: center; padding: 2rem 1rem;
            background: var(--glass); border: 1px solid var(--glass-border);
            border-radius: 20px; transition: transform 0.3s;
        }
        .stat-card:hover { transform: translateY(-5px); }
        .stat-number {
            font-size: 2.8rem; font-weight: 900;
            background: var(--gradient-1); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .stat-label { color: var(--text-muted); margin-top: 0.5rem; font-size: 0.95rem; }

        /* ---- About ---- */
        #about, #services, #philosophy, #posts, #cta, #footer { position: relative; z-index: 1; }
        .section-title {
            text-align: center; margin-bottom: 4rem;
        }
        .section-title h2 {
            font-size: clamp(2rem, 4vw, 3rem); font-weight: 900;
        }
        .section-title h2 .accent {
            background: var(--gradient-1); -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .section-title p { color: var(--text-muted); margin-top: 1rem; font-size: 1.1rem; }

        .about-content {
            max-width: 1000px; margin: 0 auto; padding: 0 5% 6rem;
            display: grid; grid-template-columns: 1fr 1.5fr; gap: 4rem;
            align-items: center;
        }
        .about-img img {
            width: 100%; aspect-ratio: 3/4; object-fit: cover;
            border-radius: 20px; border: 3px solid var(--glass-border);
        }
        .about-text p { line-height: 1.8; margin-bottom: 1.5rem; color: var(--text-muted); font-size: 1.05rem; }
        .about-text .highlight {
            color: var(--accent); font-weight: 700;
        }

        /* ---- Services ---- */
        .services-section { padding: 6rem 5%; }
        .services-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem; max-width: 1200px; margin: 0 auto;
        }
        .service-card {
            padding: 2rem; background: var(--glass); border: 1px solid var(--glass-border);
            border-radius: 20px; transition: transform 0.3s;
        }
        .service-card:hover { transform: translateY(-5px); }
        .service-icon { font-size: 2.5rem; margin-bottom: 1rem; }
        .service-card h3 { font-size: 1.3rem; margin-bottom: 0.5rem; }
        .service-card p { color: var(--text-muted); line-height: 1.6; }

        /* ---- Philosophy ---- */
        .philosophy-section {
            padding: 6rem 5%;
            background: linear-gradient(180deg, transparent 0%, rgba(200,164,78,0.03) 50%, transparent 100%);
        }
        .philosophy-content {
            max-width: 800px; margin: 0 auto; text-align: center;
        }
        .philosophy-quote {
            font-size: clamp(1.2rem, 3vw, 1.8rem);
            color: var(--text-muted); font-weight: 500;
            margin-bottom: 3rem; padding: 2rem; border-right: 4px solid var(--accent);
            line-height: 1.8;
        }
        .philosophy-rules {
            display: flex; gap: 2rem; justify-content: center; flex-wrap: wrap;
        }
        .philosophy-rule {
            padding: 1.5rem 2rem; background: var(--glass); border: 1px solid var(--glass-border);
            border-radius: 15px; font-weight: 700;
        }
        .philosophy-rule .num {
            color: var(--accent); font-size: 1.5rem; margin-bottom: 0.5rem;
        }

        /* ---- Testimonials ---- */
        .testimonials-section { padding: 6rem 5%; }
        .testimonials-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem; max-width: 1200px; margin: 0 auto;
        }
        .testimonial-card {
            padding: 2rem; background: var(--glass); border: 1px solid var(--glass-border);
            border-radius: 20px; position: relative;
        }
        .testimonial-card .stars { color: var(--accent); margin-bottom: 1rem; }
        .testimonial-card p { color: var(--text-muted); line-height: 1.6; margin-bottom: 1rem; }
        .testimonial-card .author { font-weight: 700; }
        .testimonial-card .role { color: var(--text-muted); font-size: 0.85rem; }

        /* ---- Posts (LinkedIn-style feed) ---- */
        .posts-section { padding: 6rem 5%; }
        .posts-tabs { display: flex; gap: 1rem; justify-content: center; margin-bottom: 3rem; flex-wrap: wrap; }
        .post-tab {
            padding: 0.7rem 1.8rem; border-radius: 50px; background: var(--glass);
            border: 1px solid var(--glass-border); cursor: pointer;
            color: var(--text-muted); font-weight: 600; transition: all 0.3s; font-size: 0.95rem;
        }
        .post-tab.active, .post-tab:hover { background: var(--accent); color: var(--primary); border-color: var(--accent); }
        .tabs-content { position: relative; }
        .tab-panel { display: none; }
        .tab-panel.active { display: block; }

        /* LinkedIn-style feed card */
        .linkedin-feed {
            max-width: 680px; margin: 0 auto; display: flex; flex-direction: column; gap: 1.5rem;
        }
        .feed-card {
            background: var(--glass); border: 1px solid var(--glass-border);
            border-radius: 16px; overflow: hidden; transition: transform 0.3s;
        }
        .feed-card:hover { transform: translateY(-3px); }
        .feed-header {
            display: flex; align-items: center; gap: 0.8rem; padding: 1.2rem 1.5rem 0;
        }
        .feed-avatar {
            width: 48px; height: 48px; border-radius: 50%; overflow: hidden; flex-shrink: 0;
        }
        .feed-avatar img { width: 100%; height: 100%; object-fit: cover; }
        .feed-author-info { flex: 1; }
        .feed-author-name { font-weight: 700; font-size: 1rem; }
        .feed-author-title { color: var(--text-muted); font-size: 0.8rem; }
        .feed-time { color: var(--text-muted); font-size: 0.8rem; }
        .feed-body { padding: 1rem 1.5rem; }
        .feed-text { line-height: 1.8; color: var(--text); font-size: 1rem; margin-bottom: 1rem; }
        .feed-image {
            width: 100%; border-radius: 12px; margin-bottom: 1rem;
        }
        .feed-stats {
            display: flex; gap: 1.5rem; padding: 0.8rem 1.5rem;
            border-top: 1px solid var(--glass-border);
        }
        .feed-stat { color: var(--text-muted); font-size: 0.85rem; }
        .feed-stat .num { color: var(--accent); font-weight: 700; }
        .feed-link {
            display: block; text-align: center; padding: 0.8rem;
            background: rgba(200,164,78,0.1); color: var(--accent);
            text-decoration: none; font-weight: 600; transition: background 0.3s;
        }
        .feed-link:hover { background: rgba(200,164,78,0.2); }

        /* loading state */
        .feed-loading { text-align: center; padding: 3rem; color: var(--text-muted); }
        .feed-loading .spinner {
            display: inline-block; width: 40px; height: 40px;
            border: 3px solid var(--glass-border); border-top-color: var(--accent);
            border-radius: 50%; animation: spin 0.8s linear infinite;
            margin-bottom: 1rem;
        }
        @keyframes spin { to { transform: rotate(360deg); } }

        /* ---- CTA ---- */
        .cta-section { padding: 6rem 5%; }
        .cta-box {
            max-width: 600px; margin: 0 auto; text-align: center; padding: 3rem 2rem;
            background: var(--glass); border: 1px solid var(--glass-border);
            border-radius: 30px;
        }
        .cta-box h2 { font-size: 2rem; margin-bottom: 1rem; }
        .cta-box p { color: var(--text-muted); margin-bottom: 2rem; }
        .cta-links {
            display: flex; gap: 1.5rem; justify-content: center; margin-top: 1.5rem; flex-wrap: wrap;
        }
        .cta-links a {
            color: var(--text-muted); text-decoration: none; display: flex;
            align-items: center; gap: 0.5rem; transition: color 0.3s;
        }
        .cta-links a:hover { color: var(--accent); }
        .cta-links svg { width: 20px; height: 20px; }

        /* ---- Footer ---- */
        .footer {
            text-align: center; padding: 3rem 5%; border-top: 1px solid var(--glass-border);
        }
        .footer-logo {
            font-size: 1.2rem; font-weight: 800;
            background: var(--gradient-1); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            text-decoration: none;
        }
        .footer-icons { display: flex; gap: 1.5rem; justify-content: center; margin: 1rem 0; }
        .footer-icons a { opacity: 0.5; transition: opacity 0.3s; }
        .footer-icons a:hover { opacity: 1; }
        .footer-icons svg { width: 22px; height: 22px; }
        .footer p { color: var(--text-muted); font-size: 0.85rem; }

        /* ---- Fade ---- */
        .fade-in { opacity: 0; transform: translateY(40px); transition: opacity 0.8s ease, transform 0.8s ease; }
        .fade-in.visible { opacity: 1; transform: translateY(0); }

        /* ---- Responsive ---- */
        @media (max-width: 768px) {
            .nav-links {
                position: fixed; top: 0; right: -100%; width: 75%; height: 100vh;
                background: rgba(10,22,40,0.98); flex-direction: column;
                justify-content: center; gap: 2rem; transition: right 0.4s; z-index: 999;
            }
            .nav-links.open { right: 0; }
            .menu-toggle { display: flex; }
            .hero h1 { font-size: 2.5rem; }
            .about-content { grid-template-columns: 1fr; text-align: center; gap: 2rem; }
            .about-img img { max-width: 280px; margin: 0 auto; }
            .stats-grid { grid-template-columns: repeat(2, 1fr); }
            .services-grid { grid-template-columns: 1fr; }
            .testimonials-grid { grid-template-columns: 1fr; }
            .philosophy-rules { flex-direction: column; align-items: center; }
        }
    </style>
</head>
<body>
    <!-- Navbar -->
    <nav id="navbar">
        <a href="#hero" class="nav-logo">محمد الخضر</a>
        <ul class="nav-links" id="navLinks">
            <li><a href="#about">من أنا</a></li>
            <li><a href="#services">الخدمات</a></li>
            <li><a href="#philosophy">فلسفتي</a></li>
            <li><a href="#posts">المنشورات</a></li>
            <li><a href="#cta">تواصل معي</a></li>
        </ul>
        <a href="https://wa.me/966592192220" target="_blank" class="nav-cta">واتساب</a>
        <div class="menu-toggle" id="menuToggle" onclick="toggleMenu()">
            <span></span><span></span><span></span>
        </div>
    </nav>

    <!-- Hero -->
    <section class="hero" id="hero">
        <div>
            <div class="hero-badge" style="margin-bottom:2rem;">
                <span class="badge-dot"></span> متاح للاستشارات
            </div>
            <h1>حوّل مبيعاتك من <span class="accent">عشوائية</span> إلى <span class="accent">منهجية</span></h1>
            <p class="hero-subtitle">المؤثر رقم واحد في مبيعات B2B على لينكدان في السعودية. بدأت من الصفر وبالعقل فقط. ساعدك تحوّل فريقك المبيعات من مجرد محاولات إلى نظام يحقق نتائج.</p>
            <div class="hero-btns">
                <a href="https://wa.me/966592192220" target="_blank" class="btn-primary">واتساب الان</a>
                <a href="#posts" class="btn-outline">شوف المحتوى</a>
            </div>
        </div>
    </section>

    <!-- Stats -->
    <section class="stats-section">
        <div class="stats-grid">
            <div class="stat-card fade-in">
                <div class="stat-number" data-target="30000">٠</div>
                <div class="stat-label">متابع على لينكدان</div>
            </div>
            <div class="stat-card fade-in">
                <div class="stat-number" data-target="7">٠</div>
                <div class="stat-label">أشهر #1 مبيعات</div>
            </div>
            <div class="stat-card fade-in">
                <div class="stat-number" data-target="6">٠</div>
                <div class="stat-label">خدمات استشارية</div>
            </div>
            <div class="stat-card fade-in">
                <div class="stat-number" data-target="150">٠</div>
                <div class="stat-label">+ عميل سعداء</div>
            </div>
            <div class="stat-card fade-in">
                <div class="stat-number" data-target="500">٠</div>
                <div class="stat-label">+ مشروع تم إنجازه</div>
            </div>
        </div>
    </section>

    <!-- About -->
    <section id="about">
        <div class="section-title">
            <h2>من <span class="accent">أنا</span></h2>
        </div>
        <div class="about-content">
            <div class="about-img fade-in">
                <img src="profile.jpg" alt="محمد الخضر">
            </div>
            <div class="about-text fade-in">
                <p>أنا <span class="highlight" id="about_name">محمد الخضر</span> — خبير مبيعات B2B ومؤثر رقم واحد في مبيعات لينكدان في السعودية.</p>
                <p>بدأت رحلتي من الصفر. ما كنت أملك لا شهادة كبيرة ولا واسطة. بس كنت أملك إصرار وعقل مفكر. دخلت عالم المبيعات وأنا ما أعرف الفرق بين B2B و B2C. والآن ساعدت أكثر من 150 شركة تطور مبيعاتها بشكل جذري.</p>
                <p>فلسفتي في المبيعات بسيطة: <span class="highlight">المبيعات فن قبل ما تكون علم</span> والمعرفة بدون تطبيق ما تسوى ريال. خليني أساعدك تحول محاولاتك لنظام يحقق نتائج قابلة للقياس والتكرار.</p>
            </div>
        </div>
    </section>

    <!-- Services -->
    <section id="services" class="services-section">
        <div class="section-title">
            <h2>الـ<span class="accent">خدمات</span></h2>
            <p>حلول مبيعات شاملة تناسب جميع الاحتياجات</p>
        </div>
        <div class="services-grid">
            <div class="service-card fade-in">
                <div class="service-icon">🎯</div>
                <h3>استراتيجية المبيعات</h3>
                <p>بناء خطة مبيعات متكاملة تتضمن الأهداف، القنوات، التوقيت، ومؤشرات الأداء الرئيسية لتحقيق النمو المستدام.</p>
            </div>
            <div class="service-card fade-in">
                <div class="service-icon">👥</div>
                <h3>تدريب فرق المبيعات</h3>
                <p>ورش عمل عملية لتحويل فريقك من بائعين عاديين إلى محترفين يملكون مهارات الإقناع والتفاوض المتقدمة.</p>
            </div>
            <div class="service-card fade-in">
                <div class="service-icon">📊</div>
                <h3>بناء أنظمة الـ Pipeline</h3>
                <p>تصميم وإدارة خطوط الأنابيب المبيعاتية التي تضمن تتبع كل فرصة من البداية حتى الإغلاق بشكل منظم.</p>
            </div>
            <div class="service-card fade-in">
                <div class="service-icon">🔗</div>
                <h3>LinkedIn Personal Brand</h3>
                <p>بناء Presence احترافي على LinkedIn يجذب العملاء B2B بشكل عضوي من خلال استراتيجية محتوى متخصصة.</p>
            </div>
            <div class="service-card fade-in">
                <div class="service-icon">📈</div>
                <h3>تحليل الأداء</h3>
                <p>تحليل شامل لكل مراحل عملية المبيعات من Lead Generation إلى Closing مع توصيات دقيقة للتحسين.</p>
            </div>
            <div class="service-card fade-in">
                <div class="service-icon">🤝</div>
                <h3>استشارات فردية</h3>
                <p>جلسات استشارية فردية لرجال الأعمال والمديرين لحل أهم التحديات في استراتيجات المبيعات لديهم.</p>
            </div>
        </div>
    </section>

    <!-- Philosophy -->
    <section id="philosophy" class="philosophy-section">
        <div class="section-title">
            <h2>فلسفت<span class="accent">ي</span></h2>
        </div>
        <div class="philosophy-content">
            <div class="philosophy-quote fade-in">
                لو قعدت مكاني ما تعلمت اسوي شي جديد. الدنيا ما وقفت عندي. بدأت من الصفر في مبيعات الشركات وبضرب ارقام. الحياة علمتني ان النهاية مو نهاية. انما هي بداية طريق ثاني الله كاتبه لك. ما تخاف من خسارة وظيفتك وخاف من خسارة طموحك.
            </div>
            <div class="philosophy-rules fade-in">
                <div class="philosophy-rule"><div class="num">١</div>المبيعات فن قبل علم</div>
                <div class="philosophy-rule"><div class="num">٢</div>المعرفة بدون تطبيق ما تسوى</div>
                <div class="philosophy-rule"><div class="num">٣</div>النهاية هي بداية جديدة</div>
                <div class="philosophy-rule"><div class="num">٤</div>الطموح أهم من الوظيفة</div>
            </div>
        </div>
    </section>

    <!-- Testimonials -->
    <section id="testimonials" class="testimonials-section">
        <div class="section-title">
            <h2>آراء <span class="accent">العملاء</span></h2>
        </div>
        <div class="testimonials-grid">
            <div class="testimonial-card fade-in">
                <div class="stars">★★★★★</div>
                <p>محمد غيّر طريقة تفكيرنا في المبيعات بالكامل. من 50% target achievement إلى 120% خلال 3 أشهر فقط. أسلوبه عملي وواضح ولا يضيع الوقت بالنظريات.</p>
                <div class="author">أحمد الشمري</div>
                <div class="role">مدير مبيعات — شركة تقنية</div>
            </div>
            <div class="testimonial-card fade-in">
                <div class="stars">★★★★★</div>
                <p>أفضل استثمار سويته لفرق المبيعات. محمد يفهم السوق السعودي ويعرف كيف يتعامل مع مختلف الشخصيات. النتائج تتكلم عن نفسها.</p>
                <div class="author">سارة العتيبي</div>
                <div class="role">مديرة تطوير أعمال</div>
            </div>
            <div class="testimonial-card fade-in">
                <div class="stars">★★★★★</div>
                <p>من بعد ما اشتغلنا مع محمد، المبيعات ما وقفت. كل شهر فيه نمو. الفريق عنده ثقة وحماس ما كان موجود من قبل. شكراً محمد!</p>
                <div class="author">فهد الحربي</div>
                <div class="role">CEO — شركة مقاولات</div>
            </div>
        </div>
    </section>

    <!-- Posts — Dynamic LinkedIn Feed -->
    <section id="posts" class="posts-section">
        <div class="section-title">
            <h2>أحدث <span class="accent">المنشورات</span></h2>
            <p>يتم التحديث تلقائياً من لينكدان</p>
        </div>
        <div class="linkedin-feed" id="linkedin-feed">
            <div class="feed-loading" id="feed-loading">
                <div class="spinner"></div>
                <div>جاري تحميل أحدث المنشورات...</div>
            </div>
        </div>
    </section>

    <!-- CTA -->
    <section class="cta-section" id="cta">
        <div class="cta-box fade-in">
            <h2>جاهز تطور مبيعاتك؟</h2>
            <p>تواصل معي اليوم وخلنا نبدأ شغل</p>
            <a href="https://wa.me/966592192220" target="_blank" class="btn-primary">تواصل عبر واتساب</a>
            <div class="cta-links">
                <a href="mailto:malkhedeer@gmail.com"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z" fill="currentColor"/></svg> malkhedeer@gmail.com</a>
                <a href="https://t.me/malkhedeer" target="_blank"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.479.33-.913.492-1.302.48-.428-.013-1.252-.242-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z" fill="currentColor"/></svg> Telegram</a>
                <a href="https://linkedin.com/in/mohamedalkhederb2bsales" target="_blank"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" fill="currentColor"/></svg> LinkedIn</a>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer" id="footer">
        <a href="#hero" class="footer-logo">محمد الخضر</a>
        <div class="footer-icons">
            <a href="https://linkedin.com/in/mohamedalkhederb2bsales" target="_blank" title="LinkedIn"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" fill="#8A8A8A"/></svg></a>
            <a href="https://wa.me/966592192220" target="_blank" title="WhatsApp"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24 6.305 22.344a11.882 11.882 0 0 0 5.743 1.473h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z" fill="#8A8A8A"/></svg></a>
            <a href="https://t.me/malkhedeer" target="_blank" title="Telegram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.479.33-.913.492-1.302.48-.428-.013-1.252-.242-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z" fill="#8A8A8A"/></svg></a>
            <a href="mailto:malkhedeer@gmail.com" title="Email"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z" fill="#8A8A8A"/></svg></a>
        </div>
        <p>2026 محمد الخضر. جميع الحقوق محفوظة.</p>
    </footer>

<script>
    /* ---- Navbar scroll ---- */
    window.addEventListener('scroll', () => {
        document.getElementById('navbar').classList.toggle('scrolled', window.scrollY > 50);
    });

    /* ---- Mobile menu ---- */
    function toggleMenu() {
        document.getElementById('navLinks').classList.toggle('open');
    }
    function closeMenu() {
        document.getElementById('navLinks').classList.remove('open');
    }

    /* ---- Animate numbers ---- */
    const statNumbers = document.querySelectorAll('.stat-number[data-target]');
    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const target = parseInt(el.getAttribute('data-target'));
                let count = 0;
                const inc = Math.ceil(target / 60);
                const step = () => { count += inc; if (count >= target) { count = target; } el.textContent = count.toLocaleString('ar-SA'); if (count < target) requestAnimationFrame(step); };
                step();
                statsObserver.unobserve(el);
            }
        });
    }, { threshold: 0.5 });
    statNumbers.forEach(n => statsObserver.observe(n));

    /* ---- Fade in on scroll ---- */
    const fadeEls = document.querySelectorAll('.fade-in:not(.visible)');
    const fadeObs = new IntersectionObserver((entries) => {
        entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); fadeObs.unobserve(e.target); } });
    }, { threshold: 0.1 });
    fadeEls.forEach(el => fadeObs.observe(el));

    /* ---- Dynamic LinkedIn posts fetcher ---- */
    (async function loadPosts() {
        const feed = document.getElementById('linkedin-feed');
        const loading = document.getElementById('feed-loading');

        // Helper: relative time in Arabic
        function timeAgo(ts) {
            if (!ts) return '';
            const diff = Date.now() - ts;
            const mins = Math.floor(diff / 60000);
            const hrs = Math.floor(mins / 60);
            const days = Math.floor(hrs / 24);
            if (mins < 60) return 'منذ ' + mins + ' دقيقة';
            if (hrs < 24) return 'منذ ' + hrs + ' ساعة';
            if (days <= 7) return 'منذ ' + days + ' يوم';
            return 'منذ ' + Math.floor(days / 7) + ' أسبوع';
        }

        // Helper: format numbers in Arabic
        function fmtNum(n) {
            if (!n) return '٠';
            if (n >= 1000000) return (n/1000000).toFixed(1).replace('.','٫') + 'M';
            if (n >= 1000) return (n/1000).toFixed(1).replace('.','٫') + 'K';
            return String(n);
        }

        // Try loading from posts.json first
        try {
            const res = await fetch('posts.json?_t=' + Date.now());
            if (res.ok) {
                const data = await res.json();
                if (data.posts && data.posts.length > 0) {
                    loading.remove();
                    data.posts.forEach(p => {
                        const card = document.createElement('div');
                        card.className = 'feed-card fade-in visible';
                        let mediaHTML = '';
                        if (p.mediaUrl) {
                            mediaHTML = '<img class="feed-image" src="' + p.mediaUrl + '" alt="صورة المنشور" onerror="this.style.display=\'none\'">';
                        }
                        if (p.image) {
                            mediaHTML = '<img class="feed-image" src="' + p.image + '" alt="صورة المنشور" onerror="this.style.display=\'none\'">';
                        }
                        card.innerHTML =
                            '<div class="feed-header">' +
                                '<div class="feed-avatar"><img src="profile.jpg" alt="محمد الخضر"></div>' +
                                '<div class="feed-author-info">' +
                                    '<div class="feed-author-name">' + (p.authorName || 'محمد الخضر') + '</div>' +
                                    '<div class="feed-author-title">Strategic B2B Sales Leader | Growth Architect</div>' +
                                '</div>' +
                                '<div class="feed-time">' + timeAgo(p.timestamp) + '</div>' +
                            '</div>' +
                            '<div class="feed-body">' +
                                '<div class="feed-text">' + (p.text || '').substring(0, 300) + '</div>' +
                                mediaHTML +
                            '</div>' +
                            '<div class="feed-stats">' +
                                '<div class="feed-stat">👏 <span class="num">' + fmtNum(p.likes || p.likeCount) + '</span> إعجاب</div>' +
                                '<div class="feed-stat">💬 <span class="num">' + fmtNum(p.comments || p.commentCount) + '</span> تعليق</div>' +
                                '<div class="feed-stat">🔁 <span class="num">' + fmtNum(p.reposts) + '</span> إعادة نشر</div>' +
                            '</div>' +
                            '<a href="' + (p.postUrl || p.url || 'https://linkedin.com/in/mohamedalkhederb2bsales/') + '" target="_blank" class="feed-link">اقرأ المنشور كاملا على LinkedIn ←</a>';
                        feed.appendChild(card);
                    });
                    return;
                }
            }
        } catch(e) {
            console.log('posts.json fetch failed, using fallback', e);
        }

        // Fallback: show sample posts
        loading.remove();
        const fallback = [
            {
                text: 'الحياة علمتني حاجة وحدة: ما تنتظر الفرصة، اصنعها. أنا بدأت من الصفر في مبيعات الشركات وما توقفت. كل يوم فرصة جديدة. كل رفض هو درس. كل نجاح هو بداية طريق ثاني. لو تبى تسوي فرق في حياتك المهنية، تبدأ من النهاردة. مو بكرة. النهاردة.',
                likes: 284, comments: 32, reposts: 15,
                timestamp: Date.now() - 3 * 86400000,
                postUrl: 'https://linkedin.com/in/mohamedalkhederb2bsales/'
            },
            {
                text: 'لو قعدت مكاني ما تعلمت اسوي شي جديد. الدنيا ما وقفت عندي. بدأت من الصفر في مبيعات الشركات وبضرب ارقام. الحياة علمتني ان النهاية مو نهاية. انما هي بداية طريق ثاني الله كاتبه لك. ما تخاف من خسارة وظيفتك وخاف من خسارة طموحك.',
                likes: 423, comments: 67, reposts: 28,
                timestamp: Date.now() - 7 * 86400000,
                postUrl: 'https://linkedin.com/in/mohamedalkhederb2bsales/'
            }
        ];

        fallback.forEach(p => {
            const card = document.createElement('div');
            card.className = 'feed-card fade-in visible';
            card.innerHTML =
                '<div class="feed-header">' +
                    '<div class="feed-avatar"><img src="profile.jpg" alt="محمد الخضر"></div>' +
                    '<div class="feed-author-info">' +
                        '<div class="feed-author-name">محمد الخضر</div>' +
                        '<div class="feed-author-title">Strategic B2B Sales Leader | Growth Architect</div>' +
                    '</div>' +
                    '<div class="feed-time">' + timeAgo(p.timestamp) + '</div>' +
                '</div>' +
                '<div class="feed-body">' +
                    '<div class="feed-text">' + p.text + '</div>' +
                '</div>' +
                '<div class="feed-stats">' +
                    '<div class="feed-stat">👏 <span class="num">' + (p.likes||0) + '</span> إعجاب</div>' +
                    '<div class="feed-stat">💬 <span class="num">' + (p.comments||0) + '</span> تعليق</div>' +
                    '<div class="feed-stat">🔁 <span class="num">' + (p.reposts||0) + '</span> إعادة نشر</div>' +
                '</div>' +
                '<a href="' + p.postUrl + '" target="_blank" class="feed-link">اقرأ المنشور كاملا على LinkedIn ←</a>';
            feed.appendChild(card);
        });
    })();
</script>
</body>
</html>'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

import os
size = os.path.getsize('index.html')
print(f"Done: {size} bytes written to index.html")
