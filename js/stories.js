(function () {
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  const photo = (id, w = 1000) =>
    `https://images.unsplash.com/${id}?auto=format&fit=crop&w=${w}&q=82`;

  const samples = [
    {
      id: "sample-oshogbo",
      title: "Following the river into Osogbo",
      state: "Osun",
      location: "Osogbo",
      author: "Adaeze Okafor",
      authorId: "adaeze-okafor",
      authorPhoto: photo("photo-1534528741775-53994a69daeb", 160),
      date: "2026-08-12",
      publishedDate: "2026-09-02",
      preview:
        "A slow morning beside the river became a lesson in the living art, stories and generosity of Osogbo.",
      story:
        "I arrived in Osogbo with a loose plan and enough time to change it. The city met me in layers: the hum of the morning market, the shade of old trees and the sound of conversation that seemed to carry from one street to the next.\n\nThe walk beside the river was the part I had imagined, but the people I met made the day. A local guide shared the history behind the works along the route, and suddenly every turn felt less like a view and more like an invitation to listen.\n\nI left with a camera full of details and a notebook full of names. Give yourself room to wander, ask thoughtful questions and let the day take its own shape.",
      images: [
        photo("photo-1516026672322-bc52d61a55d5"),
        photo("photo-1500530855697-b586d89ba3ee"),
        photo("photo-1470770841072-f978cf4d019e"),
      ],
      tips: "Start early for cooler walking. Ask before photographing people, and leave time to hear the stories behind the places.",
      recommendation:
        "Absolutely. Go with curiosity and make time for a local guide.",
      featured: true,
      popularity: 184,
      status: "Published",
    },
    {
      id: "sample-lagos",
      title: "Lagos, best discovered between the plans",
      state: "Lagos",
      location: "Lagos Island",
      author: "Tunde Akinyemi",
      authorId: "tunde-akinyemi",
      authorPhoto: photo("photo-1500648767791-00dcc994a43e", 160),
      date: "2026-07-18",
      publishedDate: "2026-08-21",
      preview:
        "I stopped trying to fit Lagos into a checklist and started following the conversations, the ferries and the afternoon light.",
      story:
        "Lagos moves at a pace that asks you to pay attention. I spent my first day rushing between places and my second day doing almost nothing on schedule. The second day is the one I still talk about.\n\nWe crossed the lagoon, found lunch through a recommendation from a stranger and let the afternoon stretch out. From the water, the city looked both familiar and entirely new. Back on the island, small details kept pulling me in: a doorway painted bright blue, a musician tuning up, a table of fruit arranged like a still life.\n\nMy advice is to plan the essentials, then leave a little space. The best moments were the ones I had not tried to book.",
      images: [
        photo("photo-1518391846015-55a9cc003b25"),
        photo("photo-1517248135467-4c7edcad34c4"),
        photo("photo-1500534623283-312aade485b7"),
      ],
      tips: "Give yourself extra time for local transport. Keep essentials close and ask residents for current, practical advice.",
      recommendation:
        "Yes, especially for travellers who enjoy cities with many layers.",
      featured: true,
      popularity: 212,
      status: "Published",
    },
    {
      id: "sample-cross-river",
      title: "A quieter kind of adventure in Cross River",
      state: "Cross River",
      location: "Obudu",
      author: "Sheriff Bello",
      authorId: "sheriff-bello",
      authorPhoto: photo("photo-1506794778202-cad84cf45f1d", 160),
      date: "2026-06-04",
      publishedDate: "2026-07-12",
      preview:
        "The road north kept opening into green hills, cool air and the kind of quiet that makes you notice everything.",
      story:
        "The journey towards Obudu was as much a part of the trip as the days we spent there. The landscape changed gradually, and then all at once: greener slopes, a cooler breeze and a horizon that seemed to keep moving farther away.\n\nI travelled with family and we took the long stops seriously. We shared food, spoke with people along the way and watched the clouds settle over the hills. There is something grounding about a place that asks you to slow down without making a show of it.\n\nBring layers for the cooler evenings and check local travel conditions before you leave. Most of all, leave enough time to enjoy the road.",
      images: [
        photo("photo-1464822759023-fed622ff2c3b"),
        photo("photo-1472396961693-142e6e269027"),
        photo("photo-1441974231531-c6227db76b6e"),
      ],
      tips: "Pack a light jacket and confirm road and weather conditions before travel. Start longer drives early in the day.",
      recommendation:
        "Yes. It is a lovely change of pace for anyone who enjoys open landscapes.",
      featured: true,
      popularity: 138,
      status: "Published",
    },
    {
      id: "sample-abuja",
      title: "The small trails that changed my Abuja weekend",
      state: "FCT Abuja",
      location: "Abuja",
      author: "Mariam Yusuf",
      authorId: "mariam-yusuf",
      authorPhoto: photo("photo-1531123897727-8f129e1688ce", 160),
      date: "2026-05-09",
      publishedDate: "2026-06-18",
      preview:
        "A weekend close to home turned into a collection of early walks, long breakfasts and new ways to see the capital.",
      story:
        "I thought I knew Abuja because I knew the roads I used every week. Over one unhurried weekend, I found another version of the city by taking the morning slowly and saying yes to a few local recommendations.\n\nWe started before the day warmed up, walked a familiar route at a different pace and stopped for breakfast somewhere we had driven past dozens of times. The conversations were easy; the views, even more so. I came away reminded that travel can begin with a different turn on a road you already know.\n\nChoose one part of the city rather than trying to cover everything. The best discoveries happened when we were not watching the clock.",
      images: [
        photo("photo-1500534314209-a25ddb2bd429"),
        photo("photo-1501785888041-af3ef285b470"),
        photo("photo-1470252649378-9c29740c9fa8"),
      ],
      tips: "Go early to enjoy outdoor walks before the heat builds. Ask locally about access and conditions, then keep your plan flexible.",
      recommendation: "Definitely. Abuja rewards a slower, more curious visit.",
      featured: false,
      popularity: 95,
      status: "Published",
    },
    {
      id: "sample-kano",
      title: "Kano mornings, told one conversation at a time",
      state: "Kano",
      location: "Kano",
      author: "Ibrahim Sani",
      authorId: "ibrahim-sani",
      authorPhoto: photo("photo-1507003211169-0a1dd7228f2d", 160),
      date: "2026-04-22",
      publishedDate: "2026-05-30",
      preview:
        "The city woke up around me in colour and sound, and every conversation added a little more context.",
      story:
        "I began my visit with a list of places and finished it with a list of people to thank. Kano has a rhythm all of its own, and I found that a patient morning was the best way to meet it.\n\nAt each stop I learned a little more by listening. A shopkeeper told me how long his family had worked in the neighbourhood; a driver pointed out a route I would never have found alone. By the end of the day, the city felt less like a destination and more like a series of generous introductions.\n\nWear comfortable shoes, bring water and listen before you take photographs. It made all the difference to my visit.",
      images: [
        photo("photo-1494783367193-149034c05e8f"),
        photo("photo-1488646953014-85cb44e25828"),
        photo("photo-1500534623283-312aade485b7"),
      ],
      tips: "Dress for the weather, carry water and ask permission before taking portraits. A local guide can add useful context.",
      recommendation: "Yes. Take your time and let local voices lead.",
      featured: false,
      popularity: 76,
      status: "Published",
    },
  ];

  const states = [
    "Abia",
    "Adamawa",
    "Akwa Ibom",
    "Anambra",
    "Bauchi",
    "Bayelsa",
    "Benue",
    "Borno",
    "Cross River",
    "Delta",
    "Ebonyi",
    "Edo",
    "Ekiti",
    "Enugu",
    "Gombe",
    "Imo",
    "Jigawa",
    "Kaduna",
    "Kano",
    "Katsina",
    "Kebbi",
    "Kogi",
    "Kwara",
    "Lagos",
    "Nasarawa",
    "Niger",
    "Ogun",
    "Ondo",
    "Osun",
    "Oyo",
    "Plateau",
    "Rivers",
    "Sokoto",
    "Taraba",
    "Yobe",
    "Zamfara",
    "FCT Abuja",
  ];

  const read = (key, fallback = []) => {
    try {
      return JSON.parse(localStorage.getItem(key)) || fallback;
    } catch {
      return fallback;
    }
  };

  const all = () => samples;

  const esc = (value) =>
    String(value ?? "").replace(
      /[&<>"']/g,
      (c) =>
        ({
          "&": "&amp;",
          "<": "&lt;",
          ">": "&gt;",
          '"': "&quot;",
          "'": "&#39;",
        })[c],
    );

  const dateLabel = (value) => {
    if (!value) return "";
    const d = new Date(`${value}T12:00:00`);
    return Number.isNaN(d.getTime())
      ? value
      : d.toLocaleDateString("en-NG", {
          day: "numeric",
          month: "short",
          year: "numeric",
        });
  };

  function card(story) {
    const cover =
      story.images?.[0] || photo("photo-1500530855697-b586d89ba3ee");
    const label = story.id && String(story.id).startsWith("sample-")
      ? "Sample story"
      : story.featured
        ? "Featured"
        : "";
    return `<article class="story-card"><a class="story-image" href="story.html?id=${encodeURIComponent(story.id)}" aria-label="Read ${esc(story.title)}"><img src="${esc(cover)}" alt="${esc(story.location || story.state)} as seen by ${esc(story.author)}" loading="lazy">${label ? `<span class="label">${label}</span>` : ""}</a><div class="story-meta"><span>${esc(story.state)}</span><span class="dot"></span><span>${dateLabel(story.date)}</span></div><h3><a href="story.html?id=${encodeURIComponent(story.id)}">${esc(story.title)}</a></h3><p class="preview">${esc(story.preview || "A first-person travel experience, shared by a member of our community.")}</p><div class="story-byline"><span>By <a href="profile.html?id=${encodeURIComponent(story.authorId || story.author)}">${esc(story.author)}</a></span><a class="text-link" href="story.html?id=${encodeURIComponent(story.id)}">Read story</a></div></article>`;
  }

  function render(container, items) {
    const target =
      typeof container === "string"
        ? document.getElementById(container)
        : container;
    if (!target) return;
    target.innerHTML = items.length
      ? items.map(card).join("")
      : '<div class="empty-state"><h3>No stories found just yet</h3><p>Try another search, or be the first to share an experience from here.</p><a class="button small" href="share-story.html">Share your story</a></div>';
  }

  async function initListings() {
    const grid = document.querySelector("[data-story-grid]");
    if (!grid) return;
    const stateInput = document.getElementById("state-filter");
    const sortInput = document.getElementById("sort-filter");
    const query = document.getElementById("story-search");
    const count = document.getElementById("result-count");
    const statePage = document.body.dataset.page === "state";
    const params = new URLSearchParams(location.search);

    if (query && params.get("q")) query.value = params.get("q");
    if (stateInput && params.get("state")) stateInput.value = params.get("state");

    const update = async () => {
      const state = statePage
        ? params.get("state") || ""
        : stateInput?.value || "";
      const term = (query?.value || "").trim();
      const sort = sortInput?.value || "newest";

      try {
        const queryParams = new URLSearchParams();
        if (state) queryParams.set("state", state);
        if (term) queryParams.set("q", term);
        if (sort) queryParams.set("sort", sort);

        const res = await fetch(`/api/stories/?${queryParams.toString()}`);
        if (res.ok) {
          const items = await res.json();
          render(grid, items);
          if (count)
            count.textContent = `${items.length} ${items.length === 1 ? "story" : "stories"}`;
          return;
        }
      } catch (e) {
        // Fallback to local filtering
      }

      let items = all();
      if (state)
        items = items.filter(
          (s) =>
            s.state.toLocaleLowerCase() === state.toLocaleLowerCase() ||
            (state === "Abuja" && s.state === "FCT Abuja"),
        );
      if (term)
        items = items.filter((s) =>
          [s.title, s.state, s.location, s.author, s.preview]
            .join(" ")
            .toLocaleLowerCase()
            .includes(term.toLocaleLowerCase()),
        );
      if (sort === "popular")
        items.sort((a, b) => (b.popularity || 0) - (a.popularity || 0));
      else if (sort === "featured")
        items = items.filter((s) => s.featured);
      else
        items.sort(
          (a, b) =>
            new Date(b.publishedDate || b.date) -
            new Date(a.publishedDate || a.date),
        );
      render(grid, items);
      if (count)
        count.textContent = `${items.length} ${items.length === 1 ? "story" : "stories"}`;
    };

    [stateInput, sortInput].forEach((el) => el?.addEventListener("change", update));
    query?.addEventListener("input", update);
    await update();
  }

  async function initStates() {
    const grid = document.getElementById("states-grid");
    const homeGrid = document.getElementById("home-state-grid");
    if (!grid && !homeGrid) return;

    let stateData = [];
    try {
      const res = await fetch("/api/states/");
      if (res.ok) {
        stateData = await res.json();
      }
    } catch {}

    const stateCountMap = {};
    stateData.forEach((s) => {
      stateCountMap[s.name] = s.count;
    });

    const makeCards = (list) =>
      list
        .map((name) => {
          const i = states.indexOf(name);
          const count = stateCountMap[name] !== undefined
            ? stateCountMap[name]
            : all().filter((s) => s.state === name || (name === "FCT Abuja" && s.state === "Abuja")).length;
          const queryName = name === "FCT Abuja" ? "Abuja" : name;
          return `<a class="state-card" href="state.html?state=${encodeURIComponent(queryName)}"><span class="state-number">${String(i + 1).padStart(2, "0")}</span><span><h2>${esc(name)}</h2><p>${count} ${count === 1 ? "community story" : "community stories"}</p></span><span class="state-arrow" aria-hidden="true">↗</span></a>`;
        })
        .join("");

    if (grid) grid.innerHTML = makeCards(states);
    if (homeGrid)
      homeGrid.innerHTML = makeCards([
        "Lagos",
        "FCT Abuja",
        "Osun",
        "Cross River",
      ]);
  }

  async function initFeatured() {
    const grids = document.querySelectorAll("[data-featured-grid]");
    if (!grids.length) return;

    try {
      const res = await fetch("/api/stories/?featured=true&limit=3");
      if (res.ok) {
        const featuredStories = await res.json();
        if (featuredStories.length) {
          grids.forEach((grid) => render(grid, featuredStories));
          return;
        }
      }
    } catch {}

    grids.forEach((grid) =>
      render(
        grid,
        all()
          .filter((s) => s.featured)
          .slice(0, 3),
      ),
    );
  }

  async function initArticle() {
    const root = document.getElementById("story-article");
    if (!root) return;
    const id = new URLSearchParams(location.search).get("id");
    if (!id) {
      root.innerHTML = '<section class="empty-state"><h3>Story not specified</h3><p>Please choose a story to read.</p><a class="button small" href="stories.html">Explore stories</a></section>';
      return;
    }

    let story = null;
    let isPending = false;

    try {
      const res = await fetch(`/api/stories/${encodeURIComponent(id)}/`);
      if (res.ok) {
        story = await res.json();
      } else if (res.status === 403) {
        isPending = true;
      }
    } catch {}

    if (!story) {
      story = all().find((item) => item.id === id);
    }

    if (!story) {
      root.innerHTML = isPending
        ? '<section class="empty-state"><h3>This story is being reviewed</h3><p>It is visible in the contributor account, but is not public until approved.</p><a class="button small" href="stories.html">Explore published stories</a></section>'
        : '<section class="empty-state"><h3>Story not found</h3><p>This story may have been removed or the link is incomplete.</p><a class="button small" href="stories.html">Explore stories</a></section>';
      return;
    }

    document.title = `${story.title} | Welcome to Nigeria Travel Magazine`;
    const gallery = story.images?.length
      ? story.images
      : [photo("photo-1500530855697-b586d89ba3ee")];
    const paragraphs = (
      story.story ||
      story.preview ||
      "A travel experience shared by a member of our community."
    )
      .split(/\n\n+/)
      .map((p) => `<p>${esc(p)}</p>`)
      .join("");

    const isSaved = Boolean(story.is_saved);

    root.innerHTML = `<header class="article-head"><p class="breadcrumb"><a href="stories.html">Explore stories</a> / ${esc(story.state)}</p><div class="story-meta"><span>${esc(story.state)}</span><span class="dot"></span><span>${esc(story.location || story.state)}</span><span class="dot"></span><span>${dateLabel(story.publishedDate || story.date)}</span></div><h1 class="story-title">${esc(story.title)}</h1><p class="body-lead">${esc(story.preview || "A first-person travel experience from across Nigeria.")}</p><div class="article-byline"><img class="avatar" src="${esc(story.authorPhoto || photo("photo-1534528741775-53994a69daeb", 160))}" alt=""><p>Words and photographs by<br><a href="profile.html?id=${encodeURIComponent(story.authorId || story.author)}">${esc(story.author)}</a></p><button class="button outline small" data-save-story="${esc(story.id)}">${isSaved ? "Saved" : "Save story"}</button></div></header><img class="article-hero" src="${esc(gallery[0])}" alt="${esc(story.location || story.state)} photographed by ${esc(story.author)}"><div class="article-body"><div class="article-copy"><p class="article-intro">${paragraphs}</p><h2 class="section-title" style="font-size:36px">A few notes from the journey</h2><div class="article-gallery">${gallery.map((src, i) => `<button class="gallery-image" data-gallery-index="${i}" aria-label="Enlarge travel photo ${i + 1}"><img src="${esc(src)}" alt="Travel photograph ${i + 1} from ${esc(story.location || story.state)}" loading="lazy"></button>`).join("")}</div><h2 class="section-title" style="font-size:36px">Travel tips</h2><p>${esc(story.tips || "Ask local residents for current advice and leave enough time to enjoy the experience.")}</p><h2 class="section-title" style="font-size:36px">Would you recommend it?</h2><p>${esc(story.recommendation || "Yes, I would recommend making time for this experience.")}</p></div><aside class="article-aside"><h3>At a glance</h3><p><strong>State</strong><br>${esc(story.state)}</p><p><strong>Location</strong><br>${esc(story.location || story.state)}</p><p><strong>Travelled</strong><br>${dateLabel(story.date)}</p><p><strong>Published</strong><br>${dateLabel(story.publishedDate || story.date)}</p></aside></div><section class="section wrap"><div class="section-head"><div><p class="eyebrow">Keep exploring</p><h2 class="section-title">More stories from Nigeria</h2></div></div><div class="story-grid" data-related-grid></div></section><div class="lightbox" role="dialog" aria-modal="true" aria-label="Photo viewer"><button class="lightbox-close" aria-label="Close photo">×</button><button class="lightbox-prev" aria-label="Previous photo">‹</button><img src="" alt=""><button class="lightbox-next" aria-label="Next photo">›</button></div>`;

    const relatedGrid = root.querySelector("[data-related-grid]");
    if (relatedGrid) {
      if (story.related && story.related.length) {
        render(relatedGrid, story.related);
      } else {
        render(
          relatedGrid,
          all().filter((item) => item.id !== story.id && item.state === story.state).slice(0, 3)
        );
      }
    }

    initSaveButtons();
    initLightbox(gallery);
  }

  function initSaveButtons() {
    document.querySelectorAll("[data-save-story]").forEach((button) =>
      button.addEventListener("click", async () => {
        const id = button.dataset.saveStory;
        try {
          const res = await fetch(`/api/stories/${encodeURIComponent(id)}/save/`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCookie("csrftoken") || "",
            },
          });
          if (res.status === 401 || res.status === 403) {
            location.href = `signin.html?next=${encodeURIComponent(location.pathname + location.search)}`;
            return;
          }
          const data = await res.json();
          button.textContent = data.saved ? "Saved" : "Save story";
        } catch (e) {
          // Fallback redirect
          location.href = `signin.html?next=${encodeURIComponent(location.pathname + location.search)}`;
        }
      }),
    );
  }

  function initLightbox(images) {
    const box = document.querySelector(".lightbox");
    if (!box) return;
    const image = box.querySelector("img");
    let index = 0;
    const show = (i) => {
      index = (i + images.length) % images.length;
      image.src = images[index];
      image.alt = `Travel photograph ${index + 1} of ${images.length}`;
      box.classList.add("open");
      document.body.style.overflow = "hidden";
    };
    const close = () => {
      box.classList.remove("open");
      document.body.style.overflow = "";
    };
    document
      .querySelectorAll("[data-gallery-index]")
      .forEach((button) =>
        button.addEventListener("click", () =>
          show(Number(button.dataset.galleryIndex)),
        ),
      );
    box.querySelector(".lightbox-close")?.addEventListener("click", close);
    box
      .querySelector(".lightbox-prev")
      ?.addEventListener("click", () => show(index - 1));
    box
      .querySelector(".lightbox-next")
      ?.addEventListener("click", () => show(index + 1));
    box.addEventListener("click", (e) => {
      if (e.target === box) close();
    });
    document.addEventListener("keydown", (e) => {
      if (!box.classList.contains("open")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") show(index - 1);
      if (e.key === "ArrowRight") show(index + 1);
    });
  }

  window.WTNStories = {
    samples,
    states,
    all,
    read,
    render,
    card,
    initListings,
    initStates,
    initFeatured,
    initArticle,
    initSaveButtons,
    dateLabel,
    escape: esc,
  };

  document.addEventListener("DOMContentLoaded", () => {
    initListings();
    initStates();
    initFeatured();
    initArticle();
  });
})();
