<template>
  <button
    v-show="visible"
    @click="scrollToTop"
    class="top-btn"
    aria-label="맨 위로"
  >
    ▲
  </button>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const visible = ref(false)

function onScroll() {
  visible.value = window.scrollY > 200
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => {
  window.addEventListener('scroll', onScroll)
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', onScroll)
})
</script>

<style scoped>
.top-btn {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  z-index: 999;
  background: #222;
  color: #fff;
  border: none;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  font-size: 1.3rem;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  opacity: 0.7;
  transition: opacity 0.2s, background 0.2s;
}
.top-btn:hover {
  opacity: 1;
  background: #444;
}
</style>
