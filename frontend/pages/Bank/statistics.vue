<template>
  <div>
    <!-- navbar -->
    <navbar :userBaseInfo="userBaseInfo" />
    <!-- banner -->
    <div class="main-wrapper">
        <div class="page-title">
            <div class="container">
                <div class="title-holder">
                    <div class="title-text text-center">
                        <h1>答题记录</h1>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div style="margin-top: 50px"></div>
    <!-- statement -->
    <section class="section">
      <div class="container">
          <a-table :columns="columns" :dataSource="data">
            <a-tag slot="id" slot-scope="text, record, index" :color="randomColor()">{{ index + 1 }}</a-tag>
            <router-link slot="user" slot-scope="text, record" :to="{ path: '/profile', query: { uid: record.user.uid } }">{{ record.user.nickname }}</router-link>
            <a-tag slot="subject" slot-scope="text" :color="randomColor()">{{ text }}</a-tag>
            <span slot="rate" slot-scope="text, record">{{ (record.correctQuestions / record.allQuestions).toFixed(4) * 100 }}%</span>
          </a-table>
      </div>
    </section>

    <Footer></Footer>

  </div>
</template>

<script>
import qs from 'qs'
import { mapState } from 'vuex'
import navbar from '~/components/navbar'
import Footer from '~/components/footer'

export default {
  components: {
    navbar,
    Footer
  },
  data() {
    return {
      columns: [{
        scopedSlots: { customRender: 'id' },
      }, {
        title: '用户',
        scopedSlots: { customRender: 'user' },
      }, {
        title: '科目',
        dataIndex: 'subject',
        scopedSlots: { customRender: 'subject' },
      }, {
        title: '全部题目',
        dataIndex: 'allQuestions',
      }, {
        title: '正确题目',
        dataIndex: 'correctQuestions',
      }, {
        title: '正确率',
        scopedSlots: { customRender: 'rate' },
      }, {
        title: '日期',
        dataIndex: 'date',
      }]
    }
  },
  async asyncData({ $axios }) {
    let userBaseInfo = null
    let data = null

    await $axios.get('getUserBaseInfo')
    .then((response) => {
      userBaseInfo = response.data
    })
    await $axios.get('getBankStatistics')
    .then((response) => {
        data = response.data.info
    })

    return {
      userBaseInfo: userBaseInfo,
      data: data
    }
  },
  methods: {
    randomColor() {
        let color = ['pink', 'red', 'orange', 'green', 'cyan', 'blue', 'purple']
        return color[Math.round(Math.random() * (color.length - 1))]
    },
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
</style>
