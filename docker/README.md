# Helper scripts

## Dev server

Quickly start up a dev server, wait for input and destroy it. Fresh db every time! =)

    docker/dev.sh

### What the script does

- Build
- Start the container and run development server
    - project-directory is mapped inside the container so changes are applied immediately and this script can be run multiple times without damaging the code
    - Regular ports are exposed see (Web server)
- Wait for enter
- Stop the container
- Destroy the container (Effectively destroying database)

## Test pull request

Quickly test a pull request

    docker/test_pull_request.sh remote branch

### What the script does

- Clean up work directory (assume it might destroy your uncommited things)
- Checkout a branch from a remote
    - add remotes with: git add remote **remote** git@github.com:**remote**/asylum.git
- Build
- Start the container and run development server
    - project-directory is **not** mapped
- Wait for ctrl-c
    - To login, in another terminal: docker exec -it asylum_test bash
- Destroy the server and everything with it

# Building locally

    docker build -t hacklabfi/asylum .


# Run tests on a container

When you have a container running, you can run tests with

    docker exec <container name> ./docker-entrypoint.sh py.test

# Running asylum

All of the docker commands are to be run at git repository root.

## Web server

The general idea is that a web server is going to appear at 8000 when you do docker run.

- On Linux: http://127.0.0.1:8000
- On other systems: http://192.168.100:8000 (maybe, check your docker-machine ip default)

## Maildump

- On Linux: http://127.0.0.1:1080
- On other systems: http://192.168.100:1080 (maybe, check your docker-machine ip default)

## Spawn a test server

Webserver exposed at port 8000.

    docker run --rm -it -p 8000:8000 -p 1080:1080 hacklabfi/asylum

This also **removes the container** afterwards.

## Create a test build and explore with bash

    docker run -it hacklabfi/asylum bash

## Test a pull request

    git checkout upstream/master
    git pull user pull_request
    docker build -t asylum_test .
    docker run --rm --name asylum_test -it -p 8000:8000 -p 1080:1080 asylum_test
    docker exec -it asylum_test bash

## Development environment (with project-folder mounted)

    docker run -it -p 8000:8000 -p 1080:1080 -v `pwd -P`/project:/opt/asylum hacklabfi/asylum
    docker exec -it container_name bash # Run in another terminal window

If you change anything that affects the build (requirements) you'll have to rebuild (see building locally).

Remember that if anything changes inside the docker container it might go to your git push.
Stay sharp! =)

This doesn't remove the container after ctrl-c and it can be started again if needed.

## Run in background

    docker run -d -p 8000:8000 -p 1080:1080 hacklabfi/asylum
