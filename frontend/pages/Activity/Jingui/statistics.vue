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
              <h1>金匮打卡统计</h1>
              <a-button type="primary" size="large" @click="$router.push({ path: '/activity/jingui/sign' })">打卡</a-button>
              <a-button v-if="userBaseInfo.id != -1" size="large" @click="$router.push({ path: '/activity/jingui/log', query: { uid: userBaseInfo.id } })">我的打卡</a-button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div style="margin-top: 50px"></div>
    <div class="container">
      <div class="row">
        <div class="col-md-12 col-xs-12 text-center">
          <a-tabs type="card">
            <a-tab-pane tab="每日打卡统计" key="1">
              <span>选择日期</span>
              <a-date-picker
                @change="changeDate"
                format="YYYY-MM-DD"
                :disabled-date="disabledDate"
                :default-value="moment()"
              />
              <hr />
              <client-only placeholder='Loading'>
                <a-tabs type="card">
                  <a-tab-pane tab="已打卡" key="1-1" class="text-left">
                    <a-list item-layout="vertical" size="large" :pagination="pagination" :data-source="statisticsList">
                      <div slot="footer">金匮打卡数据统计</div>
                      <a-list-item slot="renderItem" key="item.user.id" slot-scope="item, index">
                        <img
                          slot="extra"
                          width="272"
                          alt="logo"
                          :src="baseUrl + item.cover"
                        />
                        <a-list-item-meta :description="item.user.bio">
                          <a-popover slot="title" :title="item.user.username">
                            <div slot="content">
                              <a @click="$router.push({ path: '/activity/jingui/log', query: { uid: item.user.id } })">查看打卡记录</a>
                              <a @click="$router.push({ path: '/profile', query: { id: item.user.id } })">查看个人信息</a>
                            </div>
                            <a>{{ item.user.username }}</a>
                          </a-popover>
                          <a-popover slot="avatar" :title="item.user.username">
                            <a slot="content" @click="$router.push({ path: '/activity/jingui/log', query: { uid: item.user.id } })">查看打卡记录</a>
                            <a-avatar :src="baseUrl + item.user.avatar" />
                          </a-popover>
                        </a-list-item-meta>
                        {{ item.content.substring(0,100) + '......' }}
                        <br />
                        <span class="date">{{ moment(item.date).format("llll") }}</span>
                        <br />
                        <a target="_blank" :href="'/activity/jingui/detail?uid=' + item.user.id + '&date=' + date">详情</a>
                        <hr />
                        <audio-player :src="baseUrl + item.audio" />
                      </a-list-item>
                    </a-list>
                  </a-tab-pane>
                  <a-tab-pane tab="未打卡" key="1-2" class="text-left">
                    <a-list item-layout="horizontal" :pagination="pagination" :data-source="statisticsList_unsign">
                      <a-list-item slot="renderItem" slot-scope="item, index">
                        <a-list-item-meta :description="item.bio">
                          <a-popover slot="title" :title="item.username">
                            <div slot="content">
                              <a @click="$router.push({ path: '/activity/jingui/log', query: { uid: item.id } })">查看打卡记录</a>
                              <br />
                              <a @click="$router.push({ path: '/profile', query: { id: item.id } })">查看个人信息</a>
                            </div>
                            <a>{{ item.username }}</a>
                          </a-popover>
                          <a-popover slot="avatar" :title="item.username">
                            <a slot="content" @click="$router.push({ path: '/activity/jingui/log', query: { uid: item.id } })">查看打卡记录</a>
                            <a-avatar :src="baseUrl + item.avatar" />
                          </a-popover>
                        </a-list-item-meta>
                      </a-list-item>
                    </a-list>
                  </a-tab-pane>
                </a-tabs>
              </client-only>
            </a-tab-pane>
            <a-tab-pane tab="5日打卡统计(不含今天)" key="2">

            </a-tab-pane>
          </a-tabs>
        </div>
      </div>
    </div>

    <Footer></Footer>

  </div>
</template>

<script>
import qs from 'qs'
import moment from 'moment'
import navbar from '~/components/navbar'
import Footer from '~/components/footer'
import { mapState } from 'vuex'

export default {
  components: {
    navbar,
    Footer
  },
  data() {
    return {
      moment,
      date: moment().format("YYYY-MM-DD"),
      pagination: {
        pageSize: 10
      }
    }
  },
  async asyncData({ $axios, error }) {
    let userBaseInfo = null
    let statisticsList = []
    let statisticsList_unsign = []

    await $axios.get('getUserBaseInfo')
    .then((response) => {
      userBaseInfo = response.data
    })

    await $axios.get('getStatistics_JinGui')
    .then((response) => {
      if (response.data != 1) {
        statisticsList = response.data.info
      }
      else {
        error({ statusCode: 500, message: '未知错误' })
      }
    })

    await $axios.get('getStatistics_JinGui_unsign')
    .then((response) => {
      if (response.data != 1) {
        statisticsList_unsign = response.data.info
      }
      else {
        error({ statusCode: 500, message: '未知错误' })
      }
    })

    return {
      userBaseInfo: userBaseInfo,
      statisticsList: statisticsList,
      statisticsList_unsign: statisticsList_unsign
    }
  },
  methods: {
    disabledDate(current) {
      return current && current > moment().endOf('day');
    },
    changeDate(m) {
      this.date = m.format("YYYY-MM-DD")
      this.$axios.post('getStatistics_JinGui', qs.stringify({
        date: this.date
      }))
      .then((response) => {
        this.statisticsList = response.data.info
      })
      this.$axios.post('getStatistics_JinGui_unsign', qs.stringify({
        date: this.date
      }))
      .then((response) => {
        this.statisticsList_unsign = response.data.info
      })
    }
  },
  computed: mapState({
    baseUrl: state => state.baseUrl
  })
}
</script>

<style scoped>
a {
  text-decoration: none;
}
.date {
  font-style: italic;
  color: gray;
}
</style>
