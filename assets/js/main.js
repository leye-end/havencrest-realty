console.log("main.js loaded");

const API_BASE = "/api";

// ----------------- TESTIMONIALS -----------------

let testimonialsData = [];
let currentGroup = 0;
let totalGroups = 1;

const testimonialCards = document.querySelectorAll(".testimonial-card");
const navButtons = document.querySelectorAll(".nav-arrow");

function renderTestimonials() {
  if (!testimonialCards.length || !testimonialsData.length) return;
  const start = currentGroup * 3;

  testimonialCards.forEach((card, i) => {
    const data = testimonialsData[start + i];
    if (!data) {
      card.style.display = "none";
      return;
    }
    card.style.display = "";
    const imgEl = card.querySelector(".testimonial-header img");
    if (imgEl) {
      imgEl.src = data.image_url || data.img || "./assets/image/israel.jpg";
      imgEl.alt = data.name;
    }
    const h3 = card.querySelector("h3");
    if (h3) h3.textContent = data.name;
    const h4 = card.querySelector("h4");
    if (h4) h4.textContent = data.location;
    const p = card.querySelector("p");
    if (p) p.textContent = data.quote;
  });
}

async function loadTestimonials() {
  if (!testimonialCards.length) return;
  try {
    const res = await fetch(`${API_BASE}/testimonials`);
    if (res.ok) {
      const data = await res.json();
      if (Array.isArray(data) && data.length > 0) {
        testimonialsData = data;
        totalGroups = Math.max(1, Math.ceil(testimonialsData.length / 3));
        renderTestimonials();
      }
    }
  } catch (err) {
    console.warn("Could not fetch testimonials from API, falling back to static content.", err);
  }
}

navButtons.forEach((button, index) => {
  button.addEventListener("click", () => {
    if (index === 0) {
      currentGroup = (currentGroup - 1 + totalGroups) % totalGroups;
    } else {
      currentGroup = (currentGroup + 1) % totalGroups;
    }
    renderTestimonials();
  });
});

loadTestimonials();

// ----------------- MOBILE MENU -----------------

const menuToggle = document.querySelector(".menu-toggle");
const navContent = document.querySelector(".nav-content");

if (menuToggle && navContent) {
  menuToggle.addEventListener("click", () => {
    const isOpen = navContent.classList.toggle("open");
    menuToggle.setAttribute("aria-expanded", isOpen);
    menuToggle.querySelector("i").className = isOpen ? "bi bi-x-lg" : "bi bi-list";
  });

  navContent.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      navContent.classList.remove("open");
      menuToggle.querySelector("i").className = "bi bi-list";
    });
  });
}

// ----------------- CONTACT FORM & LEAD CAPTURE -----------------

const contactForm = document.querySelector(".contact-form-inner");
const emailInput = document.querySelector("#email");
const formMessage = document.querySelector(".form-message");

if (contactForm && emailInput && formMessage) {
  function showMessage(text, type) {
    formMessage.textContent = text;
    formMessage.className = "form-message " + type;
    emailInput.classList.toggle("input-error", type === "error");
  }

  contactForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = emailInput.value.trim();
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (email === "") {
      showMessage("Please enter your email address.", "error");
      return;
    }

    if (!emailPattern.test(email)) {
      showMessage("Please enter a valid email address.", "error");
      return;
    }

    showMessage("Submitting...", "info");

    try {
      const response = await fetch(`${API_BASE}/inquiries`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: email,
          inquiry_type: "newsletter"
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Unable to submit inquiry.");
      }

      showMessage("Thank you! We'll be in touch shortly.", "success");
      contactForm.reset();
    } catch (err) {
      showMessage(err.message || "Failed to submit. Please try again.", "error");
    }
  });

  emailInput.addEventListener("input", () => {
    formMessage.textContent = "";
    formMessage.className = "form-message";
    emailInput.classList.remove("input-error");
  });
}

// ----------------- DYNAMIC PROPERTY LOADER & FILTER -----------------

