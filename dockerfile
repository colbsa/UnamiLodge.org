FROM ruby:3.3.1-alpine3.20

ENV SETUPDIR=/setup
WORKDIR ${SETUPDIR}
ARG GEMFILE_DIR=.
COPY $GEMFILE_DIR/Gemfile* $GEMFILE_DIR/packages* .

# Install build dependencies
RUN set -eux; \
  apk add --no-cache --virtual build-deps \
    build-base \
    zlib-dev \
  ;

# Install Bundler
RUN set -eux; gem install bundler

# Install extra packages needed for jekyll_picture_tag
RUN set -eux; \
  apk add --no-cache --virtual extra-pkgs vips-dev imagemagick

# Install gems from `Gemfile` via Bundler
RUN set -eux; bundler install

# Remove build dependencies
RUN set -eux; apk del --no-cache build-deps

# Clean up
WORKDIR /srv/jekyll
RUN set -eux; \
  rm -rf \
    ${SETUPDIR} \
    /usr/gem/cache \
    /root/.bundle/cache \
  ;

EXPOSE 4000
ENTRYPOINT ["bundler", "exec", "jekyll"]
CMD ["--version"]
