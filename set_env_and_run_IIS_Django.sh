#!/bin/bash
echo 'starting'
export DJANGO_SECRET_KEY='p@f+0p7#4rus+uh$84zzs3dmluyf2=6f^x5#7y5&6fi$%_2u3l'
export IIS_DB_PSSWD="gazdovejaja"
python3 Hotel/manage.py runserver