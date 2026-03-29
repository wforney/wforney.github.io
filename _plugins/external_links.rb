# Adds target="_blank" and rel="nofollow noopener noreferrer" to all
# external links (those pointing outside the site's own domains).
require 'uri'

OWN_HOSTS = %w[wforney.github.io williamforney.com www.williamforney.com].freeze

def own_host?(href)
  host = URI.parse(href).host
  return true if host.nil?
  OWN_HOSTS.any? { |h| host == h || host.end_with?(".#{h}") }
rescue URI::InvalidURIError
  true
end

Jekyll::Hooks.register [:pages, :posts, :documents], :post_render do |doc|
  next unless doc.output_ext == '.html'

  doc.output = doc.output.gsub(/<a\b([^>]*?)href="(https?:\/\/[^"]+?)"([^>]*?)>/i) do
    pre, href, post = Regexp.last_match(1), Regexp.last_match(2), Regexp.last_match(3)
    all_attrs = pre + post

    if own_host?(href) || all_attrs.include?('target=')
      Regexp.last_match(0)
    else
      # Merge nofollow into any existing rel, or add new one
      if (rel_match = all_attrs.match(/rel="([^"]*)"/))
        existing = rel_match[1].split
        new_rel  = (existing | %w[nofollow noopener noreferrer]).join(' ')
        new_attrs = all_attrs.sub(/rel="[^"]*"/, "rel=\"#{new_rel}\"")
        pre2, post2 = new_attrs[0, pre.length], new_attrs[pre.length..]
        "<a#{pre2}href=\"#{href}\"#{post2} target=\"_blank\">"
      else
        "<a#{pre}href=\"#{href}\"#{post} target=\"_blank\" rel=\"nofollow noopener noreferrer\">"
      end
    end
  end
end
