document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".card");
  cards.forEach((card, index) => {
    setTimeout(() => card.classList.add("card-visible"), index * 100);
  });

  const scrollBtn = document.getElementById("scrollTopBtn");
  if (!scrollBtn) return;

  const toggleScrollBtn = () => {
    if (window.pageYOffset > 200) {
      scrollBtn.classList.add("show");
    } else {
      scrollBtn.classList.remove("show");
    }
  };

  window.addEventListener("scroll", toggleScrollBtn);
  toggleScrollBtn();

  scrollBtn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
});
