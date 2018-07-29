#!/bin/bash
set -e

for i in $(env)
do
  key=$(echo $i | cut -d "=" -f 1)
  val=$(echo $i | cut -d "=" -f 2)

  if [[ ${val:0:6} == "secret" ]]; then
    IFS=':' read -r -a array <<< "${val}"
    SECRET_PATH=${array[0]}
    MOUNT_PATH=${array[1]}

    VARIABLE=$(
      curl --silent \
      -H "X-Vault-Token: ${VAULT_TOKEN}" \
      -X GET https://vault.saronia.io:8200/v1/${SECRET_PATH}/${NODE_ENV} \
      | jq -r '.data.value'
    )

    if [[ "${VARIABLE}" == "null" ]]; then
      VARIABLE=$(
        curl --silent \
        -H "X-Vault-Token: ${VAULT_TOKEN}" \
        -X GET https://vault.saronia.io:8200/v1/${SECRET_PATH} \
        | jq -r '.data.value'
      )
    fi

    if [[ -n "${MOUNT_PATH}" ]]; then
      mkdir -p "$(dirname "${MOUNT_PATH}")" && echo ${VARIABLE} | tr " " "\n" > ${MOUNT_PATH}
      export "${key}"=${MOUNT_PATH}
    else
      export "${key}"=${VARIABLE}
    fi
  fi
done

exec $@
