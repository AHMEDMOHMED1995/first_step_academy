from flask import Flask, render_template, request, jsonify
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
from urllib.parse import quote
import arabic_reshaper
from bidi.algorithm import get_display
import os
import csv
import re


app = Flask(__name__)

BASE_DIR = app.root_path
PDF_FOLDER = os.path.join(BASE_DIR, "pdf")
DATA_FOLDER = os.path.join(BASE_DIR, "data")
CSV_FILE = os.path.join(DATA_FOLDER, "registrations.csv")
IMAGES_FOLDER = os.path.join(BASE_DIR, "static", "images")

os.makedirs(PDF_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)


def register_arabic_fonts():
    normal_font_paths = [
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\tahoma.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]

    bold_font_paths = [
        r"C:\Windows\Fonts\arialbd.ttf",
        r"C:\Windows\Fonts\tahomabd.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]

    normal_font = next((p for p in normal_font_paths if os.path.exists(p)), None)
    bold_font = next((p for p in bold_font_paths if os.path.exists(p)), None)

    if normal_font:
        pdfmetrics.registerFont(TTFont("ArabicFont", normal_font))

    if bold_font:
        pdfmetrics.registerFont(TTFont("ArabicBold", bold_font))
    elif normal_font:
        pdfmetrics.registerFont(TTFont("ArabicBold", normal_font))


register_arabic_fonts()


def rtl(text):
    text = str(text or "")
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)


def safe_filename(text):
    text = str(text or "لاعب").strip()
    text = re.sub(r'[<>:"/\\|?*]', "-", text)
    text = re.sub(r"\s+", " ", text)
    return text[:80]


def draw_right(pdf, text, x, y, size=12, bold=False, color="#1d2940"):
    font_name = "ArabicBold" if bold else "ArabicFont"

    try:
        pdf.setFont(font_name, size)
    except Exception:
        pdf.setFont("Helvetica", size)

    pdf.setFillColor(colors.HexColor(color))
    pdf.drawRightString(x, y, rtl(text))


def get_next_request_number():
    year = datetime.now().year
    count = 1

    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            count = len(rows) + 1

    return f"FSA-{year}-{count:04d}"


def save_to_csv(data, request_number, pdf_name):
    file_exists = os.path.exists(CSV_FILE)

    headers = [
        "رقم الطلب",
        "تاريخ التسجيل",
        "اسم اللاعب",
        "سن اللاعب",
        "تاريخ الميلاد",
        "مركز اللاعب",
        "المستوى",
        "القدم المفضلة",
        "هل لعب سابقا",
        "ملاحظات صحية",
        "اسم ولي الأمر",
        "صلة القرابة",
        "رقم الهاتف",
        "رقم واتساب",
        "رقم بديل",
        "المنطقة",
        "هدف التسجيل",
        "الموعد المناسب",
        "نوع الاشتراك",
        "طريقة الدفع",
        "حالة الدفع",
        "رقم عملية الدفع",
        "ملاحظات",
        "اسم ملف PDF",
    ]

    row = {
        "رقم الطلب": request_number,
        "تاريخ التسجيل": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "اسم اللاعب": data.get("playerName", ""),
        "سن اللاعب": data.get("playerAge", ""),
        "تاريخ الميلاد": data.get("birthDate", ""),
        "مركز اللاعب": data.get("playerPosition", ""),
        "المستوى": data.get("playerLevel", ""),
        "القدم المفضلة": data.get("preferredFoot", ""),
        "هل لعب سابقا": data.get("previousAcademy", ""),
        "ملاحظات صحية": data.get("healthNotes", ""),
        "اسم ولي الأمر": data.get("guardianName", ""),
        "صلة القرابة": data.get("relation", ""),
        "رقم الهاتف": data.get("phoneNumber", ""),
        "رقم واتساب": data.get("whatsappNumber", ""),
        "رقم بديل": data.get("alternativePhone", ""),
        "المنطقة": data.get("area", ""),
        "هدف التسجيل": data.get("trainingGoal", ""),
        "الموعد المناسب": data.get("preferredTime", ""),
        "نوع الاشتراك": data.get("subscriptionType", ""),
        "طريقة الدفع": data.get("paymentMethod", ""),
        "حالة الدفع": data.get("paymentStatus", ""),
        "رقم عملية الدفع": data.get("paymentReference", ""),
        "ملاحظات": data.get("notes", ""),
        "اسم ملف PDF": pdf_name,
    }

    with open(CSV_FILE, "a", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)


