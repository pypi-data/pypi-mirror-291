#!/bin/bash
# check if linux
if [ "$(uname)" == "Linux" ]; then
            sudo apt-get install python3-lxml
fi

# check if mac
if [ "$(uname)" == "Darwin" ]; then
          pip uninstall -y  lxml
          pip install --no-binary lxml lxml
fi

