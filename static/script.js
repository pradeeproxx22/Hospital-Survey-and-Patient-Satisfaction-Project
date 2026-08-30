// Reveal vitals cards as they scroll into view.
const vitals = document.querySelectorAll('.vital');

if ('IntersectionObserver' in window && vitals.length) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        setTimeout(() => entry.target.classList.add('in-view'), i * 80);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.2 });

  vitals.forEach((v) => observer.observe(v));
} else {
  // Fallback: just show them.
  vitals.forEach((v) => v.classList.add('in-view'));
}

// Survey form: submit via fetch so we can show an inline thank-you
// message instead of a full page reload. Falls back to a normal
// form POST if fetch/JS isn't available.
const form = document.getElementById('survey-form');
const successBox = document.getElementById('form-success');

if (form) {
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const submitBtn = form.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Submitting…';

    try {
      const res = await fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
      });

      if (!res.ok) throw new Error('Request failed: ' + res.status);

      form.reset();
      form.style.display = 'none';
      successBox.classList.add('visible');
      successBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
    } catch (err) {
      // No backend wired up yet, or the request failed — tell the
      // person plainly instead of failing silently.
      submitBtn.disabled = false;
      submitBtn.textContent = 'Submit response';
      alert('Could not submit right now (' + err.message + '). Please try again, or check that the /submit-survey route exists on your server.');
    }
  });
}

// Assessment form (/predict): give clear feedback on submit.
// This is a real server-rendered POST (not fetch) — we just
// disable the button and swap its label before the browser
// navigates away, so the click feels acknowledged.
const predictForm = document.getElementById('predict-form');

if (predictForm) {
  predictForm.addEventListener('submit', () => {
    const btn = document.getElementById('predict-submit-btn');
    if (!btn) return;
    btn.disabled = true;
    btn.classList.add('is-loading');
    btn.textContent = 'Analyzing your answers…';
  });
}
