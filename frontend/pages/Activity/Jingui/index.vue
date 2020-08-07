<template>
  <div>
    <!-- navbar -->
    <navbar :userBaseInfo="userBaseInfo" />
    <!-- banner -->
    <div class="main-wrapper">
        <div class="page-title-zy">
            <div class="container">
                <div class="title-holder">
                    <div class="title-text text-center">
                        <h1>金匮打卡</h1>
                        <a-button v-if="!canSign_JinGui" size="large" @click="signUp">报名</a-button>
                        <a-button v-if="canSign_JinGui" type="primary" size="large" @click="sign">打卡</a-button>
                        <a-button type="dashed" size="large" @click="$router.push({ path: '/activity/jingui/statistics' })">打卡统计</a-button>
                        <a-button v-if="userBaseInfo.uid != -1" size="large" @click="$router.push({ path: '/activity/jingui/log', query: { uid: userBaseInfo.uid } })">我的打卡</a-button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <Footer></Footer>

  </div>
</template>

<script>
import qs from 'qs'
import navbar from '~/components/navbar'
import Footer from '~/components/footer'

export default {
  components: {
    navbar,
    Footer
  },
  data() {
    return {
        content: '',
        toolbars: {
            bold: true,
            italic: true,
            header: true,
            underline: true,
            strikethrough: true,
            mark: true,
            superscript: true,
            subscript: true,
            quote: true,
            ol: true,
            ul: true,
            link: true,
            imagelink: true,
            table: true,
            help: true,
            trash: true,
            save: true,
            alignleft: true,
            aligncenter: true,
            alignright: true,
        }
    }
  },
  async asyncData({ $axios }) {
    let userBaseInfo = null
    let canSign_JinGui = false

    await $axios.get('getUserBaseInfo')
    .then((response) => {
      userBaseInfo = response.data
    })

    await $axios.post('canSign_JinGui', qs.stringify({
        auth: '金匮打卡'
    }))
    .then((response) => {
        if (response.data == 0) {
            canSign_JinGui = true
        }
        else {
            canSign_JinGui = false
        }
    })

    return {
      userBaseInfo: userBaseInfo,
      canSign_JinGui: canSign_JinGui
    }
  },
  methods: {
      signUp() {
          if (this.userBaseInfo.uid == -1) {
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
          if (this.userBaseInfo.uid == -1) {
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
  }
}
</script>

<style scoped>
</style>
