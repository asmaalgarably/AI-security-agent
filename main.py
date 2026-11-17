from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
import sys
from agent import DailyReport, ask_interactive_agent, generate_daily_report
from dotenv import load_dotenv

load_dotenv()

SEVERITY_AR = {
    "Critical": "حرج جداً",
    "High": "مرتفع الخطورة",
    "Medium": "متوسط",
    "Low": "منخفض",
}

CATEGORY_AR = {
    "AI_Development": "تطورات الذكاء الاصطناعي",
    "Cybersecurity": "الأمن السيبراني والثغرات",
    "Software_Stack": "تحديثات البرمجة والتطوير",
}


def send_email_report(report: DailyReport):
  """يحول التقرير العربي المنظم إلى صفحة HTML أنيقة ويرسله عبر Gmail باستخدام المنفذ 587."""
  sender = os.getenv("SENDER_EMAIL")
  password = os.getenv("SENDER_APP_PASSWORD")
  receiver = os.getenv("RECEIVER_EMAIL")

  if not sender or not password:
    print(
        "\n[ملاحظة]: بيانات الإيميل غير مضبوطة في ملف .env، تم عرض التقرير في"
        " الشاشة فقط."
    )
    return

  items_html = ""
  for item in report.items:
    color = "#d9534f" if item.severity in ["Critical", "High"] else "#0275d8"
    sev_label = SEVERITY_AR.get(item.severity, item.severity)
    cat_label = CATEGORY_AR.get(item.category, item.category)

    items_html += f"""
        <div style="border:1px solid #e0e0e0; border-right: 6px solid {color}; padding:16px; margin-bottom:18px; border-radius:6px; background-color:#ffffff;">
            <div style="margin-bottom:8px;">
                <span style="background:{color}; color:white; padding:4px 10px; border-radius:4px; font-size:12px; font-weight:bold;">{sev_label}</span>
                <span style="background:#f1f3f4; color:#333; padding:4px 10px; border-radius:4px; font-size:12px; margin-right:6px;">{cat_label}</span>
            </div>
            <h3 style="margin:10px 0 8px 0; color:#1a252f; font-size:18px;">{item.title}</h3>
            <p style="color:#444; font-size:14px; line-height:1.6;"><strong>الملخص التقني:</strong> {item.summary}</p>
            <p style="color:#1e4620; font-size:13px; background:#e8f5e9; padding:10px; border-radius:4px; border-right:3px solid #2e7d32;">
                <strong>الإجراء المقترح:</strong> {item.action_required}
            </p>
            <a href="{item.source_link}" style="display:inline-block; margin-top:6px; font-size:13px; color:#0275d8; text-decoration:none;">اقرأ التفاصيل من المصدر &larr;</a>
        </div>
        """

  html_body = f"""
    <html dir="rtl" lang="ar">
    <body style="font-family: 'Segoe UI', Tahoma, Arial, sans-serif; line-height:1.7; color:#333; max-width:700px; margin:auto; background-color:#f9f9f9; padding:20px;">
        <div style="background:#1a252f; color:white; padding:20px; border-radius:8px 8px 0 0; text-align:center;">
            <h2 style="margin:0; font-size:22px;">النشرة اليومية للذكاء الاصطناعي والأمن السيبراني</h2>
            <p style="margin:5px 0 0 0; font-size:13px; color:#cfd8dc;">تقرير مخصص ومترجم آلياً بواسطة وكيلكِ الذكي</p>
        </div>
        
        <div style="background:#ffffff; padding:20px; border-radius:0 0 8px 8px; border:1px solid #e0e0e0;">
            <div style="background:#f0f4f8; padding:15px; border-radius:6px; margin-bottom:20px; border-right:4px solid #1a252f;">
                <strong style="color:#1a252f; font-size:15px;">الملخص التنفيذي لليوم:</strong>
                <p style="margin:8px 0 0 0; font-size:14px; color:#2c3e50;">{report.executive_summary}</p>
            </div>
            
            {items_html}
        </div>
    </body>
    </html>
    """

  msg = MIMEMultipart("alternative")
  msg["Subject"] = "نشرة اليوم: مستجدات الذكاء الاصطناعي وثغرات الأمن السيبراني"
  msg["From"] = sender
  msg["To"] = receiver
  msg.attach(MIMEText(html_body, "html", "utf-8"))

  try:
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as server:
      server.starttls()
      server.login(sender, password)
      server.sendmail(sender, receiver, msg.as_string())
    print("\nتم إرسال التقرير المترجم بنجاح إلى بريدكِ الإلكتروني!")
  except Exception as e:
    print(f"\nفشل إرسال الإيميل: {e}")


if __name__ == "__main__":
  if "--auto" in sys.argv:
    print("=== تشغيل الوضع الآلي الإنتاجي ===")
    report = generate_daily_report()
    send_email_report(report)
    sys.exit(0)

  print("=== نظام وكيل الأمن السيبراني والذكاء الاصطناعي ===")
  print("1. توليد التقرير اليومي المترجم وإرساله للإيميل")
  print("2. الوضع التفاعلي (اسأل الوكيل ليختار الأدوات بنفسه)")

  choice = input("\nاختر رقم الوضع (1 أو 2): ").strip()

  if choice == "1":
    report = generate_daily_report()
    print(f"\n=== الملخص التنفيذي ===\n{report.executive_summary}\n")
    for idx, item in enumerate(report.items, 1):
      print(f"{idx}. [{SEVERITY_AR.get(item.severity)}] {item.title}")
      print(f"   الملخص: {item.summary}")
      print(f"   التوصية: {item.action_required}\n")

    send_email_report(report)

  elif choice == "2":
    print("\nاكتبي سؤالكِ (أو 'خروج' للإنهاء):")
    while True:
      q = input("\nأنتِ: ")
      if q.lower() in ["خروج", "exit", "quit"]:
        break
      print("الوكيل يفكر ويختار الأداة المناسبة...")
      answer = ask_interactive_agent(q)
      print(f"\nالوكيل: {answer}")