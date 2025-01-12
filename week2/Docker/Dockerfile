# syntax=docker/dockerfile:1
FROM golang:1.21 AS builder
WORKDIR /src
COPY ./example .
RUN go mod tidy && CGO_ENABLED=0 go build -o /bin/example ./tcp_server.go

FROM scratch
COPY --from=builder /bin/example /bin/example
CMD ["/bin/example"]
