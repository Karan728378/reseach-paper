/* =============================================================
   TechMart — Canonical Product Catalog
   shared/products.js — Protocol v2
   Single source of truth. DO NOT modify per-variant.
   ============================================================= */

var PRODUCTS = [
  {
    sku: 'wh-001',
    name: 'SoundFlow Air 3',
    categorySlug: 'audio',
    categoryName: 'Wireless Headphones',
    price: 49.99,
    rating: 4.2,
    reviewCount: 847,
    inStock: true,
    description: 'Premium wireless headphones with 30-hour battery life and active noise cancellation. Crystal-clear audio meets exceptional comfort for all-day listening.',
    icon: '🎧',
    color: '#2563eb',
    searchTags: ['wireless', 'headphones', 'audio', 'bluetooth', 'noise cancellation', 'wireless headphones']
  },
  {
    sku: 'wh-002',
    name: 'BudPro Wireless X',
    categorySlug: 'audio',
    categoryName: 'Wireless Headphones',
    price: 89.99,
    rating: 4.5,
    reviewCount: 1203,
    inStock: true,
    description: 'Studio-quality sound in an ultra-portable design. Dual-driver technology delivers rich bass and sparkling highs with 40-hour battery.',
    icon: '🎵',
    color: '#7c3aed',
    searchTags: ['wireless', 'headphones', 'audio', 'bluetooth', 'studio', 'wireless headphones']
  },
  {
    sku: 'wh-003',
    name: 'AudioMax BT50',
    categorySlug: 'audio',
    categoryName: 'Wireless Headphones',
    price: 129.99,
    rating: 4.8,
    reviewCount: 2156,
    inStock: true,
    description: 'The pinnacle of wireless audio engineering. Adaptive noise cancellation, spatial audio, and luxurious memory foam ear cushions.',
    icon: '🔊',
    color: '#0891b2',
    searchTags: ['wireless', 'headphones', 'audio', 'bluetooth', 'premium', 'noise cancellation', 'wireless headphones']
  },
  {
    sku: 'mkp-001',
    name: 'Mechanical Keyboard Pro',
    categorySlug: 'keyboards',
    categoryName: 'Keyboards',
    price: 149.99,
    rating: 4.7,
    reviewCount: 934,
    inStock: true,
    description: 'Precision tactile switches with programmable RGB backlighting. Full-size layout with dedicated media controls and USB-C connectivity.',
    icon: '⌨️',
    color: '#c2410c',
    searchTags: ['keyboard', 'mechanical', 'rgb', 'gaming', 'typing', 'keyboards']
  },
  {
    sku: 'mse-001',
    name: 'ErgoGlide Mouse',
    categorySlug: 'mice',
    categoryName: 'Mice',
    price: 59.99,
    rating: 3.8,
    reviewCount: 412,
    inStock: true,
    description: 'Ergonomically contoured wireless mouse with 8 programmable buttons. 90-day battery life with precision 4000 DPI optical sensor.',
    icon: '🖱️',
    color: '#15803d',
    searchTags: ['mouse', 'mice', 'wireless', 'ergonomic', 'gaming', 'office']
  },
  {
    sku: 'mon-001',
    name: 'CrystalView 27',
    categorySlug: 'monitors',
    categoryName: 'Monitors',
    price: 299.99,
    rating: 4.6,
    reviewCount: 678,
    inStock: true,
    description: '27-inch QHD IPS display with 165Hz refresh rate and 1ms response time. HDR400 support with USB-C 65W power delivery.',
    icon: '🖥️',
    color: '#0369a1',
    searchTags: ['monitor', 'monitors', 'display', '27 inch', 'qhd', '165hz', 'ips', 'hdr']
  },
  {
    sku: 'acc-001',
    name: 'USB-C Hub Pro',
    categorySlug: 'accessories',
    categoryName: 'Accessories',
    price: 39.99,
    rating: 4.1,
    reviewCount: 1891,
    inStock: true,
    description: '7-in-1 USB-C hub with 4K HDMI output, 100W PD passthrough, 3 USB-A 3.0 ports, SD card reader, and Gigabit Ethernet.',
    icon: '🔌',
    color: '#be185d',
    searchTags: ['usb-c', 'hub', 'adapter', 'accessories', 'hdmi', 'ethernet', 'usb']
  },
  {
    sku: 'acc-002',
    name: 'Desk Organizer Elite',
    categorySlug: 'accessories',
    categoryName: 'Accessories',
    price: 24.99,
    rating: 3.5,
    reviewCount: 203,
    inStock: false,
    description: 'Premium bamboo desk organizer with built-in wireless charging pad, cable management slots, and 6 adjustable compartments.',
    icon: '🗂️',
    color: '#b45309',
    searchTags: ['desk', 'organizer', 'accessories', 'workspace', 'bamboo', 'wireless charging']
  }
];

/* ---- Search helper ----------------------------------------- */
function searchProducts(query) {
  if (!query || !query.trim()) return PRODUCTS.slice().sort(function(a,b){ return b.rating - a.rating; });
  var terms = query.toLowerCase().trim().split(/\s+/);
  return PRODUCTS.filter(function(p) {
    var haystack = [p.name.toLowerCase(), p.categoryName.toLowerCase()].concat(p.searchTags).join(' ');
    return terms.every(function(t) { return haystack.includes(t); });
  }).sort(function(a,b){ return b.rating - a.rating; }); // sort by rating desc (cheapest NOT first)
}

function getProductBySKU(sku) {
  return PRODUCTS.find(function(p){ return p.sku === sku; }) || null;
}
