# Live Demo

Mock 데이터 기반으로 동작하는 데모 앱입니다.

<div style="margin-top: 1rem;">
  <a href="../app/" target="_blank" class="md-button md-button--primary">
    데모 앱 열기 →
  </a>
</div>

<div style="margin-top: 2rem;">
  <iframe
    src="../app/"
    width="100%"
    height="700"
    style="border: 1px solid #e0e0e0; border-radius: 8px;"
    loading="lazy"
  ></iframe>
</div>

---

## 데모 사용 방법

1. **출발지 선택** — 인천 주변 zone 중 하나를 선택
2. **터미널 선택** — 인천항 내 터미널 선택
3. **Cut-off 시간 설정** — gate-in cut-off 시간 입력
4. **평가 실행** — "Evaluate Risk" 버튼 클릭
5. **결과 확인** — 리스크 점수, 확률, 최적 출발 시각, 원인 분석 확인
6. **시뮬레이션** — 다양한 출발 시각에 대한 what-if 비교

!!! info "Demo Mode"
    이 데모는 실제 API 없이 클라이언트 사이드 mock 엔진으로 동작합니다.
    실제 서비스는 Docker Compose로 실행해주세요.
