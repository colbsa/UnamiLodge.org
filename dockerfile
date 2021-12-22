# The base image
FROM jekyll/builder

# `imagemagick6-dev` needs to stay in it's own command, as it overwrites some dependencies of imagemagick6
RUN apk add imagemagick

COPY Gemfile .
COPY Gemfile.lock .

USER root

# Run the install of gems within the Docker build process
RUN bundle install
