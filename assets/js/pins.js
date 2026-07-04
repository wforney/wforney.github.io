(() => {
  const dialog = document.getElementById("pin-dialog");
  if (!dialog) {
    return;
  }

  const image = document.getElementById("pin-dialog-image");
  const title = document.getElementById("pin-dialog-title");
  const excerpt = document.getElementById("pin-dialog-excerpt");
  const category = document.getElementById("pin-dialog-category");
  const source = document.getElementById("pin-dialog-source");
  const closeButton = dialog.querySelector("[data-pin-close]");

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

    dialog.showModal();
  };

  closeButton.addEventListener("click", () => dialog.close());
  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) {
      dialog.close();
    }
  });
  dialog.addEventListener("close", reset);
})();
