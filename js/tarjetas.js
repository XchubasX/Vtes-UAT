// =====================================================================
// js/tarjetas.js — TARJETAS: pestañas y filtros, dibujar la lista de mesas y sus etiquetas.
// Parte del código de index.html (separado el 29 sep 2026, fase 2).
// =====================================================================

let currentTableModalityFilter = 'virtual';

// Ciudad indicada por la URL (ej. .../Organizador-Vtes/Zaragoza), o null si no aplica.
// Tiene prioridad sobre el filtro manual de ciudad hasta que el usuario lo toque o
// le dé clic a "Limpiar filtros".
let urlCityFilter = null;

function clearUrlCityFilter() {
  if (!urlCityFilter) return;
  urlCityFilter = null;
  const basePath = window.location.pathname.replace(/[^/]+\/?$/, '');
  window.history.replaceState({}, '', basePath || '/');
}

function setTableModality(mode) {
  document.getElementById('tableModality').value = mode;
  const virtualGroup = document.getElementById('virtualFieldsGroup');
  const presencialGroup = document.getElementById('presencialFieldsGroup');
  const btnVirtual = document.getElementById('modeVirtualBtn');
  const btnPresencial = document.getElementById('modePresencialBtn');

  const isVirtual = mode === 'virtual';
  virtualGroup.style.display = isVirtual ? 'contents' : 'none';
  presencialGroup.style.display = isVirtual ? 'none' : 'contents';

  btnVirtual.classList.toggle('tab-activa', isVirtual);
  btnVirtual.classList.toggle('tab-inactiva', !isVirtual);
  btnPresencial.classList.toggle('tab-activa', !isVirtual);
  btnPresencial.classList.toggle('tab-inactiva', isVirtual);
  btnVirtual.setAttribute('aria-pressed', isVirtual ? 'true' : 'false');
  btnPresencial.setAttribute('aria-pressed', isVirtual ? 'false' : 'true');

  document.getElementById('tableSectionIcon').textContent = isVirtual ? '⚔️' : '📍';
  document.getElementById('tableSectionTitle').textContent = isVirtual ? 'Abrir Nueva Mesa de Juego' : 'Crear Nuevo Evento Presencial';
  document.getElementById('tableNameLabel').textContent = isVirtual ? 'Nombre de Mesa' : 'Nombre de Evento';
  document.getElementById('tableSectionSubtitle').textContent = isVirtual
    ? 'Crea una mesa en tu plataforma preferida con horario fijo para que otros se sumen.'
    : 'Organiza una quedada presencial para que otros confirmen asistencia.';
  document.getElementById('createTableBtnLabel').textContent = isVirtual ? 'Abrir Mesa' : 'Crear Evento';
  document.getElementById('openCreateFormLabel').textContent = isVirtual ? 'Crear mesa' : 'Crear evento presencial';
  document.getElementById('presencialFiltersBar').style.display = isVirtual ? 'none' : 'flex';
  updateNightUI('create'); // el resumen dice "Tu mesa" o "Tu evento"

  // La lista de abajo se filtra para mostrar solo lo que coincide con la modalidad seleccionada
  currentTableModalityFilter = mode;
  renderAll(currentGlobalData);
}

// Aviso de "cargando" y de error de conexión (antes la lista se veía vacía)
function showLoadProblem() {
  if (dataLoaded) return;
  document.getElementById('customTablesContainer').innerHTML = `<div class="col-span-full py-8 space-y-3"><p class="font-display font-black text-4xl text-wine-300">No se pudo conectar.</p><p class="text-zinc-300">Revisa tu internet y vuelve a cargar la página.</p><button type="button" onclick="location.reload()" class="h-12 px-6 rounded-full bg-lampara hover:bg-lampara-claro text-zinc-900 font-bold transition">Volver a cargar</button></div>`;
}

function togglePasswordView(elementId) {
  const el = document.getElementById(elementId);
  if (el) el.classList.toggle('hidden');
}

// Formato de mesa virtual: Standard (Legacy) o V5
function formatLabel(format) {
  return format === 'v5' ? 'V5' : 'Standard (Legacy)';
}
function matchesPresencialFilters(t) {
  const countryVal = document.getElementById('filterCountry').value || '';
  const cityVal = document.getElementById('filterCity').value || '';
  const dateVal = document.getElementById('filterDate').value || '';

  // Si la ciudad viene de la URL (ej. .../Organizador-Vtes/Zaragoza), manda sobre el
  // dropdown manual, y compara sin importar mayúsculas/acentos-caja.
  if (urlCityFilter) {
    if ((t.city || '').toLowerCase() !== urlCityFilter.toLowerCase()) return false;
  } else if (cityVal && (t.city || '').toLowerCase() !== cityVal.toLowerCase()) {
    return false;
  }

  if (countryVal && (t.country || '') !== countryVal) return false;
  if (dateVal) {
    // Se compara con la fecha DEL LUGAR del evento (su huso de origen),
    // que es la misma que se muestra en la tarjeta, no con la fecha de
    // quien consulta. Formato YYYY-MM-DD.
    const eventDateStr = new Date(t.utcTime).toLocaleDateString('en-CA', { timeZone: t.originTz || undefined });
    if (eventDateStr !== dateVal) return false;
  }
  return true;
}

// Filtro de País: lista con los países que tienen eventos abiertos
function updateCountryFilterOptions(presencialTables) {
  const countrySelect = document.getElementById('filterCountry');
  const currentValue = countrySelect.value;
  const countries = Array.from(new Set(presencialTables.map(t => t.country).filter(Boolean))).sort();
  countrySelect.innerHTML = '<option value="">Todos</option>' + countries.map(c => `<option value="${escapeHtml(c)}">${escapeHtml(c)}</option>`).join('');
  if (countries.includes(currentValue)) countrySelect.value = currentValue;
}

// Filtro de Ciudad: solo las ciudades del país elegido (o todas)
function updateCityFilterOptions(presencialTables) {
  const citySelect = document.getElementById('filterCity');
  const currentValue = citySelect.value;
  const countryVal = document.getElementById('filterCountry').value || '';
  const inCountry = countryVal ? presencialTables.filter(t => (t.country || '') === countryVal) : presencialTables;
  const cities = Array.from(new Set(inCountry.map(t => t.city).filter(Boolean))).sort();
  citySelect.innerHTML = '<option value="">Todas</option>' + cities.map(c => `<option value="${escapeHtml(c)}">${escapeHtml(c)}</option>`).join('');

  if (urlCityFilter) {
    // Refleja en el dropdown la ciudad de la URL si ya existe algún evento con ese
    // nombre (comparación sin distinguir mayúsculas). Si no hay coincidencia todavía,
    // el dropdown se queda en "Todas" pero el filtro de la URL sigue aplicando igual
    // (mostrará la lista vacía, no todos los eventos).
    const match = cities.find(c => c.toLowerCase() === urlCityFilter.toLowerCase());
    if (match) citySelect.value = match;
  } else if (cities.includes(currentValue)) {
    citySelect.value = currentValue;
  }
}

function clearPresencialFilters() {
  document.getElementById('filterCountry').value = '';
  document.getElementById('filterCity').value = '';
  pickerFilterDate.clear();
  clearUrlCityFilter();
  renderAll(currentGlobalData);
}

function renderAll(allData) {
  const customTablesContainer = document.getElementById('customTablesContainer');

  // Contadores de las pestañas (total de cada modalidad, sin filtros)
  const allTables = allData.filter(d => d.type === 'custom_table');
  document.getElementById('countVirtual').textContent = allTables.filter(d => (d.modality || 'virtual') === 'virtual').length;
  document.getElementById('countPresencial').textContent = allTables.filter(d => d.modality === 'presencial').length;

  const rawCustomTables = allTables.filter(d => (d.modality || 'virtual') === currentTableModalityFilter);

  let customTables = rawCustomTables;
  if (currentTableModalityFilter === 'presencial') {
    updateCountryFilterOptions(rawCustomTables);
    updateCityFilterOptions(rawCustomTables);
    customTables = rawCustomTables.filter(matchesPresencialFilters);
  }

  renderCustomTables(customTables, customTablesContainer);
}

// ---------------------------------------------------------------------
// ÍCONOS (trazos simples; reemplazan los emojis dentro de las tarjetas)
// ---------------------------------------------------------------------
const ICONO_LAPIZ = '<svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>';
const ICONO_VETAR = '<svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="m5.6 5.6 12.8 12.8"/></svg>';

// Encabezado de cada noche en la cartelera: "Hoy, martes 30", "Mañana, miércoles 1", "Jueves 2 de octubre"
function nightHeaderLabel(utcISO, tz) {
  const key = localYMD(utcISO, tz);
  const now = new Date();
  const hoy = localYMD(now.toISOString(), tz);
  const manana = localYMD(new Date(now.getTime() + 24 * 3600 * 1000).toISOString(), tz);
  const opts = { weekday: 'long', day: 'numeric', timeZone: tz || undefined };
  const corto = new Intl.DateTimeFormat('es', opts).format(new Date(utcISO)).replace(',', '');
  if (key === hoy) return `Hoy, ${corto}`;
  if (key === manana) return `Mañana, ${corto}`;
  const largo = new Intl.DateTimeFormat('es', { weekday: 'long', day: 'numeric', month: 'long', timeZone: tz || undefined }).format(new Date(utcISO)).replace(',', '');
  return largo.charAt(0).toUpperCase() + largo.slice(1);
}

// Cinco barritas de asientos (mesas virtuales): ocupados, el tuyo y libres
function seatBarsHtml(players) {
  const barras = [];
  for (let i = 0; i < 5; i++) {
    const p = players[i];
    const color = !p ? 'bg-zinc-700' : isMine(p) ? 'bg-violet-300' : 'bg-wine-500';
    barras.push(`<span class="h-2 w-9 rounded-full ${color}"></span>`);
  }
  return barras.join('');
}

function renderCustomTables(tables, container) {
  if (!dataLoaded) {
    container.innerHTML = '<p class="col-span-full text-zinc-400 py-6">Cargando mesas…</p>';
    return;
  }
  if (tables.length === 0) {
    container.innerHTML = `<p class="col-span-full text-zinc-300 py-6">${currentTableModalityFilter === 'presencial' ? 'No hay eventos presenciales creados. ¡Crea uno!' : 'No hay mesas abiertas creadas. ¡Abre una!'}</p>`;
    return;
  }

  tables.sort((a, b) => new Date(a.utcTime) - new Date(b.utcTime));

  let nocheAnterior = null;
  container.innerHTML = tables.map(t => {
    const roster = getRoster(t);
    const count = roster.players.length;
    const isPresencial = t.modality === 'presencial';
    const isFull = !isPresencial && count >= 5;
    const isReady = !isPresencial && count >= 4;
    const iOwn = isOwner(t);
    const manage = canManage(t);
    const alreadyIn = roster.entries.some(isMine);
    const id = escapeJsAttr(t.id);
    const tz = isPresencial ? t.originTz : undefined;

    let formattedDate, formattedTime;
    if (isPresencial) {
      // Hora local del lugar del evento (huso de origen), sin convertir
      const fCard = formatPresencialDateTime(t.utcTime, t.originTz, { weekday: 'short', month: 'short', day: 'numeric' }, { hour: '2-digit', minute: '2-digit' });
      formattedDate = fCard.date;
      formattedTime = fCard.time;
    } else {
      const dateObj = new Date(t.utcTime);
      formattedDate = dateObj.toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' });
      formattedTime = dateObj.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' });
    }

    // Encabezado de la noche (solo cuando cambia de día)
    const noche = localYMD(t.utcTime, tz) + (isPresencial ? '|' + (t.originTz || '') : '');
    const encabezado = noche !== nocheAnterior
      ? `<h2 class="col-span-full pt-6 pb-1 text-sm font-semibold text-zinc-400 border-b border-zinc-800">${escapeHtml(nightHeaderLabel(t.utcTime, tz))}${isPresencial && t.city ? ' · ' + escapeHtml(t.city) : ''}</h2>`
      : '';
    nocheAnterior = noche;

    // Jugadores en orden de llegada y, si es presencial, ordenados por hora de llegada
    let displayPlayers = roster.players;
    if (isPresencial) {
      displayPlayers = displayPlayers.slice().sort((a, b) => arrivalToMinutes(a.arrival) - arrivalToMinutes(b.arrival));
    }
    const myPlayers = displayPlayers.filter(isMine);
    const subs = roster.subs;
    const mySubs = subs.filter(isMine);
    const banBtn = (e) => (isAdmin && e.uid && e.uid !== myUid())
      ? `<button onclick="banEntry('${id}', '${escapeJsAttr(e.ref)}')" class="text-lampara hover:text-lampara-claro leading-none px-2 py-1.5 -my-1.5 rounded" title="Vetar esta cuenta" aria-label="Vetar la cuenta de ${escapeHtml(e.nick)}">${ICONO_VETAR}</button>`
      : '';

    // Estado junto a la hora
    const estado = isPresencial
      ? `<span class="text-emerald-300 font-semibold">${count} confirmado${count === 1 ? '' : 's'}</span>`
      : isReady
        ? `<span class="text-emerald-300 font-semibold">${count >= 5 ? 'Mesa llena' : 'Lista para jugar'} (${count}/5)</span>`
        : `<span class="text-wine-300 font-semibold">Faltan ${5 - count} jugador(es)</span>`;

    const horaColor = isPresencial ? 'text-emerald-300' : (relativeTimeLabel(t.utcTime).soon ? 'text-lampara' : 'text-zinc-100');

    // Plataforma · formato (virtual) o lugar (presencial), más marcas de "lo tuyo"
    const meta = [];
    if (isPresencial) {
      meta.push(escapeHtml(t.venue || ''));
      if (t.recurrence === 'weekly') meta.push(`cada ${escapeHtml(weekdayInZone(t.utcTime, t.originTz))}`);
    } else {
      meta.push((t.platform || '').toLowerCase().includes('lackey') || !t.platform ? 'LackeyCCG' : 'Succubus Club');
      if (t.format) meta.push(formatLabel(t.format));
    }
    const metaHtml = meta.filter(Boolean).join(' · ')
      + (iOwn ? ' · <span class="text-violet-300 font-semibold">Organizas tú</span>' : '');

    const lineaEditar = (texto, fn) => manage
      ? `<button onclick="${fn}('${id}')" class="inline-flex items-center gap-1 text-zinc-400 hover:text-zinc-100 text-sm px-1 py-1" >${ICONO_LAPIZ}${texto}</button>` : '';

    const discordHtml = `
      <p class="flex flex-wrap items-center gap-x-2 text-sm text-zinc-300">
        <span class="text-zinc-400">Discord:</span>
        ${t.discord ? `<span class="text-zinc-100 break-all">${escapeHtml(t.discord)}</span>` : `<span class="text-zinc-400 italic">no especificado</span>`}
        ${lineaEditar(t.discord ? 'Editar' : 'Definir', 'editCustomTableDiscord')}
      </p>`;

    const gamePwdHtml = `
      <p class="flex flex-wrap items-center gap-x-2 text-sm text-zinc-300">
        <span class="text-zinc-400">Contraseña:</span>
        ${t.gamePassword ? `<span id="gamepwd-${escapeHtml(t.id)}" class="hidden font-mono font-bold text-zinc-100 select-all">${escapeHtml(t.gamePassword)}</span><button onclick="togglePasswordView('gamepwd-${id}')" class="text-lampara hover:text-lampara-claro underline underline-offset-2 px-1 py-1">Ver</button>` : `<span class="text-zinc-400 italic">sin contraseña</span>`}
        ${lineaEditar(t.gamePassword ? 'Editar' : 'Definir', 'editCustomTableGamePassword')}
      </p>`;

    const hasValidMap = t.mapsLink && isValidHttpUrl(t.mapsLink);
    const venueHtml = `
      <p class="flex flex-wrap items-center gap-x-3 text-sm text-zinc-300">
        <span>${escapeHtml(t.city || '')}${t.country ? ', ' + escapeHtml(t.country) : ''}</span>
        ${hasValidMap
          ? `<a href="${escapeHtml(t.mapsLink)}" target="_blank" rel="noopener" class="text-emerald-300 hover:text-emerald-200 underline underline-offset-2 py-1">Ver ubicación</a>`
          : `<span class="text-zinc-400 italic">${t.mapsLink ? 'Link de mapa no válido' : 'sin link de mapa'}</span>`}
        ${manage ? `<button onclick="editCustomTableMapsLink('${id}')" class="inline-flex items-center gap-1 text-zinc-400 hover:text-zinc-100 text-sm px-1 py-1">${ICONO_LAPIZ}${t.mapsLink ? 'Editar' : 'Agregar'} link</button>` : ''}
      </p>`;

    const playersHtml = displayPlayers.map(p => {
      const mine = isMine(p);
      const refArg = escapeJsAttr(p.ref);
      const canEditThis = (mine || manage) && (!p.legacy || isAdmin);
      return `
        <span class="inline-flex items-center gap-1.5 ${mine ? 'bg-violet-300/15 text-violet-100 ring-1 ring-violet-300/60' : 'bg-zinc-800 text-zinc-100'} text-sm px-3 py-1.5 rounded-full">
          ${escapeHtml(p.nick)}${mine ? '<span class="text-violet-300 text-xs font-semibold">· tú</span>' : ''}${p.arrival ? `<span class="text-zinc-300 text-xs tabular-nums">· ${escapeHtml(p.arrival)}</span>` : ''}
          ${isPresencial && canEditThis ? `<button onclick="editPlayerArrival('${id}', '${refArg}')" class="text-zinc-300 hover:text-zinc-100 leading-none px-2 py-1.5 -my-1.5 rounded" title="Editar hora de llegada" aria-label="Editar hora de llegada de ${escapeHtml(p.nick)}">${ICONO_LAPIZ}</button>` : ''}
          ${!mine && canEditThis ? `<button onclick="leaveTable('${id}', '${refArg}')" class="text-zinc-300 hover:text-red-400 font-bold text-base leading-none px-2 py-1.5 -my-1.5 rounded" title="Remover jugador" aria-label="Quitar a ${escapeHtml(p.nick)}">×</button>` : ''}
          ${banBtn(p)}
        </span>`;
    }).join('');

    const subsHtml = subs.length === 0 ? '' : `
      <div class="space-y-2 border-l-2 border-zinc-700 pl-3">
        <p class="text-sm text-zinc-400">Suplentes (${subs.length}/${SUBS_MAX}) · entran en este orden si alguien sale:</p>
        <ol class="space-y-1">
          ${subs.map((s, i) => {
            const mine = isMine(s);
            const canRemove = !mine && manage && (!s.legacy || isAdmin);
            return `
            <li class="flex items-center justify-between gap-2 text-sm">
              <span class="flex items-center gap-2 min-w-0">
                <span class="text-zinc-400 tabular-nums">${i + 1}.</span>
                <span class="${mine ? 'text-violet-100' : 'text-zinc-100'} truncate">${escapeHtml(s.nick)}</span>${mine ? '<span class="text-violet-300 text-xs font-semibold shrink-0">· tú</span>' : ''}
              </span>
              <span class="flex items-center gap-1 shrink-0">
                ${banBtn(s)}
                ${canRemove ? `<button onclick="leaveTable('${id}', '${escapeJsAttr(s.ref)}')" class="text-zinc-400 hover:text-red-400 font-bold text-base leading-none px-2 py-1.5 -my-1.5 rounded" title="Quitar suplente" aria-label="Quitar a ${escapeHtml(s.nick)} de suplentes">×</button>` : ''}
              </span>
            </li>`;
          }).join('')}
        </ol>
      </div>`;

    // Botón principal (ámbar). Si ya estoy anotado (y no organizo), no hay botón para anotarme otra vez.
    const primario = 'h-12 px-6 rounded-full bg-lampara hover:bg-lampara-claro text-zinc-900 font-bold text-base transition';
    const secundario = 'h-12 px-5 rounded-full border border-zinc-700 hover:border-zinc-400 text-zinc-100 font-semibold text-base transition';
    const joinLabel = alreadyIn
      ? 'Anotar a otra persona'
      : (isPresencial ? '¡Confirmar asistencia!' : '¡Unirme a esta Mesa!');
    const openSimilarHtml = `<button onclick="openSimilarTable('${id}')" class="${secundario}">Abrir otra mesa a esta hora</button>`;
    const mainActionHtml = (alreadyIn && !manage) ? ((isFull && subs.length >= SUBS_MAX) ? openSimilarHtml : '')
      : !isFull ? `<button onclick="joinTable('${id}')" class="${alreadyIn ? secundario : primario}">${joinLabel}</button>`
      : subs.length < SUBS_MAX ? `<button onclick="joinTable('${id}', true)" class="${primario}">Apuntarme como suplente</button>`
      : openSimilarHtml;

    const leaveSubButtons = mySubs.map(s => `
      <button onclick="leaveTable('${id}', '${escapeJsAttr(s.ref)}')" class="${secundario}">Salir de suplentes${mySubs.length > 1 ? ` (${escapeHtml(s.nick)})` : ''}</button>`).join('');
    const leaveButtons = myPlayers.map(p => `
      <button onclick="leaveTable('${id}', '${escapeJsAttr(p.ref)}')" class="${secundario}">Salir${myPlayers.length > 1 ? ` (${escapeHtml(p.nick)})` : isPresencial ? ' del evento' : ' de la mesa'}</button>`).join('');

    const enlace = 'text-lampara hover:text-lampara-claro font-semibold text-base py-3 px-1';
    const accionChica = 'text-zinc-400 hover:text-zinc-100 text-sm py-2';
    const cardId = `card-custom-${escapeHtml(t.id)}`;

    return encabezado + `
      <article id="${cardId}" class="py-5 border-b border-zinc-800 space-y-3 transition-shadow">
        <div class="flex items-end gap-3 flex-wrap">
          <span class="font-display font-black text-7xl leading-[0.85] tabular-nums ${horaColor}">${formattedTime}</span>
          <span class="pb-1 text-sm">${estado}</span>
        </div>
        <p class="text-sm text-zinc-400 flex flex-wrap items-center gap-x-2 gap-y-1">
          <span>${formattedDate} · ${isPresencial ? `hora de ${escapeHtml(t.city || 'el lugar')}` : 'tu hora'}</span>
          ${nightBadgeHtml(t)}
          ${relativeBadgeHtml(t.utcTime)}
        </p>
        <h3 class="text-xl font-bold text-zinc-100 leading-snug break-words">${escapeHtml(t.name)}</h3>
        <p class="text-sm text-zinc-300">${metaHtml}</p>

        ${isPresencial ? '' : `<div class="flex items-center gap-1.5" role="img" aria-label="${Math.min(count, 5)} de 5 asientos ocupados">${seatBarsHtml(roster.players)}</div>`}

        ${t.notes ? `
        <div class="flex items-start justify-between gap-2 text-sm bg-zinc-800 rounded-xl px-3 py-2">
          <p class="text-zinc-100 break-words min-w-0">${escapeHtml(t.notes)}</p>
          ${manage ? `<button onclick="editCustomTableNotes('${id}')" class="inline-flex items-center gap-1 text-zinc-400 hover:text-zinc-100 text-sm shrink-0 px-1 py-1">${ICONO_LAPIZ}Editar</button>` : ''}
        </div>` : ''}

        <div class="space-y-1">${isPresencial ? venueHtml : discordHtml + gamePwdHtml}</div>

        ${displayPlayers.length ? `<div class="flex flex-wrap gap-2" aria-label="${isPresencial ? `Asistentes confirmados (${count})` : `Jugadores confirmados (${count}/5)`}">${playersHtml}</div>` : ''}

        ${subsHtml}

        <div class="flex flex-wrap items-center gap-x-4 gap-y-2 pt-1">
          ${mainActionHtml}
          ${leaveButtons}
          ${leaveSubButtons}
          <button onclick="shareTableInvitation('${id}')" class="${enlace}">WhatsApp</button>
          <button onclick="shareTableLink('${id}')" class="${enlace}">Compartir</button>
          <button onclick="openCalendarModal('${id}')" class="${enlace}">Calendario</button>
        </div>

        <div class="flex flex-wrap items-center gap-x-5 gap-y-1">
          ${isPresencial ? `<button onclick="window.open('sorteo.html?tableId=${encodeURIComponent(t.id)}', '_blank')" class="${accionChica}">Orden de Asientos</button>` : ''}
          ${manage && isPresencial && t.recurrence === 'weekly' ? `<button onclick="skipWeek('${id}')" class="${accionChica}">Saltar esta semana</button>` : ''}
          ${manage && !t.notes ? `<button onclick="editCustomTableNotes('${id}')" class="${accionChica}">Agregar nota</button>` : ''}
          ${manage ? `<button onclick="editTableSchedule('${id}')" class="${accionChica}">Editar horario</button>
          <button onclick="deleteEntry('${id}')" class="${accionChica} hover:text-red-400">${isPresencial ? 'Cerrar Evento' : 'Cerrar Mesa'}</button>` : ''}
        </div>
      </article>
    `;
  }).join('');
}
