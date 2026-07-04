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
    <div class="pin-card-frame">
      <img src="{{ pin.image }}" alt="{{ pin.title | escape }}" loading="lazy">
      <a href="#"
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
        <span class="pin-card-zoom" aria-hidden="true">
          <i class="fas fa-search-plus"></i>
        </span>
      </a>
    </div>
  </article>
{% endfor %}
</div>

<div id="pin-modal" class="pin-modal" hidden aria-hidden="true">
  <div class="pin-modal-shell" role="dialog" aria-modal="true" aria-label="Pin details">
    <button type="button" class="pin-modal-close" data-pin-close aria-label="Close">
      <i class="fas fa-times"></i>
    </button>
    <div class="pin-modal-media">
      <img id="pin-modal-image" alt="">
    </div>
    <div class="pin-modal-body">
      <h2 id="pin-modal-title" class="pin-modal-title"></h2>
      <p id="pin-modal-excerpt" class="pin-modal-excerpt"></p>
      <div class="pin-modal-meta">
        <span id="pin-modal-category"></span>
        <a id="pin-modal-source" class="pin-modal-source" href="#" target="_blank" rel="noopener noreferrer" hidden></a>
      </div>
    </div>
  </div>
</div>

<script src="{{ '/assets/js/pins.js' | relative_url }}"></script>
