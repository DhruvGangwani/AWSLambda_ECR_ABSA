# syntax=docker/dockerfile:1
FROM public.ecr.aws/lambda/python:3.6

WORKDIR .

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r ecs_requirements.txt --target "${LAMBDA_TASK_ROOT}"
COPY . ${LAMBDA_TASK_ROOT}


CMD ["app.aspect_sentiment"]


