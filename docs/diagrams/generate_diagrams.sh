#!/usr/bin/env bash

dir=$(cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
cd "$dir"

java -version
PLANTUML_ARGS="-o png -tpng -charset UTF-8"
#export set PLANTUML_LIMIT_SIZE=8192

java -jar plantuml.jar $PLANTUML_ARGS sd_flow_execution.plantuml
java -jar plantuml.jar $PLANTUML_ARGS sd_flow_manager.plantuml

echo "OK."
exit 0
