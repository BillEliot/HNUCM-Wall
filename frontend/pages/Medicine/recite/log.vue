<template>
  <div>
    <!-- banner -->
    <div class="main-wrapper">
        <div class="page-title-zy">
            <div class="container">
                <div class="title-holder">
                    <div class="title-text text-center">
                        <h1>中药打卡</h1>
                        <a-button type="primary" @click="$router.push({ path: '/medicine/recite' })">继续学习</a-button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <a-divider style="font-weight: bold; color: purple">祸患常积于忽微，而智勇多困于所溺</a-divider>
    <div class="container text-center">
        共打卡<span style="font-weight: bold; color: green; font-size: 48px">{{ signDays }}</span>天
        <a-row type="flex" justify="center">
            <a-col :md="20" :sm="20" :xs="24">
                <a-spin :spinning="spinning">
                    <a-calendar @panelChange="calendarChange" class="calendar">
                        <div slot="dateCellRender" slot-scope="value">
                            <!-- just a call -->
                            <span>{{ setDates(value) }}</span>
                            <span v-if="signLog[value.format('YYYY-MM-DD')]">
                                <a-icon type="check-circle" theme="twoTone" two-tone-color="#52c41a" style="font-size: 20px" />
                            </span>
                        </div>
                    </a-calendar>
                </a-spin>
            </a-col>
        </a-row>
        <a-button v-if="canShowSignButton != 'false'" type="primary" :disabled="canShowSignButton == 'done'" @click="sign" style="width: 100%">{{ canShowSignButton == 'done' ? '已打卡' : '打卡' }}</a-button>
    </div>
  </div>
</template>

<script>
import qs from 'qs'
import moment from 'moment'
import { mapState } from 'vuex'

export default {
  layout: 'common',
  middleware: 'LoginRequired',
  data() {
    return {
        moment,
        dates: [],
        signLog: {},
        spinning: false
    }
  },
  async asyncData({ $axios }) {
      let canShowSignButton = 'false'
      let signDays = 0

      await $axios.get('canSign_reciteMedicine')
      .then((response) => {
          if (response.data.code == 200) {
              canShowSignButton = response.data.status
              signDays = response.data.signDays
          }
      })

      return {
          canShowSignButton: canShowSignButton,
          signDays: signDays
      }
  },
  methods: {
      setDates(value) {
          this.dates[this.dates.length] = value.format('YYYY-MM-DD')
      },
      sign() {
          this.$axios.get('sign_reciteMedicine')
          .then((response) => {
              if (response.data.code == 200 && response.data.status == 'success') {
                  this.$message.success('打卡成功')
                  this.signLog[moment().format('YYYY-MM-DD')] = true
                  this.signDays += 1
                  this.canShowSignButton = 'done'
              }
          })
      },
      getSignLog() {
          this.spinning = true
          this.$axios.post('getSignLog_reciteMedicine', qs.stringify({
              dates: this.dates
          }, { arrayFormat: 'brackets' }))
          .then((response) => {
              this.spinning = false
              if (response.data.code == 200 && response.data.status == 'success') {
                  this.signLog = response.data.data
              }
          })
      },
      calendarChange() {
          this.getSignLog()
      }
  },
  mounted() {
      this.getSignLog()
  },
  computed: mapState({
      userBaseInfo: state => state.userBaseInfo
  })
}
</script>

<style scoped>
.calendar >>> .ant-radio-group {
    display: none;
}
</style>
