<template>
  <div class="modal-bg" @click.self="$emit('close')">
    <div class="modal-list liked-books-modal-list">
      <h2>찜한 도서</h2>
      <BookLikeList
        :books="likedBooks"
        :editable="false"
        @book-click="onBookClick"
      />
      <button class="modal-close-btn" @click="$emit('close')">닫기</button>
      <div class="pagination">
        <button v-if="prev" @click="fetchPage(prev)">이전</button>
        <button v-if="next" @click="fetchPage(next)">다음</button>
      </div>
    </div>
  </div>
</template>
<script>
import BookLikeList from './BookLikeList.vue'
import axios from 'axios'
export default {
  props: {
    userId: { type: [String, Number], required: true },
    show: Boolean
  },
  components: { BookLikeList },
  data() {
    return { likedBooks: [], next: null, prev: null }
  },
  watch: {
    show(val) {
      if (val) this.fetchLikedBooks()
    }
  },
  methods: {
    async fetchLikedBooks(url) {
      try {
        const apiUrl = url || `/api/accounts/${this.userId}/liked-books/`
        const { data } = await axios.get(apiUrl)
        this.likedBooks = data.results || data || []
        this.next = data.next
        this.prev = data.previous
      } catch {
        this.likedBooks = []
        this.next = null
        this.prev = null
      }
    },
    fetchPage(url) {
      this.fetchLikedBooks(url)
    },
    onBookClick(bookId) {
      this.$emit('book-click', bookId)
    }
  }
}
</script>
