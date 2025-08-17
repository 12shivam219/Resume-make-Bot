document.addEventListener("DOMContentLoaded", function () {
  // Stepper form functionality
  const steps = document.querySelectorAll(".form-step");
  const nextButtons = document.querySelectorAll(".btn-next");
  const prevButtons = document.querySelectorAll(".btn-prev");
  let currentStep = 0;

  // Initialize - show first step
  showStep(currentStep);

  // Next button click handler
  nextButtons.forEach((button) => {
    button.addEventListener("click", function (e) {
      e.preventDefault();
      if (validateStep(currentStep)) {
        currentStep++;
        showStep(currentStep);
      }
    });
  });

  // Previous button click handler
  prevButtons.forEach((button) => {
    button.addEventListener("click", function (e) {
      e.preventDefault();
      currentStep--;
      showStep(currentStep);
    });
  });

  function showStep(stepIndex) {
    // Hide all steps
    steps.forEach((step) => {
      step.style.display = "none";
    });

    // Show current step
    steps[stepIndex].style.display = "block";

    // Update navigation buttons
    if (stepIndex === 0) {
      document.querySelector(".btn-prev").style.display = "none";
    } else {
      document.querySelector(".btn-prev").style.display = "inline-block";
    }

    if (stepIndex === steps.length - 1) {
      document.querySelector(".btn-next").textContent = "Submit";
    } else {
      document.querySelector(".btn-next").textContent = "Next";
    }
  }

  function validateStep(stepIndex) {
    const currentStep = steps[stepIndex];
    const inputs = currentStep.querySelectorAll(
      "input[required], textarea[required], select[required]"
    );
    let isValid = true;

    inputs.forEach((input) => {
      if (!input.value.trim()) {
        input.classList.add("error");
        isValid = false;
      } else {
        input.classList.remove("error");
      }
    });

    if (!isValid) {
      alert("Please fill in all required fields");
    }

    return isValid;
  }

  // File upload preview
  const fileInputs = document.querySelectorAll('input[type="file"]');
  fileInputs.forEach((input) => {
    input.addEventListener("change", function () {
      const fileName = this.files[0]?.name || "No file selected";
      const label = this.nextElementSibling;
      if (label && label.classList.contains("file-label")) {
        label.textContent = fileName;
      }
    });
  });

  // Dynamic bullet point counters
  const bulletTextareas = document.querySelectorAll("textarea.bullet-points");
  bulletTextareas.forEach((textarea) => {
    const counter = document.createElement("div");
    counter.className = "bullet-counter";
    counter.textContent = "0/6 bullet points";
    textarea.parentNode.insertBefore(counter, textarea.nextSibling);

    textarea.addEventListener("input", function () {
      const count = this.value
        .split("\n")
        .filter((line) => line.trim().length > 0).length;
      counter.textContent = `${count}/6 bullet points`;
      if (count !== 6) {
        counter.style.color = "red";
      } else {
        counter.style.color = "green";
      }
    });
  });
});
