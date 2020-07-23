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
                            <h1>讲座动态</h1>
                            <p class="subheading">抢在第一位～</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div style="margin-top: 50px"></div>
        <!-- container -->
        <div class="container">
            <div class="row">
                <div class="col-md-12 col-sm-12">
                    <no-ssr placeholder='Loading'>
                        <a-table :columns="columns" :dataSource="lectureList">
                            <!-- author -->
                            <span slot="author" slot-scope="author">
                                <a-avatar :src="author.avatar" />
                                {{ author.nickname }}
                            </span>
                            <!-- date -->
                            <span slot="date" slot-scope="date">
                                {{ moment(date).format('lll') }}
                            </span>
                            <!-- state -->
                            <span slot="state" slot-scope="state">
                                <a-tag v-if="state == 'wait'" color="red">未开始</a-tag>
                                <a-tag v-if="state == 'running'" color="green">进行中</a-tag>
                                <a-tag v-if="state == 'done'" color="gray">已结束</a-tag>
                            </span>
                        </a-table>
                    </no-ssr>
                </div>
            </div>
        </div>

        <Footer />

    </div>
</template>

<script>
import qs from 'qs'
import moment from 'moment'
import Footer from '~/components/footer.vue'
import navbar from '~/components/navbar'
import { mapState } from 'vuex'


export default {
  components: {
      Footer,
      navbar
  },
  data() {
    return {
        columns: [{
            dataIndex: 'title',
            title: '标题'
        }, {
            dataIndex: 'lecturer',
            title: '讲座人'
        }, {
            dataIndex: 'address',
            title: '讲座地点'
        }, {
            dataIndex: 'date',
            title: '讲座日期',
            scopedSlots: { customRender: 'date' }
        }, {
            dataIndex: 'state',
            title: '讲座状态',
            scopedSlots: { customRender: 'state' }
        }]
    }
  },
  async asyncData({ $axios }) {
    let userBaseInfo = null
    let lectureList = []

    await $axios.get('getUserBaseInfo')
    .then((response) => {
        userBaseInfo = response.data
    })
    await $axios.get('getLectureList')
    .then((response) => {
        lectureList = response.data.info
    })

    return {
        userBaseInfo: userBaseInfo,
        lectureList: lectureList
    }
  },
  methods: {
      moment
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
