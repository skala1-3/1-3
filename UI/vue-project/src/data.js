// src/data.js

export const esgData = {
  companyName: "Sample Tech Inc.",
  reportingPeriod: "2024",
  totalEmissions: {
    scope1: 5500,
    scope2: 8000,
    scope3: 15000,
    unit: "tCO2e",
  },
  emissionsBreakdown: [
    { year: 2022, scope1: 4500, scope2: 7500, scope3: 12000 },
    { year: 2023, scope1: 5000, scope2: 7800, scope3: 14000 },
    { year: 2024, scope1: 5500, scope2: 8000, scope3: 15000 },
  ],
  scope3Details: {
    upstream: [
      { category: "구매 상품", emissions: 6000 },
      { category: "출장", emissions: 1500 },
      { category: "직원 통근", emissions: 800 },
    ],
    downstream: [
      { category: "판매 제품 사용", emissions: 4000 },
      { category: "판매 제품 폐기", "emissions": 1200 },
    ],
  },

  suppliers: [
    {
      id: "SUP-001",
      name: "Hanil Precision",
      country: "KR",
      industry: "Machining",
      overall_grade: "B",
      scores: { E: 62, S: 78, G: 55 },
      risk_tags: ["Scope2-missing", "No-ISO14001"],
      evidence: {
        policy: [{ title: "환경방침", status: "present", date: "2025-07-10" }],
        action: [{ title: "안전교육 분기 시행", status: "present", date: "2025-09-01" }],
        kpi: [{ title: "연간 전력원단위", status: "missing" }],
      },
      last_updated: "2025-09-15",
      audit: { updated_by: "demo_admin", version: "0.2" },
    },
    {
      id: "SUP-002",
      name: "Daemyung Plastics",
      country: "VN",
      industry: "Injection",
      overall_grade: "C",
      scores: { E: 40, S: 65, G: 60 },
      risk_tags: ["Labor-Training-Overdue"],
      evidence: {
        policy: [{ title: "윤리규정", status: "present", date: "2025-08-21" }],
        action: [{ title: "폐기물 위탁계약서", status: "present", date: "2025-06-02" }],
        kpi: [{ title: "Scope1/2 집계표", status: "present", date: "2025-09-10" }],
      },
      last_updated: "2025-09-18",
      audit: { updated_by: "demo_admin", version: "0.2" },
    },
    // ... 더 많은 목 데이터 추가 ...
  ],
  framework_ref: {
    env: "ESRS E1 (summary)",
    social: "GRI 403/408 (summary)",
    governance: "IFRS S1 Governance (summary)",
  },
};