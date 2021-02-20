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
                        <h1>我的打卡</h1>
                        <a-button type="dashed" size="large" @click="$router.push({ path: '/activity/jingui/statistics' })">打卡统计</a-button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="container">
        <a-calendar @select="onSelect">
            <div slot="dateCellRender" slot-scope="value" class="sign">
                <span>{{ setSignDate(value) }}</span>
                <span v-if="signStatus[value.format('YYYY-MM-DD')] == 1">
                    <a-icon type="check-circle" theme="twoTone" two-tone-color="#52c41a" />&nbsp;已打卡
                </span>
                <span v-else-if="signStatus[value.format('YYYY-MM-DD')] == -1">
                    <a-icon type="close-circle" theme="twoTone" two-tone-color="#ffd700" />&nbsp;未开始
                </span>
                <span v-else>
                    <a-icon type="warning" theme="twoTone" two-tone-color="#ff0000" />&nbsp;未打卡
                </span>
            </div>
            <template slot="monthCellRender" slot-scope="value">
                <span>{{ randomSaying() }}</span>
            </template>
        </a-calendar>
    </div>

    <Footer></Footer>

  </div>
</template>

<script>
import qs from 'qs'
import moment from 'moment'
import navbar from '~/components/navbar'
import Footer from '~/components/footer'

export default {
  components: {
    navbar,
    Footer
  },
  data() {
    return {
        moment,
        signDate: [],
        signStatus: []
    }
  },
  async asyncData({ $axios, query, error }) {
    let userBaseInfo = null
    let queryUID = query.id

    await $axios.get('getUserBaseInfo')
    .then((response) => {
      userBaseInfo = response.data
      if (userBaseInfo.id == -1) {
          error({ statusCode: 500, message: '先登录吧～' })
      }
    })

    await $axios.get('canSign_JinGui')
    .then((response) => {
        if (response.data != 0) {
            error({ statusCode: 500, message: '先报名吧～' })
        }
    })

    return {
      userBaseInfo: userBaseInfo,
      queryUID: queryUID
    }
  },
  methods: {
      setSignDate(value) {
          // prevent rendering
          this.signDate[this.signDate.length] = value.format("YYYY-MM-DD")
      },
      getSignStatus() {
          this.$axios.post('getSignStatus', qs.stringify({
              uid: this.queryUID,
              dates: this.signDate
          }, { arrayFormat: 'brackets' }))
          .then((response) => {
              if (response.data == 1) {
                  this.$message.error('未知错误')
              }
              else {
                  this.signStatus = response.data.info
              }
          })
      },
      onSelect(value) {
          if (this.signStatus[value.format("YYYY-MM-DD")] != 1) {
              this.$message.warning('没有打卡记录')
          }
          else {
              let routeData = this.$router.resolve({
                  path: '/activity/jingui/detail',
                  query: { uid: this.queryUID, date: value.format("YYYY-MM-DD") }
              })
              window.open(routeData.href, '_blank')
          }
      },
      randomSaying() {
          let saying = [
              '不积跬步,无以至千里',
              '不积小流,无以成江海',
              '骐骥一跃,不能十步',
              '驽马十驾,功在不舍',
              '锲而舍之,朽木不折',
              '锲而不舍,金石可镂',
              '冰冻三尺，非一日之寒',
              '水滴石穿，绳锯木断',
              '千里之堤，溃于蚁穴',
              '祸患常积于忽微，而智勇多困于所溺',
              '外物之味，久则可厌',
              '读书之味，愈久愈深'
          ]
        return saying[Math.round(Math.random() * (saying.length - 1))]
      }
  },
  mounted() {
      this.getSignStatus()
  }
}
</script>

<style scoped>
.sign {
    font-size: 18px;
}
</style>
