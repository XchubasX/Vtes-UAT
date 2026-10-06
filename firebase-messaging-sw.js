// =====================================================================
// firebase-messaging-sw.js — recibe los avisos de mesa con Elysium cerrado
// y los muestra como notificación. Al tocarla se abre la mesa (#mesa-…).
// Toma los datos de Firebase de config.js (el mismo del sitio).
// =====================================================================
self.window = self; // config.js escribe en window.VTES_CONFIG
importScripts('config.js?v=20261006a');
importScripts('https://www.gstatic.com/firebasejs/9.23.0/firebase-app-compat.js',
              'https://www.gstatic.com/firebasejs/9.23.0/firebase-messaging-compat.js');
firebase.initializeApp(self.VTES_CONFIG.firebase);
firebase.messaging(); // muestra sola la notificación y abre el enlace al tocarla
