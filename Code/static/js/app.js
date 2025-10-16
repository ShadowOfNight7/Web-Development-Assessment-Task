document.addEventListener("DOMContentLoaded", function () {
  const dropArea = document.getElementById("drop-area");
  const fileInput = document.getElementById("fileElem");
  const previewDiv = document.getElementById("image-preview");
  const dropText = document.getElementById("drop-text");
  const removeBtn = document.getElementById("remove-image-btn");

  if (!dropArea || !fileInput || !previewDiv) return;

  dropArea.addEventListener("click", function (e) {
    if (e.target !== fileInput && e.target !== removeBtn) {
      e.stopPropagation();
    }
  });

  ["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
    dropArea.addEventListener(eventName, preventDefaults, false);
  });

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  ["dragenter", "dragover"].forEach((eventName) => {
    dropArea.addEventListener(
      eventName,
      () => dropArea.classList.add("highlight"),
      false
    );
  });

  ["dragleave", "drop"].forEach((eventName) => {
    dropArea.addEventListener(
      eventName,
      () => dropArea.classList.remove("highlight"),
      false
    );
  });

  dropArea.addEventListener("drop", handleDrop, false);
  fileInput.addEventListener("change", handleFiles, false);

  removeBtn.addEventListener("click", function (e) {
    e.stopPropagation();
    fileInput.value = "";
    previewDiv.innerHTML = "";
    dropText.style.display = "block";
    removeBtn.style.display = "none";
  });

  function handleDrop(e) {
    let dt = e.dataTransfer;
    let files = dt.files;
    fileInput.files = files;
    handleFiles();
  }

  function handleFiles() {
    const file = fileInput.files[0];
    if (!file) return;

    dropText.style.display = "none";
    previewDiv.innerHTML = "<p>Loading...</p>";

    const reader = new FileReader();
    reader.onload = function (e) {
      const img = document.createElement("img");
      img.src = e.target.result;
      img.style.maxWidth = "100%";
      img.style.borderRadius = "8px";

      previewDiv.innerHTML = "";
      previewDiv.appendChild(img);
      removeBtn.style.display = "inline-block";
    };
    reader.readAsDataURL(file);
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const carousel = document.getElementById("carouselImages");
  if (!carousel) return;

  const totalSlides = carousel.children.length;
  let index = 0;
  let autoSlide = true;
  let intervalId;

  const dotsContainer = document.getElementById("carouselDots");

  for (let i = 0; i < totalSlides; i++) {
    const dot = document.createElement("span");
    dot.addEventListener("click", () => {
      index = i;
      showSlide();
    });
    dotsContainer.appendChild(dot);
  }
  const dots = dotsContainer.querySelectorAll("span");

  function updateDots() {
    dots.forEach((dot, i) => {
      dot.classList.toggle("active", i === index);
    });
  }

  function showSlide() {
    carousel.style.transform = `translateX(-${index * 600}px)`;
    updateDots();
  }

  function nextSlide() {
    index = (index + 1) % totalSlides;
    showSlide();
  }

  function prevSlide() {
    index = (index - 1 + totalSlides) % totalSlides;
    showSlide();
  }

  function startAutoSlide() {
    intervalId = setInterval(nextSlide, 3000);
  }

  function stopAutoSlide() {
    clearInterval(intervalId);
  }

  document.querySelector(".next").addEventListener("click", nextSlide);
  document.querySelector(".prev").addEventListener("click", prevSlide);

  const pauseBtn = document.getElementById("pauseBtn");
  pauseBtn.addEventListener("click", () => {
    if (autoSlide) {
      stopAutoSlide();
      pauseBtn.textContent = "▶";
    } else {
      startAutoSlide();
      pauseBtn.textContent = "⏸";
    }
    autoSlide = !autoSlide;
  });

  showSlide();
  startAutoSlide();
});

document.addEventListener("DOMContentLoaded", function () {
  const dropArea = document.getElementById("drop-area");
  const fileInput = document.getElementById("fileElem");
  const previewDiv = document.getElementById("image-preview");

  if (!dropArea || !fileInput || !previewDiv) return;

  dropArea.addEventListener("click", () => fileInput.click());

  ["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
    dropArea.addEventListener(eventName, preventDefaults, false);
  });

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  ["dragenter", "dragover"].forEach((eventName) => {
    dropArea.addEventListener(
      eventName,
      () => dropArea.classList.add("highlight"),
      false
    );
  });

  ["dragleave", "drop"].forEach((eventName) => {
    dropArea.addEventListener(
      eventName,
      () => dropArea.classList.remove("highlight"),
      false
    );
  });

  dropArea.addEventListener("drop", handleDrop, false);
  fileInput.addEventListener("change", handleFiles, false);

  function handleDrop(e) {
    let dt = e.dataTransfer;
    let files = dt.files;
    fileInput.files = files;
    handleFiles();
  }

  function handleFiles() {
    const file = fileInput.files[0];
    if (!file) return;

    previewDiv.innerHTML = "<p>Loading...</p>";

    const reader = new FileReader();
    reader.onload = function (e) {
      const img = document.createElement("img");
      img.src = e.target.result;
      img.style.maxWidth = "100%";
      img.style.borderRadius = "8px";
      previewDiv.innerHTML = "";
      previewDiv.appendChild(img);
    };
    reader.readAsDataURL(file);
  }
});
