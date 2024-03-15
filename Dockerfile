FROM ubuntu:latest
LABEL authors="v.sinitsky"

ENTRYPOINT ["top", "-b"]