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
            <a-tag slot="id" slot-scope="text" :color="randomColor()">{{ text }}</a-tag>
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
            key: 'id',
            dataIndex: 'id',
            scopedSlots: { customRender: 'id' },
        }, {
            title: '用户',
            key: 'user',
            scopedSlots: { customRender: 'user' },
        }, {
            title: '科目',
            key: 'subject',
            dataIndex: 'subject',
            scopedSlots: { customRender: 'subject' },
        }, {
            title: '全部题目',
            key: 'allQuestions',
            dataIndex: 'allQuestions',
            scopedSlots: { customRender: 'tags' },
        }, {
            title: '正确题目',
            key: 'correctQuestions',
            dataIndex: 'correctQuestions',
            scopedSlots: { customRender: 'action' },
        }, {
            title: '正确率',
            key: 'rate',
            scopedSlots: { customRender: 'rate' },
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
