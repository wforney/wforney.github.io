# Adds target="_blank" and rel="nofollow noopener noreferrer" to all
# external links (those pointing outside the site's own domains).
require 'nokogiri'

Jekyll::Hooks.register [:pages, :posts, :documents], :post_render do |doc|
  next unless doc.output_ext == '.html'

  site_host = URI.parse(doc.site.config['url'] || 'https://wforney.github.io').host rescue 'wforney.github.io'

  # All domains that belong to this site (current + future)
  own_hosts = [site_host, 'williamforney.com', 'www.williamforney.com'].uniq

  parsed = Nokogiri::HTML(doc.output)
  changed = false

  parsed.css('a[href]').each do |link|
    href = link['href'].to_s
    next unless href.start_with?('http://', 'https://')

    begin
      link_host = URI.parse(href).host
    rescue URI::InvalidURIError
      next
    end

    next if link_host.nil?
    next if own_hosts.any? { |h| link_host == h || link_host.end_with?(".#{h}") }
    next if link['target'] # already has a target

    link['target'] = '_blank'
    existing = (link['rel'] || '').split
    link['rel'] = (existing | %w[nofollow noopener noreferrer]).join(' ')
    changed = true
  end

  doc.output = parsed.to_html if changed
end
