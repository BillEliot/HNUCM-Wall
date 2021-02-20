<template>
    <mavon-editor :value="value" @change="changeEvent" ref=md @imgAdd="$imgAdd" @imgDel="$imgDel" />
</template>

<script>
import qs from 'qs'
import { mapState } from 'vuex'

export default {
  props: {
      value: ''
  },
  model: {
      prop: 'value',
      event: 'change'
  },
  data() {
    return {
    }
  },
  methods: {
      changeEvent(val) {
          this.$emit('change', val)
      },
      $imgAdd(pos, $file) {
           var formdata = new FormData()
           formdata.append('image', $file)
           this.$axios({
               url: 'uploadImg_markdown',
               method: 'post',
               data: formdata,
               headers: { 'Content-Type': 'multipart/form-data' },
           })
           .then((response) => {
               if (response.data.code == 200 && response.data.status == 'success') {
                   this.$refs.md.$img2Url(pos, this.baseUrl + response.data.data)
               }
           })
      },
      $imgDel(url) {
          this.$axios.post('removeImg_markdown', qs.stringify({
              url: url[0]
          }))
          .then((response) => {
              if (response.data.code == 200 && response.data.status == 'success') {
                  this.$message.success('删除成功')
              }
          })
      }
  },
  computed: {
      ...mapState({
          baseUrl: state => state.baseUrl
      })
  }
}
</script>

<style scoped>
</style>
