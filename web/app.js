const DEFAULT_H = Math.PI / 9;
const OMEGA_C = 47 / 125;
const ALPHA = 7.297_352_5693e-3;
const ALPHA_INV = 137.035_999_084;
const MATCH_THRESHOLD = 1e-3;
const REFUSED_NUMERIC_MISMATCH = "refused_numeric_mismatch";
const UNRESOLVED_REVIEW = "unresolved_review";

const hInput = document.querySelector("#h-input");
const resetButton = document.querySelector("#reset-button");
const actualizedValue = document.querySelector("#actualized-value");
const potentialValue = document.querySelector("#potential-value");
const omegaValue = document.querySelector("#omega-value");
const reciprocalValue = document.querySelector("#reciprocal-value");
const fineStructureTable = document.querySelector("#fine-structure-table");
const shellCards = document.querySelector("#shell-cards");
const helixSummary = document.querySelector("#helix-summary");
const helixMeter = document.querySelector("#helix-meter");

function formatNumber(value, digits = 9) {
  return new Intl.NumberFormat("en-US", {
    maximumFractionDigits: digits,
    minimumFractionDigits: Math.min(2, digits),
  }).format(value);
}

function relativeError(value, target) {
  return Math.abs(value - target) / Math.abs(target);
}

function isPrime(number) {
  if (number < 2) return false;
  if (number === 2) return true;
  if (number % 2 === 0) return false;

  const limit = Math.floor(Math.sqrt(number));
  for (let divisor = 3; divisor <= limit; divisor += 2) {
    if (number % divisor === 0) return false;
  }
  return true;
}

function twinPrimePairs(maximum) {
  const pairs = [];
  for (let candidate = 2; candidate <= maximum; candidate += 1) {
    if (isPrime(candidate) && isPrime(candidate + 2)) {
      pairs.push([candidate, candidate + 2]);
    }
  }
  return pairs;
}

function nearestTwinPrimeCenter(atomicNumber) {
  const pairs = twinPrimePairs(atomicNumber + 4);
  return pairs.reduce((nearest, pair) => {
    const center = (pair[0] + pair[1]) / 2;
    const nearestCenter = (nearest[0] + nearest[1]) / 2;
    return Math.abs(atomicNumber - center) < Math.abs(atomicNumber - nearestCenter) ? pair : nearest;
  }, pairs[0]);
}

function fineStructureRows(h) {
  return [
    {
      expression: "4π²H + π",
      value: 4 * Math.PI ** 2 * h + Math.PI,
      target: ALPHA_INV,
    },
    {
      expression: "H / (8π)",
      value: h / (8 * Math.PI),
      target: ALPHA,
    },
    {
      expression: "210H",
      value: 210 * h,
      target: ALPHA_INV,
    },
  ].map((row) => {
    const error = relativeError(row.value, row.target);
    const status = error <= MATCH_THRESHOLD ? UNRESOLVED_REVIEW : REFUSED_NUMERIC_MISMATCH;
    return { ...row, error, status, authority: "none" };
  });
}

function renderFineStructure(h) {
  fineStructureTable.replaceChildren(
    ...fineStructureRows(h).map((row) => {
      const tr = document.createElement("tr");
      const statusClass = row.error <= MATCH_THRESHOLD ? "ok" : "warn";
      tr.innerHTML = `
        <td><code>${row.expression}</code></td>
        <td>${formatNumber(row.value)}</td>
        <td>${formatNumber(row.target)}</td>
        <td>${(row.error * 100).toFixed(3)}%</td>
        <td><span class="status ${statusClass}">${row.status}</span></td>
        <td>${row.authority}</td>
      `;
      return tr;
    }),
  );
}

function renderShellClosures() {
  const closures = [
    ["Magnesium", 12],
    ["Argon", 18],
    ["Zinc", 30],
  ];

  shellCards.replaceChildren(
    ...closures.map(([element, atomicNumber]) => {
      const pair = nearestTwinPrimeCenter(atomicNumber);
      const center = (pair[0] + pair[1]) / 2;
      const offset = atomicNumber - center;
      const article = document.createElement("article");
      article.className = "shell-card";
      article.innerHTML = `
        <span>${element}</span>
        <strong>${atomicNumber}</strong>
        <p>Twin prime (${pair[0]}, ${pair[1]}) centers at ${center}; offset ${offset}. Status ${UNRESOLVED_REVIEW}; authority none.</p>
      `;
      return article;
    }),
  );
}

function renderHelix(h) {
  const reciprocal = 1 / h;
  const target = 3.6;
  const error = relativeError(reciprocal, target);
  const status = error <= MATCH_THRESHOLD ? UNRESOLVED_REVIEW : REFUSED_NUMERIC_MISMATCH;
  helixSummary.textContent = `1/H = ${formatNumber(reciprocal)} compared with ${target} residues per turn; relative error ${(error * 100).toFixed(3)}%; status ${status}; authority none.`;
  helixMeter.style.width = `${Math.min(error * 100, 100)}%`;
}

function render() {
  const h = Number.parseFloat(hInput.value);
  if (!Number.isFinite(h) || h <= 0) return;

  actualizedValue.textContent = `${formatNumber(h * 100, 4)}%`;
  potentialValue.textContent = `${formatNumber((1 - h) * 100, 4)}%`;
  omegaValue.textContent = formatNumber(OMEGA_C, 3);
  reciprocalValue.textContent = formatNumber(1 / h);

  renderFineStructure(h);
  renderShellClosures();
  renderHelix(h);
}

hInput.value = DEFAULT_H.toFixed(10);
hInput.addEventListener("input", render);
resetButton.addEventListener("click", () => {
  hInput.value = DEFAULT_H.toFixed(10);
  render();
});

render();
