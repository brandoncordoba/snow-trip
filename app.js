/* Bars: widths come from data-w so the page needs no inline styles.
   Calculator: recomputes the three weeks from the rates on the page. */
(function () {
  document.querySelectorAll(".bar[data-w]").forEach(function (el) {
    el.style.setProperty("--w", el.getAttribute("data-w"));
  });

  var dataEl = document.getElementById("calc-data");
  var form = document.getElementById("calc");
  if (!dataEl || !form) return;
  var data = JSON.parse(dataEl.textContent);
  var WEEKS = ["pre", "x", "f"];
  var $ = function (id) { return document.getElementById(id); };
  var sel = $("c-dest");
  Object.keys(data.dest).forEach(function (k) {
    var o = document.createElement("option");
    o.value = k;
    o.textContent = data.dest[k].name;
    sel.appendChild(o);
  });

  function num(id) {
    var v = parseFloat($(id).value);
    return isFinite(v) && v >= 0 ? v : 0;
  }
  function usd(n) {
    return "$" + Math.round(n).toLocaleString("en-US");
  }
  function loadRates() {
    var d = data.dest[sel.value];
    var gas = Math.round((d.miles * 2) / data.mpg * data.gas);
    WEEKS.forEach(function (w) {
      $("c-fare-" + w).value = d.drive ? 0 : d.w[w][0];
      $("c-lodge-" + w).value = d.w[w][1];
      $("c-car-" + w).value = d.drive ? gas : d.w[w][2];
    });
    $("c-feblabel").textContent = d.feb;
  }
  function render() {
    var d = data.dest[sel.value];
    var people = num("c-people"), nights = num("c-nights"), tax = 1 + num("c-tax") / 100, daily = num("c-daily");
    var carScale = d.drive ? 1 : nights / 5;
    var rows = [
      [d.drive ? "Flights (driving)" : "Flights", function (w) { return num("c-fare-" + w) * people; }],
      ["Lodging", function (w) { return num("c-lodge-" + w) * nights * tax; }],
      [d.drive ? "Gas, round trip" : "Rental car", function (w) { return num("c-car-" + w) * carScale; }],
      ["Food and activities", function () { return daily * (nights + 1); }]
    ];
    var totals = { pre: 0, x: 0, f: 0 }, body = $("c-body");
    body.textContent = "";
    function add(label, vals, total) {
      var tr = document.createElement("tr");
      var th = document.createElement("th");
      th.scope = "row";
      th.textContent = label;
      tr.appendChild(th);
      vals.forEach(function (v) {
        var td = document.createElement("td");
        td.textContent = usd(v);
        if (total) td.className = "tot";
        tr.appendChild(td);
      });
      body.appendChild(tr);
    }
    rows.forEach(function (r) {
      var vals = WEEKS.map(function (w) { var v = r[1](w); totals[w] += v; return v; });
      add(r[0], vals, false);
    });
    add("Total", WEEKS.map(function (w) { return totals[w]; }), true);
  }
  sel.addEventListener("change", function () { loadRates(); render(); });
  form.addEventListener("input", render);
  form.addEventListener("submit", function (e) { e.preventDefault(); });
  loadRates();
  render();
})();
