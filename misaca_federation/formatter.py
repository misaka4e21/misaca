import re
import html.escape as encode

def format(status, **options):
    prepend_reblog = False
    if status.reblog_of:
        prepend_reblog = status.reblog_of.account.acct
        status         = status.proper

    raw_content = status.text

    if raw_content == '':
        return ''

    if not status.is_local():
      html = reformat(raw_content)
      if options['custom_emojify']:
          html = encode_custom_emojis(html, status.emojis)
      return html #.html_safe # rubocop:disable Rails/OutputSafety

    linkable_accounts = [m.account for m in status.mentions]
    linkable_accounts.append(status.account)

    html = raw_content
    if prepend_reblog:
        html = "RT @%s #%s" % (prepend_reblog, html)
    html = encode_and_link_urls(html, linkable_accounts)
    if options["custom_emojify"]:
        html = encode_custom_emojis(html, status.emojis)
    html = simple_format(html, {}, sanitize = false)
    html = html.replace("\n", '')

    return html #.html_safe # rubocop:disable Rails/OutputSafety

def reformat(html):
    #sanitize(html, Sanitize::Config::MASTODON_STRICT)
    return html

def plaintext(status):
    if status.is_local():
        return status.text

    text = status.text.(/(<br \/>|<br>|<\/p>)+/) { |match| "#{match}\n" }
    return strip_tags(text)

def simplified_format(account, **options):
    html = linkify(account.note) if account.is_local() else reformat(account.note)
    if options["custom_emojify"]:
        html = encode_custom_emojis(html, account.emojis)
    return html#.html_safe # rubocop:disable Rails/OutputSafety

def sanitize(html, config):
    #Sanitize.fragment(html, config)
    return html

def format_spoiler(status):
    html = encode(status.spoiler_text)
    html = encode_custom_emojis(html, status.emojis)
    #html.html_safe # rubocop:disable Rails/OutputSafety
    return html

def format_display_name(account, **options):
    html = encode(account.display_name.presence or account.username)
    if options["custom_emojify"]:
        html = encode_custom_emojis(html, account.emojis)
    return html #.html_safe # rubocop:disable Rails/OutputSafety

def format_field(account, str, **options):
    if not account.is_local():
        return reformat(str) #.html_safe

    html = encode_and_link_urls(str, me = true)
    if options["custom_emojify"]:
        html = encode_custom_emojis(html, account.emojis)
    return html #.html_safe # rubocop:disable Rails/OutputSafety

def linkify(text):
    html = encode_and_link_urls(text)
    html = simple_format(html, {}, sanitize = false)
    html = html.replace("\n", "")

    return html #.html_safe # rubocop:disable Rails/OutputSafety

def encode_and_link_urls(html, accounts = None, options = {}):
    #entities = Extractor.extract_entities_with_indices(html, extract_url_without_protocol = false)

    if accounts is dict:
      options  = accounts
      accounts = None

    #rewrite(html.dup, entities) do |entity|
    #  if entity[:url]
    #    link_to_url(entity, options)
    #  elsif entity[:hashtag]
    #    link_to_hashtag(entity)
    #  elsif entity[:screen_name]
    #    link_to_mention(entity, accounts)
    return html

def count_tag_nesting(tag):
    if tag[1] == '/'
        return -1
    elif tag[-2] == '/':
        return 0
    else:
        return 1

def encode_custom_emojis(html, emojis):
    if not emojis or emojis == []:
        return html

    emoji_map = {}
    for e in emojis:
        emoji_map[e.shortcode] = full_asset_url(e.image.url('static'))

    i                     = -1
    tag_open_index        = None
    inside_shortname      = False
    shortname_start_index = -1
    invisible_depth       = 0

    while i + 1 < html.size:
      i += 1

      if invisible_depth == 0 and inside_shortname and html[i] == ':':
        shortcode = html[(shortname_start_index + 1) : (i - 1)]
        emoji     = emoji_map[shortcode]

        if emoji:
          replacement = "<img draggable=\"false\" class=\"emojione\" alt=\":{{shortcode}}:\" title=\":{{shortcode}}:\" src=\"{{emoji}}\" />"
          replacement.format(shortcode=shortcode, emoji=emoji)
          before_html = html[0 : shortname_start_index - 1] if shortname_start_index > 0 else ''
          html        = before_html + replacement + html[i + 1 : -1]
          i          += replacement.size - (shortcode.size + 2) - 1
        else:
          i -= 1

        inside_shortname = False
      elif tag_open_index and html[i] == '>':
        tag = html[tag_open_index:i]
        tag_open_index = None
        if invisible_depth > 0
          invisible_depth += count_tag_nesting(tag)
        elif tag == '<span class="invisible">':
          invisible_depth = 1
      elif html[i] == '<':
        tag_open_index   = i
        inside_shortname = False
      elif not tag_open_index and html[i] == ':':
        inside_shortname      = True
        shortname_start_index = i

    return html

def rewrite(text, entities, function):
    return text
#     chars = str(text)

#     entities = sorted(entities, key=lambda entity: entity.indices[0] if hasattr(entity) else entity['indices'][0])

#     result = []

#     last_index = 0
#     for index in range(len(entities)):
#         entity = entities[index]
#         result.append()

#     last_index = entities.reduce(0) do |index, entity|
#       indices = entity.respond_to?(:indices) ? entity.indices : entity[:indices]
#       result << encode(chars[index...indices.first].join)
#       result << yield(entity)
#       indices.last
#     end

#     result << encode(chars[last_index..-1].join)

#     result.flatten.join
#   end

  def link_to_url(entity, options = {})
    url        = Addressable::URI.parse(entity[:url])
    html_attrs = { target: '_blank', rel: 'nofollow noopener' }

    html_attrs[:rel] = "me #{html_attrs[:rel]}" if options[:me]

    Twitter::Autolink.send(:link_to_text, entity, link_html(entity[:url]), url, html_attrs)
  rescue Addressable::URI::InvalidURIError, IDN::Idna::IdnaError
    encode(entity[:url])
  end

  def link_to_mention(entity, linkable_accounts)
    acct = entity[:screen_name]

    return link_to_account(acct) unless linkable_accounts

    account = linkable_accounts.find { |item| TagManager.instance.same_acct?(item.acct, acct) }
    account ? mention_html(account) : "@#{acct}"
  end

  def link_to_account(acct)
    username, domain = acct.split('@')

    domain  = nil if TagManager.instance.local_domain?(domain)
    account = EntityCache.instance.mention(username, domain)

    account ? mention_html(account) : "@#{acct}"
  end

  def link_to_hashtag(entity)
    hashtag_html(entity[:hashtag])
  end

  def link_html(url)
    url    = Addressable::URI.parse(url).to_s
    prefix = url.match(/\Ahttps?:\/\/(www\.)?/).to_s
    text   = url[prefix.length, 30]
    suffix = url[prefix.length + 30..-1]
    cutoff = url[prefix.length..-1].length > 30

    "<span class=\"invisible\">#{encode(prefix)}</span><span class=\"#{cutoff ? 'ellipsis' : ''}\">#{encode(text)}</span><span class=\"invisible\">#{encode(suffix)}</span>"
  end

  def hashtag_html(tag)
    "<a href=\"#{tag_url(tag.downcase)}\" class=\"mention hashtag\" rel=\"tag\">#<span>#{tag}</span></a>"
  end

  def mention_html(account)
    "<span class=\"h-card\"><a href=\"#{TagManager.instance.url_for(account)}\" class=\"u-url mention\">@<span>#{account.username}</span></a></span>"
  end
end
