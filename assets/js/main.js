console.log("main.js loaded");
const testimonials = [
  {
    img: "./assets/image/israel.jpg",
    name: "Oyinlola Israel",
    location: "Lagos State",
    quote: "Havencrest Realty truly cares about its clients. They took the time to understand my needs and guided me toward finding the perfect home in Lagos. Their professionalism and attention to detail are truly unmatched."
  },
  {
    img: "./assets/image/fawaz.png",
    name: "Ayinde Fawaz",
    location: "Ogun State",
    quote: "I had an exceptional experience working with Havencrest Realty. Their expertise and personalized service exceeded my expectations and made the entire home-buying process smooth and stress-free."
  },
  {
    img: "./assets/image/hubert.png",
    name: "Adesanya Hubert",
    location: "Abuja",
    quote: "Havencrest Realty turned my dream of homeownership into reality. Their dedicated team guided me through every step and their professionalism made the entire experience seamless."
  },
  {
    img: "https://i.pravatar.cc/100?img=4",
    name: "Chidinma Okafor",
    location: "Rivers State",
    quote: "From our very first conversation, Havencrest understood exactly what I was looking for. They made what could have been a stressful process feel simple and genuinely enjoyable."
  },
  {
    img: "https://i.pravatar.cc/100?img=5",
    name: "Tunde Bakare",
    location: "Oyo State",
    quote: "What stood out most was how transparent the team was at every stage. No surprises, no pressure — just honest guidance that helped me make a confident decision."
  },
  {
    img: "https://i.pravatar.cc/100?img=6",
    name: "Amina Yusuf",
    location: "Kano State",
    quote: "Havencrest Realty went above and beyond to match me with a home that fit both my budget and my lifestyle. I recommend them to anyone serious about finding the right property."
  }
];

let currentGroup = 0;
const totalGroups = 2;

const testimonialCards = document.querySelectorAll(".testimonial-card");
const navButtons = document.querySelectorAll(".nav-arrow");

function renderTestimonials() {
  const start = currentGroup * 3;

  testimonialCards.forEach((card, i) => {
    const data = testimonials[start + i];

    card.querySelector(".testimonial-header img").src = data.img;
    card.querySelector(".testimonial-header img").alt = data.name;
    card.querySelector("h3").textContent = data.name;
    card.querySelector("h4").textContent = data.location;
    card.querySelector("p").textContent = data.quote;
  });
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

// MOBILE MENU

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

// CONTACT FORM

const contactForm = document.querySelector(".contact-form-inner");
const emailInput = document.querySelector("#email");
const formMessage = document.querySelector(".form-message");

if (contactForm && emailInput && formMessage) {

  function showMessage(text, type) {
    formMessage.textContent = text;
    formMessage.className = "form-message " + type;
    emailInput.classList.toggle("input-error", type === "error");
  }

  contactForm.addEventListener("submit", (event) => {
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

    showMessage("Thank you! We'll be in touch shortly.", "success");
    contactForm.reset();
  });

  emailInput.addEventListener("input", () => {
    formMessage.textContent = "";
    formMessage.className = "form-message";
    emailInput.classList.remove("input-error");
  });

}

// SCROLL REVEAL

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

revealTargets.forEach((element) => {
  element.classList.add("reveal");
  revealObserver.observe(element);
});

// PROPERTY FILTER

const filterButtons = document.querySelectorAll(".filter-btn");
const propertyCards = document.querySelectorAll(".all-property-grid .property-card");

if (filterButtons.length && propertyCards.length) {

  filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const filter = button.dataset.filter;

      filterButtons.forEach((btn) => btn.classList.remove("active"));
      button.classList.add("active");

      propertyCards.forEach((card) => {
        const shouldShow = filter === "all" || card.dataset.status === filter;
        card.classList.toggle("hidden", !shouldShow);
      });
    });
  });

}