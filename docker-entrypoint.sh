#!/bin/sh
set -e

echo "🚀 Starting CFA Stock Ontology..."

# Run production server
exec python main_prod.py
