FROM jupyter/pyspark-notebook:414b5d749704

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN export NODE_OPTIONS=--max-old-space-size=4096
RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager@1.1 --no-build
RUN jupyter labextension install jupyterlab-plotly@1.4.0 --no-build
RUN jupyter labextension install plotlywidget@1.4.0 --no-build
RUN jupyter lab build
RUN unset NODE_OPTIONS
