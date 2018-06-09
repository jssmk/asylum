FROM ubuntu:18.04
ENV PYTHONUNBUFFERED 1
EXPOSE 8000
ENV LC_ALL "en_US.UTF-8"
ENV LC_CTYPE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
RUN ln -fs /usr/share/zoneinfo/Europe/Helsinki /etc/localtime

# Install basics
RUN apt update
RUN apt upgrade -y
RUN apt install -yq curl sudo postgresql git python3-dev virtualenv python3-virtualenv python3-pip npm locales

RUN locale-gen en_US.UTF-8

# build-essential graphviz-dev libpq-dev nodejs python-pip python-dev python-virtualenv
# Install maildump
EXPOSE 1080
# Installation fails at the moment
RUN pip3 install maildump

# Create database
USER postgres
RUN service postgresql start && \
    createuser asylum && \
    createdb -E utf-8 -T template0 -O asylum asylum && \
    psql -U postgres -d postgres -c "alter user asylum with password 'asylum'; alter user asylum with createdb;"

# Create a newuser
USER root
RUN adduser --disabled-password --gecos '' asylum && \
    adduser asylum sudo && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Create volume
RUN mkdir /opt/asylum/ && chown asylum:asylum /opt/asylum/
# VOLUME /opt/asylum/ # Your local uid != 1000? Tough. Create an issue and add an idea how to fix it.
WORKDIR /opt/asylum/

# Install system packages
COPY project/requirements.apt /opt/asylum/
RUN awk '/^\s*[^#]/' requirements.apt | xargs -r -- sudo apt-get install --no-install-recommends -y

# Configure locales
USER root

# Install python requirements
RUN virtualenv -p `which python3` ../asylum-venv
COPY project/requirements /opt/asylum/requirements/
RUN . ../asylum-venv/bin/activate && \
    pip3 install packaging appdirs urllib3[secure] && \
    pip3 install -r requirements/local.txt && \
    chown -R asylum:asylum ../asylum-venv && \
    true

# Configure application
USER root
RUN echo "DATABASE_URL=postgres://asylum:asylum@localhost/asylum" > .env
COPY project /opt/asylum/
RUN chown -R asylum:asylum /opt/asylum/

# Build localisations
USER asylum
RUN . ../asylum-venv/bin/activate && \
    for app in locale */locale; do (cd $(dirname $app) && ../manage.py compilemessages ); done

# Test npm (this will happen again at entrypoint)
USER asylum
RUN npm run build

# Run migrate and create admin user
USER asylum
RUN sudo -u postgres service postgresql start; \
    . ../asylum-venv/bin/activate && \
    export PGPASSWORD=asylum; while true; do psql -q asylum -c 'SELECT 1;' 1>/dev/null 2>&1 ; if [ "$?" -ne "0" ]; then echo "Waiting for psql"; sleep 1; else break; fi; done && \
    ./manage.py migrate && \
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'nospamplz@hacklab.fi', 'admin') ; from rest_framework.authtoken.models import Token ; Token.objects.create(user=User.objects.get(username='admin'), key='deadbeefdeadbeefdeadbeefdeadbeefdeadbeef')" | ./manage.py shell

ENTRYPOINT ["/opt/asylum/docker-entrypoint.sh"]
