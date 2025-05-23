<!-- 
  ThreadSection 컴포넌트
  역할: 커뮤니티 쓰레드 목록을 섹션 단위로 표시 (인기/팔로우)
  Props:
    - title: String - 섹션 제목 (인기 쓰레드/팔로우 쓰레드)
    - threads: Array - 쓰레드 목록
    - type: String - 섹션 타입 ('popular', 'following')
-->
<template>
  <section class="thread-section">
    <h2>{{ title }}</h2>
    <div class="threads-container">
      <div v-for="thread in threads" :key="thread.id" class="thread-card">
        <h3>{{ thread.title }}</h3>
        <p>{{ thread.content }}</p>
        <div class="thread-info">
          <span>작성자: {{ thread.author }}</span>
          <span>좋아요: {{ thread.likes }}</span>
          <span>댓글: {{ thread.comments }}</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'ThreadSection',
  props: {
    title: {
      type: String,
      required: true
    },
    threads: {
      type: Array,
      required: true
    },
    type: {
      type: String,
      required: true,
      validator: value => ['popular', 'following'].includes(value)
    }
  }
}
</script>

<style scoped>
.thread-section {
  margin: 2rem 0;
}

.threads-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.thread-card {
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.thread-info {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: #666;
}
</style>
