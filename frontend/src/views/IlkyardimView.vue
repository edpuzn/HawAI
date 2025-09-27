<template>
  <div class="ilkyardim-container">
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          <span class="hero-icon">🚑</span>
          İlk Yardım Rehberi
        </h1>
        <p class="hero-subtitle">
          Acil durumlarda hayat kurtarıcı bilgiler ve adım adım ilkyardım
          talimatları
        </p>
        <div class="emergency-notice">
          <strong>⚠️ ÖNEMLİ:</strong> Bu bilgiler genel bilgilendirme amaçlıdır.
          Acil durumlarda mutlaka <strong>112</strong>'yi arayın!
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="quick-actions">
      <h2>Hızlı Erişim</h2>
      <div class="action-grid">
        <div class="action-card emergency">
          <div class="action-icon">📞</div>
          <h3>Acil Çağrı</h3>
          <p>112 - Ambulans</p>
          <button class="btn-emergency" @click="callEmergency">
            Hemen Ara
          </button>
        </div>
        <div class="action-card">
          <div class="action-icon">🫁</div>
          <h3>Solunum</h3>
          <p>CPR ve nefes alma teknikleri</p>
          <button class="btn-action" @click="openPopup('solunum')">
            Detaylar
          </button>
        </div>
        <div class="action-card">
          <div class="action-icon">🩸</div>
          <h3>Kanama</h3>
          <p>Kanama kontrolü ve pansuman</p>
          <button class="btn-action" @click="openPopup('kanama')">
            Detaylar
          </button>
        </div>
        <div class="action-card">
          <div class="action-icon">🔥</div>
          <h3>Yanık</h3>
          <p>Yanık tedavisi ve önlemler</p>
          <button class="btn-action" @click="openPopup('yanik')">
            Detaylar
          </button>
        </div>
      </div>
    </div>

    <!-- Common Situations -->
    <div class="common-situations">
      <h2>Sık Karşılaşılan Durumlar</h2>
      <div class="situations-grid">
        <div
          class="situation-card"
          v-for="situation in commonSituations"
          :key="situation.id"
        >
          <div class="situation-header">
            <span class="situation-icon">{{ situation.icon }}</span>
            <h3>{{ situation.title }}</h3>
          </div>
          <p class="situation-description">{{ situation.description }}</p>
          <div class="situation-steps">
            <h4>İlk Adımlar:</h4>
            <ol>
              <li v-for="step in situation.steps" :key="step">{{ step }}</li>
            </ol>
          </div>
        </div>
      </div>
    </div>

    <!-- Emergency Kit -->
    <div class="emergency-kit">
      <h2>İlkyardım Çantası</h2>
      <div class="kit-content">
        <div class="kit-list">
          <h3>Mutlaka Bulunması Gerekenler:</h3>
          <ul>
            <li v-for="item in emergencyKitItems" :key="item">{{ item }}</li>
          </ul>
        </div>
        <div class="kit-tips">
          <h3>💡 İpuçları:</h3>
          <ul>
            <li>İlkyardım çantanızı kolay erişilebilir bir yerde tutun</li>
            <li>İçeriğini düzenli olarak kontrol edin ve yenileyin</li>
            <li>Aile üyelerinize çantanın yerini öğretin</li>
            <li>İlkyardım eğitimi almayı unutmayın</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Disclaimer -->
    <div class="disclaimer">
      <div class="disclaimer-content">
        <h3>⚠️ Yasal Uyarı</h3>
        <p>
          Bu sayfadaki bilgiler genel bilgilendirme amaçlıdır ve profesyonel
          tıbbi tavsiye yerine geçmez. Acil durumlarda mutlaka 112 Acil Çağrı
          Merkezi'ni arayın ve profesyonel yardım alın. İlkyardım uygulamaları
          sadece temel eğitim almış kişiler tarafından yapılmalıdır.
        </p>
      </div>
    </div>

    <!-- Popup Modal -->
    <div v-if="showPopup" class="popup-overlay" @click="closePopup">
      <div class="popup-content" @click.stop>
        <div class="popup-header">
          <h2 class="popup-title">
            <span class="popup-icon">{{ currentPopupData.icon }}</span>
            {{ currentPopupData.title }}
          </h2>
          <button class="popup-close" @click="closePopup">×</button>
        </div>
        <div class="popup-body">
          <div class="popup-section">
            <h3>📋 Genel Bilgi</h3>
            <p>{{ currentPopupData.description }}</p>
          </div>

          <div class="popup-section">
            <h3>🚨 Acil Durum Belirtileri</h3>
            <ul class="symptoms-list">
              <li v-for="symptom in currentPopupData.symptoms" :key="symptom">
                {{ symptom }}
              </li>
            </ul>
          </div>

          <div class="popup-section">
            <h3>📝 İlk Yardım Adımları</h3>
            <ol class="steps-list">
              <li v-for="step in currentPopupData.steps" :key="step">
                {{ step }}
              </li>
            </ol>
          </div>

          <div class="popup-section">
            <h3>⚠️ Dikkat Edilecekler</h3>
            <ul class="warnings-list">
              <li v-for="warning in currentPopupData.warnings" :key="warning">
                {{ warning }}
              </li>
            </ul>
          </div>

          <div class="popup-section emergency-call">
            <h3>📞 Acil Durum</h3>
            <p>
              <strong>Bu durumda mutlaka 112'yi arayın!</strong><br />
              Profesyonel yardım gelene kadar temel ilkyardım uygulayın.
            </p>
            <button class="btn-emergency-popup" @click="callEmergency">
              📞 112'yi Ara
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

// Popup state management
const showPopup = ref(false);
const currentPopupData = ref({
  icon: "",
  title: "",
  description: "",
  symptoms: [],
  steps: [],
  warnings: [],
});

// Popup functions
function openPopup(type: string) {
  showPopup.value = true;
  currentPopupData.value = getPopupData(type);
}

function closePopup() {
  showPopup.value = false;
}

function getPopupData(type: string) {
  const popupData: Record<string, any> = {
    solunum: {
      icon: "🫁",
      title: "Solunum Sorunları ve CPR",
      description:
        "Solunum durması veya nefes alma güçlüğü durumunda uygulanacak temel ilkyardım teknikleri.",
      symptoms: [
        "Nefes alamama veya çok zor nefes alma",
        "Mavi renk değişimi (siyanoz)",
        "Bilinç kaybı",
        "Göğüs hareketlerinin durması",
        "Nabızın zayıflaması veya durması",
      ],
      steps: [
        "Güvenli ortamı sağlayın ve kişiyi sırt üstü yatırın",
        "Solunum yolunu kontrol edin (ağız ve burun)",
        "Yabancı cisim varsa çıkarın",
        "Çene kaldırma manevrası ile solunum yolunu açın",
        "10 saniye boyunca solunumu kontrol edin",
        "Solunum yoksa 30 göğüs kompresyonu yapın",
        "2 kurtarıcı nefes verin",
        "CPR'ı 112 gelene kadar devam ettirin",
      ],
      warnings: [
        "CPR sadece eğitimli kişiler tarafından yapılmalıdır",
        "Göğüs kemiğini kırmamaya dikkat edin",
        "Çok hızlı veya çok yavaş kompresyon yapmayın",
        "Kurtarıcı nefes verirken göğsün yükseldiğini kontrol edin",
      ],
    },
    kanama: {
      icon: "🩸",
      title: "Kanama Kontrolü",
      description:
        "Farklı türdeki kanamaların kontrolü ve durdurulması için temel ilkyardım teknikleri.",
      symptoms: [
        "Açık yaradan kan akışı",
        "Hızlı nabız",
        "Soluk cilt rengi",
        "Soğuk terleme",
        "Baş dönmesi veya bayılma",
      ],
      steps: [
        "Kişiyi oturtun veya yatırın",
        "Kanayan bölgeyi temiz bir bezle kapatın",
        "Doğrudan baskı uygulayın",
        "Yarayı kalp seviyesinden yukarıda tutun",
        "Kanama durmazsa daha fazla baskı uygulayın",
        "Turnike uygulayın (sadece şiddetli kanamalarda)",
        "112'yi arayın ve profesyonel yardım isteyin",
      ],
      warnings: [
        "Kanayan bölgeye doğrudan dokunmayın",
        "Yaradan çıkan nesneleri çıkarmayın",
        "Turnikeyi çok sıkı bağlamayın",
        "Kanama kontrol edilene kadar baskıyı bırakmayın",
      ],
    },
    yanik: {
      icon: "🔥",
      title: "Yanık Tedavisi",
      description:
        "Farklı derecelerdeki yanıkların ilk müdahalesi ve tedavi süreci.",
      symptoms: [
        "Kızarıklık ve ağrı (1. derece)",
        "Kabarcık oluşumu (2. derece)",
        "Derin doku hasarı (3. derece)",
        "Şok belirtileri",
        "Nefes alma güçlüğü (solunum yolu yanığı)",
      ],
      steps: [
        "Yanık bölgesini soğuk suyla 10-15 dakika yıkayın",
        "Yanık bölgesindeki takıları çıkarın",
        "Temiz, nemli bezle örtün",
        "Kabarcıkları patlatmayın",
        "Yanık kremi veya merhem sürmeyin",
        "Şok belirtileri varsa kişiyi yatırın",
        "112'yi arayın (ciddi yanıklarda)",
      ],
      warnings: [
        "Buz kullanmayın (daha fazla hasar verebilir)",
        "Yanık bölgesine yağ, tereyağı sürmeyin",
        "Kabarcıkları patlatmayın",
        "Yanık bölgesini sıkıca sarmayın",
        "Çocuklarda ve yaşlılarda daha dikkatli olun",
      ],
    },
  };

  return popupData[type] || popupData.solunum;
}

// Acil durum çağrısı
function callEmergency() {
  if (
    confirm("112 Acil Çağrı Merkezi'ni aramak istediğinizden emin misiniz?")
  ) {
    window.location.href = "tel:112";
  }
}

// Sık karşılaşılan durumlar
const commonSituations = ref([
  {
    id: 1,
    icon: "🤕",
    title: "Bilinç Kaybı",
    description: "Kişi bilincini kaybettiğinde yapılması gerekenler",
    steps: [
      "Güvenli bir ortama taşıyın",
      "Solunum yolunu kontrol edin",
      "Nabzı kontrol edin",
      "112'yi arayın",
      "CPR uygulayın (eğitimliyseniz)",
    ],
  },
  {
    id: 2,
    icon: "🫀",
    title: "Kalp Krizi",
    description: "Kalp krizi belirtileri ve ilk müdahale",
    steps: [
      "Belirtileri tanıyın (göğüs ağrısı, nefes darlığı)",
      "Kişiyi rahat pozisyona alın",
      "112'yi hemen arayın",
      "Aspirin verin (alerjisi yoksa)",
      "CPR hazırlığı yapın",
    ],
  },
  {
    id: 3,
    icon: "🍯",
    title: "Boğulma",
    description: "Solunum yolunda tıkanma durumu",
    steps: [
      "Kişinin öksürmesini teşvik edin",
      "Heimlich manevrası uygulayın",
      "112'yi arayın",
      "CPR'a hazırlanın",
      "Nesneyi çıkarmaya çalışın",
    ],
  },
  {
    id: 4,
    icon: "⚡",
    title: "Elektrik Çarpması",
    description: "Elektrik çarpması durumunda ilk müdahale",
    steps: [
      "Elektrik kaynağını kesin",
      "Kişiye dokunmayın",
      "112'yi arayın",
      "Güvenli mesafede kalın",
      "CPR uygulayın (gerekirse)",
    ],
  },
]);

// İlkyardım çantası malzemeleri
const emergencyKitItems = ref([
  "Steril gazlı bez",
  "Bandaj ve elastik bandaj",
  "Antiseptik solüsyon",
  "Makas",
  "Cımbız",
  "Termometre",
  "Ağrı kesici",
  "Soğuk kompres",
  "İlkyardım el kitabı",
  "Telefon numaraları listesi",
]);
</script>

<style scoped>
/* Dark mode için özel değişkenler */
:root[data-theme="dark"] {
  --emergency-bg: rgba(239, 68, 68, 0.15);
  --emergency-border: rgba(239, 68, 68, 0.4);
  --warning-bg: rgba(255, 193, 7, 0.15);
  --warning-border: rgba(255, 193, 7, 0.4);
  --warning-text: #ffffff;
  --popup-text: #ffffff;
  --popup-text-secondary: #e5e7eb;
  --dark-green-bg: linear-gradient(135deg, #064e3b, #065f46);
  --dark-green-border: rgba(6, 78, 59, 0.3);
}

:root[data-theme="light"] {
  --emergency-bg: rgba(239, 68, 68, 0.05);
  --emergency-border: rgba(239, 68, 68, 0.2);
  --warning-bg: rgba(255, 193, 7, 0.1);
  --warning-border: rgba(255, 193, 7, 0.3);
  --warning-text: #0f172a;
  --popup-text: #0f172a;
  --popup-text-secondary: #475569;
  --dark-green-bg: linear-gradient(135deg, #064e3b, #065f46);
  --dark-green-border: rgba(6, 78, 59, 0.3);
}

.ilkyardim-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* Hero Section */
.hero-section {
  text-align: center;
  padding: 60px 20px;
  background: var(--dark-green-bg);
  border-radius: 20px;
  margin-bottom: 40px;
  border: 1px solid var(--dark-green-border);
}

.hero-title {
  font-size: 3rem;
  font-weight: 800;
  color: #f00404;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.hero-icon {
  font-size: 3.5rem;
}

.hero-subtitle {
  font-size: 1.2rem;
  color: rgba(196, 25, 25, 0.9);
  margin-bottom: 30px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.emergency-notice {
  background: var(--warning-bg);
  border: 1px solid var(--warning-border);
  border-radius: 12px;
  padding: 20px;
  color: var(--warning-text);
  font-size: 1rem;
  max-width: 500px;
  margin: 0 auto;
}

/* Quick Actions */
.quick-actions {
  margin-bottom: 50px;
}

.quick-actions h2 {
  text-align: center;
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-900);
  margin-bottom: 40px;
}

.action-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 25px;
  margin-bottom: 40px;
}

.action-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 30px;
  text-align: center;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-sm);
}

.action-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-lg);
}

.action-card.emergency {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  border: 1px solid var(--emergency-border);
}

.action-icon {
  font-size: 3rem;
  margin-bottom: 20px;
}

.action-card h3 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 10px;
  color: inherit;
}

.action-card p {
  color: var(--text-600);
  margin-bottom: 20px;
}

.action-card.emergency p {
  color: rgba(255, 255, 255, 0.9);
}

.btn-emergency {
  background: rgba(255, 255, 255, 0.9);
  color: #dc2626;
  border: none;
  padding: 12px 24px;
  border-radius: 25px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-emergency:hover {
  background: rgba(255, 255, 255, 1);
  transform: scale(1.05);
}

.btn-action {
  display: inline-block;
  background: var(--brand-600);
  color: white;
  text-decoration: none;
  padding: 12px 24px;
  border-radius: 25px;
  font-weight: 600;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
}

.btn-action:hover {
  background: var(--brand-700);
  transform: scale(1.05);
}

/* Common Situations */
.common-situations {
  margin-bottom: 50px;
}

.common-situations h2 {
  text-align: center;
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-900);
  margin-bottom: 40px;
}

.situations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 25px;
}

.situation-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 25px;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-sm);
}

.situation-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}

.situation-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
}

.situation-icon {
  font-size: 2rem;
}

.situation-header h3 {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--text-900);
  margin: 0;
}

.situation-description {
  color: var(--text-600);
  margin-bottom: 20px;
  line-height: 1.6;
}

.situation-steps h4 {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-900);
  margin-bottom: 10px;
}

.situation-steps ol {
  margin: 0;
  padding-left: 20px;
}

.situation-steps li {
  color: var(--text-600);
  margin-bottom: 8px;
  line-height: 1.5;
}

/* Emergency Kit */
.emergency-kit {
  margin-bottom: 50px;
}

.emergency-kit h2 {
  text-align: center;
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-900);
  margin-bottom: 40px;
}

.kit-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 40px;
}

.kit-list h3,
.kit-tips h3 {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--text-900);
  margin-bottom: 20px;
}

.kit-list ul,
.kit-tips ul {
  list-style: none;
  padding: 0;
}

.kit-list li,
.kit-tips li {
  color: var(--text-600);
  margin-bottom: 10px;
  padding-left: 20px;
  position: relative;
  line-height: 1.6;
}

.kit-list li::before {
  content: "✓";
  position: absolute;
  left: 0;
  color: var(--brand-600);
  font-weight: bold;
}

.kit-tips li::before {
  content: "💡";
  position: absolute;
  left: 0;
}

/* Disclaimer */
.disclaimer {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 30px;
  margin-top: 40px;
}

.disclaimer-content h3 {
  color: #ef4444;
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 15px;
}

.disclaimer-content p {
  color: var(--popup-text-secondary);
  line-height: 1.6;
  margin: 0;
}

/* Popup Styles */
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(8px);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  animation: fadeIn 0.3s ease;
}

.popup-content {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 20px;
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-xl);
  animation: slideIn 0.3s ease;
}

.popup-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 25px 30px;
  border-bottom: 1px solid var(--dark-green-border);
  background: var(--dark-green-bg);
  border-radius: 20px 20px 0 0;
}

.popup-title {
  display: flex;
  align-items: center;
  gap: 15px;
  font-size: 1.8rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0;
}

.popup-icon {
  font-size: 2rem;
}

.popup-close {
  background: none;
  border: none;
  font-size: 2rem;
  color: rgba(255, 255, 255, 0.8);
  cursor: pointer;
  padding: 5px 10px;
  border-radius: 50%;
  transition: all 0.2s ease;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.popup-close:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

.popup-body {
  padding: 30px;
}

.popup-section {
  margin-bottom: 30px;
}

.popup-section h3 {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--popup-text);
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.popup-section p {
  color: var(--popup-text-secondary);
  line-height: 1.6;
  margin-bottom: 15px;
}

.symptoms-list,
.warnings-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.symptoms-list li,
.warnings-list li {
  color: var(--popup-text-secondary);
  margin-bottom: 10px;
  padding-left: 25px;
  position: relative;
  line-height: 1.5;
}

.symptoms-list li::before {
  content: "🔍";
  position: absolute;
  left: 0;
  top: 0;
}

.warnings-list li::before {
  content: "⚠️";
  position: absolute;
  left: 0;
  top: 0;
}

.steps-list {
  margin: 0;
  padding-left: 20px;
}

.steps-list li {
  color: var(--popup-text-secondary);
  margin-bottom: 12px;
  line-height: 1.6;
  padding-left: 5px;
}

.emergency-call {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  padding: 25px;
  border-radius: 16px;
  margin-top: 20px;
  border: 1px solid var(--emergency-border);
}

.emergency-call h3 {
  color: white;
  margin-bottom: 15px;
}

.emergency-call p {
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 20px;
}

.btn-emergency-popup {
  background: rgba(255, 255, 255, 0.9);
  color: #dc2626;
  border: none;
  padding: 12px 24px;
  border-radius: 25px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
}

.btn-emergency-popup:hover {
  background: rgba(255, 255, 255, 1);
  transform: scale(1.05);
}

/* Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-50px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
    flex-direction: column;
    gap: 10px;
  }

  .hero-icon {
    font-size: 2.5rem;
  }

  .action-grid {
    grid-template-columns: 1fr;
  }

  .situations-grid {
    grid-template-columns: 1fr;
  }

  .kit-content {
    grid-template-columns: 1fr;
    gap: 30px;
  }

  .ilkyardim-container {
    padding: 15px;
  }

  /* Popup responsive */
  .popup-overlay {
    padding: 10px;
  }

  .popup-content {
    max-height: 95vh;
  }

  .popup-header {
    padding: 20px;
  }

  .popup-title {
    font-size: 1.5rem;
  }

  .popup-body {
    padding: 20px;
  }

  .popup-section {
    margin-bottom: 25px;
  }

  .popup-section h3 {
    font-size: 1.2rem;
  }
}
</style>
