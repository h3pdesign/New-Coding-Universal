## install.sh 

This script reproduces the Azure Notebooks Preview compute container environment as closely as possible. The script is supplied **as-is** to reproduce the Azure Notebooks Preview environment frozen to June 2020 state. It is important to maintain your development environment with recent secure versions of these packages. 

### Instructions

1. Copy the contents of this folder (\environment) to your machine. 
2. Invoke `sh install.sh` 

## Known Issues

- The script expects to be executed on a Linux distro that has odbc dependencies installed. If they are missing, install using `sudo apt-get install unixodbc-dev` before running the install script.

- When installing openfst you may need to update libstdc to avoid a `GLIBCXX_3.4.21 not found` error.   
