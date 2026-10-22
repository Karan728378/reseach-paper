/* =============================================================
   TechMart — Shared Application Core
   shared/app-core.js — Protocol v2

   Reads window.__VARIANT_CONFIG__.features to apply experimental
   features to dynamically rendered DOM elements.

   Exposes for verifier:
     window.__cart__           — live cart state array
     window.__orderConfirmed__ — boolean, set on successful checkout
     window.__lastOrder__      — order object, set on successful checkout
     window.__refreshCartView__— helper: call after external cart mutation (T5)

   SCIENTIFIC CONSTRAINT:
   Experimental features are applied ONLY when their flag is true.
   No feature is applied in the absence of its flag.
   All rendering paths exist in this file; variant HTML files do NOT
   add feature logic of their own.
   ============================================================= */

(function () {
  'use strict';

  /* ---- Variant config (set by each variant's index.html) ---- */
  var cfg = window.__VARIANT_CONFIG__ || { variant: 'unknown', features: {} };
  var F = cfg.features || {};
  /* F.jsonld        — true only in v1-jsonld   */
  /* F.aria          — true only in v2-aria      */
  /* F.dataAttrs     — true only in v3-data-attrs */
  /* F.evidenceMeta  — true only in v4-evidence-meta */

  var EVIDENCE_DATE = '2026-09-01T00:00:00Z'; /* Fixed anchor — Protocol v2 §2 V4 */

  /* ================================================================
     STATE
     ================================================================ */
  window.__cart__ = JSON.parse(localStorage.getItem('techmart_cart') || '[]');
  window.__orderConfirmed__ = false;
  window.__lastOrder__ = null;

  /* ================================================================
     CART OPERATIONS
     ================================================================ */
  function addToCart(sku) {
    var product = getProductBySKU(sku);
    if (!product || !product.inStock) return;
    var existing = window.__cart__.find(function (i) { return i.sku === sku; });
    if (existing) {
      existing.quantity += 1;
    } else {
      window.__cart__.push({ sku: sku, name: product.name, quantity: 1, price: product.price });
    }
    saveCart();
    updateCartCount();
    showToast('\u2713 Added to cart: ' + product.name);
  }

  function removeFromCart(sku) {
    window.__cart__ = window.__cart__.filter(function (i) { return i.sku !== sku; });
    saveCart();
    updateCartCount();
    renderCartItems();
  }

  function updateQuantity(sku, qty) {
    var item = window.__cart__.find(function (i) { return i.sku === sku; });
    if (item) {
      item.quantity = Math.max(1, parseInt(qty, 10) || 1);
      saveCart();
      renderCartItems();
    }
  }

  function saveCart() {
    localStorage.setItem('techmart_cart', JSON.stringify(window.__cart__));
  }

  function updateCartCount() {
    var count = window.__cart__.reduce(function (s, i) { return s + i.quantity; }, 0);
    var el = document.getElementById('cart-count');
    if (el) el.textContent = count;
  }

  /* Exposed for test setup (T5 pre-loading) */
  window.__refreshCartView__ = function () {
    updateCartCount();
    renderCartItems();
  };

  /* ================================================================
     TOAST NOTIFICATION
     ================================================================ */
  var toastTimer = null;
  function showToast(msg) {
    var el = document.getElementById('cart-notification');
    if (!el) return;
    el.textContent = msg;
    el.className = 'show';
    el.style.display = 'block';
    if (toastTimer) clearTimeout(toastTimer);
    toastTimer = setTimeout(function () {
      el.className = 'hide';
      setTimeout(function () { el.style.display = 'none'; el.className = ''; }, 300);
    }, 2200);
  }

  /* ================================================================
     JSON-LD INJECTION (V1 only)
     ================================================================ */
  function injectJsonLD(data, id) {
    var existing = document.getElementById(id || 'dynamic-jsonld');
    if (existing) existing.remove();
    var script = document.createElement('script');
    script.type = 'application/ld+json';
    script.id = id || 'dynamic-jsonld';
    script.textContent = JSON.stringify(data);
    document.head.appendChild(script);
  }

  function removeJsonLD() {
    var el = document.getElementById('dynamic-jsonld');
    if (el) el.remove();
  }

  /* ================================================================
     TIME ELEMENT HELPER (V4 only)
     ================================================================ */
  function makeTimeEl() {
    var t = document.createElement('time');
    t.className = 'temporal-meta';
    t.setAttribute('datetime', EVIDENCE_DATE);
    return t;
  }

  /* ================================================================
     PRODUCT CARD RENDERER
     Called by renderHomeView() and renderSearchResults()
     Applies variant features based on F flags.
     ================================================================ */
  function renderProductCard(product) {
    var card = document.createElement('div');
    card.className = 'product-card';
    card.id = 'product-card-' + product.sku; /* Infrastructure ID — all variants */

    /* V2 — ARIA */
    if (F.aria) {
      card.setAttribute('aria-label', product.name + ', $' + product.price.toFixed(2));
    }
    /* V3 — data-* */
    if (F.dataAttrs) {
      card.setAttribute('data-product-id', product.sku);
      card.setAttribute('data-category', product.categorySlug);
    }

    /* Product image */
    var imgDiv = document.createElement('div');
    imgDiv.className = 'product-image';
    imgDiv.style.setProperty('--card-color', product.color);
    var iconSpan = document.createElement('span');
    iconSpan.className = 'product-icon';
    iconSpan.textContent = product.icon;
    imgDiv.appendChild(iconSpan);
    card.appendChild(imgDiv);

    /* Info section */
    var infoDiv = document.createElement('div');
    infoDiv.className = 'product-info';

    var nameEl = document.createElement('h3');
    nameEl.className = 'product-name';
    if (F.dataAttrs) nameEl.setAttribute('data-field', 'product-name');
    nameEl.textContent = product.name;
    infoDiv.appendChild(nameEl);

    var catEl = document.createElement('span');
    catEl.className = 'product-category';
    catEl.textContent = product.categoryName;
    infoDiv.appendChild(catEl);

    /* Price */
    var priceWrap = document.createElement('div');
    priceWrap.className = 'price-wrap';
    var priceEl = document.createElement('span');
    priceEl.className = 'product-price';
    if (F.aria) priceEl.setAttribute('aria-label', 'Price: $' + product.price.toFixed(2));
    if (F.dataAttrs) {
      priceEl.setAttribute('data-field', 'price');
      priceEl.setAttribute('data-currency', 'USD');
      priceEl.setAttribute('data-amount', String(product.price));
    }
    priceEl.textContent = '$' + product.price.toFixed(2);
    priceWrap.appendChild(priceEl);
    if (F.evidenceMeta) priceWrap.appendChild(makeTimeEl());
    infoDiv.appendChild(priceWrap);

    /* Rating */
    var ratingWrap = document.createElement('div');
    ratingWrap.className = 'rating-wrap';
    var ratingEl = document.createElement('span');
    ratingEl.className = 'product-rating';
    if (F.aria) {
      ratingEl.setAttribute('role', 'img');
      ratingEl.setAttribute('aria-label', 'Rating: ' + product.rating + ' out of 5 stars');
    }
    if (F.dataAttrs) {
      ratingEl.setAttribute('data-field', 'rating');
      ratingEl.setAttribute('data-rating', String(product.rating));
      ratingEl.setAttribute('data-review-count', String(product.reviewCount));
    }
    ratingEl.textContent = '\u2605 ' + product.rating + ' (' + product.reviewCount + ' reviews)';
    ratingWrap.appendChild(ratingEl);
    if (F.evidenceMeta) ratingWrap.appendChild(makeTimeEl());
    infoDiv.appendChild(ratingWrap);

    /* Stock */
    var stockWrap = document.createElement('div');
    stockWrap.className = 'stock-wrap';
    var stockEl = document.createElement('span');
    stockEl.className = 'product-stock ' + (product.inStock ? 'in-stock' : 'out-of-stock');
    if (F.dataAttrs) {
      stockEl.setAttribute('data-field', 'stock-status');
      stockEl.setAttribute('data-in-stock', String(product.inStock));
    }
    stockEl.textContent = product.inStock ? 'In Stock' : 'Out of Stock';
    stockWrap.appendChild(stockEl);
    if (F.evidenceMeta) stockWrap.appendChild(makeTimeEl());
    infoDiv.appendChild(stockWrap);

    card.appendChild(infoDiv);

    /* Action buttons */
    var actionsDiv = document.createElement('div');
    actionsDiv.className = 'product-actions';

    var viewBtn = document.createElement('a');
    viewBtn.className = 'btn-view';
    viewBtn.href = '#product/' + product.sku;
    viewBtn.textContent = 'View Details';
    actionsDiv.appendChild(viewBtn);

    var addBtn = document.createElement('button');
    addBtn.className = 'btn-add-cart';
    if (F.aria) addBtn.setAttribute('aria-label', 'Add item to cart');
    if (F.dataAttrs) {
      addBtn.setAttribute('data-action', 'add-to-cart');
      addBtn.setAttribute('data-product-id', product.sku);
    }
    if (!product.inStock) {
      addBtn.disabled = true;
      addBtn.textContent = 'Out of Stock';
    } else {
      addBtn.textContent = 'Add to Cart';
    }
    addBtn.addEventListener('click', function () { addToCart(product.sku); });
    actionsDiv.appendChild(addBtn);

    card.appendChild(actionsDiv);
    return card;
  }

  /* ================================================================
     HOME VIEW
     ================================================================ */
  function renderHomeView() {
    var grid = document.getElementById('featured-products-grid');
    if (!grid) return;
    grid.innerHTML = '';
    var sorted = PRODUCTS.slice().sort(function (a, b) { return b.rating - a.rating; });
    sorted.forEach(function (p) { grid.appendChild(renderProductCard(p)); });

    /* V1: inject homepage WebSite JSON-LD */
    if (F.jsonld) {
      injectJsonLD({
        '@context': 'https://schema.org',
        '@type': 'WebSite',
        'name': 'TechMart',
        'url': window.location.origin + window.location.pathname,
        'potentialAction': {
          '@type': 'SearchAction',
          'target': window.location.href.split('#')[0] + '#search?q={search_term_string}',
          'query-input': 'required name=search_term_string'
        }
      }, 'dynamic-jsonld');
    } else {
      removeJsonLD();
    }
  }

  /* ================================================================
     SEARCH
     ================================================================ */
  function performSearch(query) {
    var results = searchProducts(query); /* from products.js — sorted by rating desc */
    renderSearchResults(query, results);
  }

  function renderSearchResults(query, results) {
    var heading = document.getElementById('search-results-heading');
    if (heading) {
      heading.textContent = results.length > 0
        ? results.length + ' result' + (results.length !== 1 ? 's' : '') + ' for \u201c' + query + '\u201d'
        : 'No results for \u201c' + query + '\u201d';
    }
    var grid = document.getElementById('search-results-grid');
    if (grid) {
      grid.innerHTML = '';
      results.forEach(function (p) { grid.appendChild(renderProductCard(p)); });
    }
    var noRes = document.getElementById('search-no-results');
    if (noRes) noRes.classList.toggle('hidden', results.length > 0);

    /* V1: inject ItemList JSON-LD for search results */
    if (F.jsonld && results.length > 0) {
      injectJsonLD({
        '@context': 'https://schema.org',
        '@type': 'ItemList',
        'name': 'Search results for: ' + query,
        'numberOfItems': results.length,
        'itemListElement': results.map(function (p, idx) {
          return {
            '@type': 'ListItem',
            'position': idx + 1,
            'item': {
              '@type': 'Product',
              'name': p.name,
              'sku': p.sku,
              'offers': { '@type': 'Offer', 'price': p.price, 'priceCurrency': 'USD' }
            }
          };
        })
      }, 'dynamic-jsonld');
    }
  }

  /* ================================================================
     PRODUCT DETAIL VIEW
     ================================================================ */
  function renderProductView(sku) {
    var product = getProductBySKU(sku);
    if (!product) { location.hash = '#home'; return; }

    /* V1: inject full Product JSON-LD */
    if (F.jsonld) {
      injectJsonLD({
        '@context': 'https://schema.org',
        '@type': 'Product',
        'name': product.name,
        'description': product.description,
        'sku': product.sku,
        'category': product.categoryName,
        'offers': {
          '@type': 'Offer',
          'price': product.price,
          'priceCurrency': 'USD',
          'availability': product.inStock
            ? 'https://schema.org/InStock'
            : 'https://schema.org/OutOfStock',
          'url': window.location.href
        },
        'aggregateRating': {
          '@type': 'AggregateRating',
          'ratingValue': product.rating,
          'reviewCount': product.reviewCount
        }
      }, 'dynamic-jsonld');
    }

    var container = document.getElementById('product-detail-container');
    if (!container) return;
    container.innerHTML = '';

    var wrap = document.createElement('div');
    wrap.className = 'product-detail-inner';
    wrap.id = 'product-detail-' + product.sku;

    /* Breadcrumb */
    var bc = document.createElement('nav');
    bc.className = 'breadcrumb';
    if (F.aria) bc.setAttribute('aria-label', 'Breadcrumb');
    bc.innerHTML = '<a href="#home">Home</a> \u203a <span>' + product.categoryName + '</span> \u203a <span>' + product.name + '</span>';
    wrap.appendChild(bc);

    /* Content grid */
    var content = document.createElement('div');
    content.className = 'product-detail-content';

    /* Image */
    var imgDiv = document.createElement('div');
    imgDiv.className = 'product-detail-image';
    imgDiv.style.setProperty('--card-color', product.color);
    var iconLg = document.createElement('span');
    iconLg.className = 'product-icon-lg';
    iconLg.textContent = product.icon;
    imgDiv.appendChild(iconLg);
    content.appendChild(imgDiv);

    /* Info */
    var info = document.createElement('div');
    info.className = 'product-detail-info';

    var nameEl = document.createElement('h1');
    nameEl.className = 'product-detail-name';
    if (F.dataAttrs) nameEl.setAttribute('data-field', 'product-name');
    nameEl.textContent = product.name;
    info.appendChild(nameEl);

    var catSpan = document.createElement('span');
    catSpan.className = 'product-detail-category';
    catSpan.textContent = product.categoryName;
    info.appendChild(catSpan);

    /* Price */
    var pwrap = document.createElement('div');
    pwrap.className = 'product-detail-price-wrap';
    var pEl = document.createElement('span');
    pEl.className = 'product-detail-price';
    if (F.aria) pEl.setAttribute('aria-label', 'Price: $' + product.price.toFixed(2));
    if (F.dataAttrs) {
      pEl.setAttribute('data-field', 'price');
      pEl.setAttribute('data-currency', 'USD');
      pEl.setAttribute('data-amount', String(product.price));
    }
    pEl.textContent = '$' + product.price.toFixed(2);
    pwrap.appendChild(pEl);
    if (F.evidenceMeta) pwrap.appendChild(makeTimeEl());
    info.appendChild(pwrap);

    /* Rating */
    var rEl = document.createElement('div');
    rEl.className = 'product-detail-rating';
    if (F.aria) {
      rEl.setAttribute('role', 'img');
      rEl.setAttribute('aria-label', 'Rating: ' + product.rating + ' out of 5 stars, ' + product.reviewCount + ' reviews');
    }
    if (F.dataAttrs) {
      rEl.setAttribute('data-field', 'rating');
      rEl.setAttribute('data-rating', String(product.rating));
      rEl.setAttribute('data-review-count', String(product.reviewCount));
    }
    rEl.innerHTML = '<span class="stars">\u2605 ' + product.rating + '</span><span class="review-count">(' + product.reviewCount + ' reviews)</span>';
    if (F.evidenceMeta) rEl.appendChild(makeTimeEl());
    info.appendChild(rEl);

    /* Stock */
    var sEl = document.createElement('div');
    sEl.className = 'product-detail-stock ' + (product.inStock ? 'in-stock' : 'out-of-stock');
    if (F.dataAttrs) {
      sEl.setAttribute('data-field', 'stock-status');
      sEl.setAttribute('data-in-stock', String(product.inStock));
    }
    sEl.textContent = product.inStock ? 'In Stock' : 'Out of Stock';
    if (F.evidenceMeta) sEl.appendChild(makeTimeEl());
    info.appendChild(sEl);

    /* Description */
    var dEl = document.createElement('p');
    dEl.className = 'product-detail-description';
    if (F.dataAttrs) dEl.setAttribute('data-field', 'description');
    dEl.textContent = product.description;
    info.appendChild(dEl);

    /* Add to cart */
    var addBtn = document.createElement('button');
    addBtn.className = 'btn-add-cart btn-full';
    if (F.aria) addBtn.setAttribute('aria-label', 'Add item to cart');
    if (F.dataAttrs) {
      addBtn.setAttribute('data-action', 'add-to-cart');
      addBtn.setAttribute('data-product-id', product.sku);
    }
    if (!product.inStock) {
      addBtn.disabled = true;
      addBtn.textContent = 'Out of Stock';
    } else {
      addBtn.textContent = 'Add to Cart';
    }
    addBtn.addEventListener('click', function () { addToCart(product.sku); });
    info.appendChild(addBtn);

    content.appendChild(info);
    wrap.appendChild(content);
    container.appendChild(wrap);
  }

  /* ================================================================
     CART VIEW
     ================================================================ */
  function renderCartItems() {
    var list = document.getElementById('cart-items-list');
    var emptyState = document.getElementById('cart-empty-state');
    var summary = document.getElementById('cart-summary');
    var totalEl = document.getElementById('cart-total-amount');
    if (!list) return;

    list.innerHTML = '';

    if (window.__cart__.length === 0) {
      emptyState && emptyState.classList.remove('hidden');
      summary && summary.classList.add('hidden');
    } else {
      emptyState && emptyState.classList.add('hidden');
      summary && summary.classList.remove('hidden');

      window.__cart__.forEach(function (item) {
        var row = document.createElement('div');
        row.className = 'cart-item';
        row.id = 'cart-item-' + item.sku;

        if (F.aria) row.setAttribute('aria-label', item.name + ', quantity ' + item.quantity);
        if (F.dataAttrs) {
          row.setAttribute('data-product-id', item.sku);
          row.setAttribute('data-field', 'cart-item');
        }

        var nameEl = document.createElement('div');
        nameEl.className = 'cart-item-name';
        nameEl.textContent = item.name;
        row.appendChild(nameEl);

        var priceEl = document.createElement('div');
        priceEl.className = 'cart-item-price';
        if (F.dataAttrs) { priceEl.setAttribute('data-field', 'price'); priceEl.setAttribute('data-amount', String(item.price)); }
        priceEl.textContent = '$' + item.price.toFixed(2);
        row.appendChild(priceEl);

        var qtyIn = document.createElement('input');
        qtyIn.type = 'number';
        qtyIn.min = '1';
        qtyIn.value = item.quantity;
        qtyIn.className = 'qty-input';
        if (F.aria) qtyIn.setAttribute('aria-label', 'Item quantity');
        if (F.dataAttrs) { qtyIn.setAttribute('data-action', 'update-quantity'); qtyIn.setAttribute('data-product-id', item.sku); }
        qtyIn.addEventListener('change', (function (sku) { return function () { updateQuantity(sku, this.value); }; }(item.sku)));
        row.appendChild(qtyIn);

        var rmBtn = document.createElement('button');
        rmBtn.className = 'btn-remove-cart';
        if (F.aria) rmBtn.setAttribute('aria-label', 'Remove item from cart');
        if (F.dataAttrs) { rmBtn.setAttribute('data-action', 'remove-from-cart'); rmBtn.setAttribute('data-product-id', item.sku); }
        rmBtn.textContent = 'Remove';
        rmBtn.addEventListener('click', (function (sku) { return function () { removeFromCart(sku); }; }(item.sku)));
        row.appendChild(rmBtn);

        list.appendChild(row);
      });

      var total = window.__cart__.reduce(function (s, i) { return s + i.price * i.quantity; }, 0);
      if (totalEl) totalEl.textContent = '$' + total.toFixed(2);
    }
  }

  /* ================================================================
     CHECKOUT VIEW
     ================================================================ */
  function renderCheckoutSummary() {
    var container = document.getElementById('order-items-summary');
    var totalEl = document.getElementById('checkout-total-amount');
    if (!container) return;
    container.innerHTML = '';
    window.__cart__.forEach(function (item) {
      var line = document.createElement('div');
      line.className = 'order-summary-line';
      line.innerHTML = '<span>' + item.name + ' \u00d7' + item.quantity + '</span><span>$' + (item.price * item.quantity).toFixed(2) + '</span>';
      container.appendChild(line);
    });
    var total = window.__cart__.reduce(function (s, i) { return s + i.price * i.quantity; }, 0);
    if (totalEl) totalEl.textContent = '$' + total.toFixed(2);
  }

  /* ================================================================
     CONFIRMATION VIEW
     ================================================================ */
  function renderConfirmationView() {
    if (!window.__lastOrder__) return;
    var idEl = document.getElementById('order-id-display');
    var totEl = document.getElementById('order-total-display');
    if (idEl) idEl.textContent = window.__lastOrder__.orderId;
    if (totEl) totEl.textContent = '$' + window.__lastOrder__.total.toFixed(2);

    /* V4: add order timestamp as <time> element */
    if (F.evidenceMeta) {
      var confArea = document.getElementById('order-confirmation-area');
      if (confArea) {
        var existing = confArea.querySelector('time.temporal-meta');
        if (!existing) {
          var t = document.createElement('time');
          t.className = 'temporal-meta';
          t.setAttribute('datetime', window.__lastOrder__.timestamp);
          confArea.appendChild(t);
        }
      }
    }

    /* V1: inject Order JSON-LD */
    if (F.jsonld && window.__lastOrder__) {
      injectJsonLD({
        '@context': 'https://schema.org',
        '@type': 'Order',
        'orderNumber': window.__lastOrder__.orderId,
        'orderStatus': 'https://schema.org/OrderDelivered',
        'priceCurrency': 'USD',
        'price': window.__lastOrder__.total
      }, 'dynamic-jsonld');
    }
  }

  /* ================================================================
     NAVIGATION / ROUTER
     ================================================================ */
  var VIEWS = ['home', 'search', 'product', 'cart', 'checkout', 'confirmation'];

  function showView(name) {
    VIEWS.forEach(function (v) {
      var el = document.getElementById('view-' + v);
      if (el) el.classList.toggle('active', v === name);
    });
    /* V3: update body data-page on navigation */
    if (F.dataAttrs) document.body.setAttribute('data-page', name);
  }

  function handleRoute() {
    var hash = location.hash.replace(/^#/, '');
    if (!hash || hash === 'home') {
      showView('home');
      renderHomeView();
    } else if (hash.startsWith('search')) {
      var qStr = hash.indexOf('?') > -1 ? hash.slice(hash.indexOf('?') + 1) : '';
      var params = new URLSearchParams(qStr);
      var query = params.get('q') || '';
      var inp = document.getElementById('search-input');
      if (inp) inp.value = query;
      showView('search');
      performSearch(query);
    } else if (hash.startsWith('product/')) {
      var sku = hash.replace('product/', '');
      showView('product');
      renderProductView(sku);
    } else if (hash === 'cart') {
      showView('cart');
      renderCartItems();
    } else if (hash === 'checkout') {
      showView('checkout');
      renderCheckoutSummary();
    } else if (hash === 'confirmation') {
      showView('confirmation');
      renderConfirmationView();
    } else {
      showView('home');
      renderHomeView();
    }
  }

  /* ================================================================
     INIT
     ================================================================ */
  document.addEventListener('DOMContentLoaded', function () {
    updateCartCount();

    /* -- Search form -- */
    var searchForm = document.getElementById('search-form');
    if (searchForm) {
      searchForm.addEventListener('submit', function (e) {
        e.preventDefault();
        var q = (document.getElementById('search-input').value || '').trim();
        location.hash = '#search?q=' + encodeURIComponent(q);
      });
    }

    /* -- Cart nav link -- */
    var cartLink = document.getElementById('cart-nav-link');
    if (cartLink) {
      cartLink.addEventListener('click', function (e) {
        e.preventDefault();
        location.hash = '#cart';
      });
    }

    /* -- Logo / home link -- */
    var logoLink = document.getElementById('logo-link');
    if (logoLink) {
      logoLink.addEventListener('click', function (e) {
        e.preventDefault();
        location.hash = '#home';
      });
    }

    /* -- Hero CTA -- */
    var heroCta = document.getElementById('hero-cta-btn');
    if (heroCta) {
      heroCta.addEventListener('click', function (e) {
        e.preventDefault();
        location.hash = '#search?q=';
      });
    }

    /* -- Category buttons -- */
    var CAT_QUERIES = {
      'cat-audio':       'audio',
      'cat-keyboards':   'keyboard',
      'cat-mice':        'mouse',
      'cat-monitors':    'monitor',
      'cat-accessories': 'accessories'
    };
    document.querySelectorAll('.category-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var q = CAT_QUERIES[this.id] || this.textContent.trim().toLowerCase();
        location.hash = '#search?q=' + encodeURIComponent(q);
      });
    });

    /* -- Checkout proceed -- */
    var checkoutBtn = document.getElementById('checkout-btn');
    if (checkoutBtn) {
      checkoutBtn.addEventListener('click', function () {
        if (window.__cart__.length > 0) location.hash = '#checkout';
      });
    }

    /* -- Checkout form -- */
    var checkoutForm = document.getElementById('checkout-form');
    if (checkoutForm) {
      checkoutForm.addEventListener('submit', function (e) {
        e.preventDefault();
        var name = (document.getElementById('field-name').value || '').trim();
        var addr = (document.getElementById('field-address').value || '').trim();
        if (!name || !addr) {
          showToast('\u26a0 Please fill in Name and Address.');
          return;
        }
        var orderId = 'ORD-' + Date.now();
        var total = window.__cart__.reduce(function (s, i) { return s + i.price * i.quantity; }, 0);
        window.__orderConfirmed__ = true;
        window.__lastOrder__ = {
          orderId: orderId,
          items: window.__cart__.slice(),
          total: total,
          timestamp: new Date().toISOString()
        };
        window.__cart__ = [];
        saveCart();
        updateCartCount();
        location.hash = '#confirmation';
      });
    }

    /* -- Hash router -- */
    window.addEventListener('hashchange', handleRoute);
    handleRoute();
  });

})();
