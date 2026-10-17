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

  const message = (form, text, isError = false) => {
    const node = form.querySelector(".form-success");
    if (node) {
      node.textContent = text;
      node.classList.add("visible");
      if (isError) {
        node.style.color = "#c53030";
      } else {
        node.style.color = "";
      }
    }
  };

  function initSignup() {
    const form = document.getElementById("signup-form");
    if (!form) return;

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const submitBtn = form.querySelector("button[type=submit]");
      if (submitBtn) submitBtn.disabled = true;

      const formData = new FormData(form);
      const password = formData.get("password");
      const confirmPassword = formData.get("confirm-password");

      if (password !== confirmPassword) {
        message(form, "Your passwords do not match. Please try again.", true);
        if (submitBtn) submitBtn.disabled = false;
        return;
      }

      // Add profile photo if selected via file input
      const photoInput = document.getElementById("signup-photo");
      if (photoInput && photoInput.files && photoInput.files[0]) {
        formData.set("avatar", photoInput.files[0]);
      }

      try {
        const res = await fetch("/api/auth/signup/", {
          method: "POST",
          headers: {
            "X-CSRFToken": getCookie("csrftoken") || "",
          },
          body: formData,
        });

        const data = await res.json();
        if (res.ok) {
          localStorage.setItem("wtnUser", JSON.stringify(data.user));
          location.href = "account.html";
        } else {
          let errText = "Could not create account.";
          if (data.errors) {
            errText = Object.entries(data.errors)
              .map(([k, v]) => `${Array.isArray(v) ? v.join(" ") : v}`)
              .join(" ");
          } else if (data.error) {
            errText = data.error;
          }
          message(form, errText, true);
        }
      } catch (err) {
        message(form, "Unable to communicate with the server. Please try again.", true);
      } finally {
        if (submitBtn) submitBtn.disabled = false;
      }
    });
  }

  function initSignin() {
    const form = document.getElementById("signin-form");
    if (!form) return;

    const remembered = localStorage.getItem("wtnRememberEmail");
    if (remembered && form.elements.email) form.elements.email.value = remembered;

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const submitBtn = form.querySelector("button[type=submit]");
      if (submitBtn) submitBtn.disabled = true;

      const email = String(form.elements.email.value).trim().toLowerCase();
      const password = form.elements.password.value;
      const remember = form.elements.remember ? form.elements.remember.checked : false;

      const payload = { email, password, remember };

      try {
        const res = await fetch("/api/auth/signin/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken") || "",
          },
          body: JSON.stringify(payload),
        });

        const data = await res.json();
        if (res.ok) {
          if (remember) localStorage.setItem("wtnRememberEmail", email);
          else localStorage.removeItem("wtnRememberEmail");

          localStorage.setItem("wtnUser", JSON.stringify(data.user));

          const next = new URLSearchParams(location.search).get("next");
          location.href =
            next && /^([a-z0-9-]+\.html)(\?.*)?$/i.test(next)
              ? next
              : "account.html";
        } else {
          message(form, data.error || "Invalid login credentials.", true);
        }
      } catch (err) {
        message(form, "Server error. Please try again later.", true);
      } finally {
        if (submitBtn) submitBtn.disabled = false;
      }
    });
  }

  function storyCard(story) {
    return window.WTNStories.card(story)
      .replace(
        "</article>",
        '<div class="story-status ' +
          (story.status === "Published" ? "published" : "") +
          '">' +
          window.WTNStories.escape(story.status || "Pending Review") +
          "</div></article>",
      );
  }

  async function initAccount() {
    const root = document.getElementById("account-content");
    if (!root) return;

    root.innerHTML = '<div style="padding: 40px 0; text-align: center;"><p>Loading your traveller notebook...</p></div>';

    let user = null;
    try {
      const authRes = await fetch("/api/auth/me/");
      if (authRes.ok) {
        const authData = await authRes.json();
        if (authData.authenticated && authData.user) {
          user = authData.user;
          localStorage.setItem("wtnUser", JSON.stringify(user));
        }
      }
    } catch {}

    if (!user) {
      localStorage.removeItem("wtnUser");
      root.innerHTML =
        '<div class="empty-state"><h3>Sign in to see your stories</h3><p>Your submissions, saved reads and profile live securely in your account.</p><a class="button small" href="signin.html">Sign in</a></div>';
      return;
    }

    let userStoriesData = {
      submitted: [],
      pending: [],
      published: [],
      saved: [],
      stats: { submitted_count: 0, pending_count: 0, published_count: 0, states_count: 0 },
    };

    try {
      const storiesRes = await fetch("/api/stories/user/");
      if (storiesRes.ok) {
        userStoriesData = await storiesRes.json();
      }
    } catch {}

    const submitted = userStoriesData.submitted;
    const pending = userStoriesData.pending;
    const published = userStoriesData.published;
    const saved = userStoriesData.saved;
    const stats = userStoriesData.stats;

    root.innerHTML = `<div class="account-head"><img class="avatar" src="${window.WTNStories.escape(user.photo || "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=180&q=80")}" alt="Profile photo"><div><h2>${window.WTNStories.escape(user.name)}</h2><p>${window.WTNStories.escape(user.email)}</p><p>${window.WTNStories.escape(user.bio || "Nigeria traveller and story sharer.")}</p><div class="account-stats"><div><strong>${stats.submitted_count}</strong><span>My stories</span></div><div><strong>${stats.pending_count}</strong><span>Pending</span></div><div><strong>${stats.published_count}</strong><span>Published</span></div><div><strong>${stats.states_count}</strong><span>States shared</span></div></div></div></div><div class="account-toolbar" style="display:flex;gap:10px;margin-top:20px"><button class="button outline small" id="edit-profile">Edit profile</button><button class="button outline small" id="sign-out">Sign out</button></div><form class="form-panel" id="edit-profile-form" hidden style="margin-top:20px"><div class="form-grid"><div class="field"><label for="edit-name">Full name</label><input id="edit-name" name="name" value="${window.WTNStories.escape(user.name)}" required></div><div class="field"><label for="edit-email">Email</label><input id="edit-email" type="email" value="${window.WTNStories.escape(user.email)}" disabled></div><div class="field"><label for="edit-avatar">Profile photo</label><input id="edit-avatar" name="avatar" type="file" accept="image/*"></div><div class="field full"><label for="edit-bio">Short bio</label><textarea id="edit-bio" name="bio">${window.WTNStories.escape(user.bio || "")}</textarea></div></div><button class="button small" style="margin-top:16px" type="submit">Save profile</button><div class="form-success"></div></form><div class="account-tabs" role="tablist"><button class="active" data-account-tab="all">My stories (${submitted.length})</button><button data-account-tab="pending">Pending (${pending.length})</button><button data-account-tab="published">Published (${published.length})</button><button data-account-tab="saved">Saved (${saved.length})</button></div><div id="account-story-grid" class="story-grid"></div>`;

    const draw = (tab) => {
      let list =
        tab === "saved"
          ? saved
          : tab === "pending"
            ? pending
            : tab === "published"
              ? published
              : submitted;
      const grid = document.getElementById("account-story-grid");
      if (!grid) return;
      grid.innerHTML = list.length
        ? list.map(storyCard).join("")
        : '<div class="empty-state"><h3>' +
          (tab === "saved" ? "No saved stories yet" : "No stories here yet") +
          '</h3><p>Explore stories, or share a journey of your own.</p><a class="button small" href="' +
          (tab === "saved" ? "stories.html" : "share-story.html") +
          '">' +
          (tab === "saved" ? "Explore stories" : "Share a story") +
          "</a></div>";
    };

    draw("all");

    root.querySelectorAll("[data-account-tab]").forEach((button) =>
      button.addEventListener("click", () => {
        root
          .querySelectorAll("[data-account-tab]")
          .forEach((item) => item.classList.toggle("active", item === button));
        draw(button.dataset.accountTab);
      }),
    );

    document.getElementById("sign-out")?.addEventListener("click", async () => {
      try {
        await fetch("/api/auth/signout/", {
          method: "POST",
          headers: {
            "X-CSRFToken": getCookie("csrftoken") || "",
          },
        });
      } catch {}
      localStorage.removeItem("wtnUser");
      location.href = "index.html";
    });

    const editForm = document.getElementById("edit-profile-form");
    document.getElementById("edit-profile")?.addEventListener("click", () => {
      editForm.hidden = !editForm.hidden;
    });

    editForm?.addEventListener("submit", async (event) => {
      event.preventDefault();
      const saveBtn = editForm.querySelector("button[type=submit]");
      if (saveBtn) saveBtn.disabled = true;

      const formData = new FormData();
      formData.append("name", editForm.elements.name.value.trim());
      formData.append("bio", editForm.elements.bio.value.trim());
      const avatarFile = editForm.elements.avatar ? editForm.elements.avatar.files[0] : null;
      if (avatarFile) formData.append("avatar", avatarFile);

      try {
        const res = await fetch("/api/auth/profile/", {
          method: "PATCH",
          headers: {
            "X-CSRFToken": getCookie("csrftoken") || "",
          },
          body: formData,
        });
        const data = await res.json();
        if (res.ok) {
          localStorage.setItem("wtnUser", JSON.stringify(data.user));
          message(editForm, "Profile updated successfully.");
          setTimeout(() => initAccount(), 800);
        } else {
          message(editForm, "Failed to update profile.", true);
        }
      } catch (err) {
        message(editForm, "Server error. Could not save profile.", true);
      } finally {
        if (saveBtn) saveBtn.disabled = false;
      }
    });
  }

  function initForgot() {
    const form = document.getElementById("forgot-form");
    if (!form) return;

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const submitBtn = form.querySelector("button[type=submit]");
      if (submitBtn) submitBtn.disabled = true;

      const email = form.elements.email ? form.elements.email.value.trim() : "";

      try {
        const res = await fetch("/api/auth/forgot-password/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken") || "",
          },
          body: JSON.stringify({ email }),
        });
        const data = await res.json();
        message(form, data.message || "Password reset instructions have been sent.");
        form.reset();
      } catch (err) {
        message(form, "If an account matches that email address, password reset instructions have been sent.");
        form.reset();
      } finally {
        if (submitBtn) submitBtn.disabled = false;
      }
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    initSignup();
    initSignin();
    initAccount();
    initForgot();
  });
})();
