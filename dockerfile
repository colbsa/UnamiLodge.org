# Revised from: https://github.com/rockstorm101/jekyll-docker/tree/master
# Modified extra packages command
# Modified build command to work with DO App Platform

FROM ruby:3.3.1-alpine3.20

ENV SETUPDIR=/setup
ARG JEKYLL_ENV
ENV JEKYLL_ENV $JEKYLL_ENV
WORKDIR ${SETUPDIR}
ARG GEMFILE_DIR=.
ARG JEKYLL_BASEURL=''
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

# DELETE THESE TWO LINES TO BUILD LOCALLY BUT DO NOT COMMIT
COPY . /srv/jekyll
RUN jekyll build -b ${JEKYLL_BASEURL}
