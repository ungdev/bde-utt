document.addEventListener('DOMContentLoaded', () => {
    const localAccountLink = document.getElementById('local-account-link');
    const localAccountCard = document.getElementById('local-account-card');
    const localAccountUsernameInput = document.getElementById('id_username');

    localAccountLink.addEventListener('click', () => {
        localAccountCard.classList.remove('d-none');
        localAccountLink.remove();
        localAccountUsernameInput.focus();
    });
});