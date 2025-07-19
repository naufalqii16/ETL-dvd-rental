FROM postgres:15-alpine

# Copy database dump
COPY dvdrental.sql /docker-entrypoint-initdb.d/

# Set environment variables
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=password123
ENV POSTGRES_DB=dvdrental