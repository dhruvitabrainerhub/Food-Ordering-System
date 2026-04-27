const API = window.location.hostname === 'localhost' ? 'http://localhost:8000' : `http://${window.location.hostname}:8000`;
const FRONTEND = window.location.origin;

function getToken() { return localStorage.getItem("token"); }
function getUser() { return JSON.parse(localStorage.getItem("user") || "null"); }

async function apiFetch(url, options = {}) {
    const token = getToken();
    if (token) options.headers = { ...options.headers, "Authorization": `Bearer ${token}` };
    if (options.body && typeof options.body === "object") {
        options.headers = { ...options.headers, "Content-Type": "application/json" };
        options.body = JSON.stringify(options.body);
    }
    const res = await fetch(API + url, options);
    if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Something went wrong");
    }
    return res.json();
}

let cart = JSON.parse(localStorage.getItem("cart") || "[]");

function saveCart() { localStorage.setItem("cart", JSON.stringify(cart)); }

function addToCart(item) {
    const existing = cart.find(c => c.id === item.id);
    if (existing) existing.qty++;
    else cart.push({ ...item, qty: 1 });
    saveCart();
    updateCartBadge();
}

function updateCartBadge() {
    const badge = document.getElementById("cart-badge");
    if (badge) badge.textContent = cart.reduce((s, i) => s + i.qty, 0);
}

function checkAuth(requireAdmin = false) {
    const user = getUser();
    if (!user) { window.location.href = "/login"; return null; }
    if (requireAdmin && !user.is_admin) { window.location.href = "/"; return null; }
    return user;
}

function logout() {
    localStorage.clear();
    window.location.href = "/login";
}
