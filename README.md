# UnamiLodge.org
A Jekyll based website for communicating with Unami Lodge, One members and the greater community.

* Production branch hosted at: [https://unamilodge.org](https://unamilodge.org)
* Development branch hosted at: [https://dev.unamilodge.org](https://dev.unamilodge.org)

This site is built on our servers by Jekyll. If you are not familiar with Jekyll we recommend [starting with Jekyll Docs at jekyllrb.com/docs/](https://jekyllrb.com/docs/).

## Getting Started
Because this is a static site, most of the development can be done locally on your own computer. The most difficult part is [installing the software that powers Jekyll - Ruby](https://jekyllrb.com/docs/installation/). Updates can be made to the site without this, but then all of the testing will need to happen on the development server. (Generally speaking this just means making sure there are no typos in links and image sources.)

### Updating the Site
Anyone who wants to is more than welcome to [fork our repository](https://help.github.com/en/github/getting-started-with-github/fork-a-repo), make their changes, and submit [pull requests](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests) to our development (staging) branch. Reviews may take a few minutes up to 2 days under most circumstances.

### Markdown and Liquid
We strive to use markdown and only markdown wherever possible on this site. Our favorite guide for markdown is https://guides.github.com/features/mastering-markdown/

Liquid is the template language we use. It's not used in any normal page, but it is the skeleton that Jekyll uses. So far my favorite resource for liquid is here https://shopify.github.io/liquid/

### Posts
Post creation is one of the most common updates made to this website and repository (or at least it will be once we are satisfied with the features it offers). Before making a post, we recommend you take a look at earlier posts as guides on how to format your post. Please use the post that closest matches what you want and use that as your template. Images for all posts are pulled from /img/posts/ with post banners and thumbs coming from their respective directories. Banners are not required but thumbs and excerpts are for now.

### Pages
All pages (excluding posts and individual chapter pages) will be found primarily sourced from the root directory and in a markdown file.

Many of our pages are highly data driven, and you will find the data in those pages in /_data/. These are formatted in [YAML](https://en.wikipedia.org/wiki/YAML) and are easier to update than it sounds.

### Images
All of our images are included, compressed, and resized by [Jekyll Picture Tag](https://rbuchberger.github.io/jekyll_picture_tag/).

We have standardized on using the PNG file format. Some standard sizes (in pixels) we designed around are:
- Post Thumbnails: 800x800
- Post Banners: 800x345
- Homepage Sliders: 4500x500
- Portals: 4500x900

## TODO
Items we are still working on
- Posts
  - Later posts with the same name as an earlier post get overwritten when the site is built. This will need to be fixed in the next year before a lot of our yearly topics begin to overlap.
  - We're looking to add tags to make it easier for Lodge Members to sort through our news posts and better present our posts.
- Images
  - Fine tune the quality of images displayed on the site - balance best compression, load times, and appearance.
  - Add alt tags for better accessibility and SEO.
- Search Feature
- Asset management
  - We're currently using Jekyll Picture Tag to manage images and Jekyll Minibundle to manage versions of CSS and JS. We are currently looking to find plugins that are more feature rich to replace both of these.
