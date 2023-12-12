FROM public.ecr.aws/lambda/python:3.11 as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=$PYTHONPATH:${LAMBDA_TASK_ROOT}

WORKDIR ${LAMBDA_TASK_ROOT}

RUN pip install --upgrade pip && pip install poetry
RUN poetry config virtualenvs.create false && poetry config virtualenvs.in-project false && poetry config installer.parallel false

FROM base as dev

COPY pyproject.toml poetry.lock ./
RUN poetry install --with=dev,nolambda

COPY . .

ENTRYPOINT [ "./entrypoint.sh" ]

FROM base as nolambda

COPY pyproject.toml poetry.lock ./
RUN poetry install --with=nolambda

COPY . .

ENTRYPOINT [ "" ]

FROM base as lambda

COPY pyproject.toml poetry.lock ./
RUN poetry install --without=nolambda

COPY . .

CMD [ "handler.handler" ]