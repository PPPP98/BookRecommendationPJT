<template>
  <div class="custom-thread-card" @click="navigateToDetail">
    <div class="card-top">
      <div class="profile">
        <img :src="thread.user.profile_image" class="profile-img" />
        <div class="nickname">{{ thread.user.nickname }}</div>
      </div>
      <div class="created">{{ formatDate(thread.created_at) }}</div>
    </div>
    <div class="card-main">
      <div class="book-cover-wrap" v-if="thread.book">
        <img :src="thread.book.cover" class="book-cover" />
      </div>
      <div class="main-info">
        <div class="thread-title">{{ thread.title }}</div>
        <div class="book-title" v-if="thread.book">
          <span>{{ thread.book.title }}</span>
          <span class="author">/ {{ thread.book.author }}</span>
        </div>
      </div>
    </div>
    <div class="card-bottom">
      <span class="likes">👍 {{ thread.like_count }}</span>
      <span class="comments">💬 {{ thread.comment_count }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CustomThreadCard',
  props: {
    thread: { type: Object, required: true }
  },
  methods: {
    navigateToDetail() {
      this.$emit('thread-click', this.thread.id)
    },
    formatDate(date) {
      if (!date) return ''
      return date.slice(0, 10)
    }
  }
}
</script>

<style scoped>
.custom-thread-card {
  width: 100%;
  max-width: 900px;
  min-width: 720px;
  min-height: 160px;
  box-sizing: border-box;
  border: 1.5px solid #e0e0e0;
  border-radius: 12px;
  background: #fff;
  margin: 0 auto 1.5rem auto;
  padding: 1.6rem 2.2rem 1.2rem 2.2rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  cursor: pointer;
  transition: box-shadow 0.18s, border 0.18s;
}
.custom-thread-card:hover {
  box-shadow: 0 4px 16px rgba(25, 118, 210, 0.07);
  border: 1.5px solid #1976d2;
}
.card-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.profile {
  display: flex;
  align-items: center;
  gap: 0.7rem;
}
.profile-img {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  object-fit: cover;
  background: #f2f2f2;
}
.nickname {
  font-weight: 600;
  font-size: 1.02rem;
}
.created {
  color: #888;
  font-size: 0.95rem;
}
.card-main {
  display: flex;
  align-items: flex-start;
  gap: 1.5rem;
  margin-bottom: 1.1rem;
}
.book-cover-wrap {
  flex-shrink: 0;
  width: 60px;
  height: 80px;
  border-radius: 7px;
  overflow: hidden;
  background: #f8f8f8;
  display: flex;
  align-items: center;
  justify-content: center;
}
.book-cover {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.main-info {
  flex: 1;
  min-width: 0;
}
.thread-title {
  font-size: 1.13rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.book-title {
  font-size: 1.02rem;
  color: #222;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.author {
  color: #888;
  font-size: 0.97rem;
  margin-left: 0.3rem;
}
.card-bottom {
  display: flex;
  gap: 1.3rem;
  color: #1976d2;
  font-size: 1.05rem;
  font-weight: 500;
  margin-top: 0.2rem;
}
@media (max-width: 900px) {
  .custom-thread-card {
    max-width: 98vw;
    min-width: 98vw;
    padding: 1.2rem 0.7rem 1rem 0.7rem;
  }
}
@media (max-width: 600px) {
  .custom-thread-card {
    max-width: 100vw;
    min-width: 100vw;
    border-radius: 0;
    padding: 0.9rem 0.2rem 0.7rem 0.2rem;
  }
  .book-cover-wrap { width: 38px; height: 50px; }
  .profile-img { width: 28px; height: 28px; }
}
</style>
