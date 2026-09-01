"""Deja importar los módulos del pipeline de build, que viven en public/mockups."""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "public", "mockups"))
