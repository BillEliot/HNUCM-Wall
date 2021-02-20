<template>
  <div>
    <!-- banner -->
    <div class="main-wrapper">
        <div class="page-title-zy">
            <div class="container">
                <div class="title-holder">
                    <div class="title-text text-center">
                        <h1>金匮打卡</h1>
                        <h2 style="color: red">活动已结束</h2>
                        <a-button disabled v-if="!canSign_JinGui" size="large" @click="signUp">报名</a-button>
                        <a-button disabled v-if="canSign_JinGui" type="primary" size="large" @click="sign">打卡</a-button>
                        <a-button disabled type="dashed" size="large" @click="$router.push({ path: '/activity/jingui/statistics' })">打卡统计</a-button>
                        <a-button disabled v-if="userBaseInfo.id != -1" size="large" @click="$router.push({ path: '/activity/jingui/log', query: { uid: userBaseInfo.id } })">我的打卡</a-button>
                    </div>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>

<script>
import qs from 'qs'
import { mapState } from 'vuex'

export default {
  layout: 'common',
  data() {
    return {
    }
  },
  async asyncData({ $axios }) {
    let canSign_JinGui = false

    await $axios.get('canSign_JinGui')
    .then((response) => {
        if (response.data == 0) {
            canSign_JinGui = true
        }
        else {
            canSign_JinGui = false
        }
    })

    return {
      canSign_JinGui: canSign_JinGui
    }
  },
  methods: {
      signUp() {
          if (this.userBaseInfo.id == -1) {
              this.$message.warning('先登录吧～')
          }
          else {
              this.$axios.post('signUp', qs.stringify({
                  auth: '金匮打卡'
              }))
              .then((response) => {
                  if (response.data == 0) {
                      this.$message.success('报名成功')
                      this.canSign_JinGui = true
                  }
                  else if (response.data == 1) {
                      this.$message.warning('已经报名')
                  }
                  else {
                      this.$message.error('未知错误')
                  }
              })
          }
      },
      sign() {
          if (this.userBaseInfo.id == -1) {
              this.$message.warning('先登录吧～')
          }
          else {
              this.$axios.post('canSign_JinGui', qs.stringify({
                  auth: '金匮打卡'
              }))
              .then((response) => {
                  if (response.data == 0) {
                      this.$router.push({ path: '/activity/jingui/sign' })
                  }
                  else if (response.data == 1) {
                      this.$message.warning('先报名吧')
                  }
                  else {
                      this.$message.error('未知错误')
                  }
              })
          }
      }
  },
  computed: mapState({
      userBaseInfo: state => state.userBaseInfo
  })
}
</script>

<style scoped>
</style>
