---
icon: fas fa-thumbtack
order: 6
---

## Pins

A scrapbook of pins migrated from my old WordPress site.

{% assign sorted_pins = site.data.pins | sort: 'date' | reverse %}

<div class="pin-board">
{% for pin in sorted_pins %}
  <article class="pin-card">
    <button
      type="button"
      class="pin-card-trigger"
      data-pin-open
      onclick="openPin(this); return false;"
      data-pin-title="{{ pin.title | escape }}"
      data-pin-image="{{ pin.image | escape }}"
      data-pin-excerpt="{{ pin.excerpt | escape }}"
      data-pin-source-text="{{ pin.source_text | escape }}"
      data-pin-source-url="{{ pin.source_url | escape }}"
      data-pin-category="{{ pin.categories | first | default: '' | escape }}"
      aria-label="Zoom {{ pin.title | escape }}">
      <img src="{{ pin.image }}" alt="{{ pin.title | escape }}" loading="lazy">
      <span class="pin-card-zoom" aria-hidden="true">
        <i class="fas fa-search-plus"></i>
      </span>
    </button>
  </article>
{% endfor %}
</div>

<dialog id="pin-dialog" class="pin-dialog" aria-label="Pin details">
  <div class="pin-dialog-shell">
    <button type="button" class="pin-dialog-close" data-pin-close aria-label="Close">
      <i class="fas fa-times"></i>
    </button>
    <div class="pin-dialog-media">
      <img id="pin-dialog-image" alt="">
    </div>
    <div class="pin-dialog-body">
      <h2 id="pin-dialog-title" class="pin-dialog-title"></h2>
      <p id="pin-dialog-excerpt" class="pin-dialog-excerpt"></p>
      <div class="pin-dialog-meta">
        <span id="pin-dialog-category"></span>
        <a id="pin-dialog-source" class="pin-dialog-source" href="#" target="_blank" rel="noopener noreferrer" hidden></a>
      </div>
    </div>
  </div>
</dialog>

<script src="{{ '/assets/js/pins.js' | relative_url }}"></script>
