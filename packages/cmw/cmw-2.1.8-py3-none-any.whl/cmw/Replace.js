function ReplaceJsSetupFormSubmitListener(addedNodes) {
    addedNodes.forEach(node => {
        if (node.tagName === "FORM" && node.hasAttribute("data-replace")) {
            node.addEventListener("submit", event => {
                event.preventDefault();
                (async () => {
                    const response = await fetch(node.action, {
                        method: "POST",
                        body: new FormData(node),
                    });
                    node.outerHTML = await response.text();
                })();
            });
        }
    });
}
function ReplaceJsWatchForms() {
    const forms = document.querySelectorAll("form[data-replace]");
    setupFormSubmitListener(forms);
    const observer = new MutationObserver(mutationsList => {
        mutationsList.forEach(mutation => {
            ReplaceJsSetupFormSubmitListener(mutation.addedNodes);
        });
    });
    observer.observe(document.body, { childList: true, subtree: true });
}
const previousOnload = window.onload;
window.onload = () => {
    if (previousOnload) {
        previousOnload();
    }
    ReplaceJsWatchForms();
};
