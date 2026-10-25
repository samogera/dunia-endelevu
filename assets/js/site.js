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
    if (header) header.classList.toggle('is-scrolled', window.scrollY > 4);
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
      if (window.innerWidth > 1060 && toggle.getAttribute('aria-expanded') === 'true') setMenu(false);
    });
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
    if (el.validity.valueMissing) {
      if (el.type === 'checkbox') return 'Please tick this box to continue.';
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
    if (el.type === 'checkbox') return;
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
      var evt = (el.type === 'checkbox' || el.tagName === 'SELECT') ? 'change' : 'input';
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
      var label = button ? button.textContent : '';
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
        if (button) { button.disabled = false; button.textContent = label; }
        box.setAttribute('tabindex', '-1');
        box.focus();
      }).catch(function () {
        box.className = 'form-status form-status--error';
        box.innerHTML = '<strong>We couldn’t send that just now.</strong>Please try again, or <a href="' +
          mailtoLink(subject, data) + '">send it by email instead</a>. Nothing you typed has been lost.';
        box.hidden = false;
        if (button) { button.disabled = false; button.textContent = label; }
      });
    });
  });

  /* ---------- Footer year ---------- */
  var year = document.querySelector('[data-year]');
  if (year) year.textContent = String(new Date().getFullYear());
})();
