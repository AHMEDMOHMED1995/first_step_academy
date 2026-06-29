// ======================================================
// First Step Academy - Static Vercel Version
// المسار: static/js/main.js
// التعديل: تشغيل الموقع بدون Flask وبدون PDF + إرسال رسالة واتساب منسقة
// ======================================================

(function () {
  "use strict";

  const WHATSAPP_NUMBER = "201225990118";

  const pageIds = ["home", "about", "programs", "coach", "identity", "join", "contact"];

  function showPage(targetId) {
    const safeId = pageIds.includes(targetId) ? targetId : "home";

    pageIds.forEach((id) => {
      const section = document.getElementById(id);
      if (!section) return;

      if (id === safeId) {
        section.style.display = "";
        section.classList.add("active-page");
      } else {
        section.style.display = "none";
        section.classList.remove("active-page");
      }
    });

    document.querySelectorAll(".nav-menu a, .nav-link").forEach((link) => {
      const href = (link.getAttribute("href") || "").replace("#", "");
      link.classList.toggle("active", href === safeId);
    });

    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function initNavigation() {
    const initialHash = (window.location.hash || "#home").replace("#", "");
    showPage(initialHash);

    document.addEventListener("click", function (event) {
      const link = event.target.closest('a[href^="#"]');
      if (!link) return;

      const targetId = link.getAttribute("href").replace("#", "");
      if (!pageIds.includes(targetId)) return;

      event.preventDefault();
      history.pushState(null, "", "#" + targetId);
      showPage(targetId);
    });

    window.addEventListener("hashchange", function () {
      const targetId = (window.location.hash || "#home").replace("#", "");
      showPage(targetId);
    });
  }

  function getFormValue(form, name) {
    const field = form.querySelector(`[name="${name}"], #${name}`);
    return field ? String(field.value || "").trim() : "";
  }

  function getAnyValue(form, names) {
    for (const name of names) {
      const value = getFormValue(form, name);
      if (value) return value;
    }
    return "";
  }

  function buildRegistrationData(form) {
    const now = new Date();
    const requestNumber = "FSA-" + now.getFullYear() + "-" + String(Date.now()).slice(-6);

    return {
      requestNumber,
      createdAt: now.toLocaleString("ar-EG"),

      playerName: getAnyValue(form, ["playerName", "player_name", "name"]),
      playerAge: getAnyValue(form, ["playerAge", "player_age", "age"]),
      birthDate: getAnyValue(form, ["birthDate", "birth_date"]),
      playerPosition: getAnyValue(form, ["playerPosition", "player_position", "position"]),
      playerLevel: getAnyValue(form, ["playerLevel", "player_level", "level"]),
      preferredFoot: getAnyValue(form, ["preferredFoot", "preferred_foot"]),
      previousAcademy: getAnyValue(form, ["previousAcademy", "previous_academy"]),
      healthNotes: getAnyValue(form, ["healthNotes", "health_notes"]),

      guardianName: getAnyValue(form, ["guardianName", "guardian_name"]),
      relation: getAnyValue(form, ["relation"]),
      phoneNumber: getAnyValue(form, ["phoneNumber", "phone", "phone_number"]),
      whatsappNumber: getAnyValue(form, ["whatsappNumber", "whatsapp", "whatsapp_number"]),
      alternativePhone: getAnyValue(form, ["alternativePhone", "alternative_phone"]),
      area: getAnyValue(form, ["area", "address"]),

      trainingGoal: getAnyValue(form, ["trainingGoal", "training_goal"]),
      preferredTime: getAnyValue(form, ["preferredTime", "preferred_time"]),
      subscriptionType: getAnyValue(form, ["subscriptionType", "subscription_type"]),
      paymentMethod: getAnyValue(form, ["paymentMethod", "payment_method"]),
      paymentStatus: getAnyValue(form, ["paymentStatus", "payment_status"]),
      paymentReference: getAnyValue(form, ["paymentReference", "payment_reference"]),
      notes: getAnyValue(form, ["notes"])
    };
  }

  function valueOrDash(value) {
    return value && String(value).trim() ? String(value).trim() : "-";
  }

  function buildWhatsAppMessage(data) {
    return [
      "⚽ *طلب تسجيل جديد - أكاديمية الخطوة الأولى لكرة القدم*",
      "",
      "━━━━━━━━━━━━━━",
      "*بيانات الطلب*",
      "━━━━━━━━━━━━━━",
      "1. رقم الطلب: " + valueOrDash(data.requestNumber),
      "2. تاريخ الطلب: " + valueOrDash(data.createdAt),
      "",
      "━━━━━━━━━━━━━━",
      "*أولًا: بيانات اللاعب*",
      "━━━━━━━━━━━━━━",
      "3. اسم اللاعب: " + valueOrDash(data.playerName),
      "4. سن اللاعب: " + valueOrDash(data.playerAge),
      "5. تاريخ الميلاد: " + valueOrDash(data.birthDate),
      "6. مركز اللاعب: " + valueOrDash(data.playerPosition),
      "7. مستوى اللاعب: " + valueOrDash(data.playerLevel),
      "8. القدم المفضلة: " + valueOrDash(data.preferredFoot),
      "9. هل لعب سابقًا؟: " + valueOrDash(data.previousAcademy),
      "10. ملاحظات صحية: " + valueOrDash(data.healthNotes),
      "",
      "━━━━━━━━━━━━━━",
      "*ثانيًا: بيانات ولي الأمر*",
      "━━━━━━━━━━━━━━",
      "11. اسم ولي الأمر: " + valueOrDash(data.guardianName),
      "12. صلة القرابة: " + valueOrDash(data.relation),
      "13. رقم الهاتف الأساسي: " + valueOrDash(data.phoneNumber),
      "14. رقم واتساب: " + valueOrDash(data.whatsappNumber),
      "15. رقم بديل: " + valueOrDash(data.alternativePhone),
      "16. المنطقة / العنوان: " + valueOrDash(data.area),
      "",
      "━━━━━━━━━━━━━━",
      "*ثالثًا: التدريب والدفع*",
      "━━━━━━━━━━━━━━",
      "17. هدف التسجيل: " + valueOrDash(data.trainingGoal),
      "18. الموعد المناسب: " + valueOrDash(data.preferredTime),
      "19. نوع الاشتراك: " + valueOrDash(data.subscriptionType),
      "20. طريقة الدفع: " + valueOrDash(data.paymentMethod),
      "21. حالة الدفع: " + valueOrDash(data.paymentStatus),
      "22. رقم العملية / ملاحظة الدفع: " + valueOrDash(data.paymentReference),
      "",
      "━━━━━━━━━━━━━━",
      "*ملاحظات إضافية*",
      "━━━━━━━━━━━━━━",
      valueOrDash(data.notes),
      "",
      "✅ تم إرسال الطلب من موقع أكاديمية الخطوة الأولى لكرة القدم."
    ].join("\n");
  }

  function initRegistrationForm() {
    const form =
      document.querySelector("#joinForm") ||
      document.querySelector("#bookingForm") ||
      document.querySelector("#join form") ||
      document.querySelector("form");

    if (!form) return;

    form.addEventListener("submit", function (event) {
      event.preventDefault();

      const data = buildRegistrationData(form);

      if (!data.playerName || !data.guardianName || !data.phoneNumber) {
        alert("من فضلك املأ اسم اللاعب واسم ولي الأمر ورقم الهاتف.");
        return;
      }

      const message = buildWhatsAppMessage(data);

      const url =
        "https://wa.me/" +
        WHATSAPP_NUMBER +
        "?text=" +
        encodeURIComponent(message);

      window.open(url, "_blank", "noopener,noreferrer");
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initNavigation();
    initRegistrationForm();
  });
})();