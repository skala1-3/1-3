<script setup>
import { ref, computed } from 'vue';
import { esgData } from './data';
import ScopePieChart from './components/ScopePieChart.vue';
import EmissionsLineChart from './components/EmissionsLineChart.vue';

const { companyName, totalEmissions, emissionsBreakdown, scope3Details } = esgData;

const total =
  totalEmissions.scope1 + totalEmissions.scope2 + totalEmissions.scope3;

// SVG 아이콘은 템플릿에서 직접 사용하기 위해 문자열로 정의
const Icons = {
  Total: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M12 8v4l3 3"></path></svg>`,
  Scope1: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20M17 5H7l5 5L7 15h10"></path></svg>`,
  Scope2: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2h8v20h-8M17 10h-4M17 14h-4"></path></svg>`,
  Scope3: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 21V3M14 3v18M18 6h-8M6 18h8"></path></svg>`,
};
const viewMode = ref('grid');
const selectedSupplier = ref(null);
const filteredSuppliers = computed(() => {
  // 실제 필터링 로직 구현 (필터 상태에 따라 suppliers 배열 필터링)
  // 현재는 전체를 반환
  return esgData.suppliers;
});

const overallCount = computed(() => esgData.suppliers.length);
const verifiedCount = computed(() => esgData.suppliers.filter(s => getEvidenceStatus(s) === 'present').length);
const requestedCount = computed(() => 0); // 실제 로직 필요
const overdueCount = computed(() => 0); // 실제 로직 필요
const getGradeClass = (grade) => {
  const gradeMap = {
    'A': 'grade-A',
    'B': 'grade-B',
    'C': 'grade-C',
    'D': 'grade-D',
  };
  return gradeMap[grade];
};

const getEvidenceStatus = (supplier) => {
  // 증빙 상태를 종합적으로 판단하는 로직
  const evidences = [...supplier.evidence.policy, ...supplier.evidence.action, ...supplier.evidence.kpi];
  if (evidences.some(e => e.status === 'missing')) return 'missing';
  if (evidences.some(e => e.status === 'overdue')) return 'overdue';
  return 'present';
};

const selectSupplier = (supplier) => {
  selectedSupplier.value = supplier;
};

const closePanel = () => {
  selectedSupplier.value = null;
};
/*
업로드된 파일의 이름을 표시하고, 목(Mock) JSON 데이터를 미리보기 영역에 보여주는 로직을 추가합니다.
실제 파일 분석 로직은 아직 없으므로, 파일이 선택되면 미리 정의된 JSON 문자열을 표시하도록 구현합니다.
*/
const fileInput = ref(null);
const fileName = ref('');
const mockJsonData = {
  regulation: "ESRS E1",
  spec_version: "1.0.0",
  fields: [
    { id: "E1-1", name: "환경 목표", status: "complete" },
    { id: "E1-2", name: "기후변화 전환 계획", status: "pending" },
    { id: "E1-3", name: "에너지 소비량", status: "missing" },
  ]
};
const formattedJson = computed(() => {
  return JSON.stringify(mockJsonData, null, 2);
});

const openFilePicker = () => {
  fileInput.value.click();
};

const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    fileName.value = file.name;
    // 실제 API 연동 대신 목업 데이터로 JSON 미리보기 업데이트
    // 이 부분에서 향후 실제 파일 분석 로직을 추가할 수 있습니다.
  }
};
</script>

<template>
  <transition name="slide-fade">
        <div v-if="selectedSupplier" class="supplier-detail-panel">
          <div class="panel-header">
            <h3>{{ selectedSupplier.name }}</h3>
            <button @click="closePanel">X</button>
          </div>
          <div class="panel-section">
            <p>국가: {{ selectedSupplier.country }} | 업종: {{ selectedSupplier.industry }}</p>
          </div>
          <div class="panel-section">
            <h4>스코어링</h4>
            <div class="score-bars">
              <div class="score-bar">
                <span>E: {{ selectedSupplier.scores.E }}</span>
                <div class="bar-fill" :style="{ width: `${selectedSupplier.scores.E}%` }"></div>
              </div>
              </div>
          </div>
          <div class="panel-section">
            <h4>증빙 목록</h4>
            <div v-for="evidence in selectedSupplier.evidence.policy" :key="evidence.title">
                {{ evidence.title }} ({{ evidence.status }})
            </div>
          </div>
          <div class="panel-section">
            <h4>근거</h4>
            <p>참조 프레임워크: {{ esgData.framework_ref.env }}</p>
            <p>신뢰도: <span class="badge">SELF-DECLARED</span></p>
          </div>
        </div>
      </transition>
  <div class="main-dashboard-wrapper">
    <div class="watermark">DEMO / INTERNAL USE ONLY</div>
    <!-- 상단 바 -->
    <div class="top-bar-card">
      <header class="top-bar">
        <div class="left-section">
          <span>사업장/기간 선택</span>
          </div>
        <div class="right-section">
          <span class="notification-badge">3</span> 알림
        </div>
      </header>
    </div>
    <!-- 메인 콘텐츠 영역: 좌측 목록과 우측 대시보드 -->
    <div class="content-wrapper">
      <div class="supplier-list-section">
        <div class="supplier-map-card">
          <div class="section-header">
            <h2>협력사 ESG 맵</h2>
            <div class="view-toggle">
              <button @click="viewMode = 'grid'">그리드</button>
              <button @click="viewMode = 'table'">테이블</button>
            </div>
          </div>

          <div class="filter-bar">
            <div class="kpi-chips">
              <span class="kpi-chip">전체 {{ overallCount }}개</span>
              <span class="kpi-chip">증빙완료 {{ verifiedCount }}개</span>
              <span class="kpi-chip">개선요청 {{ requestedCount }}개</span>
              <span class="kpi-chip overdue">과기한 {{ overdueCount }}개</span>
            </div>
          </div>

          <div class="supplier-list-container">
            <div v-if="viewMode === 'grid'" class="supplier-grid">
              <div
                v-for="supplier in filteredSuppliers"
                :key="supplier.id"
                class="supplier-card"
                @click="selectSupplier(supplier)"
              >
                <div class="card-header">
                  <span class="grade-label" :class="getGradeClass(supplier.overall_grade)">
                    {{ supplier.overall_grade }}
                  </span>
                  <span class="name">{{ supplier.name }}</span>
                </div>
                <div class="card-body">
                  <div class="score-item">E: {{ supplier.scores.E }}</div>
                  <div class="score-item">S: {{ supplier.scores.S }}</div>
                  <div class="score-item">G: {{ supplier.scores.G }}</div>
                </div>
                <div class="card-footer">
                  <span class="evidence-status-icon">
                    <span v-if="getEvidenceStatus(supplier) === 'present'">✅</span>
                    <span v-else>❗</span>
                  </span>
                  <span class="last-updated">업데이트: {{ supplier.last_updated }}</span>
                </div>
                <div class="risk-tags">
                  <span
                    v-for="tag in supplier.risk_tags"
                    :key="tag"
                    class="risk-tag"
                  >{{ tag }}</span>
                </div>
              </div>
            </div>

            </div>
        </div>

        <div class="supplier-list-placeholder">
          <div class="regulation-autocomplete-ui">
            <h2>규제 스펙 자동 완성</h2>
            <p class="description">파일을 업로드하면, JSON 데이터가 자동으로 채워집니다.</p>

            <div class="upload-area">
              <input type="file" ref="fileInput" @change="handleFileChange" style="display: none;">
              <button @click="openFilePicker">파일 업로드</button>
              <span v-if="fileName">{{ fileName }}</span>
            </div>

            <div class="json-preview-container">
              <h3>미리보기</h3>
              <pre>{{ formattedJson }}</pre>
            </div>
         </div>
        </div>
      </div>

      
    </div>
  </div>
  <div class="dashboard-container">
    <header class="dashboard-header">
      <h1>{{ companyName }} ESG 대시보드</h1>
      <p>보고 기간: {{ esgData.reportingPeriod }}</p>
    </header>
  
    <div class="dashboard-content-main">
      <section class="summary-section">
        <h2>총 배출량 요약</h2>
        <div class="summary-cards">
          <div class="card">
            <h3>총량</h3>
            <p class="value">
              {{ total.toLocaleString() }} {{ totalEmissions.unit }}
            </p>
          </div>
          <div class="card">
            <h3>Scope 1</h3>
            <p class="value">
              {{ totalEmissions.scope1.toLocaleString() }} {{ totalEmissions.unit }}
            </p>
          </div>
          <div class="card">
            <h3>Scope 2</h3>
            <p class="value">
              {{ totalEmissions.scope2.toLocaleString() }} {{ totalEmissions.unit }}
            </p>
          </div>
          <div class="card">
            <h3>Scope 3</h3>
            <p class="value">
              {{ totalEmissions.scope3.toLocaleString() }} {{ totalEmissions.unit }}
            </p>
          </div>
        </div>
      </section>
      
      <div class="charts-and-table-section">
        <section class="charts-section">
          <h2>전체 배출량 비중</h2>
          <div class="chart-wrapper">
            <ScopePieChart :data="totalEmissions" />
          </div>
          <div class="chart-wrapper-emissions" style="height: 300px; width: 400px;">
            <EmissionsLineChart :data="emissionsBreakdown" />
          </div>
        </section>

        <section class="details-section">
          <h2>Scope 3 세부 배출량</h2>
          <div class="scope3-table-container" style="height: 200px; width: 250px;">
            <table>
              <thead>
                <tr>
                  <th>범주</th>
                  <th>배출량 ({{ totalEmissions.unit }})</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td colspan="2" class="category-header">Upstream 활동</td>
                </tr>
                <tr v-for="(item, index) in scope3Details.upstream" :key="`up-${index}`">
                  <td>{{ item.category }}</td>
                  <td>{{ item.emissions.toLocaleString() }}</td>
                </tr>
                <tr>
                  <td colspan="2" class="category-header">Downstream 활동</td>
                </tr>
                <tr v-for="(item, index) in scope3Details.downstream" :key="`down-${index}`">
                  <td>{{ item.category }}</td>
                  <td>{{ item.emissions.toLocaleString() }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<style>
/* src/App.vue에 CSS를 직접 추가하거나, App.css 파일을 import할 수 있습니다. */
/* 여기에 @import 규칙을 사용하여 CSS 파일을 불러옵니다.
  'scoped' 속성을 제거하여 전역 스타일로 적용합니다.
*/
@import url('@/assets/styles/App.css');

</style>