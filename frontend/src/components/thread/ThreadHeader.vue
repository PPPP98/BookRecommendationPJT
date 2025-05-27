<template>
  <div class="thread-header">
    <h1>{{ thread.title }}</h1>
    <div class="author-info">
      <router-link
        v-if="thread.user && thread.user.id"
        :to="{ name: 'UserProfile', params: { id: thread.user.id } }"
        class="author-link"
      >
        <img
          :src="thread.user.profile_image || fallbackProfile"
          :alt="thread.user.nickname || thread.user.username"
          class="author-image"
          @error="$emit('img-error', $event)"
        />
        <span class="author-name">{{ thread.user.nickname || thread.user.username }}</span>
      </router-link>
      <span class="created-at">{{ formattedDate }}</span>
    </div>
    <div class="book-info">
      <div class="book-title">{{ thread.book?.title }}</div>
      <div class="book-detail">
        <img
          class="book-cover"
          :src="thread.book?.cover || fallbackBookCover"
          :alt="thread.book?.title || '책 표지'"
          @error="$emit('book-img-error', $event)"
        />
        <div class="book-meta">
          <div class="book-author">
            <strong>저자:</strong> {{ thread.book?.author }}
          </div>
          <div class="rating">
            <span>평점: </span>
            <span class="stars">{{ '⭐'.repeat(Math.floor(thread.rating || 0)) }}</span>
            <span class="rating-number">{{ thread.rating || 0 }}/5</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  props: [
    'thread',
    'fallbackProfile',
    'fallbackBookCover',
    'formattedDate'
  ]
}
</script>
