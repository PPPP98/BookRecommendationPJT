<template>
  <div class="thread-author-card">
    <router-link :to="`/mypage/${userId}`" class="author-profile-link">
      <img
        :src="profileImage || fallbackProfile"
        :alt="nickname || username"
        @error="$emit('profile-img-error', $event)"
        class="author-image"
      />
      <div class="author-info">
        <span class="author-name">{{ nickname || username }}</span>
        <span class="thread-date">{{ date }}</span>
      </div>
    </router-link>
  </div>
</template>

<script>
export default {
  name: 'ThreadHeaderInfo',
  props: {
    profileImage: {
      type: String,
      default: ''
    },
    nickname: {
      type: String,
      default: ''
    },
    username: {
      type: String,
      default: ''
    },
    date: {
      type: String,
      required: true
    },
    userId: {
      type: [Number, String],
      required: true
    },
    fallbackProfile: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
.thread-author-card {
  background: #fff;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(182,176,159,0.1);
  border: 1px solid var(--color-border);
  margin-bottom: 1.5rem;
}

.author-profile-link {
  display: flex;
  align-items: center;
  gap: 1rem;
  text-decoration: none;
  color: inherit;
  transition: transform 0.2s ease;
}

.author-profile-link:hover {
  transform: translateY(-2px);
}

.author-image {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
  background: #efefef;
  border: 2px solid var(--color-accent);
}

.author-info {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.author-name {
  font-weight: 600;
  color: var(--color-accent);
  font-size: 1.1rem;
}

.thread-date {
  font-size: 0.9rem;
  color: #888;
}
</style>
