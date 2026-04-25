/* ============================================================
   BookTix — Main JavaScript
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

  // ── Auto-dismiss alerts after 5 seconds ──
  document.querySelectorAll('.alert').forEach(function (alert) {
    setTimeout(function () {
      alert.style.opacity = '0';
      alert.style.transition = 'opacity 0.4s';
      setTimeout(function () { alert.remove(); }, 400);
    }, 5000);
  });

  // ── Active nav link highlight ──
  var currentPath = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(function (link) {
    if (link.getAttribute('href') === currentPath) {
      link.style.color = '#fff';
      link.style.background = 'rgba(255,255,255,0.15)';
    }
  });

  // ── Ticket option radio selector enhancement ──
  document.querySelectorAll('.ticket-option').forEach(function (opt) {
    opt.addEventListener('click', function () {
      document.querySelectorAll('.ticket-option').forEach(function (o) {
        o.style.borderColor = '';
        o.style.background  = '';
      });
      this.style.borderColor = '#6C63FF';
      this.style.background  = '#f0eeff';
    });
  });

  // ── Smooth scroll for anchor links ──
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // ── QR Verification (Admin scan page) ──
  var scanInput = document.getElementById('qr-scan-input');
  var scanResult = document.getElementById('qr-scan-result');

  if (scanInput) {
    document.getElementById('verify-btn').addEventListener('click', function () {
      var bookingId = scanInput.value.trim();
      if (!bookingId) {
        showScanResult('error', 'Please enter a Booking ID.');
        return;
      }
      fetch('/bookings/verify/' + bookingId + '/')
        .then(function (r) { return r.json(); })
        .then(function (data) {
          if (data.valid) {
            showScanResult('success',
              '<strong>✓ Valid Ticket — Entry Allowed</strong><br>' +
              'Booking: ' + data.booking_id + '<br>' +
              'Name: ' + data.user + '<br>' +
              'Event: ' + data.event + '<br>' +
              'Category: ' + data.category + ' | Qty: ' + data.qty
            );
          } else {
            showScanResult('error', '<strong>✗ ' + data.message + '</strong>');
          }
        })
        .catch(function () {
          showScanResult('error', 'Network error. Please try again.');
        });
    });

    // Allow pressing Enter to verify
    scanInput.addEventListener('keypress', function (e) {
      if (e.key === 'Enter') {
        document.getElementById('verify-btn').click();
      }
    });
  }

  function showScanResult(type, html) {
    if (!scanResult) return;
    scanResult.innerHTML = html;
    scanResult.className = 'alert alert-' + (type === 'success' ? 'success' : 'error');
    scanResult.style.display = 'block';
  }

  // ── Confirm before cancelling booking ──
  document.querySelectorAll('.cancel-booking-btn').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      if (!confirm('Are you sure you want to cancel this booking?')) {
        e.preventDefault();
      }
    });
  });

  // ── Print button ──
  document.querySelectorAll('.print-ticket-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      window.print();
    });
  });

  // ── Copy booking ID to clipboard ──
  document.querySelectorAll('.copy-id-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var text = this.dataset.id;
      navigator.clipboard.writeText(text).then(function () {
        btn.textContent = 'Copied!';
        setTimeout(function () { btn.textContent = 'Copy ID'; }, 2000);
      });
    });
  });

});
