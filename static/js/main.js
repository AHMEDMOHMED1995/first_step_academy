document.addEventListener("DOMContentLoaded", function () {
  const menuToggle = document.querySelector(".menu-toggle");
  const navMenu = document.querySelector(".nav-menu");
  const header = document.querySelector(".site-header");

  const pageIds = [
    "home",
    "about",
    "programs",
    "coach",
    "identity",
    "join",
    "contact"
  ];

  function getPageSections() {
    return pageIds
      .map(function (id) {
        return document.getElementById(id);
      })
      .filter(function (section) {
        return section !== null;
      });
  }

  function forceShow(section) {
    section.classList.remove("hidden-page");
    section.classList.add("active-page");
    section.style.display = "block";
    section.style.visibility = "visible";
    section.style.opacity = "1";
  }

  function forceHide(section) {
    section.classList.add("hidden-page");
    section.classList.remove("active-page");
    section.style.display = "none";
  }

  function setActiveLink(pageId) {
    document.querySelectorAll(".nav-menu a").forEach(function (link) {
      const href = link.getAttribute("href");

      if (href === "#" + pageId) {
        link.classList.add("active-link");
      } else {
        link.classList.remove("active-link");
      }
    });
  }

  function hideUnlinkedSections() {
    document.querySelectorAll("main > section").forEach(function (section) {
      const sectionId = section.getAttribute("id");

      if (!sectionId || !pageIds.includes(sectionId)) {
        section.style.display = "none";
        section.classList.add("hidden-page");
      }
    });
  }

  function showPage(pageId) {
    if (!pageIds.includes(pageId)) {
      pageId = "home";
    }

    const targetSection = document.getElementById(pageId);

    if (!targetSection) {
      pageId = "home";
    }

    getPageSections().forEach(function (section) {
      const id = section.getAttribute("id");

      if (id === pageId) {
        forceShow(section);
      } else {
        forceHide(section);
      }
    });

    hideUnlinkedSections();
    setActiveLink(pageId);

    if (navMenu) {
      navMenu.classList.remove("active");
    }

    window.scrollTo(0, 0);
  }

  document.querySelectorAll('a[href^="#"]').forEach(function (link) {
    link.addEventListener("click", function (event) {
      const href = link.getAttribute("href");

      if (!href || href === "#") {
        return;
      }

      const pageId = href.replace("#", "");

      if (pageIds.includes(pageId)) {
        event.preventDefault();
        history.pushState(null, "", "#" + pageId);
        showPage(pageId);
      }
    });
  });

  window.addEventListener("popstate", function () {
    const pageId = window.location.hash.replace("#", "") || "home";
    showPage(pageId);
  });

  if (menuToggle && navMenu) {
    menuToggle.addEventListener("click", function () {
      navMenu.classList.toggle("active");
    });
  }

  window.addEventListener("scroll", function () {
    if (!header) return;

    if (window.scrollY > 30) {
      header.classList.add("scrolled");
    } else {
      header.classList.remove("scrolled");
    }
  });

  function getValue(id) {
    const element = document.getElementById(id);
    return element ? element.value.trim() : "";
  }

  const joinForm = document.getElementById("joinForm");

  if (joinForm) {
    joinForm.addEventListener("submit", async function (event) {
      event.preventDefault();

      const data = {
        playerName: getValue("playerName"),
        playerAge: getValue("playerAge"),
        birthDate: getValue("birthDate"),
        playerPosition: getValue("playerPosition"),
        playerLevel: getValue("playerLevel"),
        preferredFoot: getValue("preferredFoot"),
        previousAcademy: getValue("previousAcademy"),
        healthNotes: getValue("healthNotes"),

        guardianName: getValue("guardianName"),
        relation: getValue("relation"),
        phoneNumber: getValue("phoneNumber"),
        whatsappNumber: getValue("whatsappNumber"),
        alternativePhone: getValue("alternativePhone"),
        area: getValue("area"),

        trainingGoal: getValue("trainingGoal"),
        preferredTime: getValue("preferredTime"),
        subscriptionType: getValue("subscriptionType"),
        paymentMethod: getValue("paymentMethod"),
        paymentStatus: getValue("paymentStatus"),
        paymentReference: getValue("paymentReference"),
        notes: getValue("notes")
      };

      try {
        const whatsappWindow = window.open("", "_blank");

        const response = await fetch("/submit-booking", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success && result.whatsapp_url) {
          alert("تم إنشاء طلب الحجز بنجاح\nرقم الطلب: " + result.request_number);

          if (whatsappWindow) {
            whatsappWindow.location.href = result.whatsapp_url;
          } else {
            window.open(result.whatsapp_url, "_blank");
          }

          joinForm.reset();
        } else {
          alert(result.message || "حدث خطأ أثناء إرسال الطلب.");

          if (whatsappWindow) {
            whatsappWindow.close();
          }
        }
      } catch (error) {
        alert("حدث خطأ في الاتصال بالسيرفر. تأكد أن السيرفر يعمل.");
        console.error(error);
      }
    });
  }

  const firstPage = window.location.hash.replace("#", "") || "home";
  showPage(firstPage);
});