#!/bin/bash
echo "Deleting flow entry on switch $1 on table $2 with flow id $3"
curl -u admin:admin -X DELETE \
"http://127.0.0.1:8181/rests/data/opendaylight-inventory:nodes/node=$1/flow-node-inventory:table=$2/flow-node-inventory:flow=$3"
