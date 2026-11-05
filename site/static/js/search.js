// Archive search, built on the Pagefind library.
//
// Results update as you type; pressing Enter also brings them into view.
// Category and year filters show how many results each value has for the
// search words alone, so the counts do not change as filters are picked.
// Values with no results are hidden. Within a group, picking several values
// shows results matching any of them; across groups, results must match both.
(function () {
  var PAGE_SIZE = 10;
  var SUB_RESULTS = 3;
  var script = document.currentScript;
  var $ = function (id) { return document.getElementById(id); };

  if (location.protocol === "file:") {
    $("search-offline").hidden = false;
    return;
  }
  // The index is stored relative to the site root; work out where that root
  // is so the archive can live at any address or subpath.
  var root = new URL("../", script.src);

  var form = $("search-form"), input = $("search-input"), clear = $("search-clear");
  var filterBox = $("search-filters"), message = $("search-message");
  var list = $("search-results"), more = $("search-more");
  var selected = { category: new Set(), year: new Set() };
  var pagefind, current = null, shown = 0, seq = 0, reveal = false;

  var norm = function (s) { return s.replace(/\s+/g, " ").trim(); };
  var el = function (tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  };
  var plural = function (n) { return n.toLocaleString("en") + (n === 1 ? " result" : " results"); };

  // Pagefind reports filter counts only when a filter is applied, so a group
  // with nothing picked gets a filter that excludes nothing.
  var MATCH_ALL = { category: { not: "-" }, year: { not: "-" } };

  function filterQuery() {
    var f = {};
    Object.keys(selected).forEach(function (k) {
      f[k] = selected[k].size ? { any: Array.from(selected[k]) } : MATCH_ALL[k];
    });
    return f;
  }
  var anySelected = function () { return selected.category.size + selected.year.size > 0; };

  function renderFilters(counts) {
    filterBox.querySelectorAll("details").forEach(function (box) {
      var key = box.dataset.filter, values = counts[key] || {}, opts = box.querySelector(".search-options");
      var names = Object.keys(values).filter(function (v) { return values[v] > 0 || selected[key].has(v); });
      names.sort(function (a, b) { return a.localeCompare(b, "en", { numeric: true }); });
      opts.textContent = "";
      names.forEach(function (v) {
        var label = el("label", "search-option"), check = el("input");
        check.type = "checkbox";
        check.checked = selected[key].has(v);
        check.addEventListener("change", function () {
          selected[key][check.checked ? "add" : "delete"](v);
          run(input.value, false);
        });
        label.append(check, el("span", null, v), el("span", "search-count", (values[v] || 0).toLocaleString("en")));
        opts.append(label);
      });
      var n = selected[key].size, summary = box.querySelector("summary");
      summary.dataset.label = summary.dataset.label || summary.textContent;
      summary.textContent = summary.dataset.label + (n ? " (" + n + " selected)" : "");
      box.hidden = !names.length;
    });
  }

  function renderResult(data) {
    var li = el("li", "search-result"), h = el("h2");
    var a = el("a", null, data.meta.title || data.url);
    a.href = data.url;
    h.append(a);
    li.append(h);
    var p = el("p", "search-excerpt");
    p.innerHTML = data.excerpt; // Pagefind escapes the text and adds <mark>
    li.append(p);
    var subs = (data.sub_results || []).filter(function (s) { return s.url !== data.url && s.url.indexOf("#") !== -1; });
    if (subs.length) {
      var ul = el("ul", "search-subs");
      subs.slice(0, SUB_RESULTS).forEach(function (s) {
        var si = el("li"), sa = el("a", null, s.title);
        sa.href = s.url;
        var sp = el("p", "search-excerpt");
        sp.innerHTML = s.excerpt;
        si.append(sa, sp);
        ul.append(si);
      });
      li.append(ul);
    }
    if (data.meta.date) li.append(el("p", "search-date", data.meta.date));
    return li;
  }

  async function showMore() {
    var mine = seq, batch = current.results.slice(shown, shown + PAGE_SIZE);
    var data = await Promise.all(batch.map(function (r) { return r.data(); }));
    if (mine !== seq) return;
    data.forEach(function (d) { list.append(renderResult(d)); });
    shown += batch.length;
    more.hidden = shown >= current.results.length;
  }

  async function run(raw, debounce) {
    var term = norm(raw), mine = ++seq;
    clear.hidden = !raw;
    var url = new URL(location.href);
    if (term) url.searchParams.set("q", term); else url.searchParams.delete("q");
    history.replaceState(null, "", url);
    if (!term) {
      current = null;
      list.textContent = message.textContent = "";
      filterBox.hidden = more.hidden = true;
      return;
    }
    var search = debounce
      ? await pagefind.debouncedSearch(term, { filters: filterQuery() }, 300)
      : await pagefind.search(term, { filters: filterQuery() });
    if (search === null || mine !== seq) return;
    current = search;
    current.term = term;
    renderFilters(search.totalFilters || {});
    filterBox.hidden = false;
    var n = search.results.length, filtered = anySelected();
    message.textContent = (n ? plural(n) : "No results") + " for " + term + (filtered ? ", filtered" : "");
    list.textContent = "";
    shown = 0;
    await showMore();
    if (reveal && mine === seq) {
      reveal = false;
      input.blur();
      message.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }

  input.addEventListener("input", function () { run(input.value, true); });
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    reveal = true;
    run(input.value, false);
  });
  input.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { input.value = ""; run("", false); }
  });
  clear.addEventListener("click", function () { input.value = ""; run("", false); input.focus(); });
  more.addEventListener("click", showMore);

  import(new URL("pagefind/pagefind.js", root).href).then(async function (mod) {
    pagefind = mod;
    await pagefind.options({ baseUrl: root.pathname, excerptLength: 30 });
    pagefind.init();
    form.hidden = false;
    var q = new URLSearchParams(location.search).get("q");
    if (q) { input.value = q; run(q, false); }
  }, function () {
    $("search-offline").hidden = false;
  });
})();
