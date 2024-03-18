FROM postgres:16.1
RUN localedef -i pt_BR -c -f UTF-8 -A /usr/share/locale/locale.alias pt_BR.UTF-8
ENV LANG pt_BR.UTF-8

RUN apt-get update &&  \
  apt-get -y install postgresql-16-cron && \
  apt-get clean \
  && rm -rf /var/lib/apt/lists