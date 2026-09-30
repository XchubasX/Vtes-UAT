// =====================================================================
// config.js — DATOS QUE CAMBIAN ENTRE EL SITIO REAL Y EL DE PRUEBAS
// Es el ÚNICO archivo distinto entre Organizador-Vtes y Vtes-UAT.
// Al pasar cambios de pruebas al sitio real se copian todos los demás
// archivos tal cual, y este NO se toca.
// =====================================================================
window.VTES_CONFIG = {
  // true solo en el sitio de pruebas: muestra la franja naranja
  esPruebas: true,

  // Proyecto de Firebase
  firebase: {
    apiKey: "AIzaSyBQR7AaxC5F2bTKI_po7w7awZLa_KVS4zk",
    authDomain: "vtes-uat.firebaseapp.com",
    databaseURL: "https://vtes-uat-default-rtdb.firebaseio.com",
    projectId: "vtes-uat",
    storageBucket: "vtes-uat.firebasestorage.app",
    messagingSenderId: "801358504439",
    appId: "1:801358504439:web:d946e61ff0067bee69cef2"
  },

  // Site Key de reCAPTCHA Enterprise (App Check)
  recaptchaKey: '6LfWd7YtAAAAAMg-IhiLw8ukgxp2ejhX-i7RaBl-'
};
