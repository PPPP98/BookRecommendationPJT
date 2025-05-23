<!-- 
  MyThreadList 컴포넌트
  역할: 사용자가 작성한 글과 댓글 목록을 표시
  Props:
    - threads: Array - 작성한 글 목록
    - comments: Array - 작성한 댓글 목록
  이벤트:
    - @delete-thread: 글 삭제 시 발생
    - @delete-comment: 댓글 삭제 시 발생
-->
<template>
  <div class="my-thread-list">
    <div class="tabs">
      <button 
        :class="['tab-button', { active: activeTab === 'threads' }]"
        @click="activeTab = 'threads'"
      >
        내가 쓴 글
      </button>
      <button 
        :class="['tab-button', { active: activeTab === 'comments' }]"
        @click="activeTab = 'comments'"
      >
        내가 쓴 댓글
      </button>
    </div>

    <div v-if="activeTab === 'threads'" class="thread-section">
      <div v-for="thread in threads" :key="thread.id" class="thread-item">
        <div class="thread-content">
          <h3>{{ thread.title }}</h3>
          <p class="thread-summary">{{ threadSummary(thread.content) }}</p>
          <div class="thread-meta">
            <span>{{ formatDate(thread.createdAt) }}</span>
            <span>좋아요 {{ thread.likes }}</span>
            <span>댓글 {{ thread.comments.length }}</span>
          </div>
        </div>
        <div class="thread-actions">
          <button @click="editThread(thread)" class="edit-button">수정</button>
          <button @click="deleteThread(thread.id)" class="delete-button">삭제</button>
        </div>
      </div>
      
      <div v-if="threads.length === 0" class="empty-state">
        작성한 글이 없습니다.
      </div>
    </div>

    <div v-else class="comment-section">
      <div v-for="comment in comments" :key="comment.id" class="comment-item">
        <div class="comment-content">
          <p>{{ comment.content }}</p>
          <div class="comment-meta">
            <span>{{ formatDate(comment.created_at) }}</span>
            <a @click="navigateToThread(comment.thread_id)" class="thread-link">
              원문 보기
            </a>
          </div>
        </div>
        <div class="comment-actions">
          <button @click="deleteComment(comment.id)" class="delete-button">삭제</button>
        </div>
      </div>
      
      <div v-if="comments.length === 0" class="empty-state">
        작성한 댓글이 없습니다.
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MyThreadList',
  props: {
    threads: {
      type: Array,
      required: true
    },
    comments: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      activeTab: 'threads'
    }
  },
  methods: {
    threadSummary(content) {
      return content.length > 100 ? content.slice(0, 100) + '...' : content
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return new Intl.DateTimeFormat('ko-KR').format(date)
    },
    editThread(thread) {
      this.$router.push(`/threads/${thread.id}/edit`)
    },
    deleteThread(threadId) {
      if (confirm('정말 삭제하시겠습니까?')) {
        this.$emit('delete-thread', threadId)
      }
    },
    deleteComment(commentId) {
      if (confirm('정말 삭제하시겠습니까?')) {
        this.$emit('delete-comment', commentId)
      }
    },
    navigateToThread(threadId) {
      this.$router.push(`/threads/${threadId}`)
    }
  }
}
</script>

<style scoped>
.my-thread-list {
  margin: 2rem 0;
}

.tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.tab-button {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  cursor: pointer;
}

.tab-button.active {
  background: #0066cc;
  color: white;
  border-color: #0066cc;
}

.thread-item, .comment-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1rem;
  border-bottom: 1px solid #eee;
}

.thread-content, .comment-content {
  flex: 1;
}

.thread-summary {
  color: #666;
  margin: 0.5rem 0;
}

.thread-meta, .comment-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.9rem;
  color: #666;
}

.thread-actions, .comment-actions {
  display: flex;
  gap: 0.5rem;
}

.edit-button, .delete-button {
  padding: 0.25rem 0.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.edit-button {
  background: #17a2b8;
  color: white;
}

.delete-button {
  background: #dc3545;
  color: white;
}

.thread-link {
  color: #0066cc;
  cursor: pointer;
  text-decoration: underline;
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: #666;
}
</style>
