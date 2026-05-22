const fs = require("fs");
const path = require("path");

const root = process.cwd();
const sourceDir = path.join(root, "doc/agent-best-practices");
const outDir = path.join(sourceDir, "_book");
const summaryPath = path.join(sourceDir, "SUMMARY.md");

function read(file) {
  return fs.readFileSync(file, "utf8");
}

function walk(dir, files = []) {
  for (const name of fs.readdirSync(dir)) {
    const full = path.join(dir, name);
    const stat = fs.statSync(full);
    if (stat.isDirectory()) {
      walk(full, files);
    } else if (name.endsWith(".html")) {
      files.push(full);
    }
  }
  return files;
}

function markdownToText(markdown) {
  return markdown
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    .replace(/```[\s\S]*?```/g, " ")
    .replace(/`([^`]+)`/g, "$1")
    .replace(/^[-*]\s+/gm, "")
    .replace(/^#+\s*/gm, "")
    .replace(/\|/g, " ")
    .replace(/\n{2,}/g, "\n")
    .replace(/[ \t]+/g, " ")
    .trim();
}

function mdPathToUrl(mdPath) {
  if (mdPath === "README.md") return "index.html";
  if (mdPath.endsWith("/README.md")) return mdPath.replace(/README\.md$/, "");
  return mdPath.replace(/\.md$/, ".html");
}

function escapeHtmlAttribute(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function cloudflareAnalyticsTag(token) {
  const config = escapeHtmlAttribute(JSON.stringify({ token }));
  return `<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='${config}'></script>`;
}

const navigationStyleTag = `<style id="agent-summary-depth-style">.book-summary ul.summary ul.articles{display:none}.book-summary li.chapter[data-path="07-source-implementation/"]{display:none}</style>`;

const summary = read(summaryPath);
const mdPaths = [];
const seen = new Set();
for (const match of summary.matchAll(/\(([^)]+\.md)\)/g)) {
  const mdPath = match[1];
  if (!seen.has(mdPath)) {
    seen.add(mdPath);
    mdPaths.push(mdPath);
  }
}

const entries = mdPaths
  .map((mdPath) => {
    const full = path.join(sourceDir, mdPath);
    if (!fs.existsSync(full)) return null;
    const markdown = read(full)
      .split("\n")
      .filter((line) => !line.includes("[返回全局摘要]") && !line.includes("[返回本组"))
      .join("\n");
    const titleMatch = markdown.match(/^#\s+(.+)$/m);
    const title = titleMatch ? titleMatch[1].trim() : mdPath;
    const body = markdownToText(markdown)
      .trim();
    return {
      title,
      url: mdPathToUrl(mdPath),
      body,
      haystack: `${title}\n${body}`.toLowerCase(),
    };
  })
  .filter(Boolean);

const clientScript = `(() => {
  const ENTRIES = ${JSON.stringify(entries)};
  const MAX_RESULTS = 20;

  function normalize(value) {
    return String(value || "").toLowerCase().trim();
  }

  function escapeHtml(value) {
    return String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function escapeRegExp(value) {
    return String(value).replace(/[|\\\\{}()[\\]^$+*?.]/g, "\\\\$&");
  }

  function highlightTerms(query) {
    const q = normalize(query);
    if (!q) return [];
    const terms = new Set([q]);
    for (const token of q.split(/[\\s,，.。;；:：/]+/).filter(Boolean)) {
      if (token.length >= 2) terms.add(token);
    }
    return Array.from(terms).sort((a, b) => b.length - a.length);
  }

  function highlightText(text, query) {
    const html = escapeHtml(text);
    const terms = highlightTerms(query).map((term) => escapeRegExp(escapeHtml(term)));
    if (terms.length === 0) return html;
    return html.replace(new RegExp(terms.join("|"), "gi"), "<mark>$&</mark>");
  }

  function scoreEntry(query, entry) {
    const q = normalize(query);
    if (!q) return 0;
    const title = normalize(entry.title);
    const body = normalize(entry.body);
    const haystack = entry.haystack || (title + "\\n" + body);
    let score = 0;

    if (title === q) score += 100;
    if (title.includes(q)) score += 50;
    if (body.includes(q)) score += 20;

    const tokens = q.split(/[\\s,，.。;；:：/]+/).filter(Boolean);
    for (const token of tokens) {
      if (token.length < 2) continue;
      if (title.includes(token)) score += 12;
      if (body.includes(token)) score += 4;
    }

    if (score === 0 && q.length >= 2 && /[^\\x00-\\x7F]/.test(q)) {
      const chars = Array.from(q).filter((c) => !/\\s/.test(c));
      const hits = chars.filter((c) => haystack.includes(c)).length;
      if (hits >= Math.max(2, Math.ceil(chars.length * 0.7))) score += hits;
    }

    return score;
  }

  function excerpt(query, body) {
    const plain = String(body || "").replace(/\\s+/g, " ").trim();
    const q = normalize(query);
    const lower = plain.toLowerCase();
    const index = q ? lower.indexOf(q) : -1;
    const start = index > 60 ? index - 60 : 0;
    const slice = plain.slice(start, start + 220);
    return (start > 0 ? "..." : "") + slice + (start + 220 < plain.length ? "..." : "");
  }

  function basePath() {
    if (window.gitbook && gitbook.state && gitbook.state.basePath) {
      return gitbook.state.basePath;
    }
    return ".";
  }

  function render(query) {
    const input = document.querySelector("#book-search-input input");
    const container = document.querySelector("#book-search-results");
    const list = document.querySelector(".search-results-list");
    const count = document.querySelector(".search-results-count");
    const queryLabel = document.querySelector(".search-query");
    if (!input || !container || !list || !count || !queryLabel) return;

    const q = normalize(query);
    if (!q) {
      document.body.classList.remove("with-search", "search-loading");
      container.classList.remove("open", "no-results");
      list.innerHTML = "";
      return;
    }

    const results = ENTRIES
      .map((entry) => ({ entry, score: scoreEntry(q, entry) }))
      .filter((item) => item.score > 0)
      .sort((a, b) => b.score - a.score || a.entry.title.localeCompare(b.entry.title))
      .slice(0, MAX_RESULTS);

    document.body.classList.add("with-search");
    document.body.classList.remove("search-loading");
    container.classList.add("open");
    container.classList.toggle("no-results", results.length === 0);
    count.textContent = String(results.length);
    queryLabel.textContent = query;
    list.innerHTML = "";

    for (const { entry } of results) {
      const li = document.createElement("li");
      li.className = "search-results-item";

      const h3 = document.createElement("h3");
      const link = document.createElement("a");
      link.href = basePath() + "/" + entry.url;
      link.innerHTML = highlightText(entry.title, q);
      h3.appendChild(link);

      const p = document.createElement("p");
      p.innerHTML = highlightText(excerpt(q, entry.body), q);

      li.appendChild(h3);
      li.appendChild(p);
      list.appendChild(li);
    }
  }

  function bind() {
    const input = document.querySelector("#book-search-input input");
    if (!input || input.dataset.agentSearchBound === "true") return;
    input.dataset.agentSearchBound = "true";
    const scheduleRender = (event) => {
      if (event) event.stopImmediatePropagation();
      const value = input.value;
      render(value);
      setTimeout(() => render(value), 0);
      setTimeout(() => render(value), 80);
      setTimeout(() => render(value), 240);
    };
    input.addEventListener("input", scheduleRender, true);
    input.addEventListener("keyup", scheduleRender, true);
    if (input.value) scheduleRender();
  }

  function installStyles() {
    if (document.getElementById("agent-search-highlight-style")) return;
    const style = document.createElement("style");
    style.id = "agent-search-highlight-style";
    style.textContent = "#book-search-results mark{background:#ffe58a;color:inherit;padding:0 .08em;border-radius:2px;box-shadow:inset 0 -0.2em rgba(255,193,7,.35)}.book-summary ul.summary ul.articles{display:none}.book-summary li.chapter[data-path=\"07-source-implementation/\"]{display:none}";
    document.head.appendChild(style);
  }

  document.addEventListener("DOMContentLoaded", () => {
    installStyles();
    bind();
  });
  setTimeout(() => {
    installStyles();
    bind();
  }, 100);
  setTimeout(() => {
    installStyles();
    bind();
  }, 500);
})();`;

fs.writeFileSync(path.join(outDir, "agent-search.js"), clientScript, "utf8");

const buildId = Date.now();
const cloudflareAnalyticsToken = (process.env.CF_WEB_ANALYTICS_TOKEN || "").trim();
const analyticsTag = cloudflareAnalyticsToken
  ? cloudflareAnalyticsTag(cloudflareAnalyticsToken)
  : "";
let searchInjected = 0;
let analyticsInjected = 0;
const htmlFiles = walk(outDir);

for (const htmlFile of htmlFiles) {
  let html = read(htmlFile);
  const rel = path.relative(path.dirname(htmlFile), outDir).split(path.sep).join("/") || ".";
  const scriptTag = `<script src="${rel}/agent-search.js?v=${buildId}"></script>`;
  let changed = false;

  if (!html.includes("agent-search.js")) {
    html = html.replace("</body>", `    ${scriptTag}\n</body>`);
    changed = true;
    searchInjected += 1;
  }

  if (analyticsTag && !html.includes("static.cloudflareinsights.com/beacon.min.js")) {
    html = html.replace("</body>", `    ${analyticsTag}\n</body>`);
    changed = true;
    analyticsInjected += 1;
  }

  if (!html.includes("agent-summary-depth-style")) {
    html = html.replace("</head>", `    ${navigationStyleTag}\n</head>`);
    changed = true;
  }

  if (changed) {
    fs.writeFileSync(htmlFile, html, "utf8");
  }
}

console.log(`Injected custom search into ${searchInjected}/${htmlFiles.length} HTML pages with ${entries.length} search entries.`);
if (analyticsTag) {
  console.log(`Injected Cloudflare Web Analytics into ${analyticsInjected}/${htmlFiles.length} HTML pages.`);
} else {
  console.log("Skipped Cloudflare Web Analytics injection because CF_WEB_ANALYTICS_TOKEN is not set.");
}
