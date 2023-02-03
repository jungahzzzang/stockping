#run.py 기준 경로
from app import *
from flask import Blueprint, jsonify
from app.stock import getTopTen as gt