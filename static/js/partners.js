document.addEventListener('DOMContentLoaded', () => {
    const partnerCards = document.getElementsByClassName('partner-card');
    const partnerInfosCardContainer = document.getElementById('partner-infos-container');
    const partnerInfosTitle = document.getElementById('partner-name');
    const partnerInfosDescription = document.getElementById('partner-description');
    const partnerInfosIcon = document.getElementById('partner-logo');
    const partnerInfosLink = document.getElementById('partner-url');
    const partnerInfosCloseBtn = document.getElementById('partner-infos-close-btn');

    const partnersData = window.partners;

    Array.from(partnerCards).forEach(card => {
        card.addEventListener('click', () => {
            const partnerId = Number(card.id.split('_')[1]) - 1;
            const partnerData = partnersData[partnerId];

            partnerInfosTitle.textContent = partnerData.name;
            partnerInfosDescription.textContent = partnerData.description;
            partnerInfosIcon.src = partnerData.icon_url;

            if (partnerData.url) {
                partnerInfosLink.href = partnerData.url;
                partnerInfosLink.attributeStyleMap.delete('display');
            } else {
                partnerInfosLink.attributeStyleMap.set('display', 'none');
            }

            partnerInfosCardContainer.classList.remove('d-none');
            partnerInfosCardContainer.classList.add('d-flex');
        });
    });

    partnerInfosCloseBtn.addEventListener('click', () => {
        partnerInfosCardContainer.classList.remove('d-flex');
        partnerInfosCardContainer.classList.add('d-none');
    });
});