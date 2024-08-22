FROM quay.io/jupyter/minimal-notebook:hub-4.1.3
USER root
RUN pip install --no-cache -U cluster_viz 
EXPOSE 8000
EXPOSE 8888
USER ${NB_USER}
CMD ["/bin/bash","-c", "jupyterhub-singleuser"]