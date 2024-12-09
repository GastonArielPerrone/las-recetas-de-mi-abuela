#!/bin/bash
gunicorn -w 4 -b 0.0.0.0:3000 modelo_orm:app