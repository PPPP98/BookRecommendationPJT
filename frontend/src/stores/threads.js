import { defineStore } from 'pinia'
import axios from 'axios'

export const useThreadsStore = defineStore('threads', {
  state: () => ({
    threads: [],
    loading: false,
    error: null
  }),
  actions: {
    async fetchThreads(params = {}) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get('/api/threads/', { params })
        this.threads = response.data.results
      } catch (err) {
        this.error = '쓰레드 목록을 불러오는데 실패했습니다.'
        console.error('Error fetching threads:', err)
      } finally {
        this.loading = false
      }
    },
    async submitThread(payload) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.post('/api/threads/', payload)
        this.threads.unshift(response.data) // 새 쓰레드를 목록에 추가
      } catch (err) {
        this.error = '쓰레드 작성에 실패했습니다.'
        console.error('Error submitting thread:', err)
      } finally {
        this.loading = false
      }
    }
  }
})