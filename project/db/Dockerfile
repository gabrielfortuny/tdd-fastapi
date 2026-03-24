# pull official base image
FROM postgres:18

# run create.sql on init
ADD create.sql /docker-entrypoint-initdb.d
