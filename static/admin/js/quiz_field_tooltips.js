/* Converts Django admin help text into hover tooltips with an info icon. */
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.help').forEach(function (helpEl) {
    var text = helpEl.textContent.trim();
    if (!text) return;

    /* Build the icon */
    var icon = document.createElement('span');
    icon.textContent = ' \u24d8'; /* circled i */
    icon.style.cssText = [
      'cursor:help',
      'color:#417690',
      'font-size:0.95em',
      'position:relative',
      'display:inline-block',
      'margin-left:4px',
    ].join(';');

    /* Build the popup */
    var popup = document.createElement('span');
    popup.textContent = text;
    popup.style.cssText = [
      'display:none',
      'position:absolute',
      'left:1.4em',
      'top:-0.3em',
      'background:#333',
      'color:#fff',
      'padding:7px 11px',
      'border-radius:5px',
      'font-size:0.82em',
      'font-weight:normal',
      'max-width:300px',
      'min-width:180px',
      'white-space:normal',
      'line-height:1.5',
      'z-index:9999',
      'box-shadow:0 2px 8px rgba(0,0,0,0.35)',
      'pointer-events:none',
    ].join(';');

    icon.appendChild(popup);

    icon.addEventListener('mouseenter', function () { popup.style.display = 'block'; });
    icon.addEventListener('mouseleave', function () { popup.style.display = 'none'; });

    /* Attach icon to the field label */
    var row = helpEl.closest('.form-row') || helpEl.closest('p') || helpEl.parentElement;
    var label = row ? row.querySelector('label') : null;
    if (label) {
      label.appendChild(icon);
    } else {
      helpEl.parentElement.insertBefore(icon, helpEl);
    }

    /* Hide the original help text */
    helpEl.style.display = 'none';
  });
});
