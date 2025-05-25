import { defineStore } from 'pinia'
import axios from 'axios'

export const useBooksStore = defineStore('books', {
  state: () => ({
    books: [],
    categories: [],
    loading: false,
    error: null
  }),
  actions: {
    async fetchBooks(params = {}) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get('/api/books/', { params })
        this.books = response.data.results
      } catch (err) {
        this.error = '도서 목록을 불러오는데 실패했습니다.'
        console.error('Error fetching books:', err)
      } finally {
        this.loading = false
      }
    },
    async fetchCategories() {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get('/api/books/categories/')
        this.categories = response.data.categories
      } catch (err) {
        this.error = '카테고리 목록을 불러오는데 실패했습니다.'
        console.error('Error fetching categories:', err)
      } finally {
        this.loading = false
      }
    }
  }
})