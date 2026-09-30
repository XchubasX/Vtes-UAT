// =====================================================================
// comun.js — CÓDIGO COMPARTIDO POR LAS PÁGINAS DEL SITIO
// (index.html, sorteo.html y estadisticas.html)
// Se carga al inicio del <body> (App Check necesita que ya exista el <body>),
// después de los programas de Firebase (en el <head>) y de config.js.
// Es idéntico en el sitio real y en el de pruebas.
// =====================================================================

// ---------------------------------------------------------------------
// COLORES Y LETRAS DEL SITIO (Tailwind) — diseño "Noche y hora" (30 sep 2026)
// La escala "zinc" se redefine como azul noche y "wine" como rosa sangre:
// así TODO el sitio (tarjetas, ventanas, formularios) cambia desde aquí.
//   zinc-900 = fondo noche · zinc-800 = paneles · zinc-700 = bordes
//   zinc-400/300 = texto secundario · zinc-100 = texto principal
//   lampara = ámbar de las horas y del botón principal (texto oscuro encima)
// Letras: Big Shoulders Display (horas y títulos) + Public Sans (texto).
// estadisticas.html no usa Tailwind.
// ---------------------------------------------------------------------
if (window.tailwind) {
  tailwind.config = {
    theme: {
      extend: {
        fontFamily: {
          sans: ['"Public Sans"', 'system-ui', 'sans-serif'],
          display: ['"Big Shoulders Display"', '"Public Sans"', 'sans-serif']
        },
        colors: {
          zinc: {
            50: '#F6F7FD', 100: '#EEF0FB', 200: '#DDE0F5', 300: '#C9CDEB',
            400: '#AEB3D6', 500: '#8990BF', 600: '#5A6199', 700: '#454B7A',
            800: '#2A2F57', 900: '#1D2140', 950: '#151831'
          },
          wine: {
            50: '#FDF1F3', 100: '#FBE0E5', 200: '#F5BCC7', 300: '#EE93A4',
            400: '#E66A80', 500: '#E0506A', 600: '#C23A55', 700: '#9E2D45',
            800: '#7A2438', 900: '#561A29', 950: '#380F1A'
          },
          lampara: { DEFAULT: '#F4C45C', claro: '#F7D27E', oscuro: '#D9A63A' }
        }
      }
    }
  };
}

// ---------------------------------------------------------------------
// FIREBASE + APP CHECK (reCAPTCHA Enterprise)
// App Check valida que las peticiones a la base de datos vengan de la
// página publicada en xchubasx.github.io y no de una copia o un programa.
// Los datos del proyecto están en config.js.
// ---------------------------------------------------------------------
firebase.initializeApp(VTES_CONFIG.firebase);
firebase.appCheck().activate(
  new firebase.appCheck.ReCaptchaEnterpriseProvider(VTES_CONFIG.recaptchaKey),
  true // refresca el token automáticamente en segundo plano
);

// ---------------------------------------------------------------------
// TEXTO SEGURO: convierte & < > " ' en texto, para que nadie pueda meter
// código dentro de un nick, un nombre de mesa, etc.
// ---------------------------------------------------------------------
function escapeHtml(str) {
  return String(str ?? '').replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}

// ---------------------------------------------------------------------
// NORMALIZACIÓN DE JUGADORES (retrocompatible): acepta un objeto
// { nick, arrival }, un texto simple "Gabi" o "Jesus 18:00".
// ---------------------------------------------------------------------
function normalizePlayer(p) {
  if (p && typeof p === 'object') {
    return { nick: p.nick || '', arrival: p.arrival || null };
  }
  const str = (p || '').toString();
  const match = str.match(/^(.*\S)\s+(\d{1,2}):(\d{2})\s*$/);
  if (match) {
    const hh = match[2].padStart(2, '0');
    const mm = match[3];
    return { nick: match[1], arrival: `${hh}:${mm}` };
  }
  return { nick: str, arrival: null };
}

