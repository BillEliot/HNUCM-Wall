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
                            <h1>失物墙</h1>
                            <p class="subheading">失物们都回来吧～</p>
                            <br />
                            <a-button type="primary" @click="$router.push({ path: '/lose/new' })" style="margin-top: 20px">发布失物</a-button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div style="margin-top: 50px"></div>
        <!-- container -->
        <div class="container">
            <div class="row">
                <div class="col-md-6 col-md-offset-3 col-xs-12">
                    <!-- filter -->
                    <div class="filter">
                        <div class="filter">
                            <a-button @click="filterLoseTime">丢失时间<a-icon :type="type_loseTime" /></a-button>
                            <a-button @click="filterPublicTime">发布时间<a-icon :type="type_publicTime" /></a-button>
                            <a-button @click="filterFound">是否找到<a-icon :type="type_isFound" /></a-button>
                            <a-input-search
                                placeholder="搜索物品"
                                @search="searchItem"
                                enterButton
                                style="width: 35%"
                            />
                        </div>
                    </div>
                    <!-- List -->
                    <a-spin :spinning="spinning">
                        <RecycleScroller
                            v-if="hackReset"
                            :items="loseList"
                            :item-size="1"
                            key-field="id"
                            v-slot="{ item }"
                            v-infinite-scroll="infiniteLoadList"
                            infinite-scroll-disabled="busy"
                            :infinite-scroll-distance="20"
                            style="height: 100%"
                        >
                            <a-card hoverable @click="$router.push({ path: '/lose/detail', query: { id: item.id } })" style="margin-bottom: 20px">
                                <p class="losetime">丢失时间：{{ item.loseDate }}</p>
                                <h2 v-if="item.isFound" class="found">已找到</h2>
                                <h2 v-else class="notfound">未找到</h2>
                                <a-card-meta
                                    :title="item.name"
                                    :description="item.description">
                                    <a-avatar slot="avatar" :src="baseUrl + item.avatar" />
                                </a-card-meta>
                                <img :src="baseUrl + item.cover" slot="cover" style="height: 200px" />
                            </a-card>
                        </RecycleScroller>
                    </a-spin>
                    <a-spin v-if="loading" class="loading" />
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
        hackReset: true,
        loading: false,
        spinning: false,
        busy: false,
        previewCover: false,
        loseList: [],

        isSearched: false,
        filterType: '',
        order: 'normal',
        type_loseTime: 'minus',
        type_publicTime: 'minus',
        type_isFound: 'minus'
    }
  },
  async asyncData({ $axios }) {
    let userBaseInfo = null
    let loseList = []

    await $axios.get('getUserBaseInfo')
    .then((response) => {
        userBaseInfo = response.data
    })

    await $axios.post('getLoseList', qs.stringify({
        index: '0'
    }))
    .then((response) => {
        loseList = response.data.info
    })

    return {
        userBaseInfo: userBaseInfo,
        loseList: loseList
    }
  },
  methods: {
    filterLoseTime() {
        this.isSearched = false
        this.spinning = true
        this.filterType = 'loseTime'
        this.type_publicTime = 'minus'
        this.type_isFound = 'minus'
        if (this.type_loseTime == 'minus') {
            this.order = 'reverse'
            this.type_loseTime = 'down'
        }
        else if (this.type_loseTime == 'up') {
            this.order = 'reverse'
            this.type_loseTime = 'down'
        }
        else if (this.type_loseTime == 'down') {
            this.order = 'positive'
            this.type_loseTime = 'up'
        }
        this.loseList = []
        this.infiniteLoadList()
    },
    filterPublicTime() {
        this.isSearched = false
        this.spinning = true
        this.filterType = 'publicTime'
        this.type_loseTime = 'minus'
        this.type_isFound = 'minus'
        if (this.type_publicTime == 'minus') {
            this.order = 'positive'
            this.type_publicTime = 'up'
        }
        else if (this.type_publicTime == 'up') {
            this.order = 'reverse'
            this.type_publicTime = 'down'
        }
        else if (this.type_publicTime == 'down') {
            this.order = 'positive'
            this.type_publicTime = 'up'
        }
        this.loseList = []
        this.infiniteLoadList()
    },
    filterFound() {
        this.isSearched = false
        this.spinning = true
        this.filterType = 'isFound'
        this.type_loseTime = 'minus'
        this.type_publicTime = 'minus'
        if (this.type_isFound == 'minus') {
            this.order = 'positive'
            this.type_isFound = 'up'
        }
        else if (this.type_isFound == 'up') {
            this.order = 'reverse'
            this.type_isFound = 'down'
        }
        else if (this.type_isFound == 'down') {
            this.order = 'positive'
            this.type_isFound = 'up'
        }
        this.loseList = []
        this.infiniteLoadList()
    },
    searchItem(value) {
        if (!!value) {
            this.spinning = true
            this.isSearched = true
            this.$axios.post('searchLoseItem', qs.stringify({
                name: value
            }))
            .then((response) => {
                this.spinning = false
                if (response.data == 1) {
                    this.$message.error('未知错误')
                }
                else {
                    this.type_loseTime = 'minus'
                    this.type_publicTime = 'minus'
                    this.loseList = response.data.info
                    // hack reset
                    this.hackReset = false
                    this.$nextTick(() => {
                        this.hackReset = true
                    })
                    this.$notification.open({
                        message: '搜索结果',
                        description: `共搜索到 ${this.loseList.length} 条结果`,
                        icon: <a-icon type="smile" style="color: #108ee9" />,
                        duration: 0
                    })
                }
            })
        }
        else {
            this.$message.warning('输入要搜索的物品吧～')
        }
    },
    infiniteLoadList() {
        if (!this.isSearched) {
            this.loading = true
            this.$axios.post('getLoseList', qs.stringify({
                filterType: this.filterType,
                order: this.order,
                index: this.loseList.length
            }))
            .then((response) => {
                this.loading = false
                this.spinning = false
                if (response.data.info.length == 0) {
                    this.busy = true
                    this.$message.warning('到底啦～')
                }
                else {
                    this.loseList = this.loseList.concat(response.data.info)
                }
            })
        }
    }
  },
  computed: mapState({
      baseUrl: state => state.baseUrl
  })
}
</script>

<style scoped>
.filter {
    margin-bottom: 30px;
}

.loading {
  position: absolute;
  bottom: 40px;
  width: 100%;
  text-align: center;
}

.found {
    margin-top: 0;
    float: right;
    color: green;
    font-weight: bold;
}
.notfound {
    margin-top: 0;
    float: right;
    color: red;
    font-weight: bold;
}
.losetime {
    color: indigo;
    font-weight: bold;
}
</style>
