import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time

# Настройка на страницата
st.set_page_config(page_title="DataCore Audit", page_icon="🛡️", layout="centered")

st.title("🛡️ DataCore Audit")
st.subheader("Професионален експертен одит и технически решения за уебсайтове")
st.markdown("Въведи линка на твоя сайт, за да откриеш критичните грешки, които ти губят клиенти и продажби.")

target_url = st.text_input("Въведи адрес на сайт (напр. https://example.com):", "")

def detect_cms(headers, html_content):
    generator = ""
    soup = BeautifulSoup(html_content, 'html.parser')
    gen_tag = soup.find('meta', attrs={'name': 'generator'})
    if gen_tag and gen_tag.get('content'):
        generator = gen_tag.get('content').lower()
        
    if 'wordpress' in generator or 'wp-content' in html_content:
        return "WordPress"
    elif 'shopify' in html_content or 'cdn.shopify.com' in html_content:
        return "Shopify"
    elif 'wix' in html_content:
        return "Wix"
    else:
        return "Custom / Друга платформа"

if st.button("Стартирай диагностика"):
    if not target_url:
        st.warning("Моля, въведете валиден URL адрес.")
    else:
        with st.spinner("Анализиране на платформата и сигурността..."):
            if not target_url.startswith("http"):
                target_url = "https://" + target_url
                
            parsed_url = urlparse(target_url)
            errors = []
            solutions = []
            upsell_opportunities = []

            try:
                start_time = time.time()
                response = requests.get(target_url, timeout=12, headers={"User-Agent": "DataCoreAuditBot/2.0"})
                ttfb = (time.time() - start_time) * 1000
                
                # Основни метрики
                col1, col2, col3 = st.columns(3)
                col1.metric("HTTP Статус", response.status_code)
                col2.metric("Време за отговор", f"{ttfb:.0f} ms")
                
                cms = detect_cms(response.headers, response.text)
                col3.metric("Платформа", cms)

                if response.status_code != 200:
                    errors.append(f"Критичен грешен HTTP статус код: {response.status_code}")
                    solutions.append("Коригирайте сървърните рутери или пренасочванията.")
                    
                if ttfb > 800:
                    errors.append("Бавна реакция на сървъра (висок TTFB).")
                    solutions.append("Оптимизиране на базата данни и внедряване на кеширащ слой.")
                    upsell_opportunities.append("Професионална оптимизация на скоростта и хостинг миграция.")

                if parsed_url.scheme != "https":
                    errors.append("Липсва сигурна връзка (HTTPS).")
                    solutions.append("Инсталирайте и активирайте SSL сертификат.")
                    upsell_opportunities.append("Инсталация и конфигуриране на сигурен SSL сертификат.")

                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.find('title')
                if not title or not title.text.strip():
                    errors.append("Липсва заглавен таг (<title>) на началната страница.")
                    solutions.append("Добавете уникално заглавие с ключови думи в хедъра.")
                    
                description = soup.find('meta', attrs={'name': 'description'})
                if not description or not description.get('content'):
                    errors.append("Липсва мета описание (Meta Description).")
                    solutions.append("Добавете описание за по-добра видимост в търсачките.")
                    upsell_opportunities.append("Пълен On-Page SEO одит и текстова оптимизация.")

                st.divider()

                # 1. ОТКРИТИ СИМПТОМИ (Виждат се от всеки безплатно)
                st.error(f"⚠️ Открити потенциални проблеми в сайта: {len(errors)}")
                
                if not errors:
                    st.success("Поздравления! Основните автоматични проверки на началната страница минаха успешно.")
                else:
                    for i, err in enumerate(errors, 1):
                        st.warning(f"**Симптом #{i}:** {err}")

                st.divider()

                # 2. ПЛАТЕНА СТЕНА / PAYWALL ЗА РЕШЕНИЯТА
                st.markdown("### 🔒 Пълни технически решения и експертен доклад")
                st.info("""
                Точните технически решения, конфигурационни стъпки и скриптове за отстраняване на тези проблеми са скрити зад платен достъп. 
                
                Можеш да отключиш пълния експертен доклад и инструкции на промоционална цена от **10.99 €**.
                
                **Данни за плащане по сметка:**
                * **Получател:** Цветелина Здравкова Стоянова
                * **IBAN:** `BG03ESPY40040038432460`
                * **BIC:** `ESPYBGS1`
                
                *След като извършиш превода, изпрати платежния документ и линка към твоя сайт на нашите канали за контакт. Ще получиш пълния доклад с решенията, както и оферта за последваща професионална поддръжка от нашия екип.*
                """)

            except Exception as e:
                st.error(f"Възникна грешка при достъпа до сайта: {e}")

