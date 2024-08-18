function ResponseModal(content) {
    // Create the modal div
    const modal = document.createElement('div');
    modal.style.position = 'fixed';
    modal.style.top = '50%';
    modal.style.left = '50%';
    modal.style.transform = 'translate(-50%, -50%)';
    modal.style.zIndex = '1000';
    modal.style.backgroundColor = 'white';
    modal.style.padding = '20px';
    modal.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.1)';
    modal.style.borderRadius = '8px';
    modal.style.maxWidth = '80%';
    modal.style.maxHeight = '80%';
    modal.style.overflowY = 'auto';

    // Create the content div
    const contentDiv = document.createElement('div');
    contentDiv.innerHTML = content;
    modal.appendChild(contentDiv);

    // Create the dismiss button
    const dismissButton = document.createElement('button');
    dismissButton.textContent = 'Dismiss';
    dismissButton.style.marginTop = '20px';
    dismissButton.style.padding = '10px 20px';
    dismissButton.style.backgroundColor = '#007BFF';
    dismissButton.style.color = 'white';
    dismissButton.style.border = 'none';
    dismissButton.style.borderRadius = '4px';
    dismissButton.style.cursor = 'pointer';

    // Dismiss the modal on button click
    dismissButton.addEventListener('click', function() {
        document.body.removeChild(modal);
    });

    modal.appendChild(dismissButton);

    // Append the modal to the body
    document.body.appendChild(modal);
}
function ResponseModalSetupFormSubmitListener(addedNodes) {
    addedNodes.forEach(node => {
        if (node.tagName === "FORM") {
            node.addEventListener("submit", event => {
                event.preventDefault();
                (async () => {
                    try {
                        const response = await fetch(node.action, {
                            method: "POST",
                            body: new FormData(node),
                        });
                        if (response.status >= 200 && response.status < 300) {
                            node.reset();
                        }
                        ResponseModal(await response.text());
                    } catch(error) {
                        ResponseModal(`An error occurred: ${error}`);
                    }
                })();
            });
        }
    });
}
function ResponseModalWatchForms() {
    const forms = document.querySelectorAll("form");
    ResponseModalSetupFormSubmitListener(forms);
    const observer = new MutationObserver(mutationsList => {
        mutationsList.forEach(mutation => {
            ResponseModalSetupFormSubmitListener(mutation.addedNodes);
        });
    });
    observer.observe(document.body, { childList: true, subtree: true });
}
const previousOnload = window.onload;
window.onload = () => {
    if (previousOnload) {
        previousOnload();
    }
    ResponseModalWatchForms();
};