def create_booking_pdf(data, request_number):
    player_name = safe_filename(data.get("playerName"))
    pdf_name = f"طلب حجز - {player_name} - {request_number}.pdf"
    pdf_path = os.path.join(PDF_FOLDER, pdf_name)

    pdf = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    blue_dark = "#071b4d"
    blue_main = "#0b48b8"
    gold = "#f4c542"
    light_bg = "#f3f7ff"
    text = "#1d2940"
    muted = "#667085"

    pdf.setFillColor(colors.HexColor(light_bg))
    pdf.rect(0, 0, width, height, fill=1, stroke=0)

    pdf.setFillColor(colors.HexColor(blue_dark))
    pdf.roundRect(1.1 * cm, height - 4.4 * cm, width - 2.2 * cm, 3.3 * cm, 18, fill=1, stroke=0)

    logo_path = os.path.join(IMAGES_FOLDER, "logo.png")
    if os.path.exists(logo_path):
        try:
            pdf.drawImage(
                logo_path,
                1.7 * cm,
                height - 4.0 * cm,
                width=2.5 * cm,
                height=2.5 * cm,
                preserveAspectRatio=True,
                mask="auto",
            )
        except Exception:
            pass

    draw_right(pdf, "أكاديمية الخطوة الأولى لكرة القدم", width - 1.7 * cm, height - 2.15 * cm, 18, True, "#ffffff")
    draw_right(pdf, "استمارة حجز لاعب جديد", width - 1.7 * cm, height - 3.05 * cm, 24, True, gold)
    draw_right(pdf, f"رقم الطلب: {request_number}", width - 1.7 * cm, height - 3.85 * cm, 13, True, "#ffffff")

    y = height - 5.4 * cm

    def section_title(title):
        nonlocal y
        draw_right(pdf, title, width - 1.5 * cm, y, 16, True, blue_dark)
        y -= 0.55 * cm
        pdf.setStrokeColor(colors.HexColor("#d9e4ff"))
        pdf.line(1.5 * cm, y, width - 1.5 * cm, y)
        y -= 0.55 * cm

    def row(label, value):
        nonlocal y
        pdf.setFillColor(colors.white)
        pdf.roundRect(1.5 * cm, y - 0.38 * cm, width - 3 * cm, 0.72 * cm, 8, fill=1, stroke=0)
        draw_right(pdf, f"{label}:", width - 1.9 * cm, y - 0.14 * cm, 10.5, True, blue_main)
        draw_right(pdf, value or "-", width - 6.7 * cm, y - 0.14 * cm, 10.5, False, text)
        y -= 0.82 * cm

    section_title("أولًا: بيانات اللاعب")
    row("اسم اللاعب", data.get("playerName"))
    row("السن", f"{data.get('playerAge')} سنة")
    row("تاريخ الميلاد", data.get("birthDate"))
    row("مركز اللاعب", data.get("playerPosition"))
    row("مستوى اللاعب", data.get("playerLevel"))
    row("القدم المفضلة", data.get("preferredFoot"))
    row("خبرة سابقة", data.get("previousAcademy"))
    row("ملاحظات صحية", data.get("healthNotes"))

    y -= 0.25 * cm
    section_title("ثانيًا: بيانات ولي الأمر")
    row("اسم ولي الأمر", data.get("guardianName"))
    row("صلة القرابة", data.get("relation"))
    row("رقم الهاتف", data.get("phoneNumber"))
    row("رقم واتساب", data.get("whatsappNumber"))
    row("رقم بديل", data.get("alternativePhone"))
    row("المنطقة", data.get("area"))

    y -= 0.25 * cm
    section_title("ثالثًا: بيانات التدريب والدفع")
    row("هدف التسجيل", data.get("trainingGoal"))
    row("الموعد المناسب", data.get("preferredTime"))
    row("نوع الاشتراك", data.get("subscriptionType"))
    row("طريقة الدفع", data.get("paymentMethod"))
    row("حالة الدفع", data.get("paymentStatus"))
    row("رقم عملية الدفع", data.get("paymentReference"))

    if y < 5 * cm:
        pdf.showPage()
        pdf.setFillColor(colors.HexColor(light_bg))
        pdf.rect(0, 0, width, height, fill=1, stroke=0)
        y = height - 2 * cm

    y -= 0.25 * cm
    section_title("ملاحظات إضافية")
    pdf.setFillColor(colors.white)
    pdf.roundRect(1.5 * cm, y - 2.2 * cm, width - 3 * cm, 2.0 * cm, 12, fill=1, stroke=0)
    draw_right(pdf, data.get("notes") or "لا توجد ملاحظات إضافية.", width - 2 * cm, y - 0.85 * cm, 11, False, text)

    y -= 3 * cm

    pdf.setFillColor(colors.HexColor("#fff7d6"))
    pdf.roundRect(1.5 * cm, y - 2.2 * cm, width - 3 * cm, 2.0 * cm, 12, fill=1, stroke=0)

    draw_right(pdf, "إقرار ولي الأمر", width - 2 * cm, y - 0.65 * cm, 12, True, blue_dark)
    draw_right(pdf, "أقر بصحة البيانات الموضحة أعلاه، وأوافق على مشاركة اللاعب في تدريبات الأكاديمية.", width - 2 * cm, y - 1.25 * cm, 10.5, False, blue_dark)

    y -= 3 * cm

    draw_right(pdf, "توقيع ولي الأمر: ........................................", width - 2 * cm, y, 11, True, muted)
    draw_right(pdf, "توقيع إدارة الأكاديمية: ........................................", width - 2 * cm, y - 0.8 * cm, 11, True, muted)

    pdf.setFillColor(colors.HexColor(blue_dark))
    pdf.rect(0, 0, width, 1.25 * cm, fill=1, stroke=0)
    draw_right(pdf, "أكاديمية الخطوة الأولى - الساحل الشمالي - مدينة الحمام - ملعب مشري", width - 1.5 * cm, 0.48 * cm, 9.5, True, "#ffffff")
    draw_right(pdf, "01225990118 / 01142007771", 7.0 * cm, 0.48 * cm, 9.5, True, gold)

    pdf.save()
    return pdf_name


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit-booking", methods=["POST"])
def submit_booking():
    data = request.get_json(silent=True) or request.form.to_dict() or {}

    required = [
        "playerName",
        "playerAge",
        "guardianName",
        "phoneNumber",
        "whatsappNumber",
        "playerPosition",
        "playerLevel",
        "subscriptionType",
        "paymentMethod",
    ]

    for field in required:
        if not str(data.get(field, "")).strip():
            return jsonify({
                "success": False,
                "message": "من فضلك أكمل البيانات الأساسية المطلوبة."
            }), 400

    request_number = get_next_request_number()
    pdf_name = create_booking_pdf(data, request_number)
    save_to_csv(data, request_number, pdf_name)

    whatsapp_message = f"""
طلب تسجيل جديد - أكاديمية الخطوة الأولى لكرة القدم

رقم الطلب: {request_number}
ملف الطلب: {pdf_name}

بيانات اللاعب:
الاسم: {data.get("playerName")}
السن: {data.get("playerAge")} سنة
المركز: {data.get("playerPosition")}
المستوى: {data.get("playerLevel")}
القدم المفضلة: {data.get("preferredFoot") or "-"}

بيانات ولي الأمر:
الاسم: {data.get("guardianName")}
الهاتف: {data.get("phoneNumber")}
واتساب: {data.get("whatsappNumber")}
المنطقة: {data.get("area") or "-"}

التدريب والدفع:
هدف التسجيل: {data.get("trainingGoal") or "-"}
نوع الاشتراك: {data.get("subscriptionType")}
طريقة الدفع: {data.get("paymentMethod")}
حالة الدفع: {data.get("paymentStatus") or "لم يتم الدفع"}
رقم العملية: {data.get("paymentReference") or "-"}

تم حفظ الطلب تلقائيًا في ملف PDF داخل فولدر pdf،
وتم تسجيل البيانات في ملف registrations.csv داخل فولدر data.

برجاء مراجعة الطلب والتواصل مع ولي الأمر لتأكيد الموعد.
""".strip()

    whatsapp_url = "https://wa.me/201225990118?text=" + quote(whatsapp_message)

    return jsonify({
        "success": True,
        "request_number": request_number,
        "booking_id": request_number,
        "pdf_name": pdf_name,
        "whatsapp_url": whatsapp_url
    })


if __name__ == "__main__":
    app.run(debug=True)