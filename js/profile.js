(function () {
  const esc = (value) => window.WTNStories.escape(value);

  async function init() {
    const root = document.getElementById("profile-content");
    if (!root) return;
    const id = new URLSearchParams(location.search).get("id");
    if (!id) {
      root.innerHTML = '<section class="empty-state"><h3>Traveller profile not specified</h3><a class="button small" href="stories.html">Explore stories</a></section>';
      return;
    }

    let profileData = null;
    let publishedStories = [];

    try {
      const [profileRes, storiesRes] = await Promise.all([
        fetch(`/api/auth/profiles/${encodeURIComponent(id)}/`),
        fetch(`/api/stories/?author=${encodeURIComponent(id)}`),
      ]);

      if (profileRes.ok) {
        profileData = await profileRes.json();
      }
      if (storiesRes.ok) {
        publishedStories = await storiesRes.json();
      }
    } catch {}

    if (!profileData) {
      // Fallback to sample data matching
      const allStories = window.WTNStories.all();
      const matches = allStories.filter(
        (story) => story.authorId === id || story.author === id,
      );
      if (matches.length) {
        profileData = {
          name: matches[0].author,
          photo: matches[0].authorPhoto,
          bio: "A traveller sharing personal experiences from across Nigeria.",
          stats: {
            published_count: matches.length,
            states_count: new Set(matches.map((s) => s.state)).size,
          },
        };
        publishedStories = matches;
      }
    }

    if (!profileData) {
      root.innerHTML = '<section class="empty-state"><h3>Traveller not found</h3><p>We could not find a contributor matching this link.</p><a class="button small" href="stories.html">Explore stories</a></section>';
      return;
    }

    const name = profileData.name || "Traveller";
    const photo = profileData.photo || "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80";
    const bio = profileData.bio || "A traveller sharing personal experiences from across Nigeria.";
    const publishedCount = profileData.stats ? profileData.stats.published_count : publishedStories.length;
    const statesCount = profileData.stats ? profileData.stats.states_count : 0;

    root.innerHTML = `<section class="profile-hero"><img class="avatar" src="${esc(photo)}" alt="Portrait of ${esc(name)}"><div><p class="eyebrow">Community traveller</p><h1>${esc(name)}</h1><p>${esc(bio)}</p><div class="account-stats"><div><strong>${publishedCount}</strong><span>Published stories</span></div><div><strong>${statesCount}</strong><span>States shared</span></div></div></div></section><section class="section" style="padding-bottom:0"><div class="section-head"><div><p class="eyebrow">From this traveller</p><h2 class="section-title">Stories by ${esc(name.split(" ")[0])}</h2></div></div><div id="profile-stories" class="story-grid"></div></section>`;

    window.WTNStories.render(
      document.getElementById("profile-stories"),
      publishedStories,
    );
  }

  document.addEventListener("DOMContentLoaded", init);
})();
