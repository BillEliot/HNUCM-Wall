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
                    <a-table :columns="columns" :dataSource="data">
                        <!-- title -->
                        <a slot="_title" slot-scope="text">{{ text }}</a>
                        <!-- author -->
                        <span slot="author" slot-scope="author">
                            <a-avatar :src="author.avatar" />
                            {{ author.nickname }}
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
            title: '发布者',
            key: 'author',
            scopedSlots: { customRender: 'author' },
        }, {
            title: '日期',
            dataIndex: 'date',
            key: 'date',
        }],
        data: [{
            key: '1',
            title: 'John Brown',
            author: { nickname: 'Eliot', avatar: '' },
            date: '111'
        }, {
            key: '2',
            title: 'Jim Green',
            author: { nickname: 'Eliot', avatar: '' }
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
