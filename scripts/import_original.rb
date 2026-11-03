require 'nokogiri'
require 'json'
require 'uri'

ROOT = File.expand_path('..', __dir__)
BASE = 'https://mysbupt.github.io/'
def text(node)
  node.text.gsub(/[\s\u00a0\u2003]+/, ' ').strip
end
def clean(node)
  node = node.dup
  node.css('font').each { |f| f.replace(f.children) }
  node.css('a').each do |a|
    href = a['href'].to_s.strip
    if href.empty?
      a.replace(a.children)
    else
      a['href'] = URI.join(BASE, href.gsub(' ', '%20')).to_s
      a.remove_attribute('target')
      a.remove_attribute('rel')
    end
  end
  node.traverse do |n|
    next unless n.element?
    n.attribute_nodes.each { |a| n.remove_attribute(a.name) unless n.name == 'a' && a.name == 'href' }
  end
  node.inner_html.gsub(/\[New!\]/, '').gsub(/(?:&emsp;|\u2003|\u00a0)+/, ' ').strip
end
home = Nokogiri::HTML(File.read("#{ROOT}/content/original/index.html"))
sections = {}
home.css('#main h3').each do |heading|
  nodes = []
  n = heading.next_sibling
  while n && n.name != 'h3'
    nodes << n
    n = n.next_sibling
  end
  sections[text(heading)] = nodes
end
news = sections.fetch('News').select { |n| n.name == 'li' }.map do |li|
  { date: text(li)[/\d{4}\/\d{2}/], html: clean(li).sub(/\A\s*\d{4}\/\d{2}\s*/, ''), text: text(li).sub(/\[New!\]\s*/, ''), papers: li.css('font[color="#7563a4"]').map { |f| text(f) } }
end
pubdoc = Nokogiri::HTML(File.read("#{ROOT}/content/original/publications.html"))
papers = []
pubdoc.css('tr').each do |tr|
  cells = tr.css('td')
  next unless cells.length == 2
  lines = cells[1].inner_html.split(/<br\s*\/?\s*>/).map { |v| text(Nokogiri::HTML.fragment(v)) }.reject(&:empty?)
  title, authors = lines
  next unless title && authors
  venue = text(cells[0])
  papers << {title: title.sub('DiFashion: DiFashion:', 'DiFashion:'), authors: authors, venue: venue, year: 2000 + venue[/[‘’'](\d{2})/, 1].to_i, links: []}
end
recent = []
news.each do |item|
  li = Nokogiri::HTML.fragment(item[:html])
  item[:papers].each do |title|
    font = home.css('font[color="#7563a4"]').find { |f| text(f) == title }
    links = []
    n = font.next_sibling
    while n && n.name != 'br' && n.name != 'font'
      candidates = n.name == 'a' ? [n] : n.css('a')
      candidates.each do |a|
        href = a['href'].to_s.strip
        links << {label: text(a), url: URI.join(BASE, href.gsub(' ', '%20')).to_s} unless href.empty?
      end
      n = n.next_sibling
    end
    existing = papers.find { |p| p[:title].downcase == title.downcase }
    if existing
      existing[:links] = links
    else
      recent << {title: title, authors: '', venue: '', year: item[:date][0,4].to_i, links: links, announcement: item[:text], announced: item[:date]}
    end
  end
end
data = {
  source: BASE, imported: '2026-11-03',
  news: news,
  publications: recent + papers,
  service: sections.fetch('Professional Services').select { |n| n.name == 'li' }.map { |n| {title: text(n).split(' - ').first, html: clean(n)} },
  awards: sections.fetch('Honors and Awards').select { |n| n.name == 'li' }.map { |n| text(n).sub('Finallist', 'Finalist') },
  experience: sections.fetch('Education and Research Background').select { |n| n.name == 'li' }.map { |n| clean(n) }
}
File.write("#{ROOT}/content/site.json", JSON.pretty_generate(data) + "\n")
puts "Imported #{news.length} news items, #{data[:publications].length} publications, #{data[:awards].length} awards."
