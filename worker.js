// =====================================================================
// worker.js — SERVIDOR DE ELYSIUM EN CLOUDFLARE
// Casi todo es el sitio tal cual (carpeta "publicado"). La única excepción:
// /__/auth/… (la pantalla de "Entrar con Google") se reenvía por debajo a
// Firebase, para que el inicio de sesión ocurra en NUESTRO dominio.
// Así funciona también cuando Elysium se abre como app desde el ícono
// (iPhone en modo app bloquea el inicio de sesión de otro dominio).
// El proyecto de Firebase de cada sitio va en wrangler.jsonc (FIREBASE_AUTH_HOST).
// =====================================================================
export function destinoAuth(urlTexto, hostFirebase) {
  const url = new URL(urlTexto);
  if (!url.pathname.startsWith('/__/auth/')) return null;
  return 'https://' + hostFirebase + url.pathname + url.search;
}

export default {
  async fetch(request, env) {
    const destino = destinoAuth(request.url, env.FIREBASE_AUTH_HOST);
    if (destino) {
      // Reenvío transparente (no redirección): misma petición, misma respuesta
      return fetch(new Request(destino, request), { redirect: 'manual' });
    }
    return env.ASSETS.fetch(request);
  }
};
