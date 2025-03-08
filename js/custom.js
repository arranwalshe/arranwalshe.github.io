document.addEventListener('DOMContentLoaded', function() {
    // Get all links in the home header
    const homeLinks = document.querySelectorAll('.home-header a');
    
    homeLinks.forEach(link => {
        const href = link.getAttribute('href');
        // Open in new tab if it's Instagram or CV
        if (href.includes('instagram.com') || href.includes('/docs/cv.pdf')) {
            link.setAttribute('target', '_blank');
            link.setAttribute('rel', 'noopener noreferrer');
        }
    });
}); 