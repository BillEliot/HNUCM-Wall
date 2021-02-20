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
                        <h1>虚拟门诊记录</h1>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div style="margin-top: 50px"></div>
    <!-- statement -->
    <section class="section">
      <div class="container">
          <a-spin :spinning="spinning">
            <a-table :columns="columns" :dataSource="data">
              <span slot="action" slot-scope="text, record">
                <a @click="detail(record.key)">详情</a>
              </span>
            </a-table>
          </a-spin>
      </div>
    </section>

    <Footer />

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
        dataIndex: 'key'
      }, {
        title: '姓名',
        dataIndex: 'patient_name'
      }, {
        title: '性别',
        dataIndex: 'patient_gender'
      },{
        title: '年龄',
        dataIndex: 'patient_age'
      }, {
        title: '日期',
        dataIndex: 'date'
      }, {
        title: '操作',
        scopedSlots: { customRender: 'action' },
      }],
      data: [],
      spinning: false
    }
  },
  async asyncData({ $axios, error }) {
    let userBaseInfo = null
    let data = null

    await $axios.get('getUserBaseInfo')
    .then((response) => {
      userBaseInfo = response.data
      if (userBaseInfo.id == -1) {
        error({ statusCode: 403, message: '先登录吧～' })
      }
    })

    await $axios.get('getLog_VirtualDiagnosis')
    .then((response) => {
      if (response.data != 1) {
        data = response.data.info
      }
    })

    return {
      userBaseInfo: userBaseInfo,
      data: data
    }
  },
  methods: {
    detail(id) {
      let routeData = this.$router.resolve({ path: '/virtualsimulation/virtualdiagnosis/detail', query: { id: id } });
      window.open(routeData.href, '_blank');
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
</style>