const propertyGrid = document.querySelector(".all-property-grid");
const filterButtons = document.querySelectorAll(".filter-btn");

function formatPrice(price, currency = "USD") {
  if (currency === "NGN") {
    return "₦" + Number(price).toLocaleString();
  }
  return "$" + Number(price).toLocaleString();
}

function buildPropertyCard(prop) {
  const card = document.createElement("div");
  card.className = "property-card";
  card.dataset.status = prop.status;

  const statusLabel = prop.status === "for-sale" ? "FOR SALE" : (prop.status === "for-rent" ? "FOR RENT" : "SOLD");
  const detailLink = prop.slug ? `property-1.html?slug=${encodeURIComponent(prop.slug)}` : "property-1.html";

  card.innerHTML = `
    <div class="property-image-wrapper">
      <img
        src="${prop.image_url || './assets/image/hero-house.png'}"
        alt="${prop.title}"
        class="property-img"
        onerror="this.src='./assets/image/hero-house.png'"
      >
      <span class="property-status">${statusLabel}</span>
    </div>
    <div class="property-info">
      <p class="property-location">${prop.city || 'Lagos, Nigeria'}</p>
      <h3>${prop.title}</h3>
      <div class="property-details">
        <span>${prop.bedrooms} Rooms</span>
        <span>${Number(prop.sqft).toLocaleString()} sq ft</span>
      </div>
      <div class="property-footer">
        <strong>${formatPrice(prop.price, prop.currency)}</strong>
        <a href="${detailLink}" class="property-arrow">
          <i class="bi bi-arrow-up-right"></i>
        </a>
      </div>
    </div>
  `;
  return card;
}

async function loadProperties(filter = "all") {
  if (!propertyGrid) return;

  try {
    const url = filter && filter !== "all" 
      ? `${API_BASE}/properties?status=${encodeURIComponent(filter)}`
      : `${API_BASE}/properties`;

    const res = await fetch(url);
    if (!res.ok) throw new Error("Failed to load properties");
    const properties = await res.json();

    if (Array.isArray(properties) && properties.length > 0) {
      propertyGrid.innerHTML = "";
      properties.forEach(prop => {
        propertyGrid.appendChild(buildPropertyCard(prop));
      });
      observeNewCards();
    }
  } catch (err) {
    console.warn("Could not load dynamic properties from backend:", err);
  }
}

if (filterButtons.length) {
  filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const filter = button.dataset.filter;
      filterButtons.forEach((btn) => btn.classList.remove("active"));
      button.classList.add("active");

      // Filter existing cards or query API
      const cards = propertyGrid ? propertyGrid.querySelectorAll(".property-card") : [];
      if (cards.length) {
        cards.forEach((card) => {
          const shouldShow = filter === "all" || card.dataset.status === filter;
          card.classList.toggle("hidden", !shouldShow);
        });
      }
    });
  });

  // Fetch initial properties from backend
  loadProperties();
}

// ----------------- SCROLL REVEAL -----------------

const revealTargets = document.querySelectorAll(`
  .second-page-image-wrapper,
  .second-page-info,
  .choose-us-intro,
  .cards-row,
  .section-heading,
  .property-grid,
  .testimonials-heading,
  .testimonial-grid,
  .testimonial-nav,
  .contact-content,
  .properties-heading,
  .all-property-grid,
  .services-heading,
  .services-grid,
  .services-trust-intro,
  .trust-grid,
  .process-heading,
  .process-grid,
  .services-cta-content,
  .property-overview,
  .property-description,
  .property-features-heading,
  .features-grid,
  .property-detail-cta-content
`);

const revealObserver = new IntersectionObserver(
  (entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.15 }
);

function observeNewCards() {
  if (propertyGrid) {
    propertyGrid.querySelectorAll(".property-card").forEach(el => {
      el.classList.add("reveal", "visible");
    });
  }
}

revealTargets.forEach((element) => {
  element.classList.add("reveal");
  revealObserver.observe(element);
});
