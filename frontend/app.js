const form = document.querySelector("#prediction-form");
const descriptionInput = document.querySelector("#description");
const apiUrlInput = document.querySelector("#api-url");
const submitButton = document.querySelector("#submit-button");
const statusMessage = document.querySelector("#status-message");
const resultCard = document.querySelector("#result-card");
const predictedPrice = document.querySelector("#predicted-price");
const resultSummary = document.querySelector("#result-summary");
const featureList = document.querySelector("#feature-list");
const featureCount = document.querySelector("#feature-count");
const exampleChips = document.querySelectorAll(".example-chip");

function setStatus(message, state = "default") {
  statusMessage.textContent = message;
  statusMessage.classList.remove("status-error", "status-success");

  if (state === "error") {
    statusMessage.classList.add("status-error");
  }

  if (state === "success") {
    statusMessage.classList.add("status-success");
  }
}

function formatFeatureLabel(key, value) {
  return `${key}: ${value}`;
}

function formatCurrency(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(value);
}

function renderExtractedFeatures(features) {
  featureList.innerHTML = "";

  const entries = Object.entries(features);
  featureCount.textContent = `${entries.length} item${entries.length === 1 ? "" : "s"}`;

  for (const [key, value] of entries) {
    const item = document.createElement("li");
    item.textContent = formatFeatureLabel(key, value);
    featureList.appendChild(item);
  }
}

async function handlePrediction(event) {
  event.preventDefault();

  const description = descriptionInput.value.trim();
  const apiBaseUrl = apiUrlInput.value.trim().replace(/\/$/, "");

  if (!description) {
    setStatus("Please write a house description before requesting a prediction.", "error");
    return;
  }

  submitButton.disabled = true;
  setStatus("Generating prediction from your description...");

  try {
    const response = await fetch(`${apiBaseUrl}/predict-from-text`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ description }),
    });

    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.detail || "The prediction request failed.");
    }

    predictedPrice.textContent = formatCurrency(payload.predicted_price);
    resultSummary.textContent =
      "The estimate is based on the structured features extracted from the text description.";
    renderExtractedFeatures(payload.extracted_features);
    resultCard.classList.remove("hidden");
    setStatus("Prediction generated successfully.", "success");
  } catch (error) {
    resultCard.classList.add("hidden");
    featureList.innerHTML = "";
    featureCount.textContent = "0 items";
    setStatus(error.message, "error");
  } finally {
    submitButton.disabled = false;
  }
}

for (const chip of exampleChips) {
  chip.addEventListener("click", () => {
    descriptionInput.value = chip.textContent.trim();
    descriptionInput.focus();
  });
}

form.addEventListener("submit", handlePrediction);
