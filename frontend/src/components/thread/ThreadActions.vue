<template>
  <div class="thread-actions">
    <button class="like-button" @click="$emit('toggle-like')" :disabled="likeLoading">
      {{ isLiked ? '❤️' : '🤍' }} {{ thread.like_count || 0 }}명이 좋아합니다
    </button>
    <button
      v-if="showFollowButton"
      class="follow-button"
      :class="{ following: isFollowing }"
      @click="$emit('toggle-follow')"
      :disabled="followLoading"
    >
      {{ isFollowing ? '언팔로우' : '팔로우' }}
    </button>
    <button v-if="isMine" @click="$emit('start-edit')" class="edit-button">수정</button>
    <button v-if="isMine" @click="$emit('delete-thread')" class="delete-button">삭제</button>
  </div>
</template>
<script>
export default {
  props: [
    'thread',
    'isLiked',
    'likeLoading',
    'isFollowing',
    'followLoading',
    'isMine',
    'showFollowButton'
  ]
}
</script>
