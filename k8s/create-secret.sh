#!/bin/bash
secret_file="k8s/secret.yaml"

echo "apiVersion: v1" > $secret_file
echo "kind: Secret" >> $secret_file
echo "metadata:" >> $secret_file
echo "  name: secret-secure-api" >> $secret_file
echo "type: Opaque" >> $secret_file
echo "data:" >> $secret_file

while true; do
    read -p "Enter key (leave empty to finish): " key
    if [[ -z "$key" ]]; then
        break
    fi

    read -p "Enter value for $key: " value
    encoded_value=$(printf "%s" "$value" | base64)
    
    echo "  $key: $encoded_value" >> $secret_file
done

echo "Secret YAML 파일이 생성되었습니다: $secret_file"
