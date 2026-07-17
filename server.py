#!/usr/bin/env python3
"""
خادم بايثون البسيط لتشغيل لعبة "خلية الحروف"
=============================================
الاستخدام:
    python server.py

ثم افتح المتصفح على العنوان:
    http://localhost:8000
"""

import http.server
import socketserver
import webbrowser
import os
import sys

# المنفذ الافتراضي
PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    """معالج الطلبات مع دعم الترميز UTF-8"""

    def do_GET(self):
        # إعادة التوجيه من الجذر إلى index.html
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

    def end_headers(self):
        # إضافة ترويسات لمنع التخزين المؤقت أثناء التطوير
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def log_message(self, format, *args):
        # طباعة رسائل السجل باللغة العربية
        print(f"[الخادم] {self.address_string()} — {format % args}")


def main():
    # الانتقال إلى مجلد الملف
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # محاولة تشغيل الخادم
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            url = f"http://localhost:{PORT}"
            print("=" * 50)
            print("  🎮  خلية الحروف — خادم محلي")
            print("=" * 50)
            print(f"  ✅  الخادم يعمل على: {url}")
            print(f"  📂  المجلد: {os.getcwd()}")
            print(f"  🛑  لإيقاف الخادم: اضغط Ctrl+C")
            print("=" * 50)

            # فتح المتصفح تلقائياً
            try:
                webbrowser.open(url)
                print("  🌐  تم فتح المتصفح تلقائياً")
            except Exception:
                print(f"  ℹ️  افتح المتصفح يدوياً على: {url}")

            print()
            httpd.serve_forever()

    except OSError as e:
        if e.errno == 98 or e.errno == 48:  # المنفذ مشغول
            print(f"  ⚠️  المنفذ {PORT} مشغول، جارٍ تجربة منفذ آخر...")
            # تجربة منفذ بديل
            with socketserver.TCPServer(("", 0), Handler) as httpd:
                actual_port = httpd.server_address[1]
                url = f"http://localhost:{actual_port}"
                print(f"  ✅  الخادم يعمل على: {url}")
                try:
                    webbrowser.open(url)
                except Exception:
                    pass
                httpd.serve_forever()
        else:
            print(f"  ❌  خطأ في تشغيل الخادم: {e}")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n  🛑  تم إيقاف الخادم. مع السلامة!")


if __name__ == "__main__":
    main()
