<template>
  <div class="form-row">
    <label for="nickname">닉네임</label>
    <input id="nickname" v-model="nickname" @input="onInput" required maxlength="30" />
    <button type="button" @click="checkNickname" :disabled="checking">중복검사</button>
    <span v-if="checkResult === true" class="success">사용 가능한 닉네임입니다.</span>
    <span v-else-if="checkResult === false" class="error">이미 사용 중인 닉네임입니다.</span>
    <span v-if="checkError" class="error">{{ checkError }}</span>
  </div>
</template>
<script>
import axios from 'axios'
export default {
  props: ['modelValue'],
  emits: ['update:modelValue'],
  data() {
    return {
      nickname: this.modelValue || '',
      checking: false,
      checkResult: null,
      checkError: null
    }
  },
  watch: {
    modelValue(val) {
      this.nickname = val
    }
  },
  methods: {
    onInput() {
      this.$emit('update:modelValue', this.nickname)
      this.checkResult = null
      this.checkError = null
    },
    async checkNickname() {
      this.checking = true
      this.checkError = null
      try {
        const { data } = await axios.get(`/api/accounts/check-nickname/?nickname=${encodeURIComponent(this.nickname)}`)
        this.checkResult = !data.exists
      } catch {
        this.checkError = '중복검사 중 오류가 발생했습니다.'
      } finally {
        this.checking = false
      }
    }
  }
}
</script>
<style scoped>
.success { color: #1976d2; margin-left: 0.5rem; }
.error { color: #dc3545; margin-left: 0.5rem; }
</style>
