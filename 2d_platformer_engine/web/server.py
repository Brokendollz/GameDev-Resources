#!/usr/bin/env python3
"""
Simple HTTP Server for the Web Game
Run with: python server.py
Then open http://localhost:8000 in your browser
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

PORT = 8000
DIRECTORY = Path(__file__).parent

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        return super().end_headers()

def run_server():
    """Start the HTTP server."""
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        url = f"http://localhost:{PORT}"
        print(f"🎮 משחק Platformer 2D - גרסת ווב")
        print(f"📍 הסרבר פועל ב: {url}")
        print(f"🌐 פתח את הלינק בדפדפן שלך")
        print(f"⏹️  לעצור הקלד: Ctrl+C")
        print()

        # Try to open browser automatically
        try:
            webbrowser.open(url)
            print("✅ הדפדפן נפתח באופן אוטומטי")
        except:
            print(f"⚠️  לא הצלחתי לפתוח את הדפדפן, גש לעצמך ל: {url}")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n✋ המשחק עצור")

if __name__ == "__main__":
    run_server()
