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
                            <h1>校园热点</h1>
                            <p class="subheading">吃第一口瓜～</p>
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
                    <a-table :columns="columns" :dataSource="hotList">
                        <!-- title -->
                        <router-link slot="_title" slot-scope="text, record" :to="{ path: '/hot/detail', query: { id: record.key }}">
                            {{ text }}
                        </router-link>
                        <!-- publisher -->
                        <span slot="publisher" slot-scope="publisher">
                            <a-avatar :src="baseUrl + publisher.avatar" />
                            <router-link :to="{ path: '/profile', query: { uid: publisher.uid }}">
                                {{ publisher.nickname }}
                            </router-link>
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
import navbar from '~/components/navbar'
import Footer from '~/components/footer.vue'
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
        },
        {
            dataIndex: 'publisher',
            title: '发布者',
            scopedSlots: { customRender: 'publisher' },
        },
        {
            dataIndex: 'date',
            title: '日期'
        }]
    }
  },
  async asyncData({ $axios }) {
    let userBaseInfo = null
    let hotList = []

    await $axios.get('getUserBaseInfo')
    .then((response) => {
        userBaseInfo = response.data
    })
    await $axios.get('getHotList')
    .then((response) => {
        hotList = response.data.info
    })

    return {
        userBaseInfo: userBaseInfo,
        hotList: hotList
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
