const app = document.getElementById("app");
const toastRegion = document.getElementById("toast-region");

const profile = {
  name: "Yassine El Amrani",
  role: "CLIENT",
  initials: "YE",
  email: "yassine.elamrani@gmail.com",
  phone: "+212 6 12 34 56 78",
  cin: "BN981355",
  status: "Actif",
  registrationDate: "12/02/2025",
  alertLevel: "1 / 3"
};

const books = [
  {
    id: "petit-prince",
    title: "Le Petit Prince",
    author: "Antoine de Saint-Exupéry",
    category: "Roman",
    detailCategory: "Roman / Jeunesse",
    status: "Disponible",
    statusKey: "available",
    isbn: "9782070612758",
    favorites: 12,
    publication: "1943",
    coverClass: "cover-prince",
    coverUrl: "assets/images/books/petit-prince.webp",
    isNew: true,
    synopsis:
      "Le Petit Prince est une œuvre de langue française, la plus connue d'Antoine de Saint-Exupéry. Publié en 1943 à New York, c'est un conte poétique et philosophique sous l'apparence d'un conte pour enfants. Le narrateur est un aviateur qui, à la suite d'une panne de moteur, a dû se poser en catastrophe dans le désert du Sahara et tente seul de réparer son avion. Le lendemain de son atterrissage forcé, il est réveillé par une petite voix qui lui demande : « S'il vous plaît... dessine-moi un mouton ! »"
  },
  {
    id: "etranger",
    title: "L'Étranger",
    author: "Albert Camus",
    category: "Philosophie",
    detailCategory: "Philosophie",
    status: "Emprunté",
    statusKey: "borrowed",
    isbn: "9782070360024",
    favorites: 15,
    publication: "1942",
    coverClass: "cover-etranger",
    coverUrl: "assets/images/books/etranger.webp",
    isPopular: true,
    synopsis:
      "Roman majeur d'Albert Camus, L'Étranger explore l'absurde, la solitude et le rapport de l'individu aux normes sociales à travers le regard détaché de Meursault."
  },
  {
    id: "miserables",
    title: "Les Misérables",
    author: "Victor Hugo",
    category: "Classique",
    detailCategory: "Classique",
    status: "Disponible",
    statusKey: "available",
    isbn: "9782253006312",
    favorites: 20,
    publication: "1862",
    coverClass: "cover-miserables",
    coverUrl: "assets/images/books/les-miserables.jpg",
    isPopular: true,
    synopsis:
      "Les Misérables retrace les destins de Jean Valjean, Cosette, Fantine et Marius dans une fresque sociale et historique consacrée à la justice, la misère et la rédemption."
  },
  {
    id: "alchemist",
    title: "L'Alchimiste",
    author: "Paulo Coelho",
    category: "Aventure",
    detailCategory: "Roman / Aventure",
    status: "Disponible",
    statusKey: "available",
    isbn: "9782290004449",
    favorites: 18,
    publication: "1988",
    coverClass: "cover-alchemist",
    coverUrl: "assets/images/books/alchimiste.webp",
    isPopular: true,
    isNew: true,
    synopsis:
      "L'Alchimiste suit Santiago, un jeune berger andalou parti à la recherche d'un trésor. Son voyage devient une quête intérieure sur le courage, l'écoute des signes et la poursuite de sa légende personnelle."
  },
  {
    id: "nineteen-eighty-four",
    title: "1984",
    author: "George Orwell",
    category: "Dystopie",
    detailCategory: "Roman / Dystopie",
    status: "Disponible",
    statusKey: "available",
    isbn: "9782070368228",
    favorites: 26,
    publication: "1949",
    coverClass: "cover-1984",
    coverUrl: "assets/images/books/1984.jpg",
    isPopular: true,
    synopsis:
      "Dans un monde dominé par la surveillance et la manipulation du langage, Winston Smith tente de préserver une part de vérité et de liberté intérieure face à un pouvoir totalitaire."
  },
  {
    id: "pride-prejudice",
    title: "Orgueil et Préjugés",
    author: "Jane Austen",
    category: "Classique",
    detailCategory: "Classique / Société",
    status: "Disponible",
    statusKey: "available",
    isbn: "9782253004356",
    favorites: 17,
    publication: "1813",
    coverClass: "cover-pride",
    coverUrl: "assets/images/books/orgueil-et-prejuges.jpg",
    isNew: true,
    synopsis:
      "Elizabeth Bennet observe avec ironie et lucidité les codes sociaux de son époque, tandis que sa relation avec Darcy révèle les effets de l'orgueil, des préjugés et de la première impression."
  },
  {
    id: "crime-punishment",
    title: "Crime et Châtiment",
    author: "Fiodor Dostoïevski",
    category: "Psychologie",
    detailCategory: "Classique / Psychologie",
    status: "Emprunté",
    statusKey: "borrowed",
    isbn: "9782253082507",
    favorites: 14,
    publication: "1866",
    coverClass: "cover-crime",
    coverUrl: "assets/images/books/crime-et-chatiment.jpg",
    synopsis:
      "Raskolnikov, étudiant pauvre de Saint-Pétersbourg, commet un crime au nom d'une théorie morale. Le roman explore la culpabilité, la fièvre intérieure et la possibilité du repentir."
  },
  {
    id: "name-rose",
    title: "Le Nom de la Rose",
    author: "Umberto Eco",
    category: "Mystère",
    detailCategory: "Roman / Historique",
    status: "Disponible",
    statusKey: "available",
    isbn: "9782253033134",
    favorites: 16,
    publication: "1980",
    coverClass: "cover-rose",
    coverUrl: "assets/images/books/le-nom-de-la-rose.jpg",
    isPopular: true,
    synopsis:
      "Dans une abbaye médiévale, Guillaume de Baskerville enquête sur une série de morts mystérieuses. L'intrigue mêle érudition, théologie, bibliothèque interdite et enquête policière."
  },
  {
    id: "kafka-shore",
    title: "Kafka sur le rivage",
    author: "Haruki Murakami",
    category: "Contemporain",
    detailCategory: "Roman / Contemporain",
    status: "Disponible",
    statusKey: "available",
    isbn: "9782264053718",
    favorites: 19,
    publication: "2002",
    coverClass: "cover-kafka",
    coverUrl: "assets/images/books/kafka-sur-le-rivage.webp",
    isNew: true,
    synopsis:
      "Un adolescent en fuite et un vieil homme singulier avancent dans deux récits parallèles où le réel glisse vers le rêve, la mémoire et les symboles."
  }
];

