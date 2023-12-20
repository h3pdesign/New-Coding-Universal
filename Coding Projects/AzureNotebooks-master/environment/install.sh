#!/usr/bin/env bash

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
set -xeu pipefail

# Download and Install Anaconda 3 v5.3.0
INSTPATH="$HOME/anaconda3_501"
curl -Lo "inst.sh" \
     "https://repo.continuum.io/archive/Anaconda3-5.3.0-Linux-x86_64.sh"
bash "inst.sh" -b -f -p "$INSTPATH" && rm -f "inst.sh"
export PATH="$INSTPATH/bin:$PATH"

conda config --append "channels" "conda-forge"
conda config --append "channels" "pytorch"

# Pin the python version to avoid major updates on new package installs
echo "python 3.6.*" > "$INSTPATH/conda-meta/pinned"

# Install Anaconda packages for Python 3.x

# Use this to determine frozen versions
# conda install -y --file "$HERE/pkgs.txt"

conda install -y --no-deps --file "$HERE/pkgs.txt"

pip install --upgrade "pip"
pip install --upgrade "setuptools" --ignore-installed
pip install "jsonschema>=2.6.0" "mistune>=0.8.4" "plotly>=4.1.0" "terminado>=0.8.1" "pygithub>=1.43.7" "ggplot>=0.11.5"

# patch ggplot to work with newer pandas
#   https://stackoverflow.com/a/51071609/128595
( cd "$INSTPATH/lib/python3.6/site-packages/ggplot"
  { echo "H4sIAMF70VsCA7VRwUrEMBA9m6+Yo5Amm0lbbQtCD16861mqSd3Apg1NFty/N1uatVIVPDiEObw3"
    echo "815mRpm+BzYBewKEcTJvOx+64HfejmPY68lzdwLXhde9Vt9QhDH2U9uVFFgxFAwR8KbBupEFFymA"
    echo "iUIIQin9Rf4iIUsQeVPeNqXgoirKUpZYLxJtCyzPcqDn1LYEjHXjFGA42vj3zsPgCOun0UajQXWe"
    echo "H8xLqnk0Vkdb6whdVWzZhCx8fE7Nxjg7Y7JWXdDP4eS0hzu4JgxiOMWDj578IpcRuhArCBboPkqE"
    echo "CD8MSr9nRG0OdAzm8OUsCfg8RkL+fIJN47L4uikElzkWKOt6vfhKnOef8//M/wGqFSSVoQIAAA=="
  } | base64 -d | gzip -d | patch -p1
  rm -vf "stats/smoothers.pyc" "utils.pyc"
)

# This is a work around for a problem that exists in
# TF 2.0. See https://github.com/tensorflow/tensorflow/issues/30191
# for more info.
pip install wrapt --ignore-installed

# tensorflow-tensorboard is a deprecated PyPi package that is out
# of date. Since we are on a new major version of TensorFlow we
# need to rely on the new PyPi package for tensorboard, named just
# tensorboard. First we make sure to uninstall the existing package

pip uninstall tensorflow-tensorboard
pip install "tensorflow==2.0.0b1" "tensorboard==2.0.1" \
    "keras>=2.2.4" "keras-applications>=1.0.7" "keras-preprocessing>=1.0.9" \
    "scikit-bio>=0.5.5" "scikit-image>=0.15.0" "scikit-learn>=0.20.3"

pip install "pyodbc==3.1.1"
pip install "gym>=0.14.0"
pip install "pydot>=1.4.1" "theano==1.0.3"
pip install "feedparser>=5.2.1" "klein>=19.6.0" "treq>=18.6.0" "service_identity>=17.0.0"

pip install "altair>=3.2.0"

#Install pymssql==2.1.1 (breaks on latest version 2.1.3)

pip install "pymssql==2.1.1"

pip install "cntk==2.5.1"
pip install "graphviz>=0.11.1"
pip install "snakeviz>=2.0.1" "line_profiler>=2.1.2" "pympler>=0.7" "memory_profiler>=0.55.0" "pyprof2calltree>=1.4.4"
pip install "word2vec>=0.10.2" "nltk>=3.3" "dask>=0.19.3" "luigi==2.8.2"
pip install "lxml>=4.2.5" "pymc3>=3.7" "elasticsearch>=7.0.2"
pip install "docker-py>=1.10.6" "networkx>=2.2" "pyang>=2.0.1" "edward>=1.3.5" "SQLAlchemy>=1.2.14" "pykafka>=2.8.0" "kafka-python>=1.4.6" "pypachy>=0.1.5"
pip install "bqplot>=0.11.7"

pip install "openfst==1.6.1"
pip install "boto3~=1.4.8"

pip install "argcomplete>=1.10.0"

pip install "arrow>=0.14.5" "beautifier>=0.5.5" "datacleaner>=0.1.5" "dora>=0.0.2" "ftfy==5.3.0" "prettypandas>=0.0.4" "scrubadub>=1.2.0" "tabulate>=0.8.2" # https://blog.modeanalytics.com/python-data-cleaning-libraries/

pip install "okpy==1.13.11" "datascience==0.10.6"

pip install "azure>=4.0.0" "azure-cli-core==2.0.54"

pip install "azureml-sdk[notebooks, automl, explain]>=1.0.57"
pip install "azureml-dataprep>=1.1.12"
pip install "azureml-opendatasets>=1.0.57"

pip install "onnxmltools>=1.5.0" "onnxruntime>=0.5.0" "tf2onnx>=1.5.3"

pip install "azure-kusto-data>=0.0.31" "azure-kusto-ingest>=0.0.31" \
            "Kqlmagic>=0.1.101"

conda clean --verbose -ay

ln -s "$INSTPATH/bin/python" "$HOME/.local/bin/python36"

rm -rf "$HOME/.cache/pip"