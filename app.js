/* Bars: widths come from data-w so the page needs no inline styles.
   Calculator: recomputes both weeks from the rates on the page. */
(function () {
  document.querySelectorAll(".bar[data-w]").forEach(function (el) {
    el.style.setProperty("--w", el.getAttribute("data-w"));
  });

  var dataEl = document.getElementById("calc-data");
  var form = document.getElementById("calc");
  if (!dataEl || !form) return;
  var data = JSON.parse(dataEl.textContent);
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
    return (n < 0 ? "-$" : "$") + Math.abs(Math.round(n)).toLocaleString("en-US");
  }
  function loadRates() {
    var d = data.dest[sel.value];
    var gas = Math.round((d.miles * 2) / data.mpg * data.gas);
    $("c-fx").value = d.drive ? 0 : d.fx;
    $("c-ff").value = d.drive ? 0 : d.ff;
    $("c-lx").value = d.lx;
    $("c-lf").value = d.lf;
    $("c-cx").value = d.drive ? gas : d.cx;
    $("c-cf").value = d.drive ? gas : d.cf;
    $("c-feblabel").textContent = d.feb;
  }
  function render() {
    var d = data.dest[sel.value];
    var people = num("c-people"), nights = num("c-nights"), tax = 1 + num("c-tax") / 100, daily = num("c-daily");
    var carScale = d.drive ? 1 : nights / 5;
    var rows = [
      [d.drive ? "Flights (driving)" : "Flights", num("c-fx") * people, num("c-ff") * people],
      ["Lodging", num("c-lx") * nights * tax, num("c-lf") * nights * tax],
      [d.drive ? "Gas, round trip" : "Rental car", num("c-cx") * carScale, num("c-cf") * carScale],
      ["Food and activities", daily * (nights + 1), daily * (nights + 1)]
    ];
    var tx = 0, tf = 0, body = $("c-body");
    body.textContent = "";
    function add(label, a, b, total) {
      var tr = document.createElement("tr");
      var th = document.createElement("th");
      th.scope = "row";
      th.textContent = label;
      tr.appendChild(th);
      [usd(a), usd(b), (a - b >= 0 ? "+" : "") + usd(a - b)].forEach(function (t, i) {
        var td = document.createElement("td");
        td.textContent = t;
        if (total || i === 2) td.className = "tot";
        tr.appendChild(td);
      });
      body.appendChild(tr);
    }
    rows.forEach(function (r) { tx += r[1]; tf += r[2]; add(r[0], r[1], r[2], false); });
    add("Total", tx, tf, true);
  }
  sel.addEventListener("change", function () { loadRates(); render(); });
  form.addEventListener("input", render);
  form.addEventListener("submit", function (e) { e.preventDefault(); });
  loadRates();
  render();
})();
