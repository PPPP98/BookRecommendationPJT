<!-- 
  ThreadCard 컴포넌트
  역할: 커뮤니티 쓰레드 정보를 카드 형태로 표시
  Props:
    - thread: Object (필수) - 쓰레드 정보
      {
        id: Number,
        title: String,
        bookTitle: String,
        author: {
          username: String
        },
        content: String,
        likes: Number,
        comments: Array
      }
-->
<template>  <div class="thread-card" @click="navigateToDetail">
    <!-- 글 기본 정보 -->
    <div class="thread-header">
      <h3>{{ thread.title }}</h3>
      <span class="author">{{ thread.author.username }}</span>
    </div>

    <!-- 관련 도서 정보 -->
    <div class="book-info">
      <span>📚 {{ thread.bookTitle }}</span>
    </div>

    <!-- 글 내용 요약 -->
    <div class="content">
      <p>{{ threadSummary }}</p>
    </div>

    <!-- 상호작용 정보 -->
    <div class="interactions">
      <span class="likes">좋아요 {{ thread.likes }}</span>
      <span class="comments">댓글 {{ thread.comments.length }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ThreadCard',
  props: {
    thread: {
      type: Object,
      required: true,
      validator: (thread) => {
        return thread.id && thread.title && thread.bookTitle && 
               thread.author && thread.content !== undefined
      }
    }
  },  computed: {
    threadSummary() {
      return this.thread.content.length > 100
        ? this.thread.content.slice(0, 100) + '...'
        : this.thread.content
    }
  },
  methods: {
    navigateToDetail() {
      this.$emit('thread-click', this.thread.id)
    }
  }
}
</script>

<style scoped>
.thread-card {
  border: 1px solid #ddd;
  padding: 1rem;
  margin-bottom: 1rem;
}

.thread-header {
  margin-bottom: 0.5rem;
}

.author {
  color: #666;
  font-size: 0.9rem;
}

.book-info {
  margin: 0.5rem 0;
}

.content {
  margin: 1rem 0;
}

.interactions {
  display: flex;
  gap: 1rem;
  color: #666;
  font-size: 0.9rem;
}
</style>
