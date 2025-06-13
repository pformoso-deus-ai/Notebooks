FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir .
ENV ROLE=d
CMD ["python", "-m", "multi_agent_system", "execute-command", "hello"]
