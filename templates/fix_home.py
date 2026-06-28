from pathlib import Path
import re
import shutil

BASE_DIR = Path.cwd()
index_path = BASE_DIR / "templates" / "index.html"
home_css_path = BASE_DIR / "static" / "css" / "home-fix.css"

if not index_path.exists():
    raise FileNotFoundError("ملف templates/index.html غير موجود. تأكد أنك داخل فولدر المشروع.")

# Backup
backup_path = index_path.with_suffix(".html.home_backup")
shutil.copy2(index_path, backup_path)

html = index_path.read_text(encoding="utf-8")

new_home_section = r'''
<section class="elite-home-section" id="home">
  <div class="elite-home-bg"></div>
  <div class="elite-home-lines"></div>
  <div class="elite-home-light light-one"></div>
  <div class="elite-home-light light-two"></div>

  <div class="container elite-home-wrapper">
    <div class="elite-home-content">
      <div class="elite-home-badge">
        <span>⚽</span>
        <strong>First Step Football Academy</strong>
      </div>

      <h1>
        أكاديمية الخطوة الأولى
        <span>من أول لمسة.. إلى طريق الاحتراف</span>
      </h1>

      <p>
        نؤسس اللاعب من البداية، نطور مهاراته، ونبني شخصيته داخل الملعب من خلال تدريب منظم،
        متابعة فنية، وبيئة رياضية محفزة تساعده على الوصول لمستوى أعلى.
      </p>

      <div class="elite-home-actions">
        <a href="#join" class="btn btn-primary">سجّل لاعبك الآن</a>
        <a href="#programs" class="btn btn-outline">اكتشف البرامج</a>
      </div>

      <div class="elite-home-steps">
        <div>
          <strong>01</strong>
          <span>تقييم أولي</span>
        </div>
        <div>
          <strong>02</strong>
          <span>تدريب منظم</span>
        </div>
        <div>
          <strong>03</strong>
          <span>متابعة وتطوير</span>
        </div>
      </div>
    </div>

    <div class="elite-home-visual">
      <div class="elite-main-card">
        <div class="elite-card-head">
          <span>Academy Identity</span>
          <strong>انتماء · أداء · مستقبل</strong>
        </div>

        <div class="elite-logo-area">
          <img src="{{ url_for('static', filename='images/logo.png') }}" alt="شعار أكاديمية الخطوة الأولى">
          <div class="elite-football"></div>
        </div>

        <div class="elite-card-stats">
          <div>
            <strong>تأسيس</strong>
            <span>من أول خطوة</span>
          </div>
          <div>
            <strong>مهارة</strong>
            <span>تطوير عملي</span>
          </div>
          <div>
            <strong>احتراف</strong>
            <span>طريق واضح</span>
          </div>
        </div>
      </div>

      <div class="elite-mini-card mini-card-one">
        <span>🏃</span>
        <strong>تدريب منظم</strong>
      </div>

      <div class="elite-mini-card mini-card-two">
        <span>🏆</span>
        <strong>تجهيز للمنافسة</strong>
      </div>
    </div>
  </div>

  <div class="elite-home-strip">
    <div class="elite-home-track">
      <span>تأسيس صحيح</span>
      <span>تطوير مهاري</span>
      <span>إشراف فني</span>
      <span>متابعة شهرية</span>
      <span>انضباط</span>
      <span>ثقة</span>
      <span>طريق الاحتراف</span>
      <span>تأسيس صحيح</span>
      <span>تطوير مهاري</span>
      <span>إشراف فني</span>
      <span>متابعة شهرية</span>
      <span>انضباط</span>
      <span>ثقة</span>
      <span>طريق الاحتراف</span>
    </div>
  </div>
</section>
'''

pattern = re.compile(r'<section[^>]*id=["\']home["\'][\s\S]*?</section>', re.IGNORECASE)

if not pattern.search(html):
    raise RuntimeError("لم أجد قسم الرئيسية id='home' داخل index.html")

html = pattern.sub(new_home_section, html, count=1)

# Add home-fix.css after all CSS, before </head>
home_link = '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/home-fix.css\') }}?v=home-final-1" />'

if "home-fix.css" not in html:
    html = html.replace("</head>", f"  {home_link}\n</head>")

index_path.write_text(html, encoding="utf-8")

home_css = r'''
/* HOME FINAL FIX - This file overrides old accumulated home styles */

#home.elite-home-section {
  min-height: 100vh !important;
  position: relative !important;
  overflow: hidden !important;
  padding: 125px 0 92px !important;
  display: flex !important;
  align-items: center !important;
  background:
    linear-gradient(135deg, rgba(4,17,47,0.98), rgba(7,27,77,0.96) 42%, rgba(11,72,184,0.92)),
    radial-gradient(circle at 82% 18%, rgba(244,197,66,0.28), transparent 32%) !important;
}

#home.elite-home-section.app-page {
  padding: 125px 0 92px !important;
}

#home .elite-home-bg {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px);
  background-size: 58px 58px;
  opacity: 0.55;
  z-index: 1;
}

#home .elite-home-light {
  position: absolute;
  width: 520px;
  height: 520px;
  border-radius: 50%;
  filter: blur(24px);
  opacity: 0.55;
  z-index: 1;
}

#home .light-one {
  right: -180px;
  top: -180px;
  background: rgba(28,124,255,0.45);
}

#home .light-two {
  left: -200px;
  bottom: -220px;
  background: rgba(244,197,66,0.32);
}

#home .elite-home-lines {
  position: absolute;
  left: 50%;
  bottom: -155px;
  width: 1050px;
  height: 430px;
  transform: translateX(-50%) perspective(900px) rotateX(62deg);
  border: 2px solid rgba(255,255,255,0.16);
  border-radius: 50%;
  opacity: 0.45;
  z-index: 1;
}

#home .elite-home-lines::before,
#home .elite-home-lines::after {
  content: "";
  position: absolute;
  inset: 70px;
  border: 2px solid rgba(255,255,255,0.12);
  border-radius: 50%;
}

#home .elite-home-lines::after {
  inset: 145px;
}

#home .elite-home-wrapper {
  position: relative;
  z-index: 5;
  display: grid;
  grid-template-columns: 1fr 0.9fr;
  align-items: center;
  gap: 56px;
}

#home .elite-home-content {
  color: #ffffff;
}

#home .elite-home-badge {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 10px 18px;
  border-radius: 100px;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(244,197,66,0.32);
  color: #ffe08a;
  font-weight: 900;
  margin-bottom: 24px;
}

#home .elite-home-content h1 {
  font-size: clamp(48px, 6vw, 82px);
  line-height: 1.08;
  font-weight: 900;
  margin-bottom: 24px;
  color: #ffffff;
}

#home .elite-home-content h1 span {
  display: block;
  margin-top: 12px;
  color: #f4c542;
  font-size: clamp(30px, 4vw, 52px);
}

#home .elite-home-content p {
  color: rgba(255,255,255,0.82);
  font-size: 18px;
  line-height: 2;
  max-width: 720px;
  margin-bottom: 30px;
}

#home .elite-home-actions {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
  margin-bottom: 30px;
}

#home .elite-home-steps {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
  max-width: 650px;
}

#home .elite-home-steps div {
  padding: 18px;
  border-radius: 24px;
  background: rgba(255,255,255,0.09);
  border: 1px solid rgba(255,255,255,0.13);
  backdrop-filter: blur(16px);
}

#home .elite-home-steps strong {
  display: block;
  color: #ffe08a;
  font-size: 24px;
  margin-bottom: 5px;
}

#home .elite-home-steps span {
  color: rgba(255,255,255,0.78);
  font-weight: 800;
}

#home .elite-home-visual {
  position: relative;
  min-height: 560px;
}

#home .elite-main-card {
  position: absolute;
  inset: 15px 20px 45px;
  border-radius: 44px;
  padding: 28px;
  background: linear-gradient(160deg, rgba(255,255,255,0.17), rgba(255,255,255,0.06));
  border: 1px solid rgba(255,255,255,0.18);
  box-shadow: 0 38px 100px rgba(0,0,0,0.34);
  backdrop-filter: blur(20px);
  overflow: hidden;
}

#home .elite-main-card::before {
  content: "";
  position: absolute;
  inset: 24px;
  border: 1px dashed rgba(255,255,255,0.16);
  border-radius: 32px;
}

#home .elite-card-head {
  position: relative;
  z-index: 3;
  display: flex;
  justify-content: space-between;
  gap: 18px;
  align-items: center;
}

#home .elite-card-head span {
  color: rgba(255,255,255,0.72);
  font-weight: 800;
  font-size: 13px;
}

#home .elite-card-head strong {
  color: #ffe08a;
  font-weight: 900;
}

#home .elite-logo-area {
  position: relative;
  z-index: 3;
  min-height: 340px;
  display: grid;
  place-items: center;
}

#home .elite-logo-area img {
  width: 280px;
  height: 280px;
  object-fit: contain;
  background: rgba(255,255,255,0.96);
  border-radius: 50%;
  padding: 18px;
  box-shadow: 0 28px 60px rgba(0,0,0,0.30);
  animation: homeLogoFloat 4s ease-in-out infinite;
}

@keyframes homeLogoFloat {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-12px) scale(1.02); }
}

#home .elite-football {
  position: absolute;
  width: 86px;
  height: 86px;
  border-radius: 50%;
  right: 52px;
  bottom: 60px;
  background:
    radial-gradient(circle at 34% 28%, #ffffff, #e8eefc 42%, #111827 43%, #111827 49%, #ffffff 50%),
    repeating-conic-gradient(from 0deg, #ffffff 0 15deg, #111827 15deg 29deg);
  box-shadow: 0 18px 42px rgba(0,0,0,0.34), inset -10px -12px 18px rgba(0,0,0,0.18);
  animation: homeBallMove 3.5s ease-in-out infinite;
}

@keyframes homeBallMove {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  35% { transform: translate(-35px, -28px) rotate(80deg); }
  70% { transform: translate(18px, 12px) rotate(155deg); }
}

#home .elite-card-stats {
  position: absolute;
  right: 28px;
  left: 28px;
  bottom: 28px;
  z-index: 3;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

#home .elite-card-stats div {
  padding: 14px 10px;
  border-radius: 20px;
  background: rgba(255,255,255,0.92);
  text-align: center;
}

#home .elite-card-stats strong {
  display: block;
  color: #071b4d;
  font-weight: 900;
  margin-bottom: 3px;
}

#home .elite-card-stats span {
  color: #667085;
  font-size: 12px;
  font-weight: 800;
}

#home .elite-mini-card {
  position: absolute;
  z-index: 6;
  min-width: 180px;
  padding: 16px 18px;
  border-radius: 24px;
  background: rgba(255,255,255,0.94);
  color: #071b4d;
  box-shadow: 0 22px 50px rgba(0,0,0,0.22);
  backdrop-filter: blur(16px);
  animation: homeMiniFloat 4s ease-in-out infinite;
}

#home .elite-mini-card span {
  font-size: 26px;
  display: block;
  margin-bottom: 6px;
}

#home .elite-mini-card strong {
  font-weight: 900;
}

#home .mini-card-one {
  right: -5px;
  top: 135px;
}

#home .mini-card-two {
  left: 0;
  bottom: 125px;
  animation-delay: 0.8s;
}

@keyframes homeMiniFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-14px); }
}

#home .elite-home-strip {
  position: absolute;
  right: 0;
  left: 0;
  bottom: 0;
  height: 62px;
  z-index: 8;
  overflow: hidden;
  display: flex;
  align-items: center;
  background: rgba(4,17,47,0.78);
  border-top: 1px solid rgba(255,255,255,0.12);
  backdrop-filter: blur(16px);
}

#home .elite-home-track {
  display: flex;
  gap: 16px;
  white-space: nowrap;
  animation: homeStripMove 25s linear infinite;
}

#home .elite-home-track span {
  color: #ffe08a;
  font-weight: 900;
  padding: 9px 16px;
  border-radius: 100px;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.10);
}

@keyframes homeStripMove {
  from { transform: translateX(0); }
  to { transform: translateX(50%); }
}

@media (max-width: 1100px) {
  #home .elite-home-wrapper {
    grid-template-columns: 1fr;
  }

  #home .elite-home-visual {
    min-height: 520px;
  }

  #home .elite-home-steps {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 760px) {
  #home.elite-home-section,
  #home.elite-home-section.app-page {
    padding: 110px 0 92px !important;
  }

  #home .elite-home-actions .btn {
    width: 100%;
  }

  #home .elite-home-visual {
    min-height: 430px;
  }

  #home .elite-main-card {
    inset: 10px 0 40px;
    border-radius: 32px;
  }

  #home .elite-logo-area img {
    width: 210px;
    height: 210px;
  }

  #home .elite-football {
    width: 68px;
    height: 68px;
    right: 35px;
  }

  #home .elite-card-stats {
    grid-template-columns: 1fr;
  }

  #home .elite-mini-card {
    display: none;
  }
}
'''

home_css_path.write_text(home_css, encoding="utf-8")

print("تم إصلاح الرئيسية بنجاح.")
print("تم عمل نسخة احتياطية من index.html هنا:")
print(backup_path)
print("تم إنشاء ملف CSS مستقل هنا:")
print(home_css_path)