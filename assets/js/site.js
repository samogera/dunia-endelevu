/* Dunia Endelevu · site behaviour (no dependencies) */
(function () {
  'use strict';

  /* ------------------------------------------------------------------
     Where form submissions go. FormSubmit (formsubmit.co) forwards each
     submission to this inbox. The first submission sends an activation
     email to this address: open it and click "Activate Form" once.
     ------------------------------------------------------------------ */
  var FORM_INBOX = 'hello@duniaendelevu.org';
  var FORM_ENDPOINT = 'https://formsubmit.co/ajax/' + FORM_INBOX;

  var doc = document.documentElement;
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Header: height, shadow on scroll ---------- */
  var header = document.querySelector('.site-header');
  function setHeaderHeight() {
    if (header) doc.style.setProperty('--header-h', header.getBoundingClientRect().height + 'px');
  }
  setHeaderHeight();
  window.addEventListener('resize', setHeaderHeight);
  function onScroll() {
    if (header) header.classList.toggle('is-scrolled', window.scrollY > 24);
  }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ---------- Mobile menu ---------- */
  var toggle = document.querySelector('.menu-toggle');
  var menu = document.getElementById('mobile-menu');
  function setMenu(open) {
    if (!toggle || !menu) return;
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    toggle.querySelector('.menu-toggle__label').textContent = open ? 'Close' : 'Menu';
    menu.hidden = !open;
    doc.classList.toggle('menu-open', open);
    if (open) {
      setHeaderHeight();
      var first = menu.querySelector('a');
      if (first) first.focus({ preventScroll: true });
    }
  }
  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      setMenu(toggle.getAttribute('aria-expanded') !== 'true');
    });
    menu.addEventListener('click', function (e) {
      if (e.target.closest('a')) setMenu(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        setMenu(false);
        toggle.focus();
      }
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 1080 && toggle.getAttribute('aria-expanded') === 'true') setMenu(false);
    });
  }

  /* ---------- Headlines: words rise in one by one ---------- */
  document.querySelectorAll('.split').forEach(function (el) {
    if (!reduceMotion) {
      var i = 0;
      (function walk(node) {
        Array.prototype.slice.call(node.childNodes).forEach(function (child) {
          if (child.nodeType === 3) {
            var frag = document.createDocumentFragment();
            child.textContent.split(/(\s+)/).forEach(function (part) {
              if (!part) return;
              if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
              var w = document.createElement('span');
              var inner = document.createElement('span');
              w.className = 'w';
              inner.style.setProperty('--i', i++);
              inner.textContent = part;
              w.appendChild(inner);
              frag.appendChild(w);
            });
            child.parentNode.replaceChild(frag, child);
          } else if (child.nodeType === 1) {
            walk(child);
          }
        });
      })(el);
    }
    el.classList.add('is-split');
  });

  /* ---------- Numbers count up when they come into view ---------- */
  if (!reduceMotion && 'IntersectionObserver' in window) {
    document.querySelectorAll('[data-count]').forEach(function (el) {
      var end = parseFloat(el.getAttribute('data-count'));
      if (!end) return;
      el.textContent = '0';
      var obs = new IntersectionObserver(function (entries) {
        if (!entries[0].isIntersecting) return;
        obs.disconnect();
        var start = performance.now();
        (function tick(now) {
          var p = Math.min(1, (now - start) / 1400);
          el.textContent = String(Math.round(end * (1 - Math.pow(1 - p, 3))));
          if (p < 1) requestAnimationFrame(tick);
        })(start);
      }, { threshold: 0.4 });
      obs.observe(el);
    });
  }

  /* ---------- Gentle parallax on large screens ---------- */
  var drifting = document.querySelectorAll('[data-speed]');
  if (!reduceMotion && drifting.length && window.matchMedia('(min-width: 961px)').matches) {
    var queued = false;
    var drift = function () {
      var y = window.scrollY;
      drifting.forEach(function (el) { el.style.translate = '0 ' + (y * parseFloat(el.getAttribute('data-speed'))).toFixed(1) + 'px'; });
      queued = false;
    };
    window.addEventListener('scroll', function () {
      if (!queued) { queued = true; requestAnimationFrame(drift); }
    }, { passive: true });
  }

  /* ---------- Gentle reveal on scroll ---------- */
  var reveals = document.querySelectorAll('.reveal');
  if (reduceMotion || !('IntersectionObserver' in window)) {
    reveals.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  }

  /* ---------- Carousel: one card in the centre, its neighbours peeking ---------- */
  document.querySelectorAll('[data-carousel]').forEach(function (root) {
    var track = root.querySelector('.carousel__track');
    var slides = Array.prototype.slice.call(track.children);
    var section = root.closest('section') || root.parentNode;
    var prev = section.querySelector('[data-prev]');
    var next = section.querySelector('[data-next]');
    var index = Math.min(1, slides.length - 1);
    var go = function (i) {
      index = (i + slides.length) % slides.length;
      slides.forEach(function (s, n) {
        s.classList.toggle('is-active', n === index);
        s.setAttribute('aria-label', (n + 1) + ' of ' + slides.length);
      });
      var s = slides[index];
      var x = root.clientWidth / 2 - (s.offsetLeft + s.offsetWidth / 2);
      track.style.transform = 'translateX(' + x.toFixed(1) + 'px)';
    };
    slides.forEach(function (s, n) {
      s.setAttribute('aria-roledescription', 'slide');
      s.addEventListener('click', function (e) {
        if (n === index) return;
        e.preventDefault();
        go(n);
      });
      s.addEventListener('focusin', function () { if (n !== index) go(n); });
    });
    if (prev) prev.addEventListener('click', function () { go(index - 1); });
    if (next) next.addEventListener('click', function () { go(index + 1); });
    root.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') { e.preventDefault(); go(index - 1); }
      if (e.key === 'ArrowRight') { e.preventDefault(); go(index + 1); }
    });
    var startX = null;
    root.addEventListener('pointerdown', function (e) { startX = e.clientX; });
    root.addEventListener('pointerup', function (e) {
      if (startX === null) return;
      var dx = e.clientX - startX;
      startX = null;
      if (Math.abs(dx) > 40) go(index + (dx < 0 ? 1 : -1));
    });
    var resizeTimer;
    window.addEventListener('resize', function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function () { go(index); }, 120);
    });
    track.style.transition = 'none';
    go(index);
    track.offsetWidth;
    track.style.transition = '';
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { go(index); });
  });

  /* ---------- Legal pages: highlight the current section ---------- */
  var tocLinks = document.querySelectorAll('.toc a[href^="#"]');
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var tocIo = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting && map[entry.target.id]) {
          tocLinks.forEach(function (a) { a.classList.remove('is-active'); });
          map[entry.target.id].classList.add('is-active');
        }
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    Object.keys(map).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) tocIo.observe(el);
    });
  }

  /* ---------- Contact page: form tabs ---------- */
  var tablist = document.querySelector('[role="tablist"]');
  if (tablist) {
    var tabs = Array.prototype.slice.call(tablist.querySelectorAll('[role="tab"]'));
    var selectTab = function (tab, focus) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
      });
      if (focus) tab.focus();
    };
    tabs.forEach(function (tab, i) {
      tab.addEventListener('click', function () {
        selectTab(tab, false);
        if (history.replaceState) history.replaceState(null, '', '#' + tab.dataset.hash);
      });
      tab.addEventListener('keydown', function (e) {
        var next = null;
        if (e.key === 'ArrowRight') next = tabs[(i + 1) % tabs.length];
        if (e.key === 'ArrowLeft') next = tabs[(i - 1 + tabs.length) % tabs.length];
        if (next) { e.preventDefault(); selectTab(next, true); }
      });
    });
    var params = new URLSearchParams(window.location.search);
    var topic = params.get('topic');
    var wanted = window.location.hash.replace('#', '') || (topic ? 'enquiry' : '');
    var match = tabs.filter(function (t) { return t.dataset.hash === wanted; })[0];
    selectTab(match || tabs[0], false);
    if (topic) {
      var select = document.querySelector('#enquiry select[name="interest"]');
      if (select) {
        Array.prototype.forEach.call(select.options, function (o) {
          if (o.dataset.topic === topic) select.value = o.value;
        });
      }
    }
  }

  /* ---------- Buttons that preselect an enquiry topic ---------- */
  document.querySelectorAll('[data-set-interest]').forEach(function (link) {
    link.addEventListener('click', function () {
      var target = document.querySelector(link.getAttribute('href'));
      var select = target && target.querySelector('select[name="interest"]');
      if (select) select.value = link.getAttribute('data-set-interest');
    });
  });

  /* ---------- Podcast: load the Spotify player only when asked ---------- */
  document.querySelectorAll('[data-load-player]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var box = btn.closest('.player');
      var iframe = document.createElement('iframe');
      iframe.src = btn.getAttribute('data-load-player');
      iframe.title = 'Climate Gumzo on Spotify';
      iframe.loading = 'lazy';
      iframe.allow = 'autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture';
      box.innerHTML = '';
      box.appendChild(iframe);
    });
  });

  /* ---------- Forms ---------- */
  function fieldWrap(el) {
    return el.closest('.field') || el.closest('.check');
  }
  function clearError(el) {
    var wrap = fieldWrap(el);
    if (!wrap) return;
    wrap.classList.remove('is-invalid');
    el.removeAttribute('aria-invalid');
    var msg = wrap.querySelector('.field__error');
    if (msg) msg.remove();
  }
  function messageFor(el) {
    if (el.validity.valueMissing && el.getAttribute('data-msg-missing')) return el.getAttribute('data-msg-missing');
    if (el.validity.rangeUnderflow && el.getAttribute('data-msg-min')) return el.getAttribute('data-msg-min');
    if (el.validity.patternMismatch && el.getAttribute('data-msg-pattern')) return el.getAttribute('data-msg-pattern');
    if (el.validity.valueMissing) {
      if (el.type === 'checkbox') return 'Please tick this box to continue.';
      if (el.type === 'radio') return 'Please choose one.';
      if (el.tagName === 'SELECT') return 'Please choose an option.';
      return 'Please fill in this field.';
    }
    if (el.validity.typeMismatch && el.type === 'email') return 'Please enter a valid email address, like name@example.com.';
    if (el.validity.patternMismatch && el.type === 'tel') return 'Please enter a phone number, like +254 7XX XXX XXX.';
    return el.validationMessage;
  }
  function showError(el) {
    var wrap = fieldWrap(el);
    if (!wrap) return;
    clearError(el);
    wrap.classList.add('is-invalid');
    el.setAttribute('aria-invalid', 'true');
    var grouped = el.type === 'radio' || (el.type === 'checkbox' && el.closest('.choices'));
    if (el.type === 'checkbox' && !grouped) return;
    if (grouped && wrap.querySelector('.field__error')) return;
    var msg = document.createElement('span');
    msg.className = 'field__error';
    msg.id = (el.id || el.name) + '-error';
    msg.textContent = messageFor(el);
    wrap.appendChild(msg);
    el.setAttribute('aria-describedby', msg.id);
  }
  function statusBox(form) {
    var box = form.querySelector('.form-status');
    if (!box) {
      box = document.createElement('div');
      box.className = 'form-status';
      box.setAttribute('role', 'status');
      box.setAttribute('aria-live', 'polite');
      form.appendChild(box);
    }
    return box;
  }
  function mailtoLink(subject, data) {
    var lines = [];
    Object.keys(data).forEach(function (k) {
      if (k.charAt(0) !== '_') lines.push(k.replace(/_/g, ' ') + ': ' + data[k]);
    });
    return 'mailto:' + FORM_INBOX + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(lines.join('\n'));
  }

  document.querySelectorAll('form[data-form]').forEach(function (form) {
    form.setAttribute('novalidate', '');
    form.querySelectorAll('input, select, textarea').forEach(function (el) {
      var evt = (el.type === 'checkbox' || el.type === 'radio' || el.tagName === 'SELECT') ? 'change' : 'input';
      el.addEventListener(evt, function () { if (el.checkValidity()) clearError(el); });
      el.addEventListener('blur', function () {
        if (el.value && !el.checkValidity()) showError(el);
      });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var invalid = Array.prototype.filter.call(form.elements, function (el) {
        return el.willValidate && !el.checkValidity();
      });
      form.querySelectorAll('[aria-invalid]').forEach(clearError);
      form.querySelectorAll('.field__error').forEach(function (m) { m.remove(); });
      if (invalid.length) {
        invalid.forEach(showError);
        invalid[0].focus();
        return;
      }
      var honey = form.querySelector('input[name="_honey"]');
      if (honey && honey.value) return; // a bot filled the hidden field

      var data = {};
      new FormData(form).forEach(function (value, key) {
        if (key === '_honey') return;
        data[key] = data[key] ? data[key] + ', ' + value : String(value).trim();
      });
      var subject = form.getAttribute('data-subject') || 'Website message';
      data._subject = subject + ' · Dunia Endelevu website';
      data._template = 'table';
      data._captcha = 'false';
      var reply = form.getAttribute('data-autoresponse');
      if (reply && data.email) data._autoresponse = reply;
      data.page = window.location.pathname.split('/').pop() || 'index.html';

      var button = form.querySelector('[type="submit"]');
      var label = button ? button.innerHTML : '';
      if (button) { button.disabled = true; button.textContent = 'Sending…'; }
      var box = statusBox(form);
      box.hidden = true;

      fetch(FORM_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(data)
      }).then(function (res) {
        return res.json().catch(function () { return {}; }).then(function (json) {
          if (!res.ok || String(json.success) === 'false') throw new Error(json.message || 'Not sent');
        });
      }).then(function () {
        box.className = 'form-status form-status--ok';
        box.innerHTML = '<strong>' + (form.getAttribute('data-ok-title') || 'Thank you, it’s on its way.') + '</strong>' +
          (form.getAttribute('data-ok') || 'We reply within three working days.');
        box.hidden = false;
        form.reset();
        if (button) { button.disabled = false; button.innerHTML = label; }
        box.setAttribute('tabindex', '-1');
        box.focus();
      }).catch(function () {
        box.className = 'form-status form-status--error';
        box.innerHTML = '<strong>We couldn’t send that just now.</strong>Please try again, or <a href="' +
          mailtoLink(subject, data) + '">send it by email instead</a>. Nothing you typed has been lost.';
        box.hidden = false;
        if (button) { button.disabled = false; button.innerHTML = label; }
      });
    });
  });

  /* ---------- Donate: several gifts, quick amounts, live summary and progress ---------- */
  var donate = document.querySelector('form[data-donate]');
  if (donate) {
    var funds = Array.prototype.slice.call(donate.querySelectorAll('input[name="fund"]'));
    var amountInput = donate.querySelector('#d-amount');
    var chips = Array.prototype.slice.call(donate.querySelectorAll('[data-amount-chip]'));
    var nameInput = donate.querySelector('#d-name');
    var emailInput = donate.querySelector('#d-email');
    var giveSteps = Array.prototype.slice.call(donate.querySelectorAll('[data-give-step]'));
    var sumItems = document.querySelector('[data-sum-items]');
    var sumCount = document.querySelector('[data-sum-count]');
    var sumPay = document.querySelector('[data-sum-pay]');
    var sumTotals = Array.prototype.slice.call(document.querySelectorAll('[data-sum-total]'));
    var sumCredit = document.querySelector('[data-sum-credit]');
    var ksh = function (n) { return 'KSh ' + Math.round(n).toLocaleString('en'); };
    var amount = function () { var n = parseInt(amountInput.value.replace(/[^0-9]/g, ''), 10); return isNaN(n) ? 0 : n; };
    var setAmount = function (n) { amountInput.value = n ? Number(n).toLocaleString('en') : ''; };
    // show thousands separators while typing: 50000 becomes 50,000
    amountInput.addEventListener('input', function () {
      var digits = amountInput.value.replace(/[^0-9]/g, '').replace(/^0+/, '');
      setAmount(digits ? parseInt(digits, 10) : 0);
    });

    var update = function () {
      var chosen = funds.filter(function (f) { return f.checked; });
      // at least one gift is needed: every box is required until one is ticked
      funds.forEach(function (f) { f.required = chosen.length === 0; });
      var n = amount();
      chips.forEach(function (c) { c.classList.toggle('is-on', parseFloat(c.getAttribute('data-amount-chip')) === n); });
      var payLabel = donate.querySelector('[data-pay-label]');
      if (payLabel) payLabel.textContent = n > 0 ? 'Donate ' + ksh(n) : 'Donate';
      if (sumItems) {
        sumItems.innerHTML = '';
        if (!chosen.length) {
          sumItems.innerHTML = '<li class="summary__empty">Choose what to fund.</li>';
        }
        chosen.forEach(function (f) {
          var li = document.createElement('li');
          var iconEl = f.parentNode.querySelector('.choice__icon');
          li.innerHTML = iconEl ? iconEl.outerHTML : '';
          li.appendChild(document.createTextNode(f.value));
          sumItems.appendChild(li);
        });
      }
      if (sumCount) sumCount.textContent = String(chosen.length);
      var pay = donate.querySelector('input[name="pay_by"]:checked');
      if (sumPay) sumPay.textContent = pay ? pay.value : 'Not chosen';
      sumTotals.forEach(function (el) { el.textContent = ksh(n); });
      var credit = donate.querySelector('input[name="credit"]:checked');
      if (sumCredit) sumCredit.textContent = credit && credit.value === 'Show my name' ? (nameInput.value.trim() || 'Your name') : 'Anonymous';
      // tick off each numbered step once it is filled in
      var done = [chosen.length > 0, n > 0, !!pay, !!(emailInput.value && emailInput.checkValidity())];
      giveSteps.forEach(function (fs, i) { fs.classList.toggle('is-done', !!done[i]); });
    };

    chips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        var v = chip.getAttribute('data-amount-chip');
        if (v === 'custom') {
          amountInput.value = '';
          amountInput.focus();
        } else {
          setAmount(parseInt(v, 10));
          clearError(amountInput);
        }
        update();
      });
    });
    donate.addEventListener('change', function (e) {
      var t = e.target;
      // suggest the full cost of a book the first time it is ticked
      if (t.name === 'fund' && t.checked && t.getAttribute('data-amount') && !amountInput.value) {
        setAmount(parseInt(t.getAttribute('data-amount'), 10));
        clearError(amountInput);
      }
      update();
    });
    donate.addEventListener('input', update);
    donate.addEventListener('reset', function () { setTimeout(update, 0); });
    var wanted = (window.location.search.match(/[?&]for=([a-z]+)/) || [])[1];
    var pick = wanted ? donate.querySelector('input[name="fund"][data-key="' + wanted + '"]') : null;
    if (pick) {
      pick.checked = true;
      pick.dispatchEvent(new Event('change', { bubbles: true }));
    }
    update();

    // phones: show the total and a Donate button while the form is on screen but its own button is not
    var giveBar = document.querySelector('[data-give-bar]');
    var mainBtn = donate.querySelector('[type="submit"]');
    if (giveBar && mainBtn && 'IntersectionObserver' in window) {
      var formOn = false, btnOn = false;
      var syncBar = function () {
        var on = formOn && !btnOn;
        giveBar.classList.toggle('is-on', on);
        giveBar.setAttribute('aria-hidden', on ? 'false' : 'true');
        var b = giveBar.querySelector('button'); if (b) b.tabIndex = on ? 0 : -1;
      };
      new IntersectionObserver(function (en) { formOn = en[0].isIntersecting; syncBar(); }).observe(donate);
      new IntersectionObserver(function (en) { btnOn = en[0].isIntersecting; syncBar(); }).observe(mainBtn);
    }
  }

  /* ---------- Storybook: a book that opens and turns its pages, with read-aloud ---------- */
  document.querySelectorAll('[data-book]').forEach(function (root) {
    var srcs = Array.prototype.slice.call(root.querySelectorAll('.flip__src'));
    var stage = root.querySelector('.flip__stage');
    var book = root.querySelector('.flip__book');
    if (!srcs.length || !stage || !book) return;
    var sideL = book.querySelector('.flip__side--l');
    var sideR = book.querySelector('.flip__side--r');
    var prev = root.querySelector('[data-prev]');
    var next = root.querySelector('[data-next]');
    var count = root.querySelector('[data-count]');
    var bar = root.querySelector('.flip__progress span');
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
    var ext = (function () {
      try { return document.createElement('canvas').toDataURL('image/webp').indexOf('data:image/webp') === 0 ? '.webp' : '.jpg'; } catch (e) { return '.jpg'; }
    })();
    var cover = root.getAttribute('data-cover');
    var coverAlt = root.getAttribute('data-cover-alt') || '';
    var by = root.getAttribute('data-by') || '';
    var pageRatio = parseFloat(getComputedStyle(root).getPropertyValue('--page')) || 0.647;
    var spreads = srcs.map(function (li, i) {
      return { img: li.getAttribute('data-img'), text: li.getAttribute('data-say') || '', audio: li.getAttribute('data-audio'), n: i + 1 };
    });
    root.classList.add('is-ready');

    var el = function (cls) { var d = document.createElement('div'); d.className = cls; return d; };
    var img = function (src, alt) { var i = new Image(); i.decoding = 'async'; i.alt = alt || ''; i.src = src; return i; };
    var face = function (f) {
      var d;
      if (!f) return el('face face--empty');
      if (f.kind === 'cover') { d = el('face face--cover'); d.appendChild(img(cover + ext, coverAlt)); return d; }
      if (f.kind === 'pic') { d = el('face face--pic'); d.appendChild(img(f.s.img + ext, '')); return d; }
      d = el('face face--text');
      var head = document.createElement('span'); head.className = 'face__head'; head.setAttribute('aria-hidden', 'true'); head.textContent = by;
      var words = document.createElement('p'); words.className = 'face__words'; words.textContent = f.s.text;
      var num = document.createElement('span'); num.className = 'face__num'; num.setAttribute('aria-hidden', 'true'); num.textContent = String(f.s.n);
      d.appendChild(head); d.appendChild(words); d.appendChild(num);
      return d;
    };
    // shrink the words a little if a long page would not fit
    var fit = function (node) {
      var w = node && node.querySelector && node.querySelector('.face__words');
      if (!w) return;
      w.style.fontSize = '';
      var size = parseFloat(getComputedStyle(w).fontSize), guard = 0;
      while (node.scrollHeight > node.clientHeight + 1 && size > 12 && guard++ < 24) { size -= 0.5; w.style.fontSize = size + 'px'; }
    };
    var put = function (side, node) {
      while (side.firstChild) side.removeChild(side.firstChild);
      side.appendChild(node); fit(node);
    };

    // views: what is open at each step. Big screens show two pages, phones one.
    var mode = null, views = [], at = 0, busy = null, opened = false;
    var titleSay = root.getAttribute('data-title-say') || '';
    var coverAudio = root.getAttribute('data-cover-audio');
    var build = function (m) {
      var v = [m === 'spread' ? { L: null, R: { kind: 'cover' }, say: titleSay, audio: coverAudio } : { P: { kind: 'cover' }, say: titleSay, audio: coverAudio }];
      spreads.forEach(function (s) {
        if (m === 'spread') v.push({ L: { kind: 'pic', s: s }, R: { kind: 'text', s: s }, say: s.text, audio: s.audio });
        else { v.push({ P: { kind: 'pic', s: s }, say: '', hold: 1600 }); v.push({ P: { kind: 'text', s: s }, say: s.text, audio: s.audio }); }
      });
      return v;
    };
    var fitsSpread = function () {
      var w = root.clientWidth, h = window.innerHeight - 190;
      return Math.min(w, h * pageRatio * 2) >= 620;
    };
    var preload = function (i) {
      var v = views[i]; if (!v) return;
      [v.L, v.R, v.P].forEach(function (f) {
        if (f && f.kind === 'pic') img(f.s.img + ext);
        if (f && f.kind === 'cover') img(cover + ext);
      });
    };
    var ui = function () {
      count.textContent = at === 0 ? 'Cover' : at + ' of ' + (views.length - 1);
      prev.disabled = at === 0; next.disabled = at === views.length - 1;
      if (bar) bar.style.width = (at / (views.length - 1) * 100) + '%';
    };
    var paint = function () {
      var v = views[at];
      if (mode === 'spread') { put(sideL, face(v.L)); put(sideR, face(v.R)); }
      else put(sideR, face(v.P));
      book.classList.toggle('is-closed', mode === 'spread' && at === 0);
      ui(); preload(at + 1); preload(at - 1);
    };
    var setMode = function () {
      var m = fitsSpread() ? 'spread' : 'single';
      if (m === mode) { fit(sideL.firstChild); fit(sideR.firstChild); return; }
      if (busy) busy.finish();
      var spreadAt = mode === 'spread' ? at : mode === 'single' ? Math.ceil(at / 2) : 0;
      mode = m;
      root.classList.toggle('flip--spread', m === 'spread');
      root.classList.toggle('flip--single', m === 'single');
      views = build(m);
      at = m === 'spread' ? spreadAt : (spreadAt === 0 ? 0 : spreadAt * 2 - 1);
      paint();
    };

    // turn to view `to`, animating one leaf; `done` runs when the page has landed
    var go = function (to, done) {
      if (busy) busy.finish();
      if (to < 0 || to >= views.length || to === at) { if (done) done(); return; }
      var from = at, fwd = to > from, a = views[from], b = views[to];
      at = to;
      if (reduce.matches || Math.abs(to - from) > 1) { paint(); if (done) done(); return; }
      var leaf, front, back, target;
      if (mode === 'spread') {
        leaf = el('flip__leaf ' + (fwd ? 'flip__leaf--r' : 'flip__leaf--l'));
        if (fwd) { front = face(a.R); back = face(b.L); put(sideR, face(b.R)); target = sideL; }
        else { front = face(a.L); back = face(b.R); put(sideL, face(b.L)); target = sideR; }
      } else {
        leaf = el('flip__leaf flip__leaf--page' + (fwd ? '' : ' is-back'));
        if (fwd) { front = face(a.P); back = el('face face--blank'); put(sideR, face(b.P)); target = null; }
        else { front = face(b.P); back = el('face face--blank'); target = sideR; }
      }
      front.classList.add('leaf__front'); back.classList.add('leaf__back');
      leaf.appendChild(front); leaf.appendChild(back);
      book.appendChild(leaf); fit(front); fit(back);
      if (mode === 'spread') book.classList.toggle('is-closed', to === 0);
      void leaf.offsetWidth;
      leaf.classList.add('is-turning');
      ui(); preload(to + 1); preload(to - 1);
      var landed = false, timer;
      var finish = function () {
        if (landed) return;
        landed = true; clearTimeout(timer); busy = null;
        var keep = mode === 'spread' ? back : (fwd ? null : front);
        if (keep && target) { keep.classList.remove('leaf__front', 'leaf__back'); put(target, keep); }
        if (leaf.parentNode) leaf.parentNode.removeChild(leaf);
        if (done) done();
      };
      busy = { finish: finish };
      timer = setTimeout(finish, 960);
    };

    // read-aloud: recorded narration if a page has it, otherwise the device's own voice
    var synth = window.speechSynthesis;
    var canSpeak = !!(synth && window.SpeechSynthesisUtterance);
    var hasAudio = !!coverAudio || spreads.some(function (s) { return !!s.audio; });
    var buttons = Array.prototype.slice.call(root.querySelectorAll('[data-listen]'));
    var playing = false, finished = false, run = 0, line = 0, voice = null, player = null, wait = null, current = null;
    var pickVoice = function () {
      var best = null, top = -1;
      (synth.getVoices() || []).forEach(function (v) {
        var lang = String(v.lang || '').toLowerCase().replace('_', '-');
        if (lang.indexOf('en') !== 0) return;
        var s = 1;
        if (lang === 'en-ke') s += 40; else if (lang === 'en-gb') s += 20;
        else if (lang === 'en-za' || lang === 'en-ie' || lang === 'en-au') s += 12; else if (lang === 'en-us') s += 10;
        if (/natural|neural|enhanced|premium|google/i.test(v.name)) s += 15;
        if (v.localService === false) s += 2;
        if (s > top) { top = s; best = v; }
      });
      voice = best;
    };
    var sentences = function (text) {
      return (String(text).match(/[^.!?…]+[.!?…]+["”’)]*|[^.!?…]+$/g) || [])
        .map(function (t) { return t.replace(/[“”"]/g, '').trim(); })
        .filter(function (t) { return t.length > 1; });
    };
    var setPlaying = function (on) {
      playing = on;
      root.classList.toggle('is-reading', on);
      buttons.forEach(function (b) {
        b.setAttribute('aria-pressed', on ? 'true' : 'false');
        var label = b.querySelector('[data-listen-label]');
        if (label) label.textContent = on ? 'Pause' : 'Listen';
      });
    };
    var hush = function () {
      run += 1;
      clearTimeout(wait);
      if (canSpeak && (synth.speaking || synth.pending)) synth.cancel();
      if (player) player.pause();
    };
    var stop = function () { hush(); current = null; setPlaying(false); };
    var readView, after;
    after = function (token) {
      if (token !== run) return;
      if (at >= views.length - 1) { finished = true; line = 0; setPlaying(false); return; }
      wait = setTimeout(function () {
        if (token !== run) return;
        line = 0;
        go(at + 1, function () { if (token === run) readView(token); });
      }, 600);
    };
    readView = function (token) {
      var v = views[at];
      if (v.audio) {
        player = player || new Audio();
        if (player.getAttribute('data-src') !== v.audio) { player.src = v.audio; player.setAttribute('data-src', v.audio); }
        player.onended = function () { player.removeAttribute('data-src'); after(token); };
        var pr = player.play();
        if (pr && pr.catch) pr.catch(function () { if (token === run) stop(); });
        return;
      }
      if (!v.say || !canSpeak) { wait = setTimeout(function () { after(token); }, v.hold || 900); return; }
      var list = sentences(v.say);
      var say = function () {
        if (token !== run) return;
        if (line >= list.length) { after(token); return; }
        var u = new SpeechSynthesisUtterance(list[line]);
        if (voice) { u.voice = voice; u.lang = voice.lang; } else { u.lang = 'en-GB'; }
        u.rate = 0.9; u.pitch = 1.05;
        var done = false;
        var next = function () {
          if (done || token !== run) return;
          done = true; clearTimeout(wait);
          line += 1; say();
        };
        u.onend = next;
        u.onerror = function (e) {
          if (e && (e.error === 'interrupted' || e.error === 'canceled')) return;
          if (token === run) stop(); // no voice on this device
        };
        current = u; // keeps Safari from dropping the utterance before it ends
        clearTimeout(wait);
        wait = setTimeout(next, 4000 + list[line].length * 260); // in case "end" never fires
        synth.speak(u);
      };
      if (synth.paused) synth.resume();
      say();
    };
    var start = function () {
      hush();
      if (finished && at === views.length - 1) { go(0); line = 0; }
      finished = false; opened = true;
      setPlaying(true);
      readView(run);
    };
    // a page turned by hand: if reading, carry on reading from the new page
    var turnTo = function (to) {
      opened = true;
      if (to < 0 || to >= views.length || to === at) return;
      finished = false; line = 0;
      if (player) player.removeAttribute('data-src');
      if (playing) {
        hush();
        var token = run;
        go(to, function () { if (token === run) readView(token); });
      } else go(to);
    };

    setMode();
    prev.addEventListener('click', function () { turnTo(at - 1); });
    next.addEventListener('click', function () { turnTo(at + 1); });
    stage.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') { e.preventDefault(); turnTo(at - 1); }
      if (e.key === 'ArrowRight') { e.preventDefault(); turnTo(at + 1); }
    });
    var sx = null, sy = null;
    stage.addEventListener('pointerdown', function (e) { sx = e.clientX; sy = e.clientY; });
    stage.addEventListener('pointerup', function (e) {
      if (sx === null) return;
      var dx = e.clientX - sx, dy = e.clientY - sy; sx = null;
      if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy)) { turnTo(at + (dx < 0 ? 1 : -1)); return; }
      if (Math.abs(dx) < 10 && Math.abs(dy) < 10) {
        var r = book.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width;
        turnTo(at + (x > (mode === 'spread' ? 0.5 : 0.3) ? 1 : -1));
      }
    });
    stage.addEventListener('pointercancel', function () { sx = null; });
    var rt;
    window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(setMode, 150); });

    // open the book when it scrolls into view
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting || opened) return;
          opened = true; io.disconnect();
          setTimeout(function () { if (at === 0 && !playing) go(1); }, 800);
        });
      }, { threshold: 0.55 });
      io.observe(book);
    }

    if (!buttons.length || (!canSpeak && !hasAudio)) return;
    buttons.forEach(function (b) { b.hidden = false; });
    if (canSpeak) {
      pickVoice();
      if (synth.addEventListener) synth.addEventListener('voiceschanged', pickVoice);
      else synth.onvoiceschanged = pickVoice;
    }
    buttons.forEach(function (b) {
      b.addEventListener('click', function () { if (playing) stop(); else start(); });
    });
    window.addEventListener('pagehide', stop);
  });

  /* ---------- Footer year ---------- */
  var year = document.querySelector('[data-year]');
  if (year) year.textContent = String(new Date().getFullYear());
})();
