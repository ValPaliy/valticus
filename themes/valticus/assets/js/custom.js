'use strict';

/* ========================================================================
   Modern Interactive Features for Enhanced UX
   ======================================================================== */

(function() {
  // Wait for DOM to be fully loaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  function init() {
    initSmoothScroll();
    initScrollAnimations();
    initReadingProgressBar();
    initImageLazyLoading();
    initEnhancedNavigation();
    initAnimatedElements();
  }

  /* ========================================================================
     Smooth Scroll for Anchor Links
     ======================================================================== */
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');

        // Ignore empty hash or hash-only links
        if (href === '#' || href === '#!') {
          return;
        }

        const target = document.querySelector(href);
        if (target) {
          e.preventDefault();

          const headerOffset = 80;
          const elementPosition = target.getBoundingClientRect().top;
          const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

          window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
          });
        }
      });
    });
  }

  /* ========================================================================
     Scroll Animations with Intersection Observer
     ======================================================================== */
  function initScrollAnimations() {
    // Check if Intersection Observer is supported
    if (!('IntersectionObserver' in window)) {
      return;
    }

    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('fade-in');
          // Optionally unobserve after animation
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);

    // Observe elements that should animate on scroll
    const animatedElements = document.querySelectorAll('.list__item, .widget, .post__content > *, .authorbox');
    animatedElements.forEach(el => {
      el.style.opacity = '0';
      observer.observe(el);
    });
  }

  /* ========================================================================
     Reading Progress Bar for Blog Posts
     ======================================================================== */
  function initReadingProgressBar() {
    // Only show on single post pages
    const postContent = document.querySelector('.post__content');
    if (!postContent) {
      return;
    }

    // Create progress bar element
    const progressBar = document.createElement('div');
    progressBar.className = 'reading-progress';
    progressBar.innerHTML = '<div class="reading-progress__bar"></div>';
    document.body.appendChild(progressBar);

    // Add styles
    const style = document.createElement('style');
    style.textContent = `
      .reading-progress {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: rgba(0, 0, 0, 0.1);
        z-index: 1000;
        pointer-events: none;
      }
      .reading-progress__bar {
        height: 100%;
        background: linear-gradient(135deg, #0066FF 0%, #7C3AED 100%);
        width: 0%;
        transition: width 150ms ease-out;
        box-shadow: 0 0 10px rgba(0, 102, 255, 0.5);
      }
    `;
    document.head.appendChild(style);

    // Update progress on scroll
    const progressBarInner = progressBar.querySelector('.reading-progress__bar');

    function updateProgress() {
      const windowHeight = window.innerHeight;
      const documentHeight = document.documentElement.scrollHeight - windowHeight;
      const scrolled = window.pageYOffset;
      const progress = (scrolled / documentHeight) * 100;

      progressBarInner.style.width = Math.min(progress, 100) + '%';
    }

    window.addEventListener('scroll', updateProgress, { passive: true });
    updateProgress();
  }

  /* ========================================================================
     Enhanced Navigation with Scroll Effect
     ======================================================================== */
  function initEnhancedNavigation() {
    const header = document.querySelector('.header');
    if (!header) {
      return;
    }

    let lastScroll = 0;
    const scrollThreshold = 100;

    function handleScroll() {
      const currentScroll = window.pageYOffset;

      if (currentScroll > scrollThreshold) {
        header.classList.add('header--scrolled');
      } else {
        header.classList.remove('header--scrolled');
      }

      lastScroll = currentScroll;
    }

    // Add styles for scrolled header
    const style = document.createElement('style');
    style.textContent = `
      .header {
        transition: all 0.3s ease;
      }
      .header--scrolled {
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
      }
      .header--scrolled .logo {
        padding: 15px 25px;
        transition: padding 0.3s ease;
      }
    `;
    document.head.appendChild(style);

    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
  }

  /* ========================================================================
     Image Lazy Loading Enhancement
     ======================================================================== */
  function initImageLazyLoading() {
    // Modern browsers support native lazy loading
    const images = document.querySelectorAll('img[loading="lazy"]');

    // For browsers that don't support native lazy loading
    if ('loading' in HTMLImageElement.prototype) {
      return;
    }

    // Fallback using Intersection Observer
    if (!('IntersectionObserver' in window)) {
      return;
    }

    const imageObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          if (img.dataset.src) {
            img.src = img.dataset.src;
            img.removeAttribute('data-src');
          }
          imageObserver.unobserve(img);
        }
      });
    });

    images.forEach(img => imageObserver.observe(img));
  }

  /* ========================================================================
     Animated Elements on Load
     ======================================================================== */
  function initAnimatedElements() {
    // Add staggered animation to list items
    const listItems = document.querySelectorAll('.list__item');
    listItems.forEach((item, index) => {
      item.style.animationDelay = `${index * 0.1}s`;
    });

    // Add hover effect enhancements
    const cards = document.querySelectorAll('.list__item, .widget');
    cards.forEach(card => {
      card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-4px)';
      });

      card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
      });
    });

    // Add ripple effect to buttons
    const buttons = document.querySelectorAll('.btn, .pagination__item, .tags__item');
    buttons.forEach(button => {
      button.addEventListener('click', function(e) {
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;

        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');

        this.appendChild(ripple);

        setTimeout(() => {
          ripple.remove();
        }, 600);
      });
    });

    // Add ripple styles
    const style = document.createElement('style');
    style.textContent = `
      .btn, .pagination__item, .tags__item {
        position: relative;
        overflow: hidden;
      }
      .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
      }
      @keyframes ripple-animation {
        to {
          transform: scale(4);
          opacity: 0;
        }
      }
    `;
    document.head.appendChild(style);
  }

  /* ========================================================================
     Performance: Debounce Helper
     ======================================================================== */
  function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  /* ========================================================================
     Console Message
     ======================================================================== */
  console.log(
    '%c✨ Valticus Enhanced ✨',
    'color: #0066FF; font-size: 20px; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);'
  );
  console.log(
    '%cModern design system loaded successfully!',
    'color: #7C3AED; font-size: 14px;'
  );

})();
