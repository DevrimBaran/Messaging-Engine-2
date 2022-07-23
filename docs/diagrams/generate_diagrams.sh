#!/usr/bin/env bash

dir=$(cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
cd "$dir"

java -version
PLANTUML_ARGS="-o png -tpng -charset UTF-8"
#export set PLANTUML_LIMIT_SIZE=8192

java -jar plantuml.jar $PLANTUML_ARGS sd_flow_execution1.plantuml
java -jar plantuml.jar $PLANTUML_ARGS sd_flow_execution2.plantuml
java -jar plantuml.jar $PLANTUML_ARGS sd_flow_execution.plantuml
java -jar plantuml.jar $PLANTUML_ARGS sd_flow_manager.plantuml
java -jar plantuml.jar $PLANTUML_ARGS sd_flow_manager1.plantuml
java -jar plantuml.jar $PLANTUML_ARGS sd_flow_manager2.plantuml
java -jar plantuml.jar $PLANTUML_ARGS sd_flow_manager3.plantuml
java -jar plantuml.jar $PLANTUML_ARGS sd_flow_manager4.plantuml

echo "OK."
exit 0
