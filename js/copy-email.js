/**
 * Copy obfuscated email addresses to the clipboard.
 */
(function () {
    const FEEDBACK_MS = 1800;

    function showCopied(button) {
        const icon = button.querySelector('i');
        if (!icon) {
            return;
        }

        icon.classList.remove('fa-copy');
        icon.classList.add('fa-check');
        button.classList.add('is-copied');
        button.setAttribute('aria-label', 'Email copied');

        window.setTimeout(() => {
            icon.classList.remove('fa-check');
            icon.classList.add('fa-copy');
            button.classList.remove('is-copied');
            button.setAttribute('aria-label', 'Copy email address');
        }, FEEDBACK_MS);
    }

    async function copyEmail(email, button) {
        try {
            if (navigator.clipboard && window.isSecureContext) {
                await navigator.clipboard.writeText(email);
            } else {
                const helper = document.createElement('textarea');
                helper.value = email;
                helper.setAttribute('readonly', '');
                helper.style.position = 'absolute';
                helper.style.left = '-9999px';
                document.body.appendChild(helper);
                helper.select();
                document.execCommand('copy');
                document.body.removeChild(helper);
            }

            showCopied(button);
        } catch (error) {
            console.error('Failed to copy email:', error);
        }
    }

    document.addEventListener('click', (event) => {
        const button = event.target.closest('.copy-email-btn');
        if (!button) {
            return;
        }

        event.preventDefault();
        event.stopPropagation();

        const email = button.dataset.email;
        if (!email) {
            return;
        }

        copyEmail(email, button);
    });
})();
