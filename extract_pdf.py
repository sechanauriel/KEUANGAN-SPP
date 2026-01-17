#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pdfplumber

pdf_path = "1768227613.pdf"

try:
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total pages: {len(pdf.pages)}\n")
        print("="*80)
        
        for page_num, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            print(f"\n--- PAGE {page_num} ---\n")
            print(text)
            print("\n" + "="*80)
            
except Exception as e:
    print(f"Error: {e}")
