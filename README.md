Key Logger Project




מערכת מתקדמת לניטור הקשות מקלדת עם שליטה מרחוק וממשק אינטרנטי.

תוכן עניינים
תיאור הפרויקט
תכונות עיקריות
מבנה הפרויקט
פירוט פונקציונליות
דרישות
התקנה
שימוש
אבטחה
קרדיטים
תיאור הפרויקט
מערכת זו מאפשרת ניטור הקשות מקלדת בזמן אמת, שליטה מרחוק דרך שרת API, וצפייה בנתונים בממשק אינטרנטי מותאם. הפרויקט נועד למטרות למידה והדגמה טכנית.

⚠️ אזהרה: יש להשתמש במערכת זו אך ורק בסביבה חוקית ומבוקרת עם הסכמה מפורשת.

תכונות עיקריות
🔒 ניטור מאובטח: רישום הקשות עם הצפנה.
🌐 שליטה מרחוק: הפעלה/הפסקה דרך ממשק האינטרנט.
💾 אחסון גמיש: שרת או קובץ מקומי.
⚙️ ניהול מתקדם: הגדרות תדירות וזמן.
📊 ממשק משתמש: תצוגה וסינון לוגים.
מבנה הפרויקט
לקוח: key_logger_manager.py, key_logger.py, encryption.py, api_server.py, writer.py.
שרת: server.py, קבצי JSON.
ממשק: index.html, styles.css, scripts.js.
פירוט פונקציונליות
👨‍💻 Key Logger Client
איסוף: משתמש ב-pynput.
שמירה: שרת או קובץ, כל X שניות.
הצפנה: XOR עם מפתח 5.
תקשורת: דיווח מצב כל 40 שניות.
🌐 API Server
נתיבים:
/api/status/update (POST): מקבל עדכוני מצב מהלקוחות ושומר ב-device_status.json.
/api/data/upload (POST): מקבל לוגי הקשות מוצפנים, מפענח אותם ושומר ב-all_devices_data.json.
/api/data/files (GET): מחזיר לוגים עבור מכשיר לפי כתובת MAC.
/api/status/all (GET): מחזיר מצב כל המכשירים.
/api/status/check (GET): מחזיר שינויי הגדרות ללקוח לפי MAC ומסיר אותם לאחר שליחה.
/api/status/change (POST): מקבל שינויי הגדרות מהממשק האינטרנטי ושומר ב-change_device_status.json.
/api/files/list (GET): מחזיר רשימת קבצים בספריית השרת.
ניהול: שמירה ב-JSON, פענוח נתונים.
🖥️ Web Interface
תצוגה: רשימת מכשירים ולוגים.
שליטה: הגדרות דינמיות.
סינון: תאריך, שעה, חלונית.
דרישות
לקוח: Python 3.x, pynput, requests.
שרת: Python 3.x, flask, flask-cors, pytz.
ממשק: דפדפן מודרני.
התקנה
שכפל את המאגר:
bash
Wrap
Copy
git clone https://github.com/[שם המשתמש]/key-logger.git
התקן דרישות:
bash
Wrap
Copy
pip install pynput requests flask flask-cors pytz
הפעל שרת:
bash
Wrap
Copy
python server.py
הפעל לקוח:
bash
Wrap
Copy
python main.py
שימוש
פתח http://localhost:5000 לניהול.
אבטחה
🔐 הצפנה בסיסית (XOR).
🔒 מסך נעילה עם סיסמה.

קרדיטים
נוצר על ידי Hershy Rozenfeld & Moyshi Fogel.
