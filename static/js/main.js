/* ==========================================================================
   NEXCART — INTERACTIVE FRONTEND JAVASCRIPT ENGINE
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initSearchAutocomplete();
  initCountdownTimer();
  initMobileMenu();
});

/* 1. Theme Engine (Light / Dark Mode) */
function initTheme() {
  const savedTheme = localStorage.getItem('nexcart_theme') || 'light';
  document.documentElement.setAttribute('data-theme', savedTheme);
  updateThemeIcon(savedTheme);
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', current);
  localStorage.setItem('nexcart_theme', current);
  updateThemeIcon(current);
  showToast(`Switched to ${current} mode`, 'info');
}

function updateThemeIcon(theme) {
  const btn = document.getElementById('theme-toggle-btn');
  if (btn) {
    btn.innerHTML = theme === 'dark' ? '☀️' : '🌙';
  }
}

/* 2. Toast Notification Engine */
function showToast(message, type = 'success') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <div style="display:flex; align-items:center; gap:0.6rem;">
      <span style="font-weight:800; font-size:1.1rem;">${type === 'success' ? '✓' : type === 'error' ? '✕' : 'ℹ'}</span>
      <span style="font-size:0.9rem; font-weight:600;">${message}</span>
    </div>
    <button onclick="this.parentElement.remove()" style="background:none; border:none; color:inherit; cursor:pointer; font-size:1.2rem; line-height:1;">&times;</button>
  `;

  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(20px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

/* 3. CSRF Helper Token */
function getCsrfToken() {
  const cookieValue = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];
  return cookieValue || '';
}

/* 4. AJAX Add to Cart */
function addToCart(productId, quantity = 1) {
  fetch('/cart/api/add/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCsrfToken()
    },
    body: JSON.stringify({ product_id: productId, quantity: quantity })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      showToast(data.message, 'success');
      const badge = document.getElementById('cart-badge-count');
      if (badge) badge.innerText = data.cart_count;
    } else {
      showToast(data.message || 'Error adding item to cart', 'error');
    }
  })
  .catch(() => showToast('Network connection error', 'error'));
}

/* 5. AJAX Wishlist Toggle */
function toggleWishlist(productId, btnElement) {
  fetch('/wishlist/api/toggle/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCsrfToken()
    },
    body: JSON.stringify({ product_id: productId })
  })
  .then(res => {
    if (res.status === 401) {
      window.location.href = '/accounts/login/?next=' + window.location.pathname;
      return;
    }
    return res.json();
  })
  .then(data => {
    if (data && data.success) {
      showToast(data.message, 'success');
      const badge = document.getElementById('wishlist-badge-count');
      if (badge) badge.innerText = data.wishlist_count;
      if (btnElement) {
        btnElement.style.color = data.added ? '#EF4444' : 'inherit';
      }
    }
  })
  .catch(() => showToast('Error processing request', 'error'));
}

/* 6. Quick View Lightbox Modal */
function openQuickView(productId) {
  fetch(`/products/api/quick-view/${productId}/`)
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        const p = data.product;
        const modal = document.getElementById('quickview-modal');
        if (modal) {
          document.getElementById('qv-title').innerText = p.title;
          document.getElementById('qv-category').innerText = p.category;
          document.getElementById('qv-price').innerText = `$${p.price}`;
          document.getElementById('qv-desc').innerText = p.description;
          document.getElementById('qv-image').src = p.image;
          document.getElementById('qv-add-btn').setAttribute('onclick', `addToCart(${p.id}, 1); closeQuickView();`);
          document.getElementById('qv-detail-link').href = `/products/${p.slug}/`;

          modal.classList.add('active');
        }
      }
    });
}

function closeQuickView() {
  const modal = document.getElementById('quickview-modal');
  if (modal) modal.classList.remove('active');
}

/* 7. Search Autocomplete Engine */
function initSearchAutocomplete() {
  const input = document.getElementById('global-search-input');
  const dropdown = document.getElementById('search-suggestions-box');

  if (!input || !dropdown) return;

  let timeout = null;
  input.addEventListener('input', (e) => {
    clearTimeout(timeout);
    const query = e.target.value.trim();

    if (query.length < 2) {
      dropdown.classList.remove('active');
      return;
    }

    timeout = setTimeout(() => {
      fetch(`/products/api/search-suggest/?q=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(data => {
          if (data.results && data.results.length > 0) {
            dropdown.innerHTML = data.results.map(item => `
              <a href="/products/${item.slug}/" class="suggestion-item">
                <img src="${item.image}" style="width:38px; height:38px; border-radius:6px; object-fit:cover;">
                <div>
                  <div style="font-weight:700; font-size:0.85rem; color:var(--text-primary);">${item.title}</div>
                  <div style="color:var(--primary); font-size:0.8rem; font-weight:800;">$${item.price}</div>
                </div>
              </a>
            `).join('');
            dropdown.classList.add('active');
          } else {
            dropdown.classList.remove('active');
          }
        });
    }, 250);
  });

  document.addEventListener('click', (e) => {
    if (!input.contains(e.target) && !dropdown.contains(e.target)) {
      dropdown.classList.remove('active');
    }
  });
}

/* 8. Flash Sale Countdown Timer */
function initCountdownTimer() {
  const hoursEl = document.getElementById('cd-hours');
  const minsEl = document.getElementById('cd-mins');
  const secsEl = document.getElementById('cd-secs');

  if (!hoursEl || !minsEl || !secsEl) return;

  let totalSeconds = 14 * 3600 + 32 * 60 + 45;

  setInterval(() => {
    if (totalSeconds <= 0) return;
    totalSeconds--;

    const h = Math.floor(totalSeconds / 3600);
    const m = Math.floor((totalSeconds % 3600) / 60);
    const s = totalSeconds % 60;

    hoursEl.innerText = String(h).padStart(2, '0');
    minsEl.innerText = String(m).padStart(2, '0');
    secsEl.innerText = String(s).padStart(2, '0');
  }, 1000);
}

/* 9. Mobile Menu Toggle */
function initMobileMenu() {
  const toggleBtn = document.getElementById('mobile-menu-toggle-btn');
  const menuBar = document.getElementById('mobile-nav-drawer');

  if (toggleBtn && menuBar) {
    toggleBtn.addEventListener('click', () => {
      menuBar.classList.toggle('active');
    });
  }
}
