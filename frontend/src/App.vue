<template>
  <div id="app">
    <navbar class="navbar-fixed" />
    <div class="main-content">
      <router-view />
    </div>
    <TopButton />
  </div>
</template>

<script setup>
import TopButton from '@/components/common/TopButton.vue'
import Navbar from '@/components/common/Navbar.vue'
</script>

<style>
/* CSS 변수 정의 */
:root {
  --navbar-height: 64px;
}

html, body {
  margin: 0;
  padding: 0;
  font-family: 'Noto Sans KR', sans-serif;
  color: #333;
  height: 100%;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  position: relative;
}

.navbar-fixed {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: var(--navbar-height);
  z-index: 1000;
  background: #fff;
  border-bottom: 1px solid #ececec;
}

.main-content {
  flex: 1;
  margin-top: var(--navbar-height);
  width: 100%;
  position: relative;
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
