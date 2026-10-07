import streamlit as st
import streamlit.components.v1 as components
from datetime import date, timedelta
from calendar import monthrange
import re

# =============================================================================
# Sayfa Ayarları
# =============================================================================
st.set_page_config(
    page_title="Fon Hesaplama | ÜFE-TÜFE Güncelleme",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =============================================================================
# Özel CSS – Premium Koyu Tema
# =============================================================================
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Genel Gövde ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(160deg, #0f0c29 0%, #1a1a3e 40%, #24243e 100%);
}

/* ── Başlık Stili ── */
.main-title {
    text-align: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.6rem;
    font-weight: 900;
    margin-bottom: 0.2rem;
    letter-spacing: -0.5px;
}
.sub-title {
    text-align: center;
    color: #8b8fa3;
    font-size: 1rem;
    font-weight: 400;
    margin-bottom: 2rem;
}

/* ── Kart Kutusu ── */
.card-box {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.5rem 1.2rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(12px);
}

/* ── Bölüm Başlıkları ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 1rem;
}
.section-icon {
    font-size: 1.5rem;
}
.section-label {
    font-size: 1.2rem;
    font-weight: 700;
    background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.section-label-red {
    font-size: 1.2rem;
    font-weight: 700;
    background: linear-gradient(90deg, #f5576c 0%, #ff6a88 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* ── Sonuç Kartı ── */
.result-card {
    background: linear-gradient(135deg, rgba(102,126,234,0.15), rgba(118,75,162,0.15));
    border: 1px solid rgba(102,126,234,0.3);
    border-radius: 16px;
    padding: 2rem;
    margin-top: 1.5rem;
}
.result-title {
    font-size: 1.4rem;
    font-weight: 800;
    color: #e0e0ff;
    margin-bottom: 1rem;
    text-align: center;
}
.result-row {
    display: flex;
    justify-content: space-between;
    padding: 0.6rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    font-size: 0.95rem;
}
.result-label {
    color: #a0a4c0;
    font-weight: 500;
}
.result-value {
    font-weight: 700;
    color: #fff;
}
.result-value-green {
    font-weight: 800;
    color: #43e97b;
    font-size: 1.15rem;
}
.result-value-red {
    font-weight: 800;
    color: #f5576c;
    font-size: 1.15rem;
}
.result-value-gold {
    font-weight: 900;
    color: #ffd700;
    font-size: 1.3rem;
}

/* ── Limit Uyarı Kartı ── */
.limit-card {
    background: linear-gradient(135deg, rgba(255,165,0,0.15), rgba(255,69,0,0.15));
    border: 2px solid rgba(255,165,0,0.5);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-top: 1.5rem;
    text-align: center;
    animation: pulse-border 2s infinite;
}
@keyframes pulse-border {
    0%, 100% { border-color: rgba(255,165,0,0.5); }
    50% { border-color: rgba(255,69,0,0.9); }
}
.limit-title {
    font-size: 1.3rem;
    font-weight: 800;
    color: #ff8c00;
    margin-bottom: 0.5rem;
}
.limit-text {
    color: #ffd0a0;
    font-size: 1rem;
    font-weight: 500;
}
.limit-amount {
    font-size: 1.6rem;
    font-weight: 900;
    color: #ffd700;
    margin-top: 0.5rem;
}

/* ── Detay Tablosu ── */
.detail-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    margin-top: 1rem;
    border-radius: 12px;
    overflow: hidden;
}
.detail-table th {
    background: rgba(102,126,234,0.25);
    color: #c8c8ff;
    padding: 0.7rem 1rem;
    font-weight: 600;
    font-size: 0.85rem;
    text-align: left;
}
.detail-table td {
    padding: 0.6rem 1rem;
    color: #d0d0e0;
    font-size: 0.85rem;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.detail-table tr:nth-child(even) td {
    background: rgba(255,255,255,0.02);
}

/* ── Streamlit Widget Renk Düzeltmeleri ── */
.stNumberInput label, .stDateInput label, .stSelectbox label, .stSlider label, .stTextInput label {
    color: #c0c4e0 !important;
    font-weight: 500 !important;
}

/* ── Hesapla Butonu ── */
div.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 0.8rem 3rem;
    border-radius: 12px;
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 20px rgba(102,126,234,0.3);
    width: 100%;
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(102,126,234,0.5);
}

/* ── Hata / Uyarı ── */
.stAlert {
    border-radius: 12px !important;
}

/* ── Footer ── */
.footer-text {
    text-align: center;
    color: #555;
    font-size: 0.75rem;
    margin-top: 3rem;
    padding: 1rem;
}
</style>
""", unsafe_allow_html=True)



# =============================================================================
# ÜFE – TÜFE Aylık Verileri  (Ocak 2025 → Eylül 2026)
# Sıralama: (yıl, ay): (üfe_yüzde, tüfe_yüzde)
# =============================================================================
AYLIK_VERILER: dict[tuple[int, int], tuple[float, float]] = {
    (2025, 1):  (5.03, 3.06),
    (2025, 2):  (2.27, 2.12),
    (2025, 3):  (2.46, 1.88),
    (2025, 4):  (3.00, 2.76),
    (2025, 5):  (1.53, 2.48),
    (2025, 6):  (1.37, 2.46),
    (2025, 7):  (2.06, 1.73),
    (2025, 8):  (2.04, 2.48),
    (2025, 9):  (3.23, 2.52),
    (2025, 10): (2.55, 1.63),
    (2025, 11): (0.87, 0.84),
    (2025, 12): (0.89, 0.75),
    (2026, 1):  (4.84, 2.67),
    (2026, 2):  (2.96, 2.43),
    (2026, 3):  (1.94, 2.30),
    (2026, 4):  (4.18, 3.17),
    (2026, 5):  (1.71, 2.75),
    (2026, 6):  (0.99, 1.80),
    (2026, 7):  (1.78, 1.52),
    (2026, 8):  (1.84, 2.57),
    (2026, 9):  (1.84, 2.07),
}

# Hesaplama bitiş tarihi
HEDEF_TARIH = date(2026, 9, 30)

# Veri aralığı sınırları
EN_ERKEN_TARIH = date(2025, 1, 1)
EN_GEC_TARIH = date(2026, 9, 30)



# Üst limit
UST_LIMIT = 1_000_000.0


def gunluk_oran(yil: int, ay: int) -> float:
    """
    Verilen yıl-ay için ÜFE+TÜFE ortalamasını günlük orana çevirir.
    Aylık oran → günlük oran:  (1 + aylik_oran)^(1/gün_sayısı) - 1
    """
    veri = AYLIK_VERILER.get((yil, ay))
    if veri is None:
        return 0.0
    ufe, tufe = veri
    aylik_ort = (ufe + tufe) / 2.0 / 100.0   # yüzdeyi ondalığa çevir
    gun_sayisi = monthrange(yil, ay)[1]
    return (1 + aylik_ort) ** (1 / gun_sayisi) - 1


def guncelle(miktar: float, baslangic: date, bitis: date) -> tuple[float, float]:
    """
    Bir tutarı başlangıç tarihinden bitiş tarihine kadar
    günlük ÜFE+TÜFE ortalamasıyla günceller.
    Döndürür: (güncellenmiş_tutar, toplam_katsayı)
    """
    if baslangic >= bitis:
        return miktar, 1.0

    carpan = 1.0
    gun = baslangic
    while gun < bitis:
        oran = gunluk_oran(gun.year, gun.month)
        # Ay sonuna kadar kaç gün kaldı (veya bitiş tarihine kadar)
        ay_son_gun = date(gun.year, gun.month, monthrange(gun.year, gun.month)[1])
        if ay_son_gun >= bitis:
            kalan_gun = (bitis - gun).days
        else:
            kalan_gun = (ay_son_gun - gun).days + 1

        # Aynı ay içinde toplu çarpma (performans)
        carpan *= (1 + oran) ** kalan_gun
        gun += timedelta(days=kalan_gun)

    guncellenmis = miktar * carpan
    return guncellenmis, carpan


def para_format(deger: float) -> str:
    """Türk Lirası formatı: 1.234.567,89 ₺"""
    formatted = f"{deger:,.2f}"
    # Virgül → geçici, nokta → virgül, geçici → nokta
    formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{formatted} ₺"


def oran_format(deger: float) -> str:
    """Oran formatı: %12,34"""
    return f"%{deger * 100:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def parse_para(text: str) -> float | None:
    """
    Binlik ayraçlı Türk formatındaki metin girişini sayıya çevirir.
    Örnekler: '1.250.000,50' → 1250000.50,  '50000' → 50000.0
    """
    if not text or text.strip() == "":
        return None
    # Noktaları (binlik ayraç) kaldır, virgülü (ondalık) noktaya çevir
    cleaned = text.strip().replace(".", "").replace(",", ".")
    # Sadece rakam ve nokta kalmalı
    cleaned = re.sub(r"[^\d.]", "", cleaned)
    if not cleaned:
        return None
    try:
        val = float(cleaned)
        return val if val > 0 else None
    except ValueError:
        return None


def _binlik_formatla(sayi_str: str) -> str:
    """
    Rakam dizisini Türk binlik ayracıyla formatlar.
    '1250000' → '1.250.000'   |   '1250000,50' → '1.250.000,50'
    """
    if not sayi_str:
        return ""
    # Sadece rakam ve virgül kalsın
    temiz = re.sub(r"[^\d,]", "", sayi_str)
    if not temiz:
        return ""
    parcalar = temiz.split(",")
    tam_kisim = parcalar[0]
    if not tam_kisim:
        return ""
    # Binlik ayraç ekle
    sonuc = ""
    for idx, rakam in enumerate(reversed(tam_kisim)):
        if idx > 0 and idx % 3 == 0:
            sonuc = "." + sonuc
        sonuc = rakam + sonuc
    # Ondalık kısım varsa ekle
    if len(parcalar) > 1:
        ondalik = re.sub(r"[^\d]", "", parcalar[1])[:2]
        sonuc += "," + ondalik
    return sonuc


def format_binlik_callback(key: str):
    """
    st.text_input on_change callback'i.
    Session state'teki değeri binlik ayraçlı formata çevirir.
    """
    raw = st.session_state.get(key, "")
    formatted = _binlik_formatla(raw)
    st.session_state[key] = formatted


def turkce_tarih(d: date) -> str:
    """Tarihi '08 Ekim 2026' gibi Türkçe metne çevirir."""
    if d is None:
        return ""
    aylar = [
        "", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
        "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"
    ]
    return f"{d.day:02d} {aylar[d.month]} {d.year}"


# =============================================================================
# UI – Başlık
# =============================================================================
st.markdown('<h1 class="main-title">📊 Fon Hesaplama Aracı</h1>', unsafe_allow_html=True)


# Hedef tarih bilgisi
st.markdown(
    f'<div style="text-align:center; color:#667eea; font-size:0.9rem; '
    f'margin-bottom:1.5rem; font-weight:600;">'
    f'🗓️ Ekim Üfe ve Tüfe Belli Olmadığından Hesaplama 30 Eylül 2026\'ya kadar yapılmaktadır.</div>',
    unsafe_allow_html=True,
)

# =============================================================================
# UI – Yatırılan (Alış) Bölümü
# =============================================================================
st.markdown(
    '<div class="card-box">'
    '<div class="section-header">'
    '<span class="section-icon">💰</span>'
    '<span class="section-label">Yatırılan (Alış) İşlemleri</span>'
    '</div></div>',
    unsafe_allow_html=True,
)

alis_adet = st.slider(
    "Kaç adet alış (yatırma) işleminiz var?",
    min_value=1,
    max_value=30,
    value=1,
    key="alis_slider",
)

alis_tarihleri: list[date | None] = []
alis_miktarlari: list[float | None] = []

for i in range(alis_adet):
    cols = st.columns([1, 1])
    with cols[0]:
        t = st.date_input(
            f"Alış {i + 1} – Tarih",
            value=None,
            min_value=EN_ERKEN_TARIH,
            max_value=EN_GEC_TARIH,
            format="DD.MM.YYYY",
            key=f"alis_tarih_{i}",
        )
        alis_tarihleri.append(t)
    with cols[1]:
        miktar_key = f"alis_miktar_{i}"
        m_text = st.text_input(
            f"Alış {i + 1} – Miktar (₺)",
            key=miktar_key,
            placeholder="Örn: 1.250.000",
            on_change=format_binlik_callback,
            args=(miktar_key,),
        )
        alis_miktarlari.append(parse_para(m_text))

st.markdown("---")

# =============================================================================
# UI – Çekilen (Satış) Bölümü
# =============================================================================
st.markdown(
    '<div class="card-box">'
    '<div class="section-header">'
    '<span class="section-icon">📤</span>'
    '<span class="section-label-red">Çekilen (Satış) İşlemleri</span>'
    '</div></div>',
    unsafe_allow_html=True,
)

satis_adet = st.slider(
    "Kaç adet satış (çekme) işleminiz var?",
    min_value=0,
    max_value=30,
    value=0,
    key="satis_slider",
)

satis_tarihleri: list[date | None] = []
satis_miktarlari: list[float | None] = []

if satis_adet == 0:
    st.info("ℹ️ Satış işlemi bulunmuyor. Çekme işleminiz varsa yukarıdaki kaydırıcıyı artırın.")
else:
    for i in range(satis_adet):
        cols = st.columns([1, 1])
        with cols[0]:
            t = st.date_input(
                f"Satış {i + 1} – Tarih",
                value=None,
                min_value=EN_ERKEN_TARIH,
                max_value=EN_GEC_TARIH,
                format="DD.MM.YYYY",
                key=f"satis_tarih_{i}",
            )
            satis_tarihleri.append(t)
        with cols[1]:
            miktar_key = f"satis_miktar_{i}"
            m_text = st.text_input(
                f"Satış {i + 1} – Miktar (₺)",
                key=miktar_key,
                placeholder="Örn: 1.250.000",
                on_change=format_binlik_callback,
                args=(miktar_key,),
            )
            satis_miktarlari.append(parse_para(m_text))

st.markdown("---")

# =============================================================================
# Hesapla Butonu
# =============================================================================
hesapla = st.button("🧮  HESAPLA", use_container_width=True)

if hesapla:
    # ── Doğrulama ────────────────────────────────────────────────────────────
    hatalar: list[str] = []

    for i in range(alis_adet):
        if alis_tarihleri[i] is None:
            hatalar.append(f"⚠️ **Alış** bölümünün **{i + 1}. satırında** tarih bilgisi eksik.")
        if alis_miktarlari[i] is None:
            hatalar.append(f"⚠️ **Alış** bölümünün **{i + 1}. satırında** miktar bilgisi eksik veya geçersiz.")

    for i in range(satis_adet):
        if satis_tarihleri[i] is None:
            hatalar.append(f"⚠️ **Satış** bölümünün **{i + 1}. satırında** tarih bilgisi eksik.")
        if satis_miktarlari[i] is None:
            hatalar.append(f"⚠️ **Satış** bölümünün **{i + 1}. satırında** miktar bilgisi eksik veya geçersiz.")

    if hatalar:
        st.error("### ❌ Eksik Bilgiler Tespit Edildi")
        for h in hatalar:
            st.warning(h)
    else:
        # ── Hesaplama ────────────────────────────────────────────────────────
        alis_detay = []
        toplam_alis_ham = 0.0
        toplam_alis_guncel = 0.0

        for i in range(alis_adet):
            t = alis_tarihleri[i]
            m = alis_miktarlari[i]
            guncel, katsayi = guncelle(m, t, HEDEF_TARIH)
            fark = guncel - m
            alis_detay.append({
                "sira": i + 1,
                "tarih": turkce_tarih(t),
                "ham": m,
                "katsayi": katsayi,
                "guncel": guncel,
                "fark": fark,
            })
            toplam_alis_ham += m
            toplam_alis_guncel += guncel

        satis_detay = []
        toplam_satis_ham = 0.0
        toplam_satis_guncel = 0.0

        for i in range(satis_adet):
            t = satis_tarihleri[i]
            m = satis_miktarlari[i]
            guncel, katsayi = guncelle(m, t, HEDEF_TARIH)
            fark = guncel - m
            satis_detay.append({
                "sira": i + 1,
                "tarih": turkce_tarih(t),
                "ham": m,
                "katsayi": katsayi,
                "guncel": guncel,
                "fark": fark,
            })
            toplam_satis_ham += m
            toplam_satis_guncel += guncel

        net_ham = toplam_alis_ham - toplam_satis_ham
        net_guncel = toplam_alis_guncel - toplam_satis_guncel
        toplam_fark = net_guncel - net_ham

        # ── 1.000.000 TL Limit Kontrolü ─────────────────────────────────────
        limit_asildi = net_guncel > UST_LIMIT

        # ── Sonuçlar ────────────────────────────────────────────────────────
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="result-title">📈 Hesaplama Sonuçları</div>', unsafe_allow_html=True)

        # Sonuçta gösterilecek net güncel tutar (limitli)
        gosterilecek_net = min(net_guncel, UST_LIMIT) if limit_asildi else net_guncel

        # Özet Satırları
        st.markdown(f"""
        <div class="result-row">
            <span class="result-label">Toplam Yatırılan (Ham)</span>
            <span class="result-value">{para_format(toplam_alis_ham)}</span>
        </div>
        <div class="result-row">
            <span class="result-label">Toplam Yatırılan (Güncellenmiş)</span>
            <span class="result-value-green">{para_format(toplam_alis_guncel)}</span>
        </div>
        <div class="result-row">
            <span class="result-label">Toplam Çekilen (Ham)</span>
            <span class="result-value">{para_format(toplam_satis_ham)}</span>
        </div>
        <div class="result-row">
            <span class="result-label">Toplam Çekilen (Güncellenmiş)</span>
            <span class="result-value-red">{para_format(toplam_satis_guncel)}</span>
        </div>
        <div style="height: 1px; background: linear-gradient(90deg, transparent, rgba(102,126,234,0.5), transparent); margin: 1rem 0;"></div>
        <div class="result-row">
            <span class="result-label">Net Fark (Ham)</span>
            <span class="result-value">{para_format(net_ham)}</span>
        </div>
        <div class="result-row">
            <span class="result-label">Net Fark (Güncellenmiş)</span>
            <span class="result-value-gold">{para_format(net_guncel)}</span>
        </div>
        <div class="result-row">
            <span class="result-label">ÜFE+TÜFE Güncelleme Farkı</span>
            <span class="result-value-gold">{para_format(toplam_fark)}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # ── Limit Aşım Uyarısı ──────────────────────────────────────────────
        if limit_asildi:
            st.markdown(f"""
            <div class="limit-card">
                <div class="limit-title">⚠️ ÜST LİMİT AŞILDI</div>
                <div class="limit-text">
                    Hesaplanan güncellenmiş net tutar <strong>{para_format(net_guncel)}</strong> olarak belirlenmiştir.<br>
                    Ancak yasal düzenleme gereği en fazla <strong>1.000.000 ₺</strong> talep edilebilir.
                </div>
                <div class="limit-amount">Alınabilecek Maksimum: 1.000.000,00 ₺</div>
            </div>
            """, unsafe_allow_html=True)

        # ── Detay Tabloları ──────────────────────────────────────────────────
        st.markdown("---")

        col_d1, col_d2 = st.columns(2)

        with col_d1:
            st.markdown(
                '<div class="section-header">'
                '<span class="section-icon">💰</span>'
                '<span class="section-label">Alış Detayları</span>'
                '</div>',
                unsafe_allow_html=True,
            )
            rows_html = ""
            for d in alis_detay:
                rows_html += f"""
                <tr>
                    <td>{d['sira']}</td>
                    <td>{d['tarih']}</td>
                    <td>{para_format(d['ham'])}</td>
                    <td>{d['katsayi']:.6f}</td>
                    <td>{para_format(d['guncel'])}</td>
                    <td style="color:#43e97b; font-weight:600;">+{para_format(d['fark'])}</td>
                </tr>"""
            st.markdown(f"""
            <table class="detail-table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Tarih</th>
                        <th>Ham Tutar</th>
                        <th>Katsayı</th>
                        <th>Güncel Tutar</th>
                        <th>Fark</th>
                    </tr>
                </thead>
                <tbody>{rows_html}</tbody>
            </table>
            """, unsafe_allow_html=True)

        with col_d2:
            if satis_adet > 0:
                st.markdown(
                    '<div class="section-header">'
                    '<span class="section-icon">📤</span>'
                    '<span class="section-label-red">Satış Detayları</span>'
                    '</div>',
                    unsafe_allow_html=True,
                )
                rows_html = ""
                for d in satis_detay:
                    rows_html += f"""
                    <tr>
                        <td>{d['sira']}</td>
                        <td>{d['tarih']}</td>
                        <td>{para_format(d['ham'])}</td>
                        <td>{d['katsayi']:.6f}</td>
                        <td>{para_format(d['guncel'])}</td>
                        <td style="color:#f5576c; font-weight:600;">+{para_format(d['fark'])}</td>
                    </tr>"""
                st.markdown(f"""
                <table class="detail-table">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Tarih</th>
                            <th>Ham Tutar</th>
                            <th>Katsayı</th>
                            <th>Güncel Tutar</th>
                            <th>Fark</th>
                        </tr>
                    </thead>
                    <tbody>{rows_html}</tbody>
                </table>
                """, unsafe_allow_html=True)
            else:
                st.markdown(
                    '<div style="text-align:center; color:#8b8fa3; padding:2rem;">'
                    'Satış işlemi bulunmuyor.</div>',
                    unsafe_allow_html=True,
                )

        # ── Tahmini Alınacak Miktar ──────────────────────────────────────────
        st.markdown("---")
        tahmini_miktar = min(net_guncel, UST_LIMIT) if limit_asildi else net_guncel
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(67,233,123,0.12), rgba(56,249,215,0.12));
            border: 2px solid rgba(67,233,123,0.4);
            border-radius: 20px;
            padding: 2rem;
            text-align: center;
            margin-top: 1rem;
            margin-bottom: 1rem;
        ">
            <div style="color:#a0a4c0; font-size:1rem; font-weight:600; margin-bottom:0.5rem;">
                💎 Alacağınız Tahmini Miktar
            </div>
            <div style="
                font-size: 2.2rem;
                font-weight: 900;
                background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                letter-spacing: -0.5px;
            ">
                {para_format(tahmini_miktar)}
            </div>
            {"<div style='color:#ff8c00; font-size:0.85rem; margin-top:0.5rem; font-weight:500;'>⚠️ Üst limit uygulanmıştır (Maks. 1.000.000 ₺)</div>" if limit_asildi else ""}
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# Footer
# =============================================================================
st.markdown(
    '<div class="footer-text">'
    'Bu hesaplama programı tamamen bireysel imkanlarla yapılmış bir uygulama olup '
    'sonuçların doğruluğu garanti değildir.'
    '</div>',
    unsafe_allow_html=True,
)
