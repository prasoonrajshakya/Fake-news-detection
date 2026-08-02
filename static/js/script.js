/**
 * Fake News Detector - Client Side Interactivity Script
 * Lightweight & Dependency-Free
 */

document.addEventListener("DOMContentLoaded", () => {
  // 1. Auto-Focus Textarea on Load
  const textarea = document.querySelector("textarea");
  if (textarea) {
    textarea.focus();
  }

  // 2. Lock the selectbox input to read-only so users can only pick from the dropdown.
  function lockSelectboxInput() {
    const targetDocument = window.top?.document || document;
    const selectbox = targetDocument.querySelector(
      'div[data-testid="stSelectbox"]',
    );
    const comboboxInput = selectbox?.querySelector('input[role="combobox"]');

    if (comboboxInput) {
      comboboxInput.readOnly = true;
      comboboxInput.setAttribute("readonly", "true");
      comboboxInput.setAttribute("aria-readonly", "true");
      comboboxInput.setAttribute("autocomplete", "off");
      comboboxInput.style.caretColor = "transparent";

      comboboxInput.onkeydown = (e) => {
        const blockedKeys = [
          "Backspace",
          "Delete",
          "ArrowLeft",
          "ArrowRight",
          "ArrowUp",
          "ArrowDown",
          "Home",
          "End",
          "Enter",
          " ",
          "Tab",
        ];

        if (blockedKeys.includes(e.key) || e.key.length === 1) {
          e.preventDefault();
        }
      };

      comboboxInput.onpaste = (e) => e.preventDefault();
      comboboxInput.oninput = (e) => e.preventDefault();
      comboboxInput.onfocus = () => {
        setTimeout(() => {
          if (document.activeElement === comboboxInput) {
            comboboxInput.blur();
          }
        }, 10);
      };
    }
  }

  lockSelectboxInput();
  setTimeout(lockSelectboxInput, 250);
  setTimeout(lockSelectboxInput, 600);

  // 3. Character & Word Counter Sync
  function updateCounter() {
    const targetTextarea = document.querySelector("textarea");
    const charCountEl = document.getElementById("js-char-count");
    const wordCountEl = document.getElementById("js-word-count");

    if (targetTextarea && (charCountEl || wordCountEl)) {
      const text = targetTextarea.value || "";
      const charLen = text.length;
      const wordLen = text.trim() ? text.trim().split(/\s+/).length : 0;

      if (charCountEl) charCountEl.innerText = `${charLen} chars`;
      if (wordCountEl) wordCountEl.innerText = `${wordLen} words`;
    }
  }

  // Attach listener to textarea
  document.addEventListener("input", (e) => {
    if (e.target && e.target.tagName === "TEXTAREA") {
      updateCounter();
    }
  });

  // 4. Smooth Scroll to Result Card
  const resultCard = document.querySelector(".result-card");
  if (resultCard) {
    resultCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  // Initial counter update
  updateCounter();
});

/**
 * Helper function to copy prediction result text to clipboard
 */
function copyResultText(textToCopy) {
  if (navigator.clipboard) {
    navigator.clipboard
      .writeText(textToCopy)
      .then(() => {
        alert("Prediction result copied to clipboard!");
      })
      .catch((err) => {
        console.error("Failed to copy text: ", err);
      });
  }
}
