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

    // 2. Character & Word Counter Sync
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

    // 3. Smooth Scroll to Result Card
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
        navigator.clipboard.writeText(textToCopy).then(() => {
            alert("Prediction result copied to clipboard!");
        }).catch(err => {
            console.error("Failed to copy text: ", err);
        });
    }
}
