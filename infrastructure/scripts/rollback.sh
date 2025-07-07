#!/bin/bash
set -euo pipefail

cd infrastructure/terraform && terraform destroy -auto-approve -var-file=environments/${ENV:-dev}.tfvars
