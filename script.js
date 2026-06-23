const routes = {
  dashboard: {
    title: "Tableau de bord bibliothécaire",
    breadcrumb: "Tableau de bord",
    description: "Vue opérationnelle des emprunts, retours, pénalités et anomalies à traiter.",
  },
  catalogue: {
    title: "Gestion du catalogue",
    breadcrumb: "Catalogue",
    description: "Créer, consulter, modifier et supprimer les ouvrages disponibles dans la bibliothèque.",
  },
  historique: {
    title: "Historique des utilisateurs",
    breadcrumb: "Historique utilisateurs",
    description: "Consulter l'historique complet des emprunts, retours, retards, pénalités et anomalies par utilisateur.",
  },
  emprunts: {
    title: "Validation des emprunts",
    breadcrumb: "Validation emprunts",
    description: "Vérifier et valider les demandes d'emprunt avant remise des ouvrages.",
  },
  retours: {
    title: "Validation des retours",
    breadcrumb: "Validation retours",
    description: "Contrôler les ouvrages retournés, vérifier l'état du livre et clôturer les emprunts.",
  },
  "penalites-anomalies": {
    title: "Pénalités & anomalies",
    breadcrumb: "Pénalités & anomalies",
    description: "Appliquer les pénalités, suivre les retards et signaler les anomalies sur les ouvrages.",
  },
};

const app = document.getElementById("app");
const toastRegion = document.getElementById("toast-region");
const topSearchForm = document.getElementById("topSearchForm");
const topSearch = document.getElementById("topSearch");
const navLinks = document.querySelectorAll("[data-nav-link]");

let books = [
  {
    id: "LIV-2039",
    title: "Introduction aux Bases de Données",
    author: "Nadia Alaoui",
    isbn: "978-2-212-00001-4",
    category: "Informatique",
    status: "Disponible",
    copies: "6/8",
    condition: "Bon état",
    lastMovement: "Retour vérifié le 12/10/2026",
  },
  {
    id: "LIV-2040",
    title: "Architecture des Systèmes d'Information",
    author: "Karim Belkacem",
    isbn: "978-2-7460-1234-8",
    category: "Systèmes d'information",
    status: "Emprunté",
    copies: "2/5",
    condition: "Bon état",
    lastMovement: "Emprunt vérifié le 18/10/2026",
  },
  {
    id: "LIV-2041",
    title: "Réseaux Informatiques",
    author: "Leila Martin",
    isbn: "978-2-212-00442-5",
    category: "Réseaux",
    status: "Disponible",
    copies: "4/6",
    condition: "Bon état",
    lastMovement: "Retour vérifié le 24/10/2026",
  },
  {
    id: "LIV-2042",
    title: "Algorithmique Avancée",
    author: "Sami El Khatib",
    isbn: "978-2-7460-2215-6",
    category: "Algorithmique",
    status: "En traitement",
    copies: "1/4",
    condition: "À contrôler",
    lastMovement: "Contrôle interne le 18/10/2026",
  },
  {
    id: "LIV-2043",
    title: "Génie Logiciel",
    author: "Amina Charif",
    isbn: "978-2-212-00990-0",
    category: "Génie logiciel",
    status: "Disponible",
    copies: "7/7",
    condition: "Bon état",
    lastMovement: "Ajout catalogue le 12/10/2026",
  },
  {
    id: "LIV-2044",
    title: "Intelligence Artificielle Appliquée",
    author: "Rachid Lahlou",
    isbn: "978-2-7460-8877-3",
    category: "Intelligence artificielle",
    status: "Endommagé",
    copies: "0/3",
    condition: "Couverture endommagée",
    lastMovement: "Anomalie signalée le 18/10/2026",
  },
];

let users = [
  {
    id: "USR-1024",
    name: "Adam Bennis",
    program: "Master Systèmes d'Information",
    totalLoans: 18,
    delays: 1,
    penalties: 1,
    damagedBooks: 0,
    lastActivity: "24/10/2026",
    status: "Actif",
    alertLevel: "Moyen",
    events: [
      { date: "24/10/2026", label: "Retour vérifié", book: "Réseaux Informatiques", status: "Vérifié" },
      { date: "18/10/2026", label: "Retard enregistré", book: "Réseaux Informatiques", status: "En retard" },
      { date: "18/10/2026", label: "Pénalité appliquée", book: "Réseaux Informatiques", status: "Pénalité" },
      { date: "12/10/2026", label: "Emprunt validé", book: "Introduction aux Bases de Données", status: "Vérifié" },
    ],
  },
  {
    id: "USR-1041",
    name: "Hajar Bennani",
    program: "Licence Informatique",
    totalLoans: 12,
    delays: 0,
    penalties: 0,
    damagedBooks: 0,
    lastActivity: "18/10/2026",
    status: "Actif",
    alertLevel: "Faible",
    events: [
      { date: "18/10/2026", label: "Emprunt validé", book: "Architecture des Systèmes d'Information", status: "Vérifié" },
      { date: "12/10/2026", label: "Retour vérifié", book: "Génie Logiciel", status: "Vérifié" },
    ],
  },
  {
    id: "USR-1062",
    name: "Yassine El Amrani",
    program: "Master Réseaux",
    totalLoans: 21,
    delays: 3,
    penalties: 2,
    damagedBooks: 1,
    lastActivity: "18/10/2026",
    status: "Sous suivi",
    alertLevel: "Critique",
    events: [
      { date: "18/10/2026", label: "Livre signalé endommagé", book: "Intelligence Artificielle Appliquée", status: "Endommagé" },
      { date: "18/10/2026", label: "Pénalité appliquée", book: "Algorithmique Avancée", status: "Pénalité" },
      { date: "12/10/2026", label: "Retard enregistré", book: "Algorithmique Avancée", status: "En retard" },
    ],
  },
  {
    id: "USR-1088",
    name: "Nour El Fassi",
    program: "Doctorat Sciences des données",
    totalLoans: 9,
    delays: 0,
    penalties: 0,
    damagedBooks: 0,
    lastActivity: "12/10/2026",
    status: "Actif",
    alertLevel: "Faible",
    events: [
      { date: "12/10/2026", label: "Emprunt validé", book: "Génie Logiciel", status: "Vérifié" },
      { date: "04/10/2026", label: "Retour vérifié", book: "Architecture des Systèmes d'Information", status: "Vérifié" },
    ],
  },
  {
    id: "USR-1117",
    name: "Anas El Idrissi",
    program: "Licence Génie logiciel",
    totalLoans: 15,
    delays: 2,
    penalties: 1,
    damagedBooks: 0,
    lastActivity: "24/10/2026",
    status: "Sous suivi",
    alertLevel: "Moyen",
    events: [
      { date: "24/10/2026", label: "Retard enregistré", book: "Architecture des Systèmes d'Information", status: "En retard" },
      { date: "18/10/2026", label: "Emprunt validé", book: "Réseaux Informatiques", status: "Vérifié" },
    ],
  },
  {
    id: "USR-1140",
    name: "Sofia El Mansouri",
    program: "Master Intelligence Artificielle",
    totalLoans: 17,
    delays: 1,
    penalties: 1,
    damagedBooks: 1,
    lastActivity: "18/10/2026",
    status: "Actif",
    alertLevel: "Moyen",
    events: [
      { date: "18/10/2026", label: "Livre signalé endommagé", book: "Intelligence Artificielle Appliquée", status: "Endommagé" },
      { date: "12/10/2026", label: "Retour vérifié", book: "Génie Logiciel", status: "Vérifié" },
    ],
  },
];

let borrowRequests = [
  {
    id: "EMP-8841",
    user: "Hajar Bennani",
    userId: "USR-1041",
    book: "Architecture des Systèmes d'Information",
    bookId: "LIV-2040",
    requestDate: "12/10/2026",
    availability: "Disponible",
    dueDate: "26/10/2026",
    status: "En attente",
    userDelays: 0,
  },
  {
    id: "EMP-8842",
    user: "Nour El Fassi",
    userId: "USR-1088",
    book: "Génie Logiciel",
    bookId: "LIV-2043",
    requestDate: "18/10/2026",
    availability: "Disponible",
    dueDate: "01/11/2026",
    status: "En attente",
    userDelays: 0,
  },
  {
    id: "EMP-8843",
    user: "Anas El Idrissi",
    userId: "USR-1117",
    book: "Réseaux Informatiques",
    bookId: "LIV-2041",
    requestDate: "18/10/2026",
    availability: "Disponible",
    dueDate: "01/11/2026",
    status: "En attente",
    userDelays: 2,
  },
  {
    id: "EMP-8844",
    user: "Yassine El Amrani",
    userId: "USR-1062",
    book: "Intelligence Artificielle Appliquée",
    bookId: "LIV-2044",
    requestDate: "24/10/2026",
    availability: "Indisponible",
    dueDate: "07/11/2026",
    status: "Refusé",
    userDelays: 3,
  },
];

let returnRequests = [
  {
    id: "RET-3207",
    borrower: "Adam Bennis",
    userId: "USR-1024",
    book: "Réseaux Informatiques",
    bookId: "LIV-2041",
    loanDate: "28/09/2026",
    expectedDate: "12/10/2026",
    returnDate: "18/10/2026",
    delay: "6 jours",
    condition: "Bon état",
    status: "À vérifier",
  },
  {
    id: "RET-3208",
    borrower: "Sofia El Mansouri",
    userId: "USR-1140",
    book: "Intelligence Artificielle Appliquée",
    bookId: "LIV-2044",
    loanDate: "04/10/2026",
    expectedDate: "18/10/2026",
    returnDate: "18/10/2026",
    delay: "Aucun",
    condition: "Endommagé",
    status: "À vérifier",
  },
  {
    id: "RET-3209",
    borrower: "Yassine El Amrani",
    userId: "USR-1062",
    book: "Algorithmique Avancée",
    bookId: "LIV-2042",
    loanDate: "24/09/2026",
    expectedDate: "08/10/2026",
    returnDate: "24/10/2026",
    delay: "16 jours",
    condition: "Pages manquantes",
    status: "À vérifier",
  },
  {
    id: "RET-3210",
    borrower: "Nour El Fassi",
    userId: "USR-1088",
    book: "Génie Logiciel",
    bookId: "LIV-2043",
    loanDate: "04/10/2026",
    expectedDate: "18/10/2026",
    returnDate: "18/10/2026",
    delay: "Aucun",
    condition: "Bon état",
    status: "Vérifié",
  },
];

let penalties = [
  {
    id: "PEN-7710",
    user: "Adam Bennis",
    userId: "USR-1024",
    reason: "Retard de retour",
    book: "Réseaux Informatiques",
    delay: "6 jours",
    amount: "60 MAD",
    status: "En attente",
  },
  {
    id: "PEN-7711",
    user: "Yassine El Amrani",
    userId: "USR-1062",
    reason: "Retard critique",
    book: "Algorithmique Avancée",
    delay: "16 jours",
    amount: "160 MAD",
    status: "En attente",
  },
  {
    id: "PEN-7712",
    user: "Sofia El Mansouri",
    userId: "USR-1140",
    reason: "Livre endommagé",
    book: "Intelligence Artificielle Appliquée",
    delay: "Aucun",
    amount: "220 MAD",
    status: "Appliquée",
  },
];

let anomalies = [
  {
    id: "ANO-5104",
    bookId: "LIV-2044",
    book: "Intelligence Artificielle Appliquée",
    reportedBy: "Sofia El Mansouri",
    type: "Livre endommagé",
    severity: "Critique",
    date: "18/10/2026",
    status: "Ouverte",
    description: "Couverture endommagée et plusieurs pages annotées.",
  },
  {
    id: "ANO-5105",
    bookId: "LIV-2042",
    book: "Algorithmique Avancée",
    reportedBy: "Yassine El Amrani",
    type: "Pages manquantes",
    severity: "Critique",
    date: "24/10/2026",
    status: "Ouverte",
    description: "Pages 115 à 120 absentes au retour.",
  },
];

let activities = [
  { time: "10:42", action: "Retour vérifié", user: "Nour El Fassi", book: "Génie Logiciel", status: "Vérifié" },
  { time: "10:18", action: "Pénalité appliquée", user: "Sofia El Mansouri", book: "Intelligence Artificielle Appliquée", status: "Pénalité" },
  { time: "09:55", action: "Livre signalé endommagé", user: "Yassine El Amrani", book: "Algorithmique Avancée", status: "Endommagé" },
  { time: "09:20", action: "Emprunt validé", user: "Hajar Bennani", book: "Architecture des Systèmes d'Information", status: "Vérifié" },
  { time: "08:50", action: "Retard enregistré", user: "Adam Bennis", book: "Réseaux Informatiques", status: "En retard" },
];

