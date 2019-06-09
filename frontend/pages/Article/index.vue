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
                            <h1>大佬杂谈</h1>
                            <p class="subheading">都是些有用的文章哦～</p>
                            <br />
                            <a-button type="primary" @click="$router.push({ path: '/article/new' })" style="margin-top: 20px">发布文章</a-button>
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
                            <a-button>发布时间<a-icon type="minus" /></a-button>
                            <a-button>赞数<a-icon type="minus" /></a-button>
                            <a-button>硬币数<a-icon type="minus" /></a-button>
                            <a-input-search
                                placeholder="搜索文章"
                                @search="searchArticle"
                                enterButton
                                style="width: 35%"
                            />
                            <a-input-search
                                placeholder="搜索用户"
                                @search="searchUser"
                                enterButton
                                style="width: 35%"
                            />
                        </div>
                    </div>
                    <a-list
                        itemLayout="vertical"
                        :dataSource="articleList"
                        :pagination="pagination"
                        size="large"
                    >
                        <a-list-item slot="renderItem" slot-scope="item, index">
                            <span slot="actions">需要硬币： {{ item.neededCoin }}</span>
                            <span slot="actions">
                                <a-icon type="like-o" /> 122
                            </span>
                            <span slot="actions">
                                <a-icon type="message" /> 289
                            </span>
                            <a slot="actions">查看</a>
                            <div>
                                <span>发布时间：{{ item.publicDate }}</span>
                                <br />
                                <span>最后编辑：{{ item.publicDate }}</span>
                            </div>
                            <a-list-item-meta :description="item.content">
                                <a slot="title">{{ item.title }}</a>
                                <a-popover slot="avatar" :title="item.nickname">
                                    <template slot="content">
                                        <p>{{ item.bio }}</p>
                                    </template>
                                    <a-avatar :src="baseUrl + item.avatar" class="avatar" />
                                </a-popover>
                            </a-list-item-meta>
                        </a-list-item>
                    </a-list>
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
    }
  },
  async asyncData({ $axios }) {
    let userBaseInfo = null
    let articleList = []
    let pagination = {
        current: 1,
        total: 100,
        onChange(page) {
            this.current = page
        }
    }

    await $axios.get('getUserBaseInfo')
    .then((response) => {
        userBaseInfo = response.data
    })
    await $axios.post('getArticleList', qs.stringify({
        index: 1
    }))
    .then((response) => {
        if (response.data != 1) {
            articleList = response.data.list
            pagination.total = response.data.total
        }
        else {
            this.$message.error('未知错误')
        }
    })

    return {
        userBaseInfo: userBaseInfo,
        articleList: articleList,
        pagination: pagination
    }
  },
  methods: {
      searchArticle() {

      },
      searchUser() {
          
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

.avatar {
    margin-top: 15px;
    cursor: pointer;
}

.action {
    position: absolute;
    left: 0;
    bottom: 0;
}
</style>