const reservations = [
  {
    id: "res-014",
    bookId: "petit-prince",
    category: "Littérature",
    code: "RES-2026-014",
    place: "Bibliothèque Centrale APFA",
    reservationDate: "09/06/2026",
    limitDate: "12/06/2026",
    status: "Réservé",
    statusKey: "reserved",
    countdown: "2 jours restants",
    note: "Retirez votre livre avant le 12/06/2026 pour éviter une alerte."
  },
  {
    id: "res-015",
    bookId: "etranger",
    category: "Roman",
    code: "RES-2026-015",
    place: "Bibliothèque Centrale APFA",
    reservationDate: "07/06/2026",
    limitDate: "10/06/2026",
    status: "Récupérée",
    statusKey: "reserved",
    countdown: "Quelques heures",
    returnDate: "10/06/2026"
  },
  {
    id: "res-016",
    bookId: "miserables",
    category: "Classique",
    code: "RES-2026-016",
    place: "Bibliothèque Centrale APFA",
    reservationDate: "08/06/2026",
    limitDate: "11/06/2026",
    status: "Expire demain",
    statusKey: "expiring",
    countdown: "1 jour restant",
    note: "Votre réservation expirera demain si le livre n'est pas retiré."
  }
];

const borrowings = [
  {
    id: "loan-001",
    title: "Dune",
    author: "Frank Herbert",
    borrowed: "02/05/2026",
    returnedLabel: "Retourné",
    returned: "22/05/2026",
    status: "Retourné",
    statusKey: "returned",
    coverClass: "cover-dune",
    coverUrl: "assets/images/books/dune.jpg"
  },
  {
    id: "loan-002",
    title: "Sapiens",
    author: "Yuval Noah Harari",
    borrowed: "14/05/2026",
    returnedLabel: "Retourné",
    returned: "04/06/2026",
    status: "Retourné",
    statusKey: "returned",
    coverClass: "cover-sapiens",
    coverUrl: "assets/images/books/sapiens.jpg"
  },
  {
    id: "loan-003",
    title: "Atomic Habits",
    author: "James Clear",
    borrowed: "28/05/2026",
    returnedLabel: "Retour prévu",
    returned: "18/06/2026",
    status: "En cours",
    statusKey: "gold-soft",
    coverClass: "cover-atomic",
    coverUrl: "assets/images/books/atomic-habits.jpg"
  },
  {
    id: "loan-004",
    title: "Les Misérables",
    author: "Victor Hugo",
    borrowed: "10/03/2026",
    returnedLabel: "Retourné",
    returned: "08/04/2026",
    status: "Retourné en retard",
    statusKey: "late",
    coverClass: "cover-miserables",
    coverUrl: "assets/images/books/les-miserables.jpg"
  }
];

const penalties = [
  {
    date: "07/06/2026",
    reason: "Retour en retard",
    amount: "20 DH",
    status: "En attente",
    statusKey: "waiting"
  },
  {
    date: "15/05/2026",
    reason: "Livre endommagé",
    amount: "50 DH",
    status: "Réglée",
    statusKey: "returned"
  }
];

const recentActivity = [
  { icon: "bookmark_add", label: "Réservation créée", date: "08/06/2026" },
  { icon: "check_circle", label: "Livre collecté", date: "06/06/2026" },
  { icon: "comment", label: "Commentaire ajouté", date: "04/06/2026" }
];

const routeConfig = {
  login: { title: "Authentification", icon: "login" },
  dashboard: { title: "Tableau de bord", icon: "dashboard", active: "dashboard" },
  catalogue: { title: "Catalogue", icon: "auto_stories", active: "catalogue" },
  "livre-detail": { title: "Catalogue", icon: "auto_stories", active: "catalogue" },
  reservations: { title: "Mes réservations", icon: "auto_stories", active: "reservations" },
  historique: { title: "Historique des emprunts", icon: "auto_stories", active: "historique" },
  alertes: { title: "Alertes", icon: "notifications", active: "alertes" },
  penalites: { title: "Mes pénalités", icon: "auto_stories", active: "penalites" },
  profil: { title: "Mon profil", icon: "auto_stories", active: "profil" },
  parametres: { title: "Paramètres", icon: "auto_stories", active: "parametres" }
};

const state = {
  authenticated: false,
  selectedBookId: "petit-prince",
  catalogueFilter: "tous",
  searchQuery: "",
  reservedBookIds: new Set(),
  favoriteBookIds: new Set(["petit-prince", "miserables"]),
  settings: {
    reservations: true,
    alertes: true,
    penalites: true,
    nouveautes: false
  }
};

function getCurrentRoute() {
  const raw = window.location.hash.replace("#", "") || "login";
  return routeConfig[raw] ? raw : "login";
}

function navigate(route) {
  window.location.hash = `#${route}`;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function icon(name, extraClass = "") {
  return `<span class="material-symbols-outlined ${extraClass}">${name}</span>`;
}

function findBook(id) {
  return books.find((book) => book.id === id) || books[0];
}

function normalize(value) {
  return String(value)
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();
}

function makeBadge(label, key = "") {
  return `<span class="badge ${key}">${escapeHtml(label)}</span>`;
}

function bookCover(book, size = "", label = "") {
  const text = label || book.title;
  const image = book.coverUrl
    ? `<img class="cover-image" src="${book.coverUrl}" alt="Couverture de ${escapeHtml(text)}" loading="lazy">`
    : `<span class="cover-title">${escapeHtml(text)}</span>`;
  return `
    <div class="book-cover ${book.coverUrl ? "has-image" : ""} ${book.coverClass} ${size}" role="img" aria-label="Couverture de ${escapeHtml(text)}">
      ${image}
    </div>
  `;
}

function avatar(size = "") {
  return `
    <div class="avatar ${size}" aria-label="${escapeHtml(profile.name)}">
      <span>${profile.initials}</span>
      <span class="status-dot" aria-hidden="true"></span>
    </div>
  `;
}

function renderApp() {
  const route = getCurrentRoute();

  if (!state.authenticated && route !== "login") {
    history.replaceState(null, "", "#login");
    renderLogin();
    return;
  }

  if (route === "login") {
    renderLogin();
    return;
  }

  renderShell(route);
}

function renderLogin() {
  app.className = "";
  app.innerHTML = `
    <main class="login-view">
      <section class="login-card" aria-labelledby="login-title">
        <div class="login-brand" aria-hidden="true">${icon("library_books")}</div>
        <h1 id="login-title" class="login-title">Authentification</h1>
        <p class="login-subtitle">Veuillez entrer vos identifiants pour accéder au portail.</p>
        <form id="login-form" class="form-stack">
          <div class="field-group">
            <label class="field-label" for="username">Nom d'utilisateur</label>
            <div class="input-shell">
              ${icon("person")}
              <input id="username" name="username" type="text" placeholder="Username" autocomplete="username" required>
            </div>
          </div>
          <div class="field-group">
            <div class="field-row">
              <label class="field-label" for="password">Mot de passe</label>
              <a class="field-link" href="#" aria-label="Mot de passe oublié">Oublié ?</a>
            </div>
            <div class="input-shell">
              ${icon("lock")}
              <input id="password" name="password" type="password" placeholder="••••••••" autocomplete="current-password" required>
              <button class="input-action" type="button" data-action="toggle-password" aria-label="Afficher ou masquer le mot de passe">
                ${icon("visibility")}
              </button>
            </div>
          </div>
          <button class="btn btn-primary login-submit" type="submit">
            Se connecter
            ${icon("login")}
          </button>
        </form>
      </section>
    </main>
  `;
}

function renderShell(route) {
  const config = routeConfig[route];
  const activeRoute = config.active || route;
  app.className = "app-layout";
  app.innerHTML = `
    ${renderSidebar(activeRoute)}
    <main>
      ${renderTopbar(config)}
      ${renderPage(route)}
    </main>
  `;
}

function renderSidebar(activeRoute) {
  const groups = [
    {
      label: "Mon espace",
      items: [
        { route: "dashboard", href: "#dashboard", icon: "dashboard", label: "Tableau de bord" }
      ]
    },
    {
      label: "Bibliothèque",
      items: [
        { route: "catalogue", href: "#catalogue", icon: "auto_stories", label: "Catalogue", filled: true },
        { route: "reservations", href: "#reservations", icon: "bookmark_manager", label: "Mes réservations" },
        { route: "historique", href: "#historique", icon: "history_edu", label: "Historique des emprunts" }
      ]
    },
    {
      label: "Mon compte",
      items: [
        { route: "alertes", href: "#alertes", icon: "notifications", label: "Alertes" },
        { route: "penalites", href: "#penalites", icon: "error", label: "Pénalités" },
        { route: "profil", href: "#profil", icon: "person", label: "Profil" }
      ]
    },
    {
      label: "Session",
      session: true,
      items: [
        { route: "parametres", href: "#parametres", icon: "settings", label: "Paramètres" },
        { route: "logout", href: "#login", icon: "logout", label: "Déconnexion", logout: true }
      ]
    }
  ];

  return `
    <aside class="sidebar" aria-label="Navigation client">
      <div class="brand-block">
        <div class="brand-icon" aria-hidden="true">${icon("book_4", "icon-filled")}</div>
        <h1 class="brand-title">Smart Library</h1>
      </div>
      <nav class="nav">
        ${groups.map((group) => `
          <section class="nav-section ${group.session ? "session-section" : ""}">
            <p class="nav-heading">${group.label}</p>
            ${group.items.map((item) => {
              const isActive = item.route === activeRoute;
              const classes = ["nav-link", isActive ? "active" : "", item.logout ? "logout" : ""].filter(Boolean).join(" ");
              return `
                <a class="${classes}" href="${item.href}" ${item.logout ? 'data-action="logout"' : ""}>
                  ${icon(item.icon, item.filled || isActive ? "icon-filled" : "")}
                  <span>${item.label}</span>
                </a>
              `;
            }).join("")}
          </section>
        `).join("")}
      </nav>
    </aside>
  `;
}

function renderTopbar(config) {
  return `
    <header class="topbar">
      <div class="topbar-left">
        <div class="topbar-title">
          ${icon(config.icon)}
          <span>${escapeHtml(config.title)}</span>
        </div>
        <label class="search-shell" for="global-search">
          ${icon("search")}
          <input id="global-search" type="search" value="${escapeHtml(state.searchQuery)}" placeholder="Rechercher par titre, auteur ou ISBN..." autocomplete="off">
        </label>
      </div>
      <div class="user-chip">
        <div class="user-copy">
          <span class="user-name">${profile.name}</span>
          <span class="user-role">${profile.role}</span>
        </div>
        ${avatar()}
      </div>
    </header>
  `;
}

function renderPage(route) {
  switch (route) {
    case "dashboard":
      return renderDashboard();
    case "catalogue":
      return renderCatalogue();
    case "livre-detail":
      return renderBookDetail();
    case "reservations":
      return renderReservations();
    case "historique":
      return renderHistory();
    case "alertes":
      return renderAlerts();
    case "penalites":
      return renderPenalties();
    case "profil":
      return renderProfile();
    case "parametres":
      return renderSettings();
    default:
      return renderCatalogue();
  }
}

function getClientStats() {
  const returnedLoans = borrowings.filter((loan) => ["returned", "late"].includes(loan.statusKey));
  const onTimeReturns = returnedLoans.filter((loan) => loan.statusKey === "returned").length;
  const onTimeRate = returnedLoans.length ? Math.round((onTimeReturns / returnedLoans.length) * 100) : 0;

  return {
    totalLoans: borrowings.length,
    activeLoans: borrowings.filter((loan) => loan.statusKey === "gold-soft").length,
    returnedLoans: returnedLoans.length,
    lateReturns: returnedLoans.filter((loan) => loan.statusKey === "late").length,
    onTimeRate,
    lateRate: 100 - onTimeRate,
    activeReservations: reservations.filter((reservation) => reservation.status !== "Récupérée").length,
    pendingPenalties: penalties.filter((penalty) => penalty.statusKey === "waiting").length
  };
}

function renderDashboardKpi(label, value, iconName, note, tone = "") {
  return `
    <article class="stats-kpi-card ${tone}">
      <div class="stats-kpi-top">
        <span class="stats-kpi-label">${escapeHtml(label)}</span>
        ${icon(iconName)}
      </div>
      <strong class="stats-kpi-value">${escapeHtml(value)}</strong>
      <span class="stats-kpi-note">${escapeHtml(note)}</span>
    </article>
  `;
}

function renderDashboard() {
  const stats = getClientStats();
  const trendValues = [0, 0, 1, 0, 3, 0];
  const trendLabels = ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin"];
  const chartMax = Math.max(...trendValues, 1);
  const chartPoints = trendValues.map((value, index) => {
    const x = 32 + index * 111;
    const y = 170 - (value / chartMax) * 112;
    return `${x},${y}`;
  });
  const areaPoints = `32,170 ${chartPoints.join(" ")} 587,170`;

  return `
    <section class="content dashboard-content">
      <header class="stats-page-head">
        <div>
          <span class="section-kicker">Vue personnelle</span>
          <h1>Mes statistiques</h1>
          <p>Suivez vos emprunts, réservations, retours et pénalités.</p>
        </div>
        <span class="stats-period">${icon("date_range")} Janvier - Juin 2026</span>
      </header>

      <section class="stats-kpi-grid" aria-label="Indicateurs personnels">
        ${renderDashboardKpi("Emprunts totaux", String(stats.totalLoans), "local_library", `${stats.activeLoans} emprunt actif`)}
        ${renderDashboardKpi("Réservations actives", String(stats.activeReservations), "bookmark_manager", "À retirer en bibliothèque", "gold")}
        ${renderDashboardKpi("Retours à l'heure", `${stats.onTimeRate}%`, "task_alt", `${stats.returnedLoans} livres retournés`, "success")}
        ${renderDashboardKpi("Pénalités en attente", String(stats.pendingPenalties), "gavel", "20 DH à régulariser", stats.pendingPenalties ? "danger" : "")}
      </section>

      <div class="stats-analytics-grid">
        <article class="analytics-panel trend-panel">
          <header class="analytics-heading">
            <div>
              <h2>Tendances d'emprunt</h2>
              <p>Vos emprunts enregistrés sur les six derniers mois.</p>
            </div>
            <span class="analytics-pill">6 derniers mois</span>
          </header>
          <div class="trend-summary">
            <strong>${stats.totalLoans}</strong>
            <span>emprunts au total</span>
          </div>
          <div class="trend-chart" role="img" aria-label="Emprunts mensuels de janvier à juin 2026">
            <svg viewBox="0 0 620 200" preserveAspectRatio="none" aria-hidden="true">
              <line class="trend-grid-line" x1="32" y1="58" x2="587" y2="58"></line>
              <line class="trend-grid-line" x1="32" y1="95" x2="587" y2="95"></line>
              <line class="trend-grid-line" x1="32" y1="132" x2="587" y2="132"></line>
              <line class="trend-baseline" x1="32" y1="170" x2="587" y2="170"></line>
              <polygon class="trend-area" points="${areaPoints}"></polygon>
              <polyline class="trend-line" points="${chartPoints.join(" ")}"></polyline>
              ${chartPoints.map((point, index) => {
                const [x, y] = point.split(",");
                return `<circle class="trend-point" cx="${x}" cy="${y}" r="5"><title>${trendLabels[index]} : ${trendValues[index]} emprunt${trendValues[index] > 1 ? "s" : ""}</title></circle>`;
              }).join("")}
            </svg>
            <div class="trend-axis" aria-hidden="true">
              ${trendLabels.map((label) => `<span>${label}</span>`).join("")}
            </div>
          </div>
        </article>

        <article class="analytics-panel return-panel">
          <header class="analytics-heading">
            <div>
              <h2>Statut des retours</h2>
              <p>Répartition de vos livres rendus.</p>
            </div>
          </header>
          <div class="return-donut" style="--on-time-rate: ${stats.onTimeRate}%" role="img" aria-label="${stats.onTimeRate}% de retours à l'heure et ${stats.lateRate}% en retard">
            <div class="return-donut-center">
              <strong>${stats.onTimeRate}%</strong>
              <span>à l'heure</span>
            </div>
          </div>
          <div class="return-legend">
            <div><span class="legend-dot on-time"></span><span>Retours à l'heure</span><strong>${stats.onTimeRate}%</strong></div>
            <div><span class="legend-dot late"></span><span>Retours en retard</span><strong>${stats.lateRate}%</strong></div>
          </div>
        </article>
      </div>

      <div class="stats-lower-grid">
        <article class="analytics-panel account-panel">
          <header class="analytics-heading">
            <div>
              <h2>Vue d'ensemble</h2>
              <p>État actuel de votre activité Smart Library.</p>
            </div>
          </header>
          <div class="account-stat-list">
            <div><span>${icon("menu_book")} Emprunts actifs</span><strong>${stats.activeLoans}</strong></div>
            <div><span>${icon("bookmark")} Réservations à retirer</span><strong>${stats.activeReservations}</strong></div>
            <div><span>${icon("favorite")} Livres favoris</span><strong>${state.favoriteBookIds.size}</strong></div>
            <div><span>${icon("payments")} Pénalités actives</span><strong>${stats.pendingPenalties}</strong></div>
          </div>
        </article>

        <article class="analytics-panel recent-loans-panel">
          <header class="analytics-heading">
            <div>
              <h2>Derniers emprunts</h2>
              <p>Vos ouvrages les plus récents.</p>
            </div>
            <a class="text-link" href="#historique">Voir l'historique ${icon("arrow_forward")}</a>
          </header>
          <div class="dashboard-loan-list">
            ${borrowings.slice(0, 3).map((loan) => `
              <div class="dashboard-loan-row">
                ${bookCover({ title: loan.title, coverClass: loan.coverClass, coverUrl: loan.coverUrl }, "micro", loan.title)}
                <div>
                  <strong>${escapeHtml(loan.title)}</strong>
                  <span>${escapeHtml(loan.author)}</span>
                </div>
                ${makeBadge(loan.status, loan.statusKey)}
              </div>
            `).join("")}
          </div>
        </article>
      </div>
    </section>
  `;
}

function renderCatalogue() {
  const filteredBooks = filterBooks();
  const availableCount = books.filter((book) => book.statusKey === "available").length;
  const categoryCount = new Set(books.map((book) => book.category)).size;
  return `
    <section class="content compact-top">
      <header class="catalogue-intro">
        <div>
          <span class="eyebrow">Collection 2026</span>
          <h1>Explorez la bibliothèque</h1>
          <p>Découvrez des classiques, des romans contemporains et des ouvrages de référence sélectionnés pour les lecteurs Smart Library.</p>
        </div>
        <div class="catalogue-summary" aria-label="Résumé du catalogue">
          <div><strong>${books.length}</strong><span>Ouvrages</span></div>
          <div><strong>${availableCount}</strong><span>Disponibles</span></div>
          <div><strong>${categoryCount}</strong><span>Catégories</span></div>
        </div>
      </header>
      <div class="breadcrumb-row">
        ${renderBreadcrumb(["Accueil", "Catalogue"])}
        <div class="pill-row" role="group" aria-label="Filtres du catalogue">
          ${[
            ["tous", "Tous"],
            ["disponibles", "Disponibles"],
            ["populaires", "Populaires"],
            ["nouveautes", "Nouveautés"]
          ].map(([key, label]) => `
            <button class="pill ${state.catalogueFilter === key ? "active" : ""}" type="button" data-action="catalogue-filter" data-filter="${key}">
              ${label}
            </button>
          `).join("")}
        </div>
      </div>
      <div class="book-grid">
        ${filteredBooks.length ? filteredBooks.map(renderBookCard).join("") : '<div class="empty-state">Aucun ouvrage ne correspond à votre recherche.</div>'}
      </div>
    </section>
  `;
}

function filterBooks() {
  const query = normalize(state.searchQuery);
  return books.filter((book) => {
    const matchSearch = !query || normalize(`${book.title} ${book.author} ${book.isbn} ${book.category}`).includes(query);
    const matchFilter =
      state.catalogueFilter === "tous" ||
      (state.catalogueFilter === "disponibles" && book.statusKey === "available") ||
      (state.catalogueFilter === "populaires" && (book.isPopular || book.favorites >= 15)) ||
      (state.catalogueFilter === "nouveautes" && book.isNew);
    return matchSearch && matchFilter;
  });
}

function renderBookCard(book) {
  const favorite = state.favoriteBookIds.has(book.id);
  return `
    <article class="book-card">
      <div class="book-visual">
        ${bookCover(book)}
        <div class="book-status">${makeBadge(book.status, book.statusKey)}</div>
        <button class="favorite-float ${favorite ? "active" : ""}" type="button" data-action="toggle-favorite" data-book-id="${book.id}" aria-label="Ajouter ${escapeHtml(book.title)} aux favoris">
          ${icon("favorite", favorite ? "icon-filled" : "")}
        </button>
      </div>
      <div class="book-body">
        <div class="card-meta-line">
          <span class="category">${escapeHtml(book.category)}</span>
          <span class="favorite-count ${favorite ? "active" : ""}">
            ${icon("favorite", favorite ? "icon-filled" : "icon-filled")}
            <span>${book.favorites + (favorite && !["petit-prince", "miserables"].includes(book.id) ? 1 : 0)}</span>
          </span>
        </div>
        <div>
          <h2 class="book-title">${escapeHtml(book.title)}</h2>
          <p class="book-author">${escapeHtml(book.author)}</p>
        </div>
        <div class="book-facts">
          <span>${icon("calendar_month")}${book.publication}</span>
          <span>${icon("menu_book")}${escapeHtml(book.detailCategory)}</span>
        </div>
        <div class="card-footer">
          <span class="isbn">ISBN: ${book.isbn}</span>
          <button class="btn ${book.statusKey === "available" ? "btn-gold" : ""}" type="button" data-action="view-details" data-book-id="${book.id}">
            Voir détails
            ${icon("arrow_forward")}
          </button>
        </div>
      </div>
    </article>
  `;
}

function renderBookDetail() {
  const book = findBook(state.selectedBookId);
  const favorite = state.favoriteBookIds.has(book.id);
  const isReserved = state.reservedBookIds.has(book.id);
  const canReserve = book.statusKey === "available";
  return `
    <section class="content compact-top">
      <div class="breadcrumb-row">
        ${renderBreadcrumb(["Accueil", "Catalogue", "Détail de l'ouvrage"])}
      </div>
      <div class="detail-grid">
        <div>
          <div class="book-visual">
            ${bookCover(book, "large-cover")}
            <div class="book-status">${makeBadge(book.status, book.statusKey)}</div>
          </div>
          <div class="metadata-card">
            ${metadataRow("ISBN", book.isbn, "mono")}
            ${metadataRow("Catégorie", book.detailCategory)}
            ${metadataRow("Publication", book.publication)}
          </div>
        </div>
        <div>
          <h1 class="detail-title">${escapeHtml(book.title)}</h1>
          <p class="detail-author">${escapeHtml(book.author)}</p>
          <div class="favorite-count ${favorite ? "active" : ""}">
            ${icon("favorite", favorite ? "icon-filled" : "icon-filled")}
            <span>${book.favorites}</span>
          </div>
          <div class="detail-actions">
            <button class="btn btn-primary" type="button" data-action="reserve-book" data-book-id="${book.id}" ${canReserve && !isReserved ? "" : "disabled"}>
              ${isReserved ? "Ouvrage réservé" : canReserve ? "Réserver l'ouvrage" : "Ouvrage emprunté"}
            </button>
            <button class="btn btn-secondary favorite-inline ${favorite ? "active" : ""}" type="button" data-action="toggle-favorite" data-book-id="${book.id}">
              ${icon("favorite", favorite ? "icon-filled" : "")}
              ${favorite ? "Retirer des favoris" : "Ajouter aux favoris"}
            </button>
          </div>
          <div class="callout">
            ${icon("info")}
            <span>Vous disposez de <strong>3 jours</strong> pour retirer l'ouvrage après réservation au comptoir de la bibliothèque SMART LIBRARY.</span>
          </div>
          <h2 class="section-title">Synopsis</h2>
          <p class="prose">${escapeHtml(book.synopsis)}</p>
        </div>
      </div>
      <div class="lower-detail-grid">
        <section class="panel">
          <h2 class="panel-title">Disponibilité</h2>
          ${metadataRow("Statut", book.status)}
          ${metadataRow("Exemplaires", canReserve ? "4 restants" : "0 restant")}
          ${metadataRow("Dernière réservation", "Il y a 2 jours")}
        </section>
        <section class="panel">
          <h2 class="panel-title">Avis des lecteurs</h2>
          <div class="review-list">
            ${renderReview("Sara Benjelloun", "15 Janvier 2026", "Un chef-d'œuvre intemporel qui touche le cœur à chaque lecture.")}
            ${renderReview("Othmane Idrissi", "08 Mars 2026", "Une poésie magnifique et des leçons de vie essentielles.")}
            ${renderReview("Mehdi Tazi", "20 Mars 2026", "À lire et à relire, peu importe l'âge.")}
          </div>
        </section>
      </div>
    </section>
  `;
}

function metadataRow(label, value, valueClass = "") {
  return `
    <div class="metadata-row">
      <span class="mini-label">${escapeHtml(label)}</span>
      <span class="metadata-value ${valueClass}">${escapeHtml(value)}</span>
    </div>
  `;
}

function renderReview(name, date, text) {
  return `
    <article class="review">
      <div class="review-avatar" aria-hidden="true">${icon("person")}</div>
      <div class="review-body">
        <div class="review-head">
          <strong>${escapeHtml(name)}</strong>
          <span class="review-date">${escapeHtml(date)}</span>
        </div>
        <p class="review-text">"${escapeHtml(text)}"</p>
      </div>
    </article>
  `;
}

function renderReservations() {
  return `
    <section class="content">
      <header class="page-head">
        <h1>Mes Réservations</h1>
        <p>Consultez et suivez vos réservations actives.</p>
      </header>
      <div class="reservation-grid">
        ${reservations.map(renderReservationCard).join("")}
      </div>
      <section class="rules-alert-panel">
        <div>
          <h2 class="panel-heading">${icon("gavel", "gold")}Règles de réservation</h2>
          <ul class="rule-list">
            <li>Une réservation reste active pendant 3 jours.</li>
            <li>Après expiration, le livre redevient disponible.</li>
            <li>Une réservation expirée génère automatiquement une alerte.</li>
            <li>Après 3 alertes, le compte est bloqué.</li>
          </ul>
        </div>
        <div>
          <h2 class="panel-heading">${icon("warning", "danger")}État de l'alerte</h2>
          <div class="alert-state-box">
            <p><strong>Niveau d'alerte actuel : <span class="field-value danger">1 / 3</span></strong></p>
            ${renderRiskLine(["Niveau 1", "Niveau 2", "Niveau 3", "Blocage"], 0)}
          </div>
        </div>
      </section>
    </section>
  `;
}

function renderReservationCard(reservation) {
  const book = findBook(reservation.bookId);
  return `
    <article class="reservation-card">
      <div class="reservation-top">
        ${bookCover(book, "thumb")}
        <div class="reservation-info">
          <div class="card-meta-line">
            <span class="category">${escapeHtml(reservation.category)}</span>
            <span class="reservation-code">${reservation.code}</span>
          </div>
          <h2 class="reservation-title">${escapeHtml(book.title)}</h2>
          <p class="book-author">${escapeHtml(book.author)}</p>
          <p class="reservation-place">${icon("location_on")} ${escapeHtml(reservation.place)}</p>
        </div>
      </div>
      <div class="reservation-details">
        <div class="date-grid">
          <div>
            <span class="date-label">Réservation</span>
            <span class="date-value">${reservation.reservationDate}</span>
          </div>
          <div>
            <span class="date-label">Limite retrait</span>
            <span class="date-value">${reservation.limitDate}</span>
          </div>
        </div>
        <div class="status-row ${reservation.countdown === "Quelques heures" ? "highlight" : ""}">
          <span class="countdown">${icon(reservation.countdown === "Quelques heures" ? "alarm" : "schedule")} ${reservation.countdown}</span>
          ${makeBadge(reservation.status, reservation.statusKey)}
        </div>
        ${reservation.returnDate ? `
          <p class="return-date">Date de retour <strong>${reservation.returnDate}</strong></p>
        ` : `
          <p class="reservation-note">"${escapeHtml(reservation.note)}"</p>
        `}
      </div>
    </article>
  `;
}

function renderHistory() {
  const filtered = filterBorrowings();
  const stats = getClientStats();
  return `
    <section class="content">
      <header class="page-head">
        <h1>Historique des emprunts</h1>
        <p>Consultez vos emprunts passés et actuels.</p>
      </header>
      <div class="kpi-grid">
        ${renderKpi("Total emprunts", String(stats.totalLoans))}
        ${renderKpi("Livres retournés", String(stats.returnedLoans))}
        ${renderKpi("Emprunts actifs", String(stats.activeLoans), "gold")}
        ${renderKpi("Retards", String(stats.lateReturns), "danger")}
      </div>
      <div class="history-list">
        ${filtered.length ? filtered.map(renderHistoryRow).join("") : '<div class="empty-state">Aucun emprunt ne correspond à votre recherche.</div>'}
      </div>
    </section>
  `;
}

function filterBorrowings() {
  const query = normalize(state.searchQuery);
  return borrowings.filter((loan) => !query || normalize(`${loan.title} ${loan.author} ${loan.status}`).includes(query));
}

function renderKpi(label, value, tone = "") {
  return `
    <article class="kpi-card">
      <span class="kpi-label">${escapeHtml(label)}</span>
      <strong class="kpi-value ${tone}">${escapeHtml(value)}</strong>
    </article>
  `;
}

function renderHistoryRow(loan) {
  return `
    <article class="history-row">
      <div class="history-book">
        ${bookCover({ title: loan.title, coverClass: loan.coverClass, coverUrl: loan.coverUrl }, "micro", loan.title)}
        <div>
          <h2 class="history-title">${escapeHtml(loan.title)}</h2>
          <p class="history-author">${escapeHtml(loan.author)}</p>
        </div>
      </div>
      <div class="history-meta">
        <div class="history-date">
          <span class="mini-label">Emprunté</span>
          <strong>${loan.borrowed}</strong>
        </div>
        <div class="history-date">
          <span class="mini-label">${loan.returnedLabel}</span>
          <strong>${loan.returned}</strong>
        </div>
        ${makeBadge(loan.status, loan.statusKey)}
      </div>
    </article>
  `;
}

function renderAlerts() {
  return `
    <section class="content">
      <header class="page-head">
        <h1>Centre des Alertes</h1>
        <p>Suivi des alertes liées aux réservations et emprunts.</p>
      </header>
      <div class="kpi-grid">
        ${renderKpi("Niveau d'alerte actuel", "1 / 3")}
        ${renderKpi("Alertes actives", "1")}
        ${renderKpi("Réservations expirées", "1")}
        ${renderKpi("Statut du compte", "Actif", "gold")}
      </div>
      <section class="risk-progress-card">
        <h2 class="section-kicker">Progression du risque</h2>
        ${renderRiskLine(["Niveau 1", "Niveau 2", "Niveau 3", "Bloqué"], 0, true)}
        <p class="prose risk-copy">Chaque réservation non récupérée dans le délai autorisé génère une alerte. Après 3 alertes : Le compte est automatiquement bloqué.</p>
      </section>
      <div class="alerts-layout">
        <section class="panel active-alert">
          <div class="panel-bar"><h2>Alerte active</h2></div>
          <div class="alert-body">
            <div class="alert-icon">${icon("warning")}</div>
            <div class="alert-fields">
              ${alertField("Type", "Réservation expirée")}
              ${alertField("Livre", "Dune")}
              ${alertField("Date réservation", "05/06/2026", "normal")}
              ${alertField("Expiration", "08/06/2026", "normal")}
              ${alertField("Statut", "Non récupérée", "danger")}
              ${alertField("Conséquence", "+1 alerte enregistrée")}
            </div>
          </div>
        </section>
        <aside class="panel dark-rules">
          <h2 class="panel-heading">${icon("gavel", "gold")}Rappel des règles</h2>
          <ul class="rule-list">
            <li>Une réservation doit être récupérée dans un délai de 3 jours.</li>
            <li>Passé ce délai : la réservation expire, le livre retourne au catalogue, une alerte est enregistrée.</li>
            <li>Après 3 alertes : le compte est bloqué automatiquement.</li>
          </ul>
        </aside>
      </div>
    </section>
  `;
}

function alertField(label, value, tone = "") {
  return `
    <div>
      <span class="mini-label">${escapeHtml(label)}</span>
      <div class="field-value ${tone}">${escapeHtml(value)}</div>
    </div>
  `;
}

function renderRiskLine(labels, activeIndex, numbered = false) {
  return `
    <div class="risk-line">
      ${labels.map((label, index) => `
        <div class="risk-node ${index === activeIndex ? "active" : ""}">
          ${numbered ? `<span class="risk-number">${index < 3 ? index + 1 : icon("block")}</span>` : '<span class="risk-dot"></span>'}
          <span>${escapeHtml(label)}</span>
        </div>
      `).join("")}
    </div>
  `;
}

function renderPenalties() {
  return `
    <section class="content">
      <header class="page-head">
        <h1>Mes pénalités</h1>
        <p>Consultez les pénalités associées à votre compte et leur état de traitement.</p>
      </header>
      <div class="kpi-grid">
        ${renderKpi("Total pénalités", "2")}
        ${renderKpi("En attente", "1")}
        ${renderKpi("Réglées", "1")}
        <article class="kpi-card highlight">
          <span class="kpi-label">Montant total</span>
          <strong class="kpi-value">20 DH</strong>
        </article>
      </div>
      <div class="penalty-layout">
        <section class="panel table-panel">
          <h2 class="table-title">Historique des pénalités</h2>
          <div class="table-wrap">
            <table class="table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Motif</th>
                  <th>Montant</th>
                  <th>Statut</th>
                </tr>
              </thead>
              <tbody>
                ${penalties.map((penalty) => `
                  <tr>
                    <td>${penalty.date}</td>
                    <td>${escapeHtml(penalty.reason)}</td>
                    <td><strong>${penalty.amount}</strong></td>
                    <td>${makeBadge(penalty.status, penalty.statusKey)}</td>
                  </tr>
                `).join("")}
              </tbody>
            </table>
          </div>
        </section>
        <aside class="rules-card">
          <h2 class="panel-title">Règles des pénalités</h2>
          <div class="definition-list">
            ${definition("Retard de retour", "-> Pénalité automatique appliquée après dépassement du délai autorisé.")}
            ${definition("Livre endommagé", "-> Pénalité calculée selon le niveau de gravité.")}
            ${definition("Livre perdu", "-> Remplacement de l'ouvrage ou remboursement de sa valeur.")}
          </div>
        </aside>
      </div>
    </section>
  `;
}

function definition(term, text) {
  return `
    <div>
      <p class="definition-term">${escapeHtml(term)}</p>
      <p class="definition-text">${escapeHtml(text)}</p>
    </div>
  `;
}

function renderProfile() {
  return `
    <section class="content">
      <header class="page-head">
        <h1>Mon profil</h1>
        <p>Consultez les informations de votre compte et votre activité récente.</p>
      </header>
      <section class="profile-hero">
        ${avatar("large")}
        <div>
          <h2 class="profile-name">${profile.name}</h2>
          ${makeBadge(profile.status, "active")}
        </div>
      </section>
      <div class="info-grid">
        ${infoCard("CIN", profile.cin)}
        ${infoCard("Email", profile.email)}
        ${infoCard("Téléphone", profile.phone)}
        ${infoCard("Date d'inscription", profile.registrationDate)}
        ${infoCard("Statut", profile.status)}
        ${infoCard("Niveau d'alerte", profile.alertLevel)}
      </div>
      <section>
        <h2 class="panel-title">Résumé de l'activité</h2>
        <div class="activity-grid">
          ${activityCard("5", "Réservations")}
          ${activityCard("4", "Emprunts")}
          ${activityCard("15", "Livres favoris")}
          ${activityCard("6", "Commentaires")}
        </div>
      </section>
      <section>
        <h2 class="panel-title">Activité récente</h2>
        <div class="recent-list">
          ${recentActivity.map((item) => `
            <article class="recent-item">
              <div class="recent-action">
                ${icon(item.icon)}
                <span>${escapeHtml(item.label)}</span>
              </div>
              <span class="mono mini-label">${item.date}</span>
            </article>
          `).join("")}
        </div>
      </section>
    </section>
  `;
}

function infoCard(label, value) {
  return `
    <article class="info-card">
      <span class="mini-label">${escapeHtml(label)}</span>
      <strong class="info-value">${escapeHtml(value)}</strong>
    </article>
  `;
}

function activityCard(value, label) {
  return `
    <article class="activity-card">
      <strong class="activity-value">${escapeHtml(value)}</strong>
      <span class="mini-label">${escapeHtml(label)}</span>
    </article>
  `;
}

function renderSettings() {
  return `
    <section class="content">
      <header class="page-head">
        <h1>Paramètres</h1>
        <p>Personnalisez votre compte et gérez vos préférences d'utilisation.</p>
      </header>
      <div class="settings-grid">
        <section class="settings-section">
          <h2>Compte</h2>
          ${settingRow("Email", profile.email, button("Modifier", "settings-toast", "Modification de l'email indisponible dans ce prototype."))}
          ${settingRow("Téléphone", profile.phone, button("Modifier", "settings-toast", "Modification du téléphone indisponible dans ce prototype."))}
        </section>
        <section class="settings-section">
          <h2>Sécurité</h2>
          ${settingRow("Changer mot de passe", "", button("Mettre à jour", "settings-toast", "Changement de mot de passe simulé."))}
          ${settingRow("Authentification à deux facteurs", "Désactivée", button("Activer", "settings-toast primary", "Activation 2FA simulée."), "danger")}
        </section>
        <section class="settings-section">
          <h2>Notifications</h2>
          ${toggleRow("Réservations", "reservations")}
          ${toggleRow("Alertes", "alertes")}
          ${toggleRow("Pénalités", "penalites")}
          ${toggleRow("Nouveautés catalogue", "nouveautes")}
        </section>
        <section class="settings-section">
          <h2>Préférences</h2>
          ${settingRow("Langue", "Français", button("Modifier", "settings-toast", "La langue reste fixée au français dans ce prototype."))}
          ${settingRow("Thème", "Clair", button("Modifier", "settings-toast", "Le thème clair correspond à la référence Stitch."))}
        </section>
        <div class="info-note">
          ${icon("info")}
          <span>Les paramètres sont enregistrés automatiquement. Aucune action supplémentaire n'est nécessaire après modification.</span>
        </div>
      </div>
    </section>
  `;
}

function settingRow(title, subtitle, actionHtml, subtitleTone = "") {
  return `
    <div class="setting-row">
      <div>
        <span class="setting-title">${escapeHtml(title)}</span>
        ${subtitle ? `<span class="setting-sub ${subtitleTone}">${escapeHtml(subtitle)}</span>` : ""}
      </div>
      ${actionHtml}
    </div>
  `;
}

function button(label, action, message) {
  const isPrimary = action.includes("primary");
  return `
    <button class="btn ${isPrimary ? "btn-primary" : ""}" type="button" data-action="${action.split(" ")[0]}" data-message="${escapeHtml(message)}">
      ${escapeHtml(label)}
    </button>
  `;
}

function toggleRow(label, key) {
  const active = state.settings[key];
  return `
    <div class="setting-row">
      <span class="setting-title">${escapeHtml(label)}</span>
      <button class="toggle ${active ? "on" : ""}" type="button" data-action="toggle-setting" data-setting="${key}" aria-label="Activer ou désactiver ${escapeHtml(label)}" aria-pressed="${active}">
      </button>
    </div>
  `;
}

function renderBreadcrumb(parts) {
  return `
    <nav class="breadcrumb" aria-label="Fil d'Ariane">
      ${parts.map((part, index) => {
        const isLast = index === parts.length - 1;
        const text = escapeHtml(part);
        return `
          ${index > 0 ? icon("chevron_right") : ""}
          ${isLast ? `<span>${text}</span>` : `<a href="${index === 0 ? "#catalogue" : "#catalogue"}">${text}</a>`}
        `;
      }).join("")}
    </nav>
  `;
}

function showToast(message) {
  toastRegion.innerHTML = `<div class="toast">${escapeHtml(message)}</div>`;
  window.clearTimeout(showToast.timer);
  showToast.timer = window.setTimeout(() => {
    toastRegion.innerHTML = "";
  }, 2600);
}

function rerenderPreservingSearchFocus() {
  const active = document.activeElement;
  const shouldRestore = active && active.id === "global-search";
  const value = state.searchQuery;
  renderApp();
  if (shouldRestore) {
    const input = document.getElementById("global-search");
    if (input) {
      input.focus();
      input.setSelectionRange(value.length, value.length);
    }
  }
}

document.addEventListener("submit", (event) => {
  if (event.target.id !== "login-form") return;
  event.preventDefault();
  state.authenticated = true;
  state.searchQuery = "";
  state.catalogueFilter = "tous";
  navigate("dashboard");
});

document.addEventListener("click", (event) => {
  const actionTarget = event.target.closest("[data-action]");
  if (!actionTarget) return;

  const action = actionTarget.dataset.action;

  if (action === "toggle-password") {
    const input = document.getElementById("password");
    const iconNode = actionTarget.querySelector(".material-symbols-outlined");
    if (input && iconNode) {
      const visible = input.type === "text";
      input.type = visible ? "password" : "text";
      iconNode.textContent = visible ? "visibility" : "visibility_off";
    }
    return;
  }

  if (action === "logout") {
    event.preventDefault();
    state.authenticated = false;
    state.searchQuery = "";
    state.selectedBookId = "petit-prince";
    showToast("Session fermée.");
    navigate("login");
    return;
  }

  if (action === "catalogue-filter") {
    state.catalogueFilter = actionTarget.dataset.filter;
    renderApp();
    return;
  }

  if (action === "view-details") {
    state.selectedBookId = actionTarget.dataset.bookId;
    navigate("livre-detail");
    return;
  }

  if (action === "toggle-favorite") {
    const bookId = actionTarget.dataset.bookId;
    const book = findBook(bookId);
    if (state.favoriteBookIds.has(bookId)) {
      state.favoriteBookIds.delete(bookId);
      showToast(`${book.title} retiré des favoris.`);
    } else {
      state.favoriteBookIds.add(bookId);
      showToast(`${book.title} ajouté aux favoris.`);
    }
    renderApp();
    return;
  }

  if (action === "reserve-book") {
    const bookId = actionTarget.dataset.bookId;
    const book = findBook(bookId);
    if (book.statusKey !== "available") {
      showToast("Cet ouvrage n'est pas disponible à la réservation.");
      return;
    }
    state.reservedBookIds.add(bookId);
    if (!reservations.some((reservation) => reservation.bookId === bookId && reservation.dynamic)) {
      reservations.unshift({
        id: `res-${Date.now()}`,
        bookId,
        category: book.category,
        code: `RES-2026-${String(reservations.length + 17).padStart(3, "0")}`,
        place: "Bibliothèque Centrale APFA",
        reservationDate: "19/06/2026",
        limitDate: "22/06/2026",
        status: "Réservé",
        statusKey: "reserved",
        countdown: "3 jours restants",
        note: "Votre réservation vient d'être créée. Présentez-vous au comptoir avant la date limite.",
        dynamic: true
      });
    }
    showToast("Réservation créée avec succès.");
    renderApp();
    return;
  }

  if (action === "toggle-setting") {
    const key = actionTarget.dataset.setting;
    state.settings[key] = !state.settings[key];
    showToast("Préférence mise à jour.");
    renderApp();
    return;
  }

  if (action === "settings-toast") {
    showToast(actionTarget.dataset.message || "Action simulée.");
  }
});

document.addEventListener("input", (event) => {
  if (event.target.id !== "global-search") return;
  state.searchQuery = event.target.value;
  rerenderPreservingSearchFocus();
});

window.addEventListener("hashchange", renderApp);

if (!window.location.hash) {
  history.replaceState(null, "", "#login");
}

renderApp();
