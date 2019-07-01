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
                    <a-table :columns="columns" :dataSource="data">
                        <!-- title -->
                        <a slot="_title" slot-scope="text">{{ text }}</a>
                        <!-- author -->
                        <span slot="author" slot-scope="author">
                            <a-avatar :src="author.avatar" />
                            {{ author.nickname }}
                        </span>
                        <!-- state -->
                        <span slot="state" slot-scope="state">
                            <a-tag v-if="state == 'wait'" color="red">未开始</a-tag>
                            <a-tag v-if="state == 'running'" color="green">进行中</a-tag>
                            <a-tag v-if="state == 'done'" color="gray">已结束</a-tag>
                        </span>
                    </a-table>
                </div>
            </div>
        </div>

        <Footer />

    </div>
</template>

<script>
import qs from 'qs'
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
            title: '标题',
            key: 'title',
            scopedSlots: { customRender: '_title' },
        }, {
            dataIndex: 'author',
            title: '讲座人',
            key: 'author',
        }, {
            title: '讲座地点',
            dataIndex: 'location',
            key: 'location',
        }, {
            title: '讲座日期',
            dataIndex: 'date',
            key: 'date',
        },
        {
            title: '讲座状态',
            dataIndex: 'state',
            key: 'state',
            scopedSlots: { customRender: 'state' },
        }],
        data: [{
            key: '1',
            title: 'John Brown',
            author: 'aaa',
            location: '三教',
            date: '111',
            state: 'running'
        }]
    }
  },
  async asyncData({ $axios }) {
    let userBaseInfo = null

    await $axios.get('getUserBaseInfo')
    .then((response) => {
        userBaseInfo = response.data
    })

    return {
        userBaseInfo: userBaseInfo,
    }
  },
  methods: {
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
