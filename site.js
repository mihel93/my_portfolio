// Shared script for every page: chart tooltips and the skills star schema.

/* ---------- Tooltips ----------
   Any element with a data-tip attribute shows a tooltip on hover or keyboard focus.
   On touch screens, tapping it shows the tooltip. */
(function () {
  var tip = document.createElement('div');
  tip.className = 'tooltip';
  tip.setAttribute('role', 'tooltip');
  document.body.appendChild(tip);
  var current = null;

  function place(x, y) {
    var w = tip.offsetWidth, h = tip.offsetHeight;
    var left = Math.min(Math.max(8, x - w / 2), window.innerWidth - w - 8);
    var top = y - h - 14;
    if (top < 8) top = y + 20;          // flip below if there is no room above
    tip.style.left = left + 'px';
    tip.style.top = top + 'px';
  }
  function show(el, x, y) {
    current = el;
    tip.textContent = el.getAttribute('data-tip');
    tip.classList.add('is-visible');
    if (x === undefined) {
      var r = el.getBoundingClientRect();
      x = r.left + r.width / 2;
      y = r.top;
    }
    place(x, y);
  }
  function hide() {
    current = null;
    tip.classList.remove('is-visible');
  }

  document.addEventListener('mouseover', function (e) {
    var el = e.target.closest('[data-tip]');
    if (el && el !== current) show(el, e.clientX, e.clientY);
    if (!el && current) hide();
  });
  document.addEventListener('mousemove', function (e) {
    if (current) place(e.clientX, e.clientY);
  });
  document.addEventListener('focusin', function (e) {
    var el = e.target.closest('[data-tip]');
    if (el) show(el); else hide();
  });
  document.addEventListener('focusout', hide);
  document.addEventListener('touchstart', function (e) {
    var el = e.target.closest('[data-tip]');
    if (el) {
      var t = e.touches[0];
      show(el, t.clientX, t.clientY);
    } else {
      hide();
    }
  }, { passive: true });
  window.addEventListener('scroll', function () {
    if (current && document.activeElement !== current) hide();
  }, { passive: true });

  // A project thumbnail sits above the row's link, so a click on it opens the write-up
  document.querySelectorAll('.project .thumb').forEach(function (thumb) {
    var link = thumb.closest('.project').querySelector('h3 a');
    if (!link) return;
    thumb.addEventListener('click', function () { window.location.href = link.href; });
  });
})();

/* ---------- Skills star schema ----------
   Draws relationship lines from the fact table to each dimension
   ("*" on the fact side, "1" on the dimension side) and highlights a
   table's relationship on hover. */
(function () {
  var star = document.querySelector('.star');
  if (!star) return;
  var svg = star.querySelector('.st-lines');
  var fact = star.querySelector('.st-fact');
  var dims = star.querySelectorAll('.st-table:not(.st-fact)');
  var NS = 'http://www.w3.org/2000/svg';

  function edge(r, toward) {
    var cx = r.left + r.width / 2, cy = r.top + r.height / 2;
    var dx = toward.x - cx, dy = toward.y - cy;
    var k = 1 / Math.max(Math.abs(dx) / (r.width / 2), Math.abs(dy) / (r.height / 2));
    return { x: cx + dx * k, y: cy + dy * k };
  }
  function add(parent, name, attrs, text) {
    var n = document.createElementNS(NS, name);
    for (var a in attrs) n.setAttribute(a, attrs[a]);
    if (text) n.textContent = text;
    parent.appendChild(n);
    return n;
  }
  function along(p, q, d) {
    var L = Math.hypot(q.x - p.x, q.y - p.y);
    return { x: p.x + (q.x - p.x) * d / L, y: p.y + (q.y - p.y) * d / L };
  }

  function draw() {
    svg.innerHTML = '';
    if (getComputedStyle(svg).display === 'none') return;
    var box = star.getBoundingClientRect();
    function rel(el) {
      var r = el.getBoundingClientRect();
      return { left: r.left - box.left, top: r.top - box.top, width: r.width, height: r.height };
    }
    var f = rel(fact);
    var fc = { x: f.left + f.width / 2, y: f.top + f.height / 2 };
    dims.forEach(function (d) {
      var r = rel(d);
      var dc = { x: r.left + r.width / 2, y: r.top + r.height / 2 };
      var a = edge(f, dc), b = edge(r, fc);
      var g = add(svg, 'g', { 'class': 'st-edge', 'data-key': d.getAttribute('data-key') });
      add(g, 'line', { x1: a.x, y1: a.y, x2: b.x, y2: b.y, 'class': 'st-rel' });
      var L = Math.hypot(b.x - a.x, b.y - a.y);
      var nx = -(b.y - a.y) / L * 9, ny = (b.x - a.x) / L * 9;   // nudge labels beside the line
      var m1 = along(a, b, 14), m2 = along(b, a, 14);
      add(g, 'text', { x: m1.x + nx, y: m1.y + ny + 4, 'class': 'st-card' }, '*');
      add(g, 'text', { x: m2.x + nx, y: m2.y + ny + 4, 'class': 'st-card' }, '1');
    });
    svg.setAttribute('viewBox', '0 0 ' + box.width + ' ' + box.height);
    if (activeKey) highlight(activeKey);   // keep the highlight after a redraw
  }

  var activeKey = null;
  function highlight(key) {
    activeKey = key;
    svg.querySelectorAll('.st-edge').forEach(function (g) {
      g.classList.toggle('is-active', key === 'all' || g.getAttribute('data-key') === key);
    });
    star.classList.toggle('has-focus', !!key);
    dims.forEach(function (d) {
      d.classList.toggle('is-linked', key === 'all' || d.getAttribute('data-key') === key);
    });
    fact.classList.toggle('is-linked', !!key);
  }
  // Hovering a single skill highlights its table's relationship.
  // In the fact table, a key highlights the dimension it points to.
  star.querySelectorAll('.st-table li').forEach(function (li) {
    var table = li.closest('.st-table');
    var key = li.getAttribute('data-ref') ||
              (table === fact ? null : table.getAttribute('data-key'));
    function on() { if (key) highlight(key); }
    function off() { highlight(null); }
    li.addEventListener('mouseenter', on);
    li.addEventListener('mouseleave', off);
    li.addEventListener('focus', on);
    li.addEventListener('blur', off);
  });

  window.addEventListener('resize', draw);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(draw);
  draw();
})();
