require "cgi"
require "date"
require "jekyll"
require "minitest/autorun"
require "pathname"
require "yaml"

ROOT = Pathname.new(__dir__).parent
SITE = ROOT.join("_site")

class SiteTest < Minitest::Test
  def test_core_pages_are_generated
    %w[
      index.html
      news/index.html
      search/index.html
      chapters/find/index.html
      contact/index.html
      sitemap.xml
    ].each do |path|
      assert_file SITE.join(path)
    end
  end

  def test_generated_chapter_pages_match_chapter_data
    chapters = YAML.safe_load_file(ROOT.join("_data/chapters.yml"), aliases: true)

    chapters.each do |chapter|
      slug = sanitize_filename(chapter.fetch("email"))
      page = SITE.join("chapters/#{slug}/index.html")

      assert_file page
      assert_includes page.read, CGI.escapeHTML(chapter.fetch("chapter-name"))
    end
  end

  def test_news_posts_have_unique_generated_slugs
    slugs = Hash.new { |hash, key| hash[key] = [] }

    post_files.each do |post|
      slug = news_output_slug_for(post)
      slugs[slug] << post.relative_path_from(ROOT).to_s
    end

    duplicates = slugs.select { |_slug, files| files.length > 1 }
    assert_empty duplicates, "duplicate /news/:title/ slugs would overwrite output pages: #{duplicates.inspect}"
  end

  def test_news_post_output_pages_exist
    post_files.each do |post|
      assert_file SITE.join("news/#{news_output_slug_for(post)}/index.html")
    end
  end

  def test_news_post_image_references_exist
    missing = []

    post_files.each do |post|
      data = front_matter(post)

      thumbnail = data["thumbnail"]
      if thumbnail.to_s.strip.empty?
        missing << "#{post.relative_path_from(ROOT)}: missing thumbnail"
      elsif !ROOT.join("img/posts/thumbs/#{thumbnail}").file?
        missing << "#{post.relative_path_from(ROOT)}: missing thumbnail file #{thumbnail}"
      end

      banner = data["banner"]
      if banner && !ROOT.join("img/posts/banners/#{banner}").file?
        missing << "#{post.relative_path_from(ROOT)}: missing banner file #{banner}"
      end
    end

    assert_empty missing
  end

  def test_picture_tag_outputs_are_generated
    logo_outputs = Dir[SITE.join("generated/img/logo-300-*").to_s]
    thumbnail_outputs = Dir[SITE.join("generated/img/posts/thumbs/*").to_s]

    refute_empty logo_outputs, "expected jekyll_picture_tag to generate logo output"
    assert_operator thumbnail_outputs.length, :>, 25
  end

  def test_key_pages_do_not_contain_unrendered_liquid
    %w[
      index.html
      news/index.html
      chapters/badenpowell/index.html
    ].each do |path|
      html = SITE.join(path).read

      assert_nil html.match(/{{/), "#{path} contains unrendered Liquid output"
      assert_nil html.match(/{%/), "#{path} contains unrendered Liquid tag"
    end
  end

  def test_search_page_renders_index_and_dependencies
    html = SITE.join("search/index.html").read

    assert_includes html, "window.store"
    assert_includes html, "lunr.min.js"
    assert_includes html, "assets/custom/js/search"
  end

  private

  def assert_file(path)
    assert path.file?, "expected #{path.relative_path_from(ROOT)} to exist"
  end

  def post_files
    Dir[ROOT.join("_posts/news/*.md")].map { |path| Pathname.new(path) }.sort
  end

  def front_matter(path)
    content = path.read
    match = content.match(/\A---\s*\n(.*?)\n---\s*\n/m)
    return {} unless match

    YAML.safe_load(match[1], permitted_classes: [Date, Time], aliases: true) || {}
  end

  def news_output_slug_for(path)
    title = path.basename(".md").to_s.sub(/\A\d{4}-\d{2}-\d{2}-/, "")
    Jekyll::Utils.slugify(title, mode: "pretty", cased: true)
  end

  def sanitize_filename(name)
    return name.to_s if name.is_a?(Integer)

    name.tr(
      "ÀÁÂÃÄÅàáâãäåĀāĂăĄąÇçĆćĈĉĊċČčÐðĎďĐđÈÉÊËèéêëĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħÌÍÎÏìíîïĨĩĪīĬĭĮįİıĴĵĶķĸĹĺĻļĽľĿŀŁłÑñŃńŅņŇňŉŊŋÑñÒÓÔÕÖØòóôõöøŌōŎŏŐőŔŕŖŗŘřŚśŜŝŞşŠšſŢţŤťŦŧÙÚÛÜùúûüŨũŪūŬŭŮůŰűŲųŴŵÝýÿŶŷŸŹźŻżŽž",
      "AAAAAAaaaaaaAaAaAaCcCcCcCcCcDdDdDdEEEEeeeeEeEeEeEeEeGgGgGgGgHhHhIIIIiiiiIiIiIiIiIiJjKkkLlLlLlLlLlNnNnNnNnnNnNnOOOOOOooooooOoOoOoRrRrRrSsSsSsSssTtTtTtUUUUuuuuUuUuUuUuUuUuWwYyyYyYZzZzZz"
    ).downcase.strip.gsub(" ", "-").gsub(/[^\w.-]/, "")
  end
end
