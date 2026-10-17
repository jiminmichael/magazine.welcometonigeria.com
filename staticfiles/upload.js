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

  const toDataUrl = (file) =>
    new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = () => reject(new Error("Could not read this image."));
      reader.readAsDataURL(file);
    });

  async function compress(file) {
    const data = await toDataUrl(file);
    return new Promise((resolve) => {
      const image = new Image();
      image.onload = () => {
        const scale = Math.min(1, 1400 / Math.max(image.width, image.height));
        const canvas = document.createElement("canvas");
        canvas.width = Math.round(image.width * scale);
        canvas.height = Math.round(image.height * scale);
        canvas
          .getContext("2d")
          .drawImage(image, 0, 0, canvas.width, canvas.height);
        resolve(canvas.toDataURL("image/jpeg", 0.76));
      };
      image.onerror = () => resolve(data);
      image.src = data;
    });
  }

  let selectedPreviews = [];
  let selectedFileObjects = [];

  function initPhotoPreviews() {
    const input = document.getElementById("story-photos");
    if (!input) return;
    const preview = document.getElementById("photo-previews");
    const submit = document.querySelector(
      '#story-submit-form button[type="submit"]',
    );

    const render = () => {
      preview.innerHTML = selectedPreviews
        .map(
          (src, index) =>
            `<div class="preview-item"><img src="${src}" alt="Selected trip photo ${index + 1}"><button type="button" data-remove-photo="${index}" aria-label="Remove photo ${index + 1}">×</button></div>`,
        )
        .join("");
      preview.querySelectorAll("[data-remove-photo]").forEach((button) =>
        button.addEventListener("click", () => {
          const idx = Number(button.dataset.removePhoto);
          selectedPreviews.splice(idx, 1);
          selectedFileObjects.splice(idx, 1);
          input.value = "";
          render();
        }),
      );
    };

    input.addEventListener("change", async () => {
      const files = [...input.files].filter((file) =>
        file.type.startsWith("image/"),
      );
      if (submit) submit.disabled = true;
      document.getElementById("upload-message").textContent =
        "Preparing your photos...";
      if (files.length > 4) {
        document.getElementById("upload-message").textContent =
          "You can choose up to four photos per story.";
        input.value = "";
        if (submit) submit.disabled = false;
        return;
      }
      try {
        selectedPreviews = await Promise.all(files.map(compress));
        selectedFileObjects = files;
        document.getElementById("upload-message").textContent = "";
        render();
      } catch {
        document.getElementById("upload-message").textContent =
          "One or more photos could not be read. Please try different files.";
      } finally {
        if (submit) submit.disabled = false;
      }
    });

    input._getSelected = () => selectedPreviews;
    input._clearSelected = () => {
      selectedPreviews = [];
      selectedFileObjects = [];
      input.value = "";
      render();
    };
  }

  async function initProfilePhoto() {
    const input = document.querySelector("#profile-photo, #signup-photo");
    if (!input) return;
    input.addEventListener("change", async () => {
      const file = input.files[0];
      if (!file) return;
      if (file.size > 5 * 1024 * 1024) {
        input.setCustomValidity("Please choose an image under 5 MB.");
        input.reportValidity();
        input.value = "";
        return;
      }
      try {
        const previewUrl = await compress(file);
        if (input.form) input.form.dataset.photo = previewUrl;
        const image = document.getElementById("profile-photo-preview");
        if (image) {
          image.src = previewUrl;
          image.hidden = false;
        }
      } catch {
        if (input.form) input.form.dataset.photo = "";
      }
    });
  }

  function initSubmission() {
    const form = document.getElementById("story-submit-form");
    if (!form) return;
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) submitBtn.disabled = true;
      const out = form.querySelector(".form-success");

      const photoInput = form.querySelector("#story-photos");
      const values = new FormData(form);

      const formData = new FormData();
      formData.append("name", String(values.get("name") || "").trim());
      formData.append("email", String(values.get("email") || "").trim());
      formData.append("state", String(values.get("state") || ""));
      formData.append("location", String(values.get("location") || "").trim());
      formData.append("travel_date", String(values.get("travel-date") || ""));
      formData.append("title", String(values.get("title") || "").trim());
      formData.append("experience", String(values.get("experience") || "").trim());
      formData.append("enjoyed", String(values.get("enjoyed") || "").trim());
      formData.append("recommend", String(values.get("recommend") || "Not specified"));
      formData.append("travel_tips", String(values.get("travel-tips") || "").trim());

      selectedFileObjects.forEach((file) => {
        formData.append("photos", file);
      });

      try {
        const res = await fetch("/api/stories/submit/", {
          method: "POST",
          headers: {
            "X-CSRFToken": getCookie("csrftoken") || "",
          },
          body: formData,
        });

        const data = await res.json();
        if (res.ok) {
          if (out) {
            out.textContent = data.message || "Your story has been submitted successfully for review.";
            out.style.color = "";
            out.classList.add("visible");
          }
          form.reset();
          if (photoInput && photoInput._clearSelected) {
            photoInput._clearSelected();
          }
          const uploadMsg = document.getElementById("upload-message");
          if (uploadMsg) uploadMsg.textContent = "";
        } else {
          let errText = "Could not submit story.";
          if (data.errors) {
            errText = Object.entries(data.errors)
              .map(([k, v]) => `${Array.isArray(v) ? v.join(" ") : v}`)
              .join(" ");
          } else if (data.error) {
            errText = data.error;
          }
          if (out) {
            out.textContent = errText;
            out.style.color = "#c53030";
            out.classList.add("visible");
          }
        }
      } catch (err) {
        if (out) {
          out.textContent = "Server error. Could not submit story at this time.";
          out.style.color = "#c53030";
          out.classList.add("visible");
        }
      } finally {
        if (submitBtn) submitBtn.disabled = false;
      }
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    initPhotoPreviews();
    initProfilePhoto();
    initSubmission();
  });
})();
