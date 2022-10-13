@ECHO OFF
celery -A dj_fundoo_notes worker -l INFO --pool=solo