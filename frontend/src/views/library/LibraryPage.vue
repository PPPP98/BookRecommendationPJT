<!-- 
  LibraryPage 컴포넌트
  역할: 도서관 위치와 실시간 이용 현황을 보여주는 페이지
  기능:
    - 도서관 목록 표시
    - 지도에 도서관 위치 표시
    - 도서관별 실시간 이용 현황 확인
  데이터 구조:
    - libraries: Array<{
        id: number,
        name: string,
        address: string,
        coordinates: { lat: number, lng: number },
        currentVisitors: number,
        maxCapacity: number,
        operatingHours: string,
        distance: number,
        tel: string
      }>
-->
<template>
  <div class="library-page">
    <Navbar />
    
    <main class="main-content">
      <h1>주변 도서관</h1>

      <LibraryMap 
        :libraries="libraries" 
        :currentLocation="currentLocation"
      />
    </main>

    <Footer />
  </div>
</template>

<script>
import { libraries } from '@/mocks/libraries'
import Navbar from '@/components/common/Navbar.vue'
import Footer from '@/components/common/Footer.vue'
import LibraryMap from '@/components/library/LibraryMap.vue'

export default {
  name: 'LibraryPage',
  components: {
    Navbar,
    Footer,
    LibraryMap
  },
  data() {
    return {
      libraries: libraries,
      currentLocation: {
        lat: 37.5012,
        lng: 127.0396
      }
    }
  }
}
</script>

<style scoped>
.library-page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  margin-bottom: 2rem;
}
</style>
