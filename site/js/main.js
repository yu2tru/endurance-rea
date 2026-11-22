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
