<template>
  <div class="background-image">
    <!-- 배경 이미지 -->
    <div class="overlay"></div> <!-- 반투명 회색 필터 오버레이 -->
  </div>
</template>

<script setup>
// 심플한 배경 이미지 컴포넌트
</script>

<style scoped>
.background-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('/MainImage.jpg');
  background-size: cover;
  background-position: center;
  z-index: 1;
}

/* 반투명 회색 필터 오버레이 */
.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4); /* 검은색 반투명 필터 (40% 투명도) */
  z-index: 2;
}

@media (max-width: 1024px) {
  .background-image {
    width: 100%;
  }
}

@media (max-width: 768px) {
  .background-image {
    width: 100%;
    height: 100%;
  }
}
</style>
