function handleDropdowns() {
    const targetSections = document.querySelectorAll('section[id*="lemur"], section[id*="streaming"]');
    console.log(targetSections.length);
    // call disableButton() on buttons that are descendants of .fern-endpoint-url elements within the target sections
    targetSections.forEach(section => {
        const fernEndpointElements = section.querySelectorAll('.fern-endpoint-url');
        fernEndpointElements.forEach(element => {
            const buttons = element.querySelectorAll('button.fern-button');
            buttons.forEach(button => {
                // Remove all existing click event listeners
                const newButton = button.cloneNode(true);
                button.parentNode.replaceChild(newButton, button);

                // Add capturing phase event listener to block all clicks
                newButton.addEventListener('click', (e) => {
                    e.preventDefault();
                    return false;
                }, true);
            });
        });
    });
}

// Listen for URL changes, even when the app doesn't reload the full page
function watchForUrlChanges() {
    let lastUrl = window.location.href;

    // Set an interval to check for URL changes every 500ms
    setInterval(() => {
        const currentUrl = window.location.href;

        if (currentUrl !== lastUrl) {
            lastUrl = currentUrl;
            handleDropdowns();
        }
    }, 500);
}

// run logic when page initially loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        handleDropdowns();
        watchForUrlChanges();
    });
} else {
    handleDropdowns();
    watchForUrlChanges();
}