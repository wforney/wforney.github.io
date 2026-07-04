(() => {
  const modal = document.getElementById("pin-modal");
  if (!modal) {
    return;
  }

  const image = document.getElementById("pin-modal-image");
  const title = document.getElementById("pin-modal-title");
  const excerpt = document.getElementById("pin-modal-excerpt");
  const category = document.getElementById("pin-modal-category");
  const source = document.getElementById("pin-modal-source");
  const closeButton = modal.querySelector("[data-pin-close]");

  const reset = () => {
    image.removeAttribute("src");
    image.alt = "";
    title.textContent = "";
    excerpt.textContent = "";
    category.textContent = "";
    source.removeAttribute("href");
    source.textContent = "";
    source.hidden = true;
  };

  window.openPin = (trigger) => {
    image.src = trigger.dataset.pinImage || "";
    image.alt = trigger.dataset.pinTitle || "";
    title.textContent = trigger.dataset.pinTitle || "";
    excerpt.textContent = trigger.dataset.pinExcerpt || "";
    category.textContent = trigger.dataset.pinCategory || "";

    const sourceUrl = trigger.dataset.pinSourceUrl || "";
    const sourceText = trigger.dataset.pinSourceText || "";

    if (sourceUrl) {
      source.href = sourceUrl;
      source.textContent = sourceText || sourceUrl;
      source.hidden = false;
    } else {
      source.hidden = true;
    }

    modal.hidden = false;
    modal.setAttribute("aria-hidden", "false");
    document.body.classList.add("pin-modal-open");
  };

  const closeModal = () => {
    modal.hidden = true;
    modal.setAttribute("aria-hidden", "true");
    document.body.classList.remove("pin-modal-open");
    reset();
  };

  closeButton.addEventListener("click", closeModal);
  modal.addEventListener("click", (event) => {
    if (event.target === modal) {
      closeModal();
    }
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !modal.hidden) {
      closeModal();
    }
  });
})();
