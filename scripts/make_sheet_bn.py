"""Bangla variant: python make_sheet_bn.py spec_bn.json out.pdf"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bn_patch  # noqa: F401  (patches text drawing/measuring before sheet is used)
import make_sheet
make_sheet.main()
