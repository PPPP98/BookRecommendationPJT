<!-- 
  LibraryMap 컴포넌트
  역할: 내 위치 기반 도서관 목록 및 지도 표시
  Props:
    - libraries: Array - 도서관 목록
    - currentLocation: Object - 현재 위치 좌표
  기능:
    - 도서관 목록 표시 (거리순 정렬)
    - 지도에 도서관 위치 표시
    - 도서관 상세 정보 표시
-->
<template>
  <div class="library-map">
    <!-- 도서관 목록 -->
    <div class="library-list">
      <div class="list-header">
        <h2>주변 도서관</h2>
        <div class="filters">
          <select v-model="sortBy" class="sort-select">
            <option value="distance">거리순</option>
            <option value="capacity">여유순</option>
            <option value="name">이름순</option>
          </select>
        </div>
      </div>

      <div class="list-content">
        <div 
          v-for="library in sortedLibraries" 
          :key="library.id"
          class="library-item"
          :class="{ active: selectedLibrary?.id === library.id }"
          @click="selectLibrary(library)"
        >
          <div class="library-info">
            <h3>{{ library.name }}</h3>
            <p class="address">{{ library.address }}</p>
            <div class="meta-info">
              <span class="distance">{{ library.distance }}km</span>
              <span class="capacity">
                현재 {{ library.currentVisitors }}/{{ library.maxCapacity }}명
              </span>
            </div>
          </div>
          <div class="library-status">
            <div class="status-indicator" :class="getCapacityClass(library)">
              {{ getCapacityText(library) }}
            </div>
            <p class="hours">{{ library.operatingHours }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 지도 영역 -->
    <div class="map-container">
      <!-- 실제 구현 시에는 카카오맵 또는 구글맵 API 사용 -->
      <div class="mock-map">
        <div class="map-center">현재 위치</div>
        <div 
          v-for="library in libraries"
          :key="library.id"
          class="map-marker"
          :class="{ active: selectedLibrary?.id === library.id }"          :style="{
              left: `${library.coordinates.lng * 100}px`,
              top: `${library.coordinates.lat * 100}px`
            }"
          @click="selectLibrary(library)"
        >
          📍
        </div>
      </div>

      <!-- 선택된 도서관 상세 정보 -->
      <div v-if="selectedLibrary" class="library-detail">
        <h3>{{ selectedLibrary.name }}</h3>
        <p>{{ selectedLibrary.address }}</p>
        <p>전화: {{ selectedLibrary.tel }}</p>
        <p>운영시간: {{ selectedLibrary.operatingHours }}</p>
        <div class="capacity-info">
          <div class="capacity-bar">
            <div 
              class="capacity-fill"              :style="{
                width: `${(selectedLibrary.currentVisitors / selectedLibrary.maxCapacity) * 100}%`
              }"
              :class="getCapacityClass(selectedLibrary)"
            ></div>
          </div>
          <p>현재 {{ selectedLibrary.currentVisitors }}명 / 최대 {{ selectedLibrary.maxCapacity }}명</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LibraryMap',
  props: {
    libraries: {
      type: Array,
      required: true
    },
    currentLocation: {
      type: Object,
      default: () => ({
        lat: 37.5012,
        lng: 127.0396
      })
    }
  },
  data() {
    return {
      selectedLibrary: null,
      sortBy: 'distance'
    }
  },
  computed: {
    sortedLibraries() {
      return [...this.libraries].sort((a, b) => {
        switch (this.sortBy) {
          case 'distance':
            return a.distance - b.distance
          case 'capacity':
            return (a.currentVisitors / a.maxCapacity) - (b.currentVisitors / b.maxCapacity)
          case 'name':
            return a.name.localeCompare(b.name)
          default:
            return 0
        }
      })
    }
  },
  methods: {
    selectLibrary(library) {
      this.selectedLibrary = library
    },
    getCapacityClass(library) {
      const ratio = library.currentVisitors / library.maxCapacity
      if (ratio < 0.5) return 'low'
      if (ratio < 0.8) return 'medium'
      return 'high'
    },
    getCapacityText(library) {
      const ratio = library.currentVisitors / library.maxCapacity
      if (ratio < 0.5) return '여유'
      if (ratio < 0.8) return '보통'
      return '혼잡'
    }
  }
}
</script>

<style scoped>
.library-map {
  display: grid;
  grid-template-columns: 350px 1fr;
  gap: 2rem;
  height: 600px;
}

.library-list {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.list-header {
  padding: 1rem;
  border-bottom: 1px solid #ddd;
  background: #f5f5f5;
}

.list-content {
  flex: 1;
  overflow-y: auto;
}

.library-item {
  padding: 1rem;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
}

.library-item:hover {
  background: #f5f5f5;
}

.library-item.active {
  background: #e3f2fd;
}

.library-info h3 {
  margin: 0 0 0.5rem 0;
}

.address {
  color: #666;
  font-size: 0.9rem;
  margin: 0.25rem 0;
}

.meta-info {
  display: flex;
  gap: 1rem;
  font-size: 0.9rem;
  color: #666;
}

.library-status {
  text-align: right;
}

.status-indicator {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.9rem;
  font-weight: 500;
}

.status-indicator.low {
  background: #d4edda;
  color: #155724;
}

.status-indicator.medium {
  background: #fff3cd;
  color: #856404;
}

.status-indicator.high {
  background: #f8d7da;
  color: #721c24;
}

.hours {
  font-size: 0.9rem;
  color: #666;
  margin-top: 0.25rem;
}

.map-container {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
}

.mock-map {
  height: 100%;
  background: #f5f5f5;
  position: relative;
}

.map-center {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  padding: 0.5rem;
  background: #0066cc;
  color: white;
  border-radius: 4px;
}

.map-marker {
  position: absolute;
  transform: translate(-50%, -50%);
  font-size: 2rem;
  cursor: pointer;
}

.map-marker.active {
  color: #0066cc;
  transform: translate(-50%, -50%) scale(1.2);
}

.library-detail {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 1rem;
  background: white;
  border-top: 1px solid #ddd;
}

.capacity-bar {
  height: 8px;
  background: #eee;
  border-radius: 4px;
  overflow: hidden;
  margin: 0.5rem 0;
}

.capacity-fill {
  height: 100%;
  transition: width 0.3s ease;
}

.capacity-fill.low {
  background: #28a745;
}

.capacity-fill.medium {
  background: #ffc107;
}

.capacity-fill.high {
  background: #dc3545;
}

@media (max-width: 768px) {
  .library-map {
    grid-template-columns: 1fr;
  }
}
</style>
