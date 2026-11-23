// Endurance Real Estate Advisors: mobile nav + contact form. No dependencies.
(function () {
  var btn = document.querySelector('.menu-btn');
  if (btn) {
    btn.addEventListener('click', function () {
      var open = document.body.classList.toggle('nav-open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && document.body.classList.contains('nav-open')) {
        document.body.classList.remove('nav-open');
        btn.setAttribute('aria-expanded', 'false');
        btn.focus();
      }
    });
  }

  var form = document.getElementById('contact-form');
  if (!form) return;

  // Preselect topic from ?topic=careers etc.
  var topic = new URLSearchParams(location.search).get('topic');
  var sel = form.querySelector('#topic');
  if (topic && sel) {
    for (var i = 0; i < sel.options.length; i++) {
      if (sel.options[i].value === topic) sel.selectedIndex = i;
    }
  }

  var status = document.getElementById('form-status');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!form.checkValidity()) { form.reportValidity(); return; }
    var data = new FormData(form);
    if (data.get('company_website')) return; // honeypot
    var endpoint = form.getAttribute('data-endpoint');
    if (endpoint) {
      status.textContent = 'Sending...';
      fetch(endpoint, { method: 'POST', body: data, headers: { Accept: 'application/json' } })
        .then(function (r) {
          if (!r.ok) throw new Error();
          form.reset();
          status.textContent = 'Thank you. Your message was sent and we will be in touch shortly.';
        })
        .catch(function () {
          status.textContent = 'Sorry, something went wrong. Please call (646) 662-3546 or email greg.gang@endurance-rea.com.';
        });
      return;
    }
    // No endpoint configured: open the visitor's email app with the message prefilled.
    var subject = (data.get('topic') || 'Inquiry') + ' | ' + data.get('first_name') + ' ' + data.get('last_name');
    var body = [
      'Name: ' + data.get('first_name') + ' ' + data.get('last_name'),
      'Email: ' + data.get('email'),
      'Phone: ' + (data.get('phone') || ''),
      'Company: ' + (data.get('company') || ''),
      'Topic: ' + (data.get('topic') || ''),
      '',
      data.get('message') || ''
    ].join('\n');
    location.href = 'mailto:greg.gang@endurance-rea.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    status.textContent = 'Your email app should open with your message ready to send. If it does not, email greg.gang@endurance-rea.com or call (646) 662-3546.';
  });
})();

// Scroll reveal: every content block fades and rises into place as it enters the viewport.
(function () {
  window.__reveal = true;
  var root = document.documentElement;
  var SEL = '.hero-body > *,.intro > *,.split > .media,.split > div:not(.media) > *,.cols > div > *,.cols > .rows > *,.stat,.q,.post,.postrow,.person,.faq-group > h2,.faqs > .faq,.narrow > h2,.narrow > p,.narrow > ul,.prose > *,.contact-grid > div > *,.contact-grid > aside > h2,.details > div,.cta .wrap > *,.section > .wrap > p';
  var items = Array.prototype.slice.call(document.querySelectorAll('main :is(' + SEL + ')'));
  var show = function (el) { el.classList.add('is-visible'); };
  if (!('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) {
    items.forEach(show); return;
  }
  var io = new IntersectionObserver(function (entries) {
    var step = 0;
    entries.filter(function (e) { return e.isIntersecting; })
      .sort(function (a, b) { return a.target.compareDocumentPosition(b.target) & 4 ? -1 : 1; })
      .forEach(function (e) {
        e.target.style.setProperty('--step', Math.min(step++, 4));
        show(e.target);
        io.unobserve(e.target);
      });
  }, { rootMargin: '0px 0px -6% 0px', threshold: 0.08 });
  items.forEach(function (el) { io.observe(el); });
  // Clear the stagger delay after the entrance so hover transitions stay instant.
  items.forEach(function (el) {
    el.addEventListener('transitionend', function (ev) {
      if (ev.target === el && ev.propertyName === 'opacity') el.style.removeProperty('--step');
    });
  });
})();

// FAQ: only one answer open at a time (native details[name] plus a fallback for older browsers).
(function () {
  var faqs = Array.prototype.slice.call(document.querySelectorAll('details.faq'));
  faqs.forEach(function (d) {
    d.addEventListener('toggle', function () {
      if (!d.open) return;
      faqs.forEach(function (o) { if (o !== d && o.open) o.open = false; });
    });
  });
})();