// ---------------------------------------------------------------------
// BOTÓN DE CONTACTO 💬: REPORTAR BUG / SUGERENCIA
// Aparece en las páginas cuyo <body> tiene el atributo data-contacto.
// Se envía por correo directo vía EmailJS — no se escribe nada en
// Firebase ni se guarda ningún dato del usuario en el sitio. El correo
// (si el usuario lo deja) solo viaja como "reply-to".
// ---------------------------------------------------------------------
const CONTACTO_HTML = `
  <!-- BOTÓN FLOTANTE: REPORTAR BUG / SUGERENCIA -->
  <button type="button" onclick="openFeedbackModal()" title="Reportar un bug o sugerencia" aria-label="Reportar un bug o sugerencia" class="fixed bottom-4 right-4 z-40 bg-wine-600 hover:bg-wine-500 text-white rounded-full w-12 h-12 shadow-lg shadow-wine-900/40 flex items-center justify-center text-xl transition transform hover:scale-105">
    💬
  </button>

  <!-- MODAL: REPORTAR BUG / SUGERENCIA (no guarda nada en Firebase, se envía por correo vía EmailJS) -->
  <div id="feedbackModal" class="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
    <div class="bg-zinc-800 border border-zinc-700 rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
      <div class="flex items-center gap-3 border-b border-zinc-700 pb-3">
        <span class="text-2xl">💬</span>
        <h3 class="text-lg font-bold text-wine-400">Reportar un bug o sugerencia</h3>
      </div>
      <p class="text-xs text-zinc-400">Tu mensaje se envía directo por correo. No se guarda nada en la base de datos del sitio.</p>
      <form id="feedbackForm" class="space-y-3">
        <div>
          <label class="block text-xs font-semibold text-zinc-400 mb-1">Mensaje</label>
          <textarea id="feedbackMessage" required rows="4" maxlength="2000" placeholder="Describe el bug o la funcionalidad que te gustaría..." class="w-full bg-zinc-900 border border-zinc-700 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-wine-500 resize-none"></textarea>
        </div>
        <div>
          <label class="block text-xs font-semibold text-zinc-400 mb-1">Tu correo (opcional, solo si quieres que te respondamos)</label>
          <input type="email" id="feedbackEmail" placeholder="tucorreo@ejemplo.com" class="w-full bg-zinc-900 border border-zinc-700 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-wine-500">
        </div>
        <p id="feedbackStatus" class="text-xs hidden"></p>
        <div class="flex gap-2 pt-1">
          <button type="submit" id="feedbackSubmitBtn" class="flex-1 bg-wine-600 hover:bg-wine-500 text-white font-bold py-2 rounded-lg text-sm transition disabled:opacity-50 disabled:cursor-not-allowed">
            Enviar
          </button>
          <button type="button" onclick="closeFeedbackModal()" class="text-sm font-medium text-zinc-400 hover:text-zinc-200 border border-zinc-700 rounded-lg px-4 transition">
            Cancelar
          </button>
        </div>
      </form>
    </div>
  </div>
`;


function openFeedbackModal() {
  document.getElementById('feedbackModal').classList.remove('hidden');
}

function closeFeedbackModal() {
  document.getElementById('feedbackModal').classList.add('hidden');
  document.getElementById('feedbackForm').reset();
  const status = document.getElementById('feedbackStatus');
  status.classList.add('hidden');
  status.textContent = '';
}

function enviarFeedback(e) {
  e.preventDefault();
  const message = document.getElementById('feedbackMessage').value.trim();
  const email = document.getElementById('feedbackEmail').value.trim();
  if (!message) return;

  const btn = document.getElementById('feedbackSubmitBtn');
  const status = document.getElementById('feedbackStatus');
  btn.disabled = true;
  btn.textContent = 'Enviando...';

  emailjs.send('service_ehnpqcs', 'template_d1h2h9k', {
    message: message,
    page: /sorteo/.test(location.pathname) ? 'sorteo' : 'index',
    reply_to: email || '(no proporcionado)'
  }).then(() => {
    status.textContent = '✅ ¡Gracias! Tu mensaje fue enviado.';
    status.className = 'text-xs text-emerald-400';
    status.classList.remove('hidden');
    document.getElementById('feedbackForm').reset();
    btn.disabled = false;
    btn.textContent = 'Enviar';
    setTimeout(closeFeedbackModal, 2000);
  }).catch(() => {
    status.textContent = '❌ No se pudo enviar. Intenta de nuevo en un momento.';
    status.className = 'text-xs text-red-400';
    status.classList.remove('hidden');
    btn.disabled = false;
    btn.textContent = 'Enviar';
  });
}

// ---------------------------------------------------------------------
// VENTANA "ACERCA DE" (botón "?" del encabezado). El contenido está en
// cada página, porque es distinto en cada una.
// ---------------------------------------------------------------------
function openAboutModal(section) {
  document.getElementById('aboutModal').classList.remove('hidden');
  // Desde la línea "Aviso legal" del pie de página, ir directo a esa sección
  if (section === 'legal') {
    const el = document.getElementById('aboutLegal');
    if (el) setTimeout(() => el.scrollIntoView({ block: 'start' }), 0);
  }
}
function closeAboutModal() {
  document.getElementById('aboutModal').classList.add('hidden');
}

// ---------------------------------------------------------------------
// AL TERMINAR DE CARGAR LA PÁGINA
// ---------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
  // Franja naranja del sitio de pruebas
  if (VTES_CONFIG.esPruebas) {
    const franja = document.createElement('div');
    franja.style.cssText = 'background:#b45309;color:#fff;text-align:center;font:600 13px sans-serif;padding:6px;margin:0 0 8px';
    franja.textContent = '⚠️ SITIO DE PRUEBAS — los datos aquí no son reales';
    document.body.prepend(franja);
  }
  // Botón 💬 y su ventana
  if (document.body.hasAttribute('data-contacto')) {
    emailjs.init({ publicKey: 'MIO26Qm3IZUFiwvB3' });
    document.body.insertAdjacentHTML('beforeend', CONTACTO_HTML);
    document.getElementById('feedbackForm').addEventListener('submit', enviarFeedback);
  }
});
