// =====================================================================
// Firebase SIMULADO (en memoria) para probar las páginas sin red.
// Imita lo que usa el sitio: base de datos (ref, on, update, set, remove,
// transaction, contadores y hora del servidor), inicio de sesión y App Check.
// Controles para las pruebas:
//   window.__SEED__        datos iniciales de la base (se define antes)
//   window.__store()       ver la base de datos en este momento
//   window.__writes        lista de todas las escrituras
//   window.__setUser(u)    iniciar sesión como u ({uid, displayName}) o null
//   window.__NEXT_USER__   cuenta que "elige" el botón Entrar con Google
//   window.__failNext(fn)  simular que Firebase rechaza la próxima escritura
// =====================================================================
(function () {
  const TS = { '.sv': 'timestamp' };
  let store = window.__SEED__ || {};
  let clock = Date.now();
  const listeners = [];
  window.__writes = [];
  window.__failNext = null; // función (updatesObj) => bool para simular rechazo

  function split(p) { return (p || '').split('/').filter(Boolean); }
  function getAt(p) { let n = store; for (const k of split(p)) { if (n == null || typeof n !== 'object') return null; n = n[k]; } return n === undefined ? null : n; }
  function clone(v) { return v == null ? null : JSON.parse(JSON.stringify(v)); }
  function resolve(v, cur) {
    if (v && typeof v === 'object') {
      if (v['.sv'] === 'timestamp') return ++clock;
      if (v['.sv'] && v['.sv'].increment !== undefined) return (typeof cur === 'number' ? cur : 0) + v['.sv'].increment;
      const o = {}; for (const k of Object.keys(v)) { const r = resolve(v[k], cur && cur[k]); if (r !== null && r !== undefined) o[k] = r; } return Object.keys(o).length ? o : null;
    }
    return v;
  }
  function setAt(p, v) {
    const ks = split(p); if (!ks.length) { store = v || {}; return; }
    let n = store; for (let i = 0; i < ks.length - 1; i++) { if (n[ks[i]] == null || typeof n[ks[i]] !== 'object') n[ks[i]] = {}; n = n[ks[i]]; }
    const last = ks[ks.length - 1];
    const val = resolve(v, n[last]);
    if (val === null || val === undefined) delete n[last]; else n[last] = val;
  }
  function notify() { listeners.forEach(l => l.cb(snap(l.path))); }
  function snap(path) { const v = clone(getAt(path)); return { val: () => v, exists: () => v !== null, key: split(path).pop() }; }
  let pushN = 0;
  function ref(path = '') {
    const r = {
      key: split(path).pop() || null,
      child: (c) => ref(split(path).concat(split(c)).join('/')),
      push: () => ref(split(path).concat(['-k' + Date.now().toString(36) + (pushN++)]).join('/')),
      get: () => Promise.resolve(snap(path)),
      on: (ev, cb) => { listeners.push({ path, cb }); setTimeout(() => cb(snap(path)), 0); },
      update: (obj) => apply(Object.fromEntries(Object.entries(obj).map(([k, v]) => [split(path).concat(split(k)).join('/'), v]))),
      set: (v) => apply({ [path]: v }),
      remove: () => apply({ [path]: null }),
      transaction: (fn) => { const cur = clone(getAt(path)); const nv = fn(cur); if (nv === undefined) return Promise.resolve({ committed: false }); return apply({ [path]: nv }).then(() => ({ committed: true })); }
    };
    return r;
  }
  function apply(updates) {
    window.__writes.push(clone(updates));
    if (window.__failNext && window.__failNext(updates)) { window.__failNext = null; return Promise.reject(new Error('PERMISSION_DENIED')); }
    Object.entries(updates).forEach(([p, v]) => setAt(p, v));
    setTimeout(notify, 0);
    return Promise.resolve();
  }
  // Auth simulado
  const authListeners = [];
  const authObj = {
    currentUser: null,
    onAuthStateChanged: (cb) => { authListeners.push(cb); setTimeout(() => cb(authObj.currentUser), 0); },
    signInWithRedirect: () => { window.__redirigioAGoogle = true; return Promise.resolve(); },
    getRedirectResult: () => Promise.resolve(window.__RESULTADO_REDIRECT__ || { user: null }),
    signInWithPopup: () => { authObj.currentUser = window.__NEXT_USER__ || { uid: 'uidA', displayName: 'Ana' }; authListeners.forEach(cb => cb(authObj.currentUser)); return Promise.resolve({ user: authObj.currentUser }); },
    signOut: () => { authObj.currentUser = null; authListeners.forEach(cb => cb(null)); return Promise.resolve(); }
  };
  window.__setUser = (u) => { authObj.currentUser = u; authListeners.forEach(cb => cb(u)); };
  window.__store = () => store;
  function GoogleAuthProvider() { this.setCustomParameters = () => {}; }
  const authFn = () => authObj; authFn.GoogleAuthProvider = GoogleAuthProvider;
  const dbFn = () => ({ ref });
  dbFn.ServerValue = { TIMESTAMP: TS, increment: (n) => ({ '.sv': { increment: n } }) };
  window.firebase = {
    initializeApp: () => {},
    // Igual que el SDK real: reCAPTCHA mete un <div> en document.body al activarse,
    // así que falla si todavía no existe el <body> (por ejemplo, si se llama desde el <head>).
    appCheck: () => ({ activate: () => { if (!document.body) throw new TypeError("Cannot read properties of null (reading 'appendChild')"); window.__appCheckActive = true; } }),
    database: dbFn,
    auth: authFn
  };
  window.firebase.appCheck.ReCaptchaEnterpriseProvider = function () {};
})();
