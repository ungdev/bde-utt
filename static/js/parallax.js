(() => {
    const container = document.querySelector('.parallax-background');

    if (!container) {
        return;
    }

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        return;
    }

    const logoElements = Array.from(container.querySelectorAll('.parallax-logo'));

    if (logoElements.length === 0) {
        return;
    }

    const logos = logoElements.map((element, index) => {
        const size = Number(element.dataset.size || 90);

        element.style.width = `${size}px`;

        return {
            element,
            size,
            x: Number(element.dataset.x || 0),
            y: Number(element.dataset.y || 0),
            speed: Number(element.dataset.speed || 1),
            depth: Number(element.dataset.depth || 0.02),
            direction: element.dataset.direction === 'up' ? -1 : 1,
            drift: Number(element.dataset.drift || 16),
            phase: index * 1.37,
        };
    });

    let viewportWidth = window.innerWidth;
    let viewportHeight = window.innerHeight;
    let scrollY = window.scrollY;

    const updateViewport = () => {
        viewportWidth = window.innerWidth;
        viewportHeight = window.innerHeight;
    };

    window.addEventListener('resize', updateViewport);
    window.addEventListener('scroll', () => {
        scrollY = window.scrollY;
    }, { passive: true });

    const animate = (timeMs) => {
        const time = timeMs / 1000;

        for (const logo of logos) {
            const travelHeight = viewportHeight + logo.size * 2;
            const yOffset = (logo.y / 100) * travelHeight;
            const flow = (yOffset + time * logo.speed * 65 + scrollY * logo.depth * logo.speed) % travelHeight;
            const y = logo.direction > 0
                ? flow - logo.size
                : viewportHeight - flow - logo.size;

            const xBase = (logo.x / 100) * viewportWidth;
            const xDrift = Math.sin(time * logo.speed + logo.phase) * logo.drift;
            const rotate = Math.sin(time * (logo.speed * 0.6) + logo.phase) * 7;

            logo.element.style.transform = `translate3d(${xBase + xDrift}px, ${y}px, 0) rotate(${rotate}deg)`;
        }

        window.requestAnimationFrame(animate);
    };

    window.requestAnimationFrame(animate);
})();
