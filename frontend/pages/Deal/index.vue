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
                            <h1>二手墙</h1>
                            <p class="subheading">旧东西们都复活吧～</p>
                            <br />
                            <a-button type="primary" @click="$router.push({ path: '/deal/new' })">发布物品</a-button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div style="margin-top: 50px"></div>
        <!-- container -->
        <div class="container">
            <div class="row">
                <div class="col-md-6 col-md-offset-3 col-sm-12">
                    <div class="filter">
                        <a-button>时间<a-icon type="minus" /></a-button>
                        <a-button>新度<a-icon type="minus" /></a-button>
                        <a-button>价格<a-icon type="minus" /></a-button>
                        <a-button>售出<a-icon type="minus" /></a-button>
                        <a-input-search
                            placeholder="搜索物品"
                            @search="searchItem"
                            enterButton
                            style="width: 30%"
                        />
                    </div>
                    <!-- List -->
                    <RecycleScroller
                        :items="dealList"
                        :item-size="20"
                        v-slot="{ item }"
                        v-infinite-scroll="infiniteLoadList"
                        infinite-scroll-disabled="busy"
                        :infinite-scroll-distance="20"
                        style="height: 100%"
                    >
                        <a-card hoverable @click="$router.push({ path: '/deal/detail', query: { id: item.id } })">
                            <p class="price">最低价：¥ {{ item.price }}</p>
                            <div class="info">
                                <span class="new">
                                    <a-rate :defaultValue="item.new" disabled :count="2.5" /> {{ item.new*2 }} 成新
                                </span>
                                <br />
                                <h2 v-if="item.isFound" class="sold">已售出</h2>
                                <h2 v-else class="notsold">未售出</h2>
                            </div>
                            <a-card-meta
                                :title="item.name"
                                :description="item.description">
                                <a-avatar slot="avatar" :src="baseUrl + item.avatar" />
                            </a-card-meta>
                            <img :src="baseUrl + item.cover" slot="cover" style="height: 200px" />
                        </a-card>
                    </RecycleScroller>
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
        loading: false,
        busy: false,
        previewCover: false,
        dealList: []
    }
  },
  async asyncData({ $axios }) {
    let userBaseInfo = null
    let dealList = []

    await $axios.get('getUserBaseInfo')
    .then((response) => {
        userBaseInfo = response.data
    })

    await $axios.post('getDealList', qs.stringify({
        index: '0'
    }))
    .then((response) => {
        dealList = response.data.info
    })

    return {
        userBaseInfo: userBaseInfo,
        dealList: dealList
    }
  },
  methods: {
    searchItem() {

    },
    infiniteLoadList() {
        this.loading = true
        this.$axios.post('getDealList', qs.stringify({
            index: this.dealList.length
        }))
        .then((response) => {
            this.loading = false
            if (response.data.info.length == 0) {
                this.busy = true
                this.$message.warning('到底啦～')
            }
            else {
                this.dealList = this.dealList.concat(response.data.info)
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
.filter {
    margin-bottom: 50px;
}

.loading {
  position: absolute;
  bottom: 40px;
  width: 100%;
  text-align: center;
}

.info {
    margin-top: -25px;
    float: right;
}
.sold {
    margin-top: 0;
    float: right;
    color: green;
    font-weight: bold;
}
.notsold {
    margin-top: 0;
    float: right;
    color: red;
    font-weight: bold;
}
.price {
    color: indigo;
    font-weight: bold;
}
.new {
    color: darkgreen;
    font-size: 15px;
    font-weight: bold;
}
</style>
