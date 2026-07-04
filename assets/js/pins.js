(() => {
  const getModal = () => document.getElementById("pin-modal");
  const getModalFields = () => ({
    image: document.getElementById("pin-modal-image"),
    title: document.getElementById("pin-modal-title"),
    excerpt: document.getElementById("pin-modal-excerpt"),
    category: document.getElementById("pin-modal-category"),
    source: document.getElementById("pin-modal-source"),
    closeButton: document.querySelector("#pin-modal [data-pin-close]"),
  });

  const reset = () => {
    const { image, title, excerpt, category, source } = getModalFields();
    if (!image || !title || !excerpt || !category || !source) {
      return;
    }

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
    const modal = getModal();
    const { image, title, excerpt, category, source } = getModalFields();
    if (!modal || !image || !title || !excerpt || !category || !source) {
      return;
    }

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
    const modal = getModal();
    if (!modal) {
      return;
    }

    modal.hidden = true;
    modal.setAttribute("aria-hidden", "true");
    document.body.classList.remove("pin-modal-open");
    reset();
  };

  const { closeButton } = getModalFields();
  if (closeButton) {
    closeButton.addEventListener("click", closeModal);
  }

  const modal = getModal();
  if (!modal) {
    return;
  }

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
