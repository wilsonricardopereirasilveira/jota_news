#!/bin/bash
# Backup database
pg_dump $POSTGRES_DB > backup_$(date +%F).sql
