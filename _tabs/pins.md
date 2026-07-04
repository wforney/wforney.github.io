---
icon: fas fa-thumbtack
order: 6
---

## Pins

A scrapbook of pins migrated from my old WordPress site.

<div class="pin-board">
{% for pin in site.data.pins %}
  <article class="pin-card card">
    <a class="pin-card-image" href="{{ pin.url }}" target="_blank" rel="noopener noreferrer">
      <img src="{{ pin.image }}" alt="{{ pin.title | xml_escape }}" loading="lazy">
    </a>
    <div class="card-body pin-card-body">
      <h2 class="card-title">{{ pin.title }}</h2>
      {% if pin.excerpt %}
        <p class="pin-card-excerpt">{{ pin.excerpt }}</p>
      {% endif %}
      <div class="pin-card-meta">
        {% if pin.categories.size > 0 %}
          <span>{{ pin.categories[0] }}</span>
        {% endif %}
        <a class="pin-card-link" href="{{ pin.url }}" target="_blank" rel="noopener noreferrer">Open pin</a>
      </div>
    </div>
  </article>
{% endfor %}
</div>
