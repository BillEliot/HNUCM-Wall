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
                            <h1>求助墙</h1>
                            <p class="subheading">有问题找小伙伴们哦～</p>
                            <br />
                            <a-button type="primary" @click="$router.push({ path: '/help/new' })" style="margin-top: 20px">发布求助</a-button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div style="margin-top: 50px"></div>
        <!-- container -->
        <div class="container">
            <div class="row">
                <div class="col-md-12">
                    <!-- filter -->
                    <div class="filter">
                        <div class="filter">
                            <a-button @click="filterDate">时间<a-icon :type="type_date" /></a-button>
                        </div>
                    </div>
                    <a-spin :spinning="spinning">
                        <a-list
                            itemLayout="vertical"
                            :dataSource="helpList"
                            :pagination="pagination"
                            size="large"
                        >
                            <a-list-item slot="renderItem" slot-scope="item, index">
                                <span slot="actions">
                                    <a-icon type="message" /> {{ item.comments }}
                                </span>
                                <a slot="actions" @click="$router.push({ path: '/help/detail', query: { id: item.id } })">查看</a>
                                <div>
                                    <span>发布时间：{{ moment(item.date).format('lll') }}</span>
                                </div>
                                <a-list-item-meta :description="item.content">
                                    <a slot="title" @click="$router.push({ path: '/help/detail', query: { id: item.id } })">{{ item.title }}</a>
                                </a-list-item-meta>
                                <div class="avatar-card text-center">
                                    <a-avatar
                                        :size="64"
                                        :src="baseUrl + item.user.avatar"
                                        @click="$router.push({ path: '/profile', query: { uid: item.user.uid } })"
                                        class="avatar"
                                    />
                                    <br />
                                    <a @click="$router.push({ path: '/profile', query: { uid: item.user.uid } })">{{ item.user.nickname }}</a>
                                    <span>{{ item.user.bio }}</span>
                                </div>
                            </a-list-item>
                        </a-list>
                    </a-spin>
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
import { max } from 'moment'

export default {
  components: {
      Footer,
      navbar
  },
  data() {
    return {
        moment,

        spinning: false,
        filterType: '',
        order: 'normal',
        type_date: 'minus',

        pagination: {
            current: 1,
            pageSize: 10,
            total: 1,
            onChange(page) {
                if (this.current != page) {
                    this.current = page
                    this.spinning = true
                    $axios.post('getHelpList', qs.stringify({
                        filterType: this.filterType,
                        order: this.order,
                        index: page - 1
                    }))
                    .then((response) => {
                        this.spinning = false
                        if (response.data != 1) {
                            this.articleList = response.data.list
                            this.pagination.total = response.data.total
                        }
                    })
                }
            }
        }
    }
  },
  async asyncData({ $axios, error }) {
    let userBaseInfo = null
    let helpList = []
    let pagination = {}

    await $axios.get('getUserBaseInfo')
    .then((response) => {
        userBaseInfo = response.data
    })
    await $axios.post('getHelpList', qs.stringify({
        index: 0
    }))
    .then((response) => {
        if (response.data != 1) {
            helpList = response.data.list
            pagination.total = response.data.total
        }
        else {
            error({ statusCode: 500, message: '未知错误' })
        }
    })

    return {
        userBaseInfo: userBaseInfo,
        helpList: helpList,
        pagination: pagination
    }
  },
  methods: {
      filterDate() {
          this.isSearched = false
          this.spinning = true
          this.filterType = 'date'
          this.type_thumbsUp = 'minus'
          this.type_coin = 'minus'
          if (this.type_date == 'minus') {
              this.order = 'positive'
              this.type_date = 'up'
          }
          else if (this.type_date == 'up') {
              this.order = 'reverse'
              this.type_date = 'down'
          }
          else if (this.type_date == 'down') {
              this.order = 'positive'
              this.type_date = 'up'
          }
          this.getHelpList()
      },
      getHelpList() {
          this.$axios.post('getHelpList', qs.stringify({
              filterType: this.filterType,
              order: this.order,
              index: 0
          }))
          .then((response) => {
              this.spinning = false
              if (response.data != 1) {
                  this.helpList = response.data.list
                  this.pagination.total = response.data.total
              }
              else {
                  this.$message.error('未知错误')
              }
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

.avatar-card {
    float: right;
    width: 100px;
    height: 100px;
    margin-top: -32%;
}
.avatar {
    margin-top: 15px;
    cursor: pointer;
}

@media screen and (min-width: 992px) {
    .avatar-card {
        margin-top: -10%;
    }
}

.action {
    position: absolute;
    left: 0;
    bottom: 0;
}

.search-tag {
    margin-top: 10px;
}
</style>
