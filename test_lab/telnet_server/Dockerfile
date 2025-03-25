FROM alpine:latest

RUN apk update
RUN apk add busybox-extras

EXPOSE 23

RUN adduser -D -s /bin/sh baptiste && echo "baptiste:superpassword" | chpasswd

CMD ["telnetd", "-F"]