const state = {
  route: "dashboard",
  selectedBookId: "LIV-2039",
  selectedUserId: "USR-1024",
  selectedBorrowId: "EMP-8841",
  selectedReturnId: "RET-3207",
  catalogueMode: "view",
  editingBookId: null,
  anomalyPrefill: null,
  filters: {
    catalogueSearch: "",
    catalogueCategory: "",
    catalogueStatus: "",
    historySearch: "",
    historyStatus: "",
    historyAlert: "",
    borrowSearch: "",
    returnSearch: "",
    penaltySearch: "",
  },
};

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function normalizeText(value) {
  return String(value ?? "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();
}

function includesQuery(query, ...values) {
  const normalizedQuery = normalizeText(query).trim();
  if (!normalizedQuery) return true;
  return values.some((value) => normalizeText(value).includes(normalizedQuery));
}

function routeFromHash() {
  const hash = window.location.hash.replace("#", "");
  return routes[hash] ? hash : "dashboard";
}

function setRoute(route) {
  if (!routes[route]) return;
  if (routeFromHash() === route) {
    render();
  } else {
    window.location.hash = route;
  }
}

function selectedAttr(current, value) {
  return current === value ? " selected" : "";
}

function icon(name, className = "") {
  return `<span class="material-symbols-outlined ${className}" aria-hidden="true">${name}</span>`;
}

function statusClass(label) {
  const value = normalizeText(label);
  if (["disponible", "verifie", "bon etat", "appliquee", "traite", "actif", "faible"].includes(value)) {
    return "status-success";
  }
  if (["emprunte", "penalite", "moyen", "en traitement", "ouverte"].includes(value)) {
    return "status-gold";
  }
  if (["en retard", "indisponible", "a verifier", "sous suivi"].includes(value)) {
    return "status-warning";
  }
  if (["endommage", "critique", "refuse", "annulee", "pages manquantes"].includes(value)) {
    return "status-danger";
  }
  return "status-muted";
}

function statusPill(label) {
  return `<span class="status-pill ${statusClass(label)}">${escapeHtml(label)}</span>`;
}

function tableMarkup(headers, rows, emptyText = "Aucun résultat pour ces filtres.") {
  const head = headers
    .map((header) => {
      const item = typeof header === "string" ? { label: header } : header;
      return `<th scope="col"${item.className ? ` class="${item.className}"` : ""}>${escapeHtml(item.label)}</th>`;
    })
    .join("");
  const body = rows.length
    ? rows.join("")
    : `<tr><td class="empty-cell" colspan="${headers.length}">${escapeHtml(emptyText)}</td></tr>`;

  return `
    <div class="table-shell">
      <table>
        <thead><tr>${head}</tr></thead>
        <tbody>${body}</tbody>
      </table>
    </div>
  `;
}

function pageFrame(routeKey, content, actions = "") {
  const route = routes[routeKey];
  return `
    <nav class="breadcrumbs" aria-label="Fil d'Ariane">
      <a href="#dashboard">Accueil</a>
      ${icon("chevron_right")}
      <strong>${escapeHtml(route.breadcrumb)}</strong>
    </nav>
    <header class="page-heading">
      <div>
        <h1>${escapeHtml(route.title)}</h1>
        <p>${escapeHtml(route.description)}</p>
      </div>
      ${actions ? `<div class="page-actions">${actions}</div>` : ""}
    </header>
    ${content}
  `;
}

function countDelays() {
  return returnRequests.filter((item) => item.delay !== "Aucun" && item.status !== "Vérifié").length;
}

function damagedBookCount() {
  const damagedIds = new Set([
    ...books.filter((book) => book.status === "Endommagé").map((book) => book.id),
    ...anomalies.filter((item) => normalizeText(item.type).includes("endommage")).map((item) => item.bookId),
  ]);
  return damagedIds.size;
}

function addActivity(action, user, book, status) {
  activities.unshift({ time: "Maintenant", action, user, book, status });
  activities = activities.slice(0, 8);
}

function nextId(prefix, list) {
  const next = list.reduce((max, item) => {
    const number = Number(String(item.id).replace(`${prefix}-`, ""));
    return Number.isFinite(number) ? Math.max(max, number) : max;
  }, 0) + 1;
  return `${prefix}-${next}`;
}

function findBook(id) {
  return books.find((book) => book.id === id);
}

function findUser(id) {
  return users.find((user) => user.id === id);
}

function findBorrow(id) {
  return borrowRequests.find((request) => request.id === id);
}

function findReturn(id) {
  return returnRequests.find((request) => request.id === id);
}

function renderKpi(label, value, iconName, note) {
  return `
    <article class="kpi-card">
      <span class="kpi-label">${escapeHtml(label)}</span>
      ${icon(iconName)}
      <strong class="kpi-value">${escapeHtml(value)}</strong>
      <span class="kpi-note">${escapeHtml(note)}</span>
    </article>
  `;
}

function renderDashboard() {
  const borrowPending = borrowRequests.filter((item) => item.status === "En attente").length;
  const returnPending = returnRequests.filter((item) => item.status === "À vérifier").length;
  const penaltyPending = penalties.filter((item) => item.status === "En attente").length;
  const currentLoans = books.filter((book) => book.status === "Emprunté").length + borrowRequests.filter((item) => item.status === "Vérifié").length;

  const kpis = [
    renderKpi("Emprunts en cours", currentLoans, "local_library", "Flux actif"),
    renderKpi("Emprunts à vérifier", borrowPending, "assignment", "Demandes ouvertes"),
    renderKpi("Retours à vérifier", returnPending, "fact_check", "Contrôles du jour"),
    renderKpi("Retards actifs", countDelays(), "schedule", "À suivre"),
    renderKpi("Livres endommagés", damagedBookCount(), "report", "Contrôle requis"),
    renderKpi("Pénalités en attente", penaltyPending, "gavel", "Application requise"),
  ].join("");

  const activityRows = activities.map((item) => `
    <tr>
      <td class="nowrap">${escapeHtml(item.time)}</td>
      <td>${escapeHtml(item.action)}</td>
      <td>${escapeHtml(item.user)}</td>
      <td>${escapeHtml(item.book)}</td>
      <td>${statusPill(item.status)}</td>
    </tr>
  `);

  const content = `
    <section class="kpi-grid" aria-label="Indicateurs opérationnels">${kpis}</section>

    <div class="dashboard-grid">
      <div class="dashboard-column">
        <section class="card">
          <div class="card-header">
            <div>
              <h2>Alertes opérationnelles</h2>
              <p>Points à traiter pendant la permanence.</p>
            </div>
            <span class="meta-label">Aujourd'hui</span>
          </div>
          <div class="alert-stack">
            <article class="alert-row">
              ${icon("schedule")}
              <div>
                <strong>Retours en retard</strong>
                <span>Adam Bennis et Yassine El Amrani ont des retours dépassant la date prévue.</span>
              </div>
              ${statusPill("En retard")}
            </article>
            <article class="alert-row">
              ${icon("report")}
              <div>
                <strong>Livres signalés endommagés</strong>
                <span>Intelligence Artificielle Appliquée et Algorithmique Avancée nécessitent un contrôle.</span>
              </div>
              ${statusPill("Endommagé")}
            </article>
            <article class="alert-row">
              ${icon("assignment_turned_in")}
              <div>
                <strong>Emprunts en attente de validation</strong>
                <span>${borrowPending} demandes attendent une décision bibliothécaire.</span>
              </div>
              ${statusPill("En attente")}
            </article>
          </div>
        </section>

        <section class="card">
          <div class="card-header">
            <div>
              <h2>Activité récente</h2>
              <p>Dernières opérations enregistrées au comptoir.</p>
            </div>
          </div>
          ${tableMarkup(["Heure", "Action", "Utilisateur", "Livre", "Statut"], activityRows, "Aucune activité récente.")}
        </section>
      </div>

      <div class="dashboard-column">
        <section class="card">
          <div class="card-header">
            <h2>Actions rapides</h2>
          </div>
          <div class="quick-actions">
            <button type="button" class="btn btn-primary" data-action="quick-add-book">${icon("library_add")}Ajouter un livre</button>
            <button type="button" class="btn btn-dark" data-action="navigate" data-route="emprunts">${icon("assignment_turned_in")}Vérifier un emprunt</button>
            <button type="button" class="btn btn-secondary" data-action="navigate" data-route="retours">${icon("fact_check")}Vérifier un retour</button>
            <button type="button" class="btn btn-secondary" data-action="quick-anomaly">${icon("report")}Signaler anomalie</button>
          </div>
        </section>

        <section class="card">
          <div class="card-header">
            <h2>Tâches en attente</h2>
          </div>
          <div class="task-list">
            <article class="task-row">${icon("assignment")}<div><strong>3 emprunts à vérifier</strong><span>Priorité comptoir</span></div>${statusPill("En attente")}</article>
            <article class="task-row">${icon("fact_check")}<div><strong>2 retours à vérifier</strong><span>Contrôle d'état requis</span></div>${statusPill("À vérifier")}</article>
            <article class="task-row">${icon("report")}<div><strong>1 anomalie livre</strong><span>Signalement à compléter</span></div>${statusPill("Endommagé")}</article>
          </div>
        </section>

        <section class="card chart-card">
          <div class="card-header">
            <h2>Emprunts hebdomadaires</h2>
          </div>
          <div class="bar-chart" aria-label="Barres des emprunts hebdomadaires">
            ${[
              ["Lun", 46],
              ["Mar", 58],
              ["Mer", 70],
              ["Jeu", 64],
              ["Ven", 82],
              ["Sam", 38],
              ["Dim", 22],
            ].map(([day, height], index) => `
              <div class="bar-item">
                <span class="bar ${index === 4 ? "is-highlight" : ""}" style="height:${height}%"></span>
                <span class="bar-label">${day}</span>
              </div>
            `).join("")}
          </div>
        </section>
      </div>
    </div>
  `;

  return pageFrame("dashboard", content);
}

function renderCatalogue() {
  const categories = [...new Set(books.map((book) => book.category))];
  const statuses = ["Disponible", "Emprunté", "En traitement", "Endommagé"];
  const filteredBooks = books.filter((book) => {
    const matchesSearch = includesQuery(state.filters.catalogueSearch, book.title, book.author, book.isbn, book.id);
    const matchesCategory = !state.filters.catalogueCategory || book.category === state.filters.catalogueCategory;
    const matchesStatus = !state.filters.catalogueStatus || book.status === state.filters.catalogueStatus;
    return matchesSearch && matchesCategory && matchesStatus;
  });

  const rows = filteredBooks.map((book) => `
    <tr>
      <td class="identifier">${escapeHtml(book.id)}</td>
      <td><div class="table-title"><strong>${escapeHtml(book.title)}</strong><span>${escapeHtml(book.author)}</span></div></td>
      <td>${escapeHtml(book.author)}</td>
      <td class="identifier">${escapeHtml(book.isbn)}</td>
      <td>${escapeHtml(book.category)}</td>
      <td>${statusPill(book.status)}</td>
      <td>${escapeHtml(book.copies)}</td>
      <td>
        <div class="table-actions">
          <button type="button" class="btn btn-secondary btn-small" data-action="select-book" data-id="${escapeHtml(book.id)}">${icon("visibility")}Consulter</button>
          <button type="button" class="btn btn-secondary btn-small" data-action="edit-book" data-id="${escapeHtml(book.id)}">${icon("edit")}Modifier</button>
          <button type="button" class="btn btn-danger btn-small" data-action="delete-book" data-id="${escapeHtml(book.id)}">${icon("delete")}Supprimer</button>
        </div>
      </td>
    </tr>
  `);

  const selectedBook = findBook(state.selectedBookId) || books[0];
  const detail = state.catalogueMode === "view" ? renderBookDetail(selectedBook) : renderBookForm();

  const content = `
    <div class="toolbar-row">
      <label class="field">
        <span>Recherche</span>
        <span class="input-with-icon">
          ${icon("search")}
          <input type="search" data-filter="catalogueSearch" value="${escapeHtml(state.filters.catalogueSearch)}" placeholder="Rechercher par titre, auteur ou ISBN">
        </span>
      </label>
      <label class="field">
        <span>Catégorie</span>
        <select data-filter="catalogueCategory">
          <option value="">Toutes catégories</option>
          ${categories.map((category) => `<option value="${escapeHtml(category)}"${selectedAttr(state.filters.catalogueCategory, category)}>${escapeHtml(category)}</option>`).join("")}
        </select>
      </label>
      <label class="field">
        <span>Statut</span>
        <select data-filter="catalogueStatus">
          <option value="">Tous les statuts</option>
          ${statuses.map((status) => `<option value="${escapeHtml(status)}"${selectedAttr(state.filters.catalogueStatus, status)}>${escapeHtml(status)}</option>`).join("")}
        </select>
      </label>
      <button type="button" class="btn btn-primary" data-action="start-create-book">${icon("add")}Ajouter un livre</button>
    </div>

    <div class="layout-two">
      <section class="card">
        <div class="card-header">
          <div>
            <h2>Ouvrages du catalogue</h2>
            <p>${filteredBooks.length} ouvrage(s) affiché(s)</p>
          </div>
        </div>
        ${tableMarkup(["ID", "Titre", "Auteur", "ISBN", "Catégorie", "Statut", "Exemplaires", { label: "Actions", className: "text-right" }], rows)}
      </section>

      <aside class="card">
        ${detail}
      </aside>
    </div>
  `;

  return pageFrame("catalogue", content);
}

function renderBookDetail(book) {
  if (!book) {
    return `<div class="empty-state">Aucun ouvrage sélectionné.</div>`;
  }

  return `
    <div class="card-header">
      <div>
        <h2>Détails de l'ouvrage</h2>
        <p>Aperçu de l'ouvrage sélectionné.</p>
      </div>
      ${statusPill(book.status)}
    </div>
    <dl class="detail-list">
      <div class="detail-row"><dt>Titre</dt><dd>${escapeHtml(book.title)}</dd></div>
      <div class="detail-row"><dt>Auteur</dt><dd>${escapeHtml(book.author)}</dd></div>
      <div class="detail-row"><dt>ISBN</dt><dd class="identifier">${escapeHtml(book.isbn)}</dd></div>
      <div class="detail-row"><dt>Disponibilité</dt><dd>${statusPill(book.status)} <span class="meta-label">${escapeHtml(book.copies)}</span></dd></div>
      <div class="detail-row"><dt>État</dt><dd>${escapeHtml(book.condition)}</dd></div>
      <div class="detail-row"><dt>Dernier mouvement</dt><dd>${escapeHtml(book.lastMovement)}</dd></div>
    </dl>
  `;
}

function renderBookForm() {
  const isEdit = state.catalogueMode === "edit";
  const book = isEdit ? findBook(state.editingBookId) : null;
  const values = book || {
    title: "",
    author: "",
    isbn: "",
    category: "Informatique",
    status: "Disponible",
    copies: "1/1",
    condition: "Bon état",
    lastMovement: "Ajout catalogue en cours",
  };

  return `
    <div class="card-header">
      <div>
        <h2>${isEdit ? "Modifier l'ouvrage" : "Ajouter un livre"}</h2>
        <p>${isEdit ? "Mettre à jour les informations du catalogue." : "Créer une nouvelle fiche d'ouvrage."}</p>
      </div>
    </div>
    <form class="form-stack" data-form="book">
      <div class="form-grid">
        <label class="field">
          <span>Titre</span>
          <input name="title" required value="${escapeHtml(values.title)}">
        </label>
        <label class="field">
          <span>Auteur</span>
          <input name="author" required value="${escapeHtml(values.author)}">
        </label>
        <label class="field">
          <span>ISBN</span>
          <input name="isbn" required value="${escapeHtml(values.isbn)}">
        </label>
        <label class="field">
          <span>Catégorie</span>
          <select name="category">
            ${["Informatique", "Systèmes d'information", "Réseaux", "Algorithmique", "Génie logiciel", "Intelligence artificielle"].map((category) => `<option value="${escapeHtml(category)}"${selectedAttr(values.category, category)}>${escapeHtml(category)}</option>`).join("")}
          </select>
        </label>
        <label class="field">
          <span>Statut</span>
          <select name="status">
            ${["Disponible", "Emprunté", "En traitement", "Endommagé"].map((status) => `<option value="${escapeHtml(status)}"${selectedAttr(values.status, status)}>${escapeHtml(status)}</option>`).join("")}
          </select>
        </label>
        <label class="field">
          <span>Exemplaires</span>
          <input name="copies" required value="${escapeHtml(values.copies)}">
        </label>
      </div>
      <label class="field">
        <span>État du livre</span>
        <input name="condition" required value="${escapeHtml(values.condition)}">
      </label>
      <label class="field">
        <span>Dernier mouvement</span>
        <input name="lastMovement" required value="${escapeHtml(values.lastMovement)}">
      </label>
      <div class="form-actions">
        <button type="button" class="btn btn-secondary" data-action="cancel-book-form">Annuler</button>
        <button type="submit" class="btn btn-primary">${icon("save")}Enregistrer</button>
      </div>
    </form>
  `;
}

function renderHistorique() {
  const filteredUsers = users.filter((user) => {
    const matchesSearch = includesQuery(state.filters.historySearch, user.id, user.name, user.program);
    const matchesStatus = !state.filters.historyStatus || user.status === state.filters.historyStatus;
    const matchesAlert = !state.filters.historyAlert || user.alertLevel === state.filters.historyAlert;
    return matchesSearch && matchesStatus && matchesAlert;
  });
  const selectedUser = findUser(state.selectedUserId) || users[0];

  const rows = filteredUsers.map((user) => `
    <tr>
      <td class="identifier">${escapeHtml(user.id)}</td>
      <td><div class="table-title"><strong>${escapeHtml(user.name)}</strong><span>${escapeHtml(user.program)}</span></div></td>
      <td>${escapeHtml(user.totalLoans)}</td>
      <td>${escapeHtml(user.delays)}</td>
      <td>${escapeHtml(user.penalties)}</td>
      <td>${escapeHtml(user.damagedBooks)}</td>
      <td>${escapeHtml(user.lastActivity)}</td>
      <td>
        <div class="table-actions">
          <button type="button" class="btn btn-secondary btn-small" data-action="select-user" data-id="${escapeHtml(user.id)}">${icon("visibility")}Voir historique complet</button>
          <button type="button" class="btn btn-secondary btn-small" data-action="view-user-penalties" data-id="${escapeHtml(user.id)}">${icon("gavel")}Voir pénalités</button>
          <button type="button" class="btn btn-secondary btn-small" data-action="view-user-incidents" data-id="${escapeHtml(user.id)}">${icon("report")}Voir incidents</button>
        </div>
      </td>
    </tr>
  `);

  const content = `
    <div class="toolbar-row compact">
      <label class="field">
        <span>Recherche</span>
        <span class="input-with-icon">
          ${icon("search")}
          <input type="search" data-filter="historySearch" value="${escapeHtml(state.filters.historySearch)}" placeholder="Rechercher un utilisateur">
        </span>
      </label>
      <label class="field">
        <span>Statut</span>
        <select data-filter="historyStatus">
          <option value="">Tous les statuts</option>
          ${["Actif", "Sous suivi"].map((status) => `<option value="${escapeHtml(status)}"${selectedAttr(state.filters.historyStatus, status)}>${escapeHtml(status)}</option>`).join("")}
        </select>
      </label>
      <label class="field">
        <span>Niveau d'alerte</span>
        <select data-filter="historyAlert">
          <option value="">Tous les niveaux</option>
          ${["Faible", "Moyen", "Critique"].map((level) => `<option value="${escapeHtml(level)}"${selectedAttr(state.filters.historyAlert, level)}>${escapeHtml(level)}</option>`).join("")}
        </select>
      </label>
      <button type="button" class="btn btn-secondary" data-action="export-history">${icon("download")}Exporter l'historique</button>
    </div>

    <div class="layout-two">
      <section class="card">
        <div class="card-header">
          <div>
            <h2>Historique par utilisateur</h2>
            <p>${filteredUsers.length} profil(s) consultable(s)</p>
          </div>
        </div>
        ${tableMarkup(["ID utilisateur", "Nom", "Emprunts totaux", "Retards", "Pénalités", "Livres endommagés", "Dernière activité", { label: "Actions", className: "text-right" }], rows)}
      </section>

      <aside class="card history-panel">
        ${renderUserHistory(selectedUser)}
      </aside>
    </div>
  `;

  return pageFrame("historique", content);
}

function renderUserHistory(user) {
  if (!user) {
    return `<div class="empty-state">Aucun utilisateur sélectionné.</div>`;
  }

  const timeline = user.events.map((event) => `
    <article class="timeline-row">
      ${icon("radio_button_checked")}
      <div>
        <strong>${escapeHtml(event.label)}</strong>
        <span>${escapeHtml(event.book)}</span>
      </div>
      <div class="nowrap">
        <time>${escapeHtml(event.date)}</time>
        ${statusPill(event.status)}
      </div>
    </article>
  `).join("");

  return `
    <div class="card-header">
      <div>
        <h2>Historique complet</h2>
        <p>${escapeHtml(user.name)} - ${escapeHtml(user.id)}</p>
      </div>
      ${statusPill(user.alertLevel)}
    </div>
    <div class="history-metrics">
      <div class="history-metric"><span>Emprunts passés</span><strong>${escapeHtml(user.totalLoans)}</strong></div>
      <div class="history-metric"><span>Retours validés</span><strong>${escapeHtml(Math.max(user.totalLoans - user.delays, 0))}</strong></div>
      <div class="history-metric"><span>Retards</span><strong>${escapeHtml(user.delays)}</strong></div>
      <div class="history-metric"><span>Incidents</span><strong>${escapeHtml(user.damagedBooks)}</strong></div>
    </div>
    <dl class="detail-list">
      <div class="detail-row"><dt>Pénalités appliquées</dt><dd>${escapeHtml(user.penalties)}</dd></div>
      <div class="detail-row"><dt>Incidents de livres endommagés</dt><dd>${escapeHtml(user.damagedBooks)}</dd></div>
      <div class="detail-row"><dt>Dernière activité</dt><dd>${escapeHtml(user.lastActivity)}</dd></div>
    </dl>
    <div class="timeline">${timeline}</div>
  `;
}

function renderEmprunts() {
  const filteredRequests = borrowRequests.filter((request) =>
    includesQuery(state.filters.borrowSearch, request.id, request.user, request.book, request.bookId, request.status)
  );
  const selected = findBorrow(state.selectedBorrowId) || borrowRequests[0];

  const rows = filteredRequests.map((request) => `
    <tr>
      <td class="identifier">${escapeHtml(request.id)}</td>
      <td><div class="table-title"><strong>${escapeHtml(request.user)}</strong><span>${escapeHtml(request.userId)}</span></div></td>
      <td>${escapeHtml(request.book)}</td>
      <td>${escapeHtml(request.requestDate)}</td>
      <td>${statusPill(request.availability)}</td>
      <td>${escapeHtml(request.dueDate)}</td>
      <td>${statusPill(request.status)}</td>
      <td>
        <div class="table-actions">
          <button type="button" class="btn btn-primary btn-small" data-action="verify-borrow" data-id="${escapeHtml(request.id)}" ${request.status === "Vérifié" ? "disabled" : ""}>${icon("check_circle")}Emprunt vérifié</button>
          <button type="button" class="btn btn-secondary btn-small" data-action="refuse-borrow" data-id="${escapeHtml(request.id)}" ${request.status === "Vérifié" ? "disabled" : ""}>${icon("block")}Refuser</button>
          <button type="button" class="btn btn-secondary btn-small" data-action="borrow-user-profile" data-id="${escapeHtml(request.userId)}">${icon("person")}Profil utilisateur</button>
          <button type="button" class="btn btn-secondary btn-small" data-action="borrow-book-details" data-id="${escapeHtml(request.bookId)}">${icon("menu_book")}Détails livre</button>
        </div>
      </td>
    </tr>
  `);

  const content = `
    <section class="summary-strip" aria-label="Synthèse des emprunts">
      ${renderSummaryCard("Demandes en attente", borrowRequests.filter((item) => item.status === "En attente").length, "assignment")}
      ${renderSummaryCard("Emprunts vérifiés aujourd'hui", borrowRequests.filter((item) => item.status === "Vérifié").length, "check_circle")}
      ${renderSummaryCard("Livres indisponibles", borrowRequests.filter((item) => item.availability === "Indisponible").length, "block")}
      ${renderSummaryCard("Utilisateurs avec retard", borrowRequests.filter((item) => item.userDelays > 0).length, "schedule")}
    </section>

    <div class="layout-two">
      <section class="card">
        <div class="card-header">
          <div>
            <h2>Demandes d'emprunt</h2>
            <p>${filteredRequests.length} demande(s) affichée(s)</p>
          </div>
        </div>
        ${tableMarkup(["ID demande", "Utilisateur", "Livre", "Date demande", "Disponibilité", "Date retour prévue", "Statut", { label: "Actions", className: "text-right" }], rows)}
      </section>

      <aside class="card validation-detail">
        ${renderBorrowDetail(selected)}
      </aside>
    </div>
  `;

  return pageFrame("emprunts", content);
}

function renderSummaryCard(label, value, iconName) {
  return `
    <article class="summary-card">
      <span>${escapeHtml(label)}</span>
      ${icon(iconName)}
      <strong>${escapeHtml(value)}</strong>
    </article>
  `;
}

function renderBorrowDetail(request) {
  if (!request) {
    return `<div class="empty-state">Aucune demande sélectionnée.</div>`;
  }

  const user = findUser(request.userId);
  const book = findBook(request.bookId);

  return `
    <div class="card-header">
      <div>
        <h2>Détail de validation</h2>
        <p>${escapeHtml(request.id)}</p>
      </div>
      ${statusPill(request.status)}
    </div>
    <dl class="detail-list">
      <div class="detail-row"><dt>Identité utilisateur</dt><dd>${escapeHtml(request.user)}<br><span class="identifier">${escapeHtml(request.userId)}</span></dd></div>
      <div class="detail-row"><dt>Livre demandé</dt><dd>${escapeHtml(request.book)}<br><span class="identifier">${escapeHtml(request.bookId)}</span></dd></div>
      <div class="detail-row"><dt>Disponibilité</dt><dd>${statusPill(request.availability)} ${book ? `<span class="meta-label">${escapeHtml(book.copies)}</span>` : ""}</dd></div>
      <div class="detail-row"><dt>Retards utilisateur</dt><dd>${escapeHtml(user ? user.delays : request.userDelays)}</dd></div>
      <div class="detail-row"><dt>Date retour recommandée</dt><dd>${escapeHtml(request.dueDate)}</dd></div>
    </dl>
    <label class="field note-field">
      <span>Notes</span>
      <textarea placeholder="Notes du bibliothécaire">${request.userDelays > 0 ? "Vérifier les retards actifs avant remise." : ""}</textarea>
    </label>
  `;
}

function renderRetours() {
  const filteredReturns = returnRequests.filter((request) =>
    includesQuery(state.filters.returnSearch, request.id, request.borrower, request.book, request.condition, request.status)
  );
  const selected = findReturn(state.selectedReturnId) || returnRequests[0];

  const rows = filteredReturns.map((request) => `
    <tr>
      <td class="identifier">${escapeHtml(request.id)}</td>
      <td><div class="table-title"><strong>${escapeHtml(request.borrower)}</strong><span>${escapeHtml(request.userId)}</span></div></td>
      <td>${escapeHtml(request.book)}</td>
      <td>${escapeHtml(request.loanDate)}</td>
      <td>${escapeHtml(request.expectedDate)}</td>
      <td>${escapeHtml(request.returnDate)}</td>
      <td>${request.delay === "Aucun" ? statusPill("Bon état") : statusPill("En retard")} <span class="meta-label">${escapeHtml(request.delay)}</span></td>
      <td>${statusPill(request.condition)}</td>
      <td>
        <div class="table-actions">
          <button type="button" class="btn btn-primary btn-small" data-action="verify-return" data-id="${escapeHtml(request.id)}" ${request.status === "Vérifié" ? "disabled" : ""}>${icon("check_circle")}Retour vérifié</button>
          <button type="button" class="btn btn-secondary btn-small" data-action="report-return-anomaly" data-id="${escapeHtml(request.id)}">${icon("report")}Signaler anomalie</button>
          <button type="button" class="btn btn-secondary btn-small" data-action="create-return-penalty" data-id="${escapeHtml(request.id)}">${icon("gavel")}Appliquer pénalité</button>
          <button type="button" class="btn btn-secondary btn-small" data-action="return-history" data-id="${escapeHtml(request.userId)}">${icon("manage_search")}Voir historique</button>
        </div>
      </td>
    </tr>
  `);

  const content = `
    <section class="summary-strip" aria-label="Synthèse des retours">
      ${renderSummaryCard("Retours en attente", returnRequests.filter((item) => item.status === "À vérifier").length, "fact_check")}
      ${renderSummaryCard("Retours vérifiés aujourd'hui", returnRequests.filter((item) => item.status === "Vérifié").length, "check_circle")}
      ${renderSummaryCard("Retours en retard", countDelays(), "schedule")}
      ${renderSummaryCard("Livres à contrôler", returnRequests.filter((item) => item.condition !== "Bon état").length, "report")}
    </section>

    <div class="layout-two">
      <section class="card">
        <div class="card-header">
          <div>
            <h2>Retours à contrôler</h2>
            <p>${filteredReturns.length} retour(s) affiché(s)</p>
          </div>
        </div>
        ${tableMarkup(["ID retour", "Emprunteur", "Livre", "Date emprunt", "Retour prévu", "Date retour", "Retard", "État du livre", { label: "Actions", className: "text-right" }], rows)}
      </section>

      <aside class="card validation-detail">
        ${renderReturnInspection(selected)}
      </aside>
    </div>
  `;

  return pageFrame("retours", content);
}

function renderReturnInspection(request) {
  if (!request) {
    return `<div class="empty-state">Aucun retour sélectionné.</div>`;
  }

  return `
    <div class="card-header">
      <div>
        <h2>Contrôle du retour</h2>
        <p>${escapeHtml(request.id)} - ${escapeHtml(request.book)}</p>
      </div>
      ${statusPill(request.status)}
    </div>
    <dl class="detail-list">
      <div class="detail-row"><dt>Emprunteur</dt><dd>${escapeHtml(request.borrower)}</dd></div>
      <div class="detail-row"><dt>Retour prévu</dt><dd>${escapeHtml(request.expectedDate)}</dd></div>
      <div class="detail-row"><dt>Retard</dt><dd>${escapeHtml(request.delay)}</dd></div>
      <div class="detail-row"><dt>État actuel</dt><dd>${statusPill(request.condition)}</dd></div>
    </dl>
    <div class="form-stack note-field">
      <label class="field">
        <span>Condition du livre</span>
        <select>
          ${["Aucun dommage", "Pages manquantes", "Annotations", "Couverture endommagée"].map((condition) => `<option${selectedAttr(request.condition === "Bon état" ? "Aucun dommage" : request.condition, condition)}>${escapeHtml(condition)}</option>`).join("")}
        </select>
      </label>
      <div class="check-group">
        <span>Points contrôlés</span>
        <div class="check-list">
          <label><input type="checkbox" ${request.condition === "Bon état" ? "checked" : ""}>Aucun dommage</label>
          <label><input type="checkbox" ${request.condition === "Pages manquantes" ? "checked" : ""}>Pages manquantes</label>
          <label><input type="checkbox" ${request.condition === "Annotations" ? "checked" : ""}>Annotations</label>
          <label><input type="checkbox" ${request.condition === "Endommagé" ? "checked" : ""}>Livre endommagé</label>
        </div>
      </div>
      <label class="field">
        <span>Notes du bibliothécaire</span>
        <textarea placeholder="Notes de contrôle">${request.condition !== "Bon état" ? "Contrôle complémentaire recommandé." : ""}</textarea>
      </label>
      <button type="button" class="btn btn-secondary" data-action="save-return-inspection">${icon("save")}Enregistrer le contrôle</button>
    </div>
  `;
}

function renderPenalites() {
  const filteredPenalties = penalties.filter((penalty) =>
    includesQuery(state.filters.penaltySearch, penalty.id, penalty.user, penalty.reason, penalty.book, penalty.status)
  );

  const penaltyRows = filteredPenalties.map((penalty) => `
    <tr>
      <td class="identifier">${escapeHtml(penalty.id)}</td>
      <td><div class="table-title"><strong>${escapeHtml(penalty.user)}</strong><span>${escapeHtml(penalty.userId)}</span></div></td>
      <td>${escapeHtml(penalty.reason)}</td>
      <td>${escapeHtml(penalty.book)}</td>
      <td>${penalty.delay === "Aucun" ? escapeHtml(penalty.delay) : statusPill(penalty.delay.includes("16") ? "Critique" : "En retard")} <span class="meta-label">${escapeHtml(penalty.delay)}</span></td>
      <td class="amount">${escapeHtml(penalty.amount)}</td>
      <td>${statusPill(penalty.status)}</td>
      <td>
        <div class="table-actions">
          <button type="button" class="btn btn-primary btn-small" data-action="apply-penalty" data-id="${escapeHtml(penalty.id)}" ${penalty.status === "Appliquée" ? "disabled" : ""}>${icon("gavel")}Appliquer pénalité</button>
          <button type="button" class="btn btn-secondary btn-small" data-action="history-from-penalty" data-id="${escapeHtml(penalty.userId)}">${icon("manage_search")}Voir historique</button>
          <button type="button" class="btn btn-secondary btn-small" data-action="cancel-penalty" data-id="${escapeHtml(penalty.id)}">${icon("close")}Annuler</button>
        </div>
      </td>
    </tr>
  `);

  const anomalyRows = anomalies.map((anomaly) => `
    <tr>
      <td class="identifier">${escapeHtml(anomaly.id)}</td>
      <td><div class="table-title"><strong>${escapeHtml(anomaly.book)}</strong><span>${escapeHtml(anomaly.bookId)}</span></div></td>
      <td>${escapeHtml(anomaly.reportedBy)}</td>
      <td>${escapeHtml(anomaly.type)}</td>
      <td>${statusPill(anomaly.severity)}</td>
      <td>${escapeHtml(anomaly.date)}</td>
      <td>${statusPill(anomaly.status)}</td>
      <td>
        <div class="table-actions">
          <button type="button" class="btn btn-secondary btn-small" data-action="prefill-anomaly" data-id="${escapeHtml(anomaly.id)}">${icon("report")}Signaler anomalie</button>
          <button type="button" class="btn btn-primary btn-small" data-action="mark-anomaly-treated" data-id="${escapeHtml(anomaly.id)}" ${anomaly.status === "Traité" ? "disabled" : ""}>${icon("done")}Marquer traité</button>
          <button type="button" class="btn btn-secondary btn-small" data-action="anomaly-details" data-id="${escapeHtml(anomaly.id)}">${icon("visibility")}Détails</button>
        </div>
      </td>
    </tr>
  `);

  const content = `
    <section class="summary-strip" aria-label="Synthèse des pénalités et anomalies">
      ${renderSummaryCard("Pénalités en attente", penalties.filter((item) => item.status === "En attente").length, "gavel")}
      ${renderSummaryCard("Montant total", totalPenaltyAmount(), "payments")}
      ${renderSummaryCard("Livres endommagés", damagedBookCount(), "report")}
      ${renderSummaryCard("Retards critiques", penalties.filter((item) => normalizeText(item.reason).includes("critique")).length, "priority_high")}
    </section>

    <div class="layout-balanced">
      <section class="card">
        <div class="card-header">
          <div>
            <h2>Pénalités</h2>
            <p>Retards et montants à appliquer.</p>
          </div>
        </div>
        ${tableMarkup(["ID", "Utilisateur", "Motif", "Livre", "Retard", "Montant", "Statut", { label: "Actions", className: "text-right" }], penaltyRows)}
      </section>

      <section class="card">
        <div class="card-header">
          <div>
            <h2>Signalements d'anomalies</h2>
            <p>Suivi des livres endommagés et anomalies matérielles.</p>
          </div>
        </div>
        ${tableMarkup(["ID anomalie", "Livre", "Signalé par", "Type anomalie", "Gravité", "Date", "Statut", { label: "Actions", className: "text-right" }], anomalyRows)}
      </section>
    </div>

    <section class="card note-field">
      ${renderAnomalyForm()}
    </section>
  `;

  return pageFrame("penalites-anomalies", content);
}

function totalPenaltyAmount() {
  const total = penalties
    .filter((penalty) => penalty.status !== "Annulée")
    .reduce((sum, penalty) => sum + Number.parseInt(penalty.amount, 10), 0);
  return `${total} MAD`;
}

function renderAnomalyForm() {
  const prefill = state.anomalyPrefill || {};
  return `
    <div class="card-header">
      <div>
        <h2>Signaler une anomalie</h2>
        <p>Déclaration bibliothécaire liée à un ouvrage.</p>
      </div>
    </div>
    <form class="form-stack" data-form="anomaly">
      <div class="form-grid">
        <label class="field">
          <span>ID livre</span>
          <input name="bookId" required value="${escapeHtml(prefill.bookId || "")}" placeholder="LIV-2039">
        </label>
        <label class="field">
          <span>Utilisateur concerné</span>
          <input name="reportedBy" required value="${escapeHtml(prefill.reportedBy || "")}" placeholder="Nom utilisateur">
        </label>
        <label class="field">
          <span>Type d'anomalie</span>
          <select name="type">
            ${["Livre endommagé", "Pages manquantes", "Annotations au stylo", "Couverture déchirée", "Code-barres illisible"].map((type) => `<option value="${escapeHtml(type)}"${selectedAttr(prefill.type || "Livre endommagé", type)}>${escapeHtml(type)}</option>`).join("")}
          </select>
        </label>
        <label class="field">
          <span>Gravité</span>
          <select name="severity">
            ${["Faible", "Moyen", "Critique"].map((level) => `<option value="${escapeHtml(level)}"${selectedAttr(prefill.severity || "Moyen", level)}>${escapeHtml(level)}</option>`).join("")}
          </select>
        </label>
        <label class="field">
          <span>État du livre</span>
          <select name="condition">
            ${["Bon état", "À contrôler", "Endommagé", "Pages manquantes"].map((condition) => `<option value="${escapeHtml(condition)}"${selectedAttr(prefill.condition || "À contrôler", condition)}>${escapeHtml(condition)}</option>`).join("")}
          </select>
        </label>
      </div>
      <label class="field">
        <span>Description</span>
        <textarea name="description" required placeholder="Description concise de l'anomalie">${escapeHtml(prefill.description || "")}</textarea>
      </label>
      <div class="form-actions">
        <button type="button" class="btn btn-secondary" data-action="declare-damaged">${icon("report")}Déclarer livre endommagé</button>
        <button type="submit" class="btn btn-primary">${icon("add")}Signaler anomalie</button>
      </div>
    </form>
  `;
}

function render() {
  state.route = routeFromHash();
  document.title = `${routes[state.route].title} - Smart Library`;

  navLinks.forEach((link) => {
    const isActive = link.dataset.navLink === state.route;
    link.classList.toggle("active", isActive);
    const iconNode = link.querySelector(".material-symbols-outlined");
    if (iconNode) iconNode.classList.toggle("filled", isActive);
    if (isActive) {
      link.setAttribute("aria-current", "page");
    } else {
      link.removeAttribute("aria-current");
    }
  });

  const renderers = {
    dashboard: renderDashboard,
    catalogue: renderCatalogue,
    historique: renderHistorique,
    emprunts: renderEmprunts,
    retours: renderRetours,
    "penalites-anomalies": renderPenalites,
  };

  app.innerHTML = renderers[state.route]();
  window.scrollTo({ top: 0, behavior: "auto" });
}

function renderWithFocus(filterKey, selectionStart, selectionEnd) {
  render();
  requestAnimationFrame(() => {
    const field = document.querySelector(`[data-filter="${filterKey}"]`);
    if (!field) return;
    field.focus();
    if (typeof field.setSelectionRange === "function" && selectionStart !== null) {
      field.setSelectionRange(selectionStart, selectionEnd);
    }
  });
}

function showToast(message) {
  const toast = document.createElement("div");
  toast.className = "toast";
  toast.textContent = message;
  toastRegion.appendChild(toast);
  window.setTimeout(() => {
    toast.remove();
  }, 3200);
}

function handleAction(button) {
  const action = button.dataset.action;
  const id = button.dataset.id;

  switch (action) {
    case "navigate":
      setRoute(button.dataset.route);
      break;
    case "quick-add-book":
      state.catalogueMode = "create";
      state.editingBookId = null;
      setRoute("catalogue");
      break;
    case "quick-anomaly":
      state.anomalyPrefill = null;
      setRoute("penalites-anomalies");
      break;
    case "start-create-book":
      state.catalogueMode = "create";
      state.editingBookId = null;
      render();
      break;
    case "select-book":
      state.selectedBookId = id;
      state.catalogueMode = "view";
      state.editingBookId = null;
      render();
      break;
    case "edit-book":
      state.selectedBookId = id;
      state.editingBookId = id;
      state.catalogueMode = "edit";
      render();
      break;
    case "delete-book":
      deleteBook(id);
      break;
    case "cancel-book-form":
      state.catalogueMode = "view";
      state.editingBookId = null;
      render();
      break;
    case "export-history":
      showToast("Historique exporté avec succès.");
      break;
    case "select-user":
      state.selectedUserId = id;
      render();
      break;
    case "view-user-penalties":
      state.selectedUserId = id;
      showToast("Pénalités affichées dans l'historique complet.");
      render();
      break;
    case "view-user-incidents":
      state.selectedUserId = id;
      showToast("Incidents affichés dans l'historique complet.");
      render();
      break;
    case "verify-borrow":
      verifyBorrow(id);
      break;
    case "refuse-borrow":
      refuseBorrow(id);
      break;
    case "borrow-user-profile":
      state.selectedUserId = id;
      setRoute("historique");
      break;
    case "borrow-book-details":
      state.selectedBookId = id;
      state.catalogueMode = "view";
      setRoute("catalogue");
      break;
    case "verify-return":
      verifyReturn(id);
      break;
    case "report-return-anomaly":
      reportReturnAnomaly(id);
      break;
    case "create-return-penalty":
      createPenaltyFromReturn(id);
      break;
    case "return-history":
      state.selectedUserId = id;
      setRoute("historique");
      break;
    case "save-return-inspection":
      showToast("Contrôle du retour enregistré.");
      break;
    case "apply-penalty":
      applyPenalty(id);
      break;
    case "cancel-penalty":
      cancelPenalty(id);
      break;
    case "history-from-penalty":
      state.selectedUserId = id;
      setRoute("historique");
      break;
    case "prefill-anomaly":
    case "anomaly-details":
      prefillAnomaly(id, action === "anomaly-details");
      break;
    case "mark-anomaly-treated":
      markAnomalyTreated(id);
      break;
    case "declare-damaged":
      createAnomalyFromForm(button.closest("form"), true);
      break;
    case "logout":
      showToast("Déconnexion demandée.");
      break;
    default:
      break;
  }
}

function deleteBook(id) {
  const book = findBook(id);
  if (!book) return;
  books = books.filter((item) => item.id !== id);
  if (state.selectedBookId === id) {
    state.selectedBookId = books[0]?.id || "";
  }
  state.catalogueMode = "view";
  showToast("Livre supprimé du catalogue.");
  addActivity("Livre supprimé", "Bibliothécaire", book.title, "Vérifié");
  render();
}

function verifyBorrow(id) {
  const request = findBorrow(id);
  if (!request) return;
  request.status = "Vérifié";
  state.selectedBorrowId = id;
  const book = findBook(request.bookId);
  if (book && request.availability === "Disponible") {
    book.status = "Emprunté";
    book.lastMovement = `Emprunt vérifié le ${request.requestDate}`;
  }
  addActivity("Emprunt validé", request.user, request.book, "Vérifié");
  showToast("Emprunt vérifié avec succès.");
  render();
}

function refuseBorrow(id) {
  const request = findBorrow(id);
  if (!request) return;
  request.status = "Refusé";
  state.selectedBorrowId = id;
  addActivity("Emprunt refusé", request.user, request.book, "Refusé");
  showToast("Demande d'emprunt refusée.");
  render();
}

function verifyReturn(id) {
  const request = findReturn(id);
  if (!request) return;
  request.status = "Vérifié";
  state.selectedReturnId = id;
  const book = findBook(request.bookId);
  if (book && request.condition === "Bon état") {
    book.status = "Disponible";
    book.lastMovement = `Retour vérifié le ${request.returnDate}`;
  }
  addActivity("Retour vérifié", request.borrower, request.book, "Vérifié");
  showToast("Retour vérifié avec succès.");
  render();
}

function reportReturnAnomaly(id) {
  const request = findReturn(id);
  if (!request) return;
  const book = findBook(request.bookId);
  const anomaly = {
    id: nextId("ANO", anomalies),
    bookId: request.bookId,
    book: request.book,
    reportedBy: request.borrower,
    type: request.condition === "Bon état" ? "Livre endommagé" : request.condition,
    severity: request.condition === "Bon état" ? "Moyen" : "Critique",
    date: request.returnDate,
    status: "Ouverte",
    description: `Anomalie signalée lors du retour ${request.id}.`,
  };
  anomalies.unshift(anomaly);
  request.condition = "Endommagé";
  if (book) {
    book.status = "Endommagé";
    book.condition = anomaly.type;
    book.lastMovement = `Anomalie signalée le ${request.returnDate}`;
  }
  addActivity("Livre signalé endommagé", request.borrower, request.book, "Endommagé");
  showToast("Anomalie signalée pour le livre retourné.");
  render();
}

function createPenaltyFromReturn(id) {
  const request = findReturn(id);
  if (!request) return;
  const alreadyExists = penalties.some((penalty) => penalty.id.includes(request.id));
  const amount = request.delay === "Aucun" ? 80 : Number.parseInt(request.delay, 10) * 10;
  penalties.unshift({
    id: nextId("PEN", penalties),
    user: request.borrower,
    userId: request.userId,
    reason: request.delay === "Aucun" ? "Anomalie de retour" : "Retard de retour",
    book: request.book,
    delay: request.delay,
    amount: `${amount} MAD`,
    status: alreadyExists ? "En attente" : "En attente",
  });
  addActivity("Pénalité préparée", request.borrower, request.book, "Pénalité");
  showToast("Pénalité ajoutée à la liste.");
  render();
}

function applyPenalty(id) {
  const penalty = penalties.find((item) => item.id === id);
  if (!penalty) return;
  penalty.status = "Appliquée";
  addActivity("Pénalité appliquée", penalty.user, penalty.book, "Pénalité");
  showToast("Pénalité appliquée.");
  render();
}

function cancelPenalty(id) {
  const penalty = penalties.find((item) => item.id === id);
  if (!penalty) return;
  penalty.status = "Annulée";
  showToast("Pénalité annulée.");
  render();
}

function prefillAnomaly(id, showDetails) {
  const anomaly = anomalies.find((item) => item.id === id);
  if (!anomaly) return;
  state.anomalyPrefill = {
    bookId: anomaly.bookId,
    reportedBy: anomaly.reportedBy,
    type: anomaly.type,
    severity: anomaly.severity,
    condition: anomaly.type,
    description: anomaly.description,
  };
  showToast(showDetails ? "Détails de l'anomalie chargés dans le formulaire." : "Formulaire prêt pour un nouveau signalement.");
  render();
}

function markAnomalyTreated(id) {
  const anomaly = anomalies.find((item) => item.id === id);
  if (!anomaly) return;
  anomaly.status = "Traité";
  showToast("Anomalie marquée traitée.");
  render();
}

function createAnomalyFromForm(form, forceDamaged = false) {
  if (!form) return;
  const data = new FormData(form);
  const bookId = String(data.get("bookId") || "").trim();
  const book = findBook(bookId);
  const type = forceDamaged ? "Livre endommagé" : String(data.get("type") || "Livre endommagé");
  const condition = forceDamaged ? "Endommagé" : String(data.get("condition") || "À contrôler");
  const anomaly = {
    id: nextId("ANO", anomalies),
    bookId,
    book: book ? book.title : bookId,
    reportedBy: String(data.get("reportedBy") || "").trim(),
    type,
    severity: String(data.get("severity") || "Moyen"),
    date: "24/10/2026",
    status: "Ouverte",
    description: String(data.get("description") || `${type} signalé au comptoir.`).trim(),
  };

  if (!anomaly.bookId || !anomaly.reportedBy || !anomaly.description) {
    showToast("Compléter les champs obligatoires avant le signalement.");
    return;
  }

  anomalies.unshift(anomaly);
  if (book) {
    book.status = condition === "Endommagé" || normalizeText(type).includes("endommage") ? "Endommagé" : "En traitement";
    book.condition = condition;
    book.lastMovement = `Anomalie signalée le ${anomaly.date}`;
  }
  addActivity("Livre signalé endommagé", anomaly.reportedBy, anomaly.book, "Endommagé");
  state.anomalyPrefill = null;
  showToast(forceDamaged ? "Livre endommagé déclaré." : "Anomalie signalée.");
  render();
}

function saveBook(form) {
  const data = new FormData(form);
  const payload = {
    title: String(data.get("title") || "").trim(),
    author: String(data.get("author") || "").trim(),
    isbn: String(data.get("isbn") || "").trim(),
    category: String(data.get("category") || "Informatique"),
    status: String(data.get("status") || "Disponible"),
    copies: String(data.get("copies") || "1/1").trim(),
    condition: String(data.get("condition") || "Bon état").trim(),
    lastMovement: String(data.get("lastMovement") || "Mise à jour catalogue").trim(),
  };

  if (!payload.title || !payload.author || !payload.isbn) {
    showToast("Titre, auteur et ISBN sont obligatoires.");
    return;
  }

  if (state.catalogueMode === "edit") {
    const book = findBook(state.editingBookId);
    if (!book) return;
    Object.assign(book, payload);
    state.selectedBookId = book.id;
    showToast("Livre modifié dans le catalogue.");
  } else {
    const newBook = {
      id: nextId("LIV", books),
      ...payload,
    };
    books.unshift(newBook);
    state.selectedBookId = newBook.id;
    showToast("Livre ajouté au catalogue.");
  }

  state.catalogueMode = "view";
  state.editingBookId = null;
  addActivity("Catalogue mis à jour", "Bibliothécaire", payload.title, "Vérifié");
  render();
}

document.addEventListener("click", (event) => {
  const button = event.target.closest("[data-action]");
  if (!button) return;
  event.preventDefault();
  handleAction(button);
});

document.addEventListener("input", (event) => {
  const target = event.target;
  const filterKey = target.dataset?.filter;
  if (!filterKey || target.tagName === "SELECT") return;
  state.filters[filterKey] = target.value;
  renderWithFocus(filterKey, target.selectionStart, target.selectionEnd);
});

document.addEventListener("change", (event) => {
  const target = event.target;
  const filterKey = target.dataset?.filter;
  if (!filterKey) return;
  state.filters[filterKey] = target.value;
  render();
});

document.addEventListener("submit", (event) => {
  const form = event.target;
  if (form === topSearchForm) {
    event.preventDefault();
    const searchKeyByRoute = {
      catalogue: "catalogueSearch",
      historique: "historySearch",
      emprunts: "borrowSearch",
      retours: "returnSearch",
      "penalites-anomalies": "penaltySearch",
    };
    const key = searchKeyByRoute[state.route];
    if (key) {
      state.filters[key] = topSearch.value.trim();
      showToast("Recherche appliquée à la page courante.");
      render();
    } else {
      showToast("Recherche prête pour les pages opérationnelles.");
    }
    return;
  }

  if (form.dataset.form === "book") {
    event.preventDefault();
    saveBook(form);
    return;
  }

  if (form.dataset.form === "anomaly") {
    event.preventDefault();
    createAnomalyFromForm(form);
  }
});

window.addEventListener("hashchange", render);

if (!window.location.hash) {
  window.location.hash = "dashboard";
} else {
  render();
}
