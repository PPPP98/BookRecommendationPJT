<template>
  <div id="app">
    <router-view />
    <TopButton />
  </div>
</template>

<script setup>
import TopButton from '@/components/common/TopButton.vue'
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  font-family: 'Noto Sans KR', sans-serif;
  color: #333;
}

#app {
  min-height: 100vh;
}

a {
  text-decoration: none;
  color: inherit;
}

* {
  box-sizing: border-box;
}

h1, h2, h3, h4, h5, h6, p {
  margin-top: 0;
}

button {
  cursor: pointer;
}
</style>
