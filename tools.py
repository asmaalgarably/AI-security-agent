import feedparser
import requests
from langchain_core.tools import tool


@tool
def fetch_cybersecurity_news(limit: int = 5) -> str:
  """تُستخدم لجلب أحدث أخبار الأمن السيبراني والثغرات المكتشفة خلال آخر 24 ساعة."""
  url = "https://feeds.feedburner.com/TheHackersNews"
  feed = feedparser.parse(url)
  results = []

  for entry in feed.entries[:limit]:
    results.append(
        "<untrusted_data source='TheHackerNews'>\n "
        f" <title>{entry.get('title', '')}</title>\n "
        f" <link>{entry.get('link', '')}</link>\n "
        f" <summary>{entry.get('summary', '')[:500]}</summary>\n</untrusted_data>"
    )

  return (
      "\n".join(results) if results else "لم يتم العثور على أخبار أمنية حديثة."
  )


@tool
def fetch_ai_news(limit: int = 5) -> str:
  """تُستخدم لجلب أحدث أخبار وتطورات الذكاء الاصطناعي والنماذج اللغوية (LLMs)."""
  url = "https://hnrss.org/newest?q=AI+OR+LLM+OR+Agent"
  feed = feedparser.parse(url)
  results = []

  for entry in feed.entries[:limit]:
    results.append(
        "<untrusted_data source='HackerNews_AI'>\n "
        f" <title>{entry.get('title', '')}</title>\n "
        f" <link>{entry.get('link', '')}</link>\n "
        f" <summary>{entry.get('summary', '')[:500]}</summary>\n</untrusted_data>"
    )

  return (
      "\n".join(results) if results else "لم يتم العثور على أخبار تقنية حديثة."
  )


@tool
def search_cve_database(keyword: str) -> str:
  """تُستخدم للبحث في قاعدة بيانات الثغرات الوطنية (NVD) عن ثغرات عام 2026 لتقنية محددة مثل Django أو React أو Python."""
  # تم تحديد نطاق التاريخ لعام 2026 لجلب الثغرات الحديثة فقط
  api_url = (
      f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={keyword}"
      "&pubStartDate=2026-01-01T00:00:00.000&pubEndDate=2026-12-31T23:59:59.999"
      "&resultsPerPage=3"
  )

  try:
    response = requests.get(api_url, timeout=15)
    if response.status_code != 200:
      return f"تعذر الاتصال بقاعدة بيانات NVD للبحث عن {keyword}."

    data = response.json()
    vulnerabilities = data.get("vulnerabilities", [])
    if not vulnerabilities:
      return f"لا توجد ثغرات مسجلة في عام 2026 للكلمة المفتاحية: {keyword}."

    results = []
    for item in vulnerabilities:
      cve = item.get("cve", {})
      cve_id = cve.get("id", "N/A")
      descriptions = cve.get("descriptions", [])
      desc_text = next(
          (d["value"] for d in descriptions if d["lang"] == "en"),
          "No description",
      )

      results.append(
          f"<untrusted_data source='NVD_CVE'>\n  <cve_id>{cve_id}</cve_id>\n "
          f" <description>{desc_text[:500]}</description>\n</untrusted_data>"
      )
    return "\n".join(results)

  except Exception as e:
    return f"حدث خطأ أثناء البحث: {str(e)}"