FROM python:3-alpine

RUN adduser -g "User for lrn-cli" -h /home/lrn-cli -D -u 1000 lrn-cli
WORKDIR /home/lrn-cli
COPY dist/* /home/lrn-cli
RUN pip install *.whl

USER lrn-cli

ENTRYPOINT [ "lrn-cli" ]
