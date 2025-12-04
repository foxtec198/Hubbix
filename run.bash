/home/guibs/Documentos/Hubbix/venv/bin/python3 -m gunicorn wsgi:app \
    --bind 0.0.0.0:9560 \
    --timeout 120 \
    --log-level info \
    --access-logfile - \
    --error-logfile -