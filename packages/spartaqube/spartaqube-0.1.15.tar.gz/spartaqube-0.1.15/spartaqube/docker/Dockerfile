FROM python:3.11

RUN apt-get update && apt-get install -y unixodbc-dev
# Environement variable for docker version 
ENV IS_REMOTE_SPARTAQUBE_CONTAINER=True
# Creat database folder for database persistence
RUN mkdir -p /app/APPDATA/local_db 

# **********************************************************************************************************************
# INSTALL PIP + LIBRARIES
# **********************************************************************************************************************
RUN pip install --upgrade pip
RUN pip install spartaqube
COPY ./entrypoint_docker.py .
COPY ./entrypoint.sh .

# **********************************************************************************************************************
# SPARTAQUBE executable from environment variables
# **********************************************************************************************************************
ENV PATH="/usr/local/lib/python3.11/site-packages/spartaqube/cli/:${PATH}"

# **********************************************************************************************************************
# START SPARTAQUBE ON SPECIFIC PORT
# **********************************************************************************************************************
ENTRYPOINT ["sh", "/entrypoint.sh"]
# CMD tail -f /dev/null