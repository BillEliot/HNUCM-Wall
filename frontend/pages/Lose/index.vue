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
                            <a-input-search
                                placeholder="搜索物品"
                                @search="searchItem"
                                enterButton
                                style="width: 30%"
                            />
                        </div>
                    </div>
                    <!-- List -->
                    <RecycleScroller
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
        loseList: [],
        filterName: '',
        order: 'normal',
        type_loseTime: 'minus',
        type_publicTime: 'minus'
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
        this.filterName = 'loseTime'
        this.type_publicTime = 'minus'
        if (this.type_loseTime == 'minus') {
            this.order = 'reverse'
            this.type_loseTime = 'down'
            this.loseList = []
            this.infiniteLoadList()
        }
        else if (this.type_loseTime == 'up') {
            this.order = 'reverse'
            this.type_loseTime = 'down'
            this.loseList = []
            this.infiniteLoadList()
        }
        else if (this.type_loseTime == 'down') {
            this.order = 'positive'
            this.type_loseTime = 'up'
            this.loseList = []
            this.infiniteLoadList()
        }
    },
    filterPublicTime() {
        this.filterName = 'publicTime'
        this.type_loseTime = 'minus'
        if (this.type_publicTime == 'minus') {
            this.order = 'positive'
            this.type_publicTime = 'up'
            this.loseList = []
            this.infiniteLoadList()
        }
        else if (this.type_publicTime == 'up') {
            this.order = 'reverse'
            this.type_publicTime = 'down'
            this.loseList = []
            this.infiniteLoadList()
        }
        else if (this.type_publicTime == 'down') {
            this.order = 'positive'
            this.type_publicTime = 'up'
            this.loseList = []
            this.infiniteLoadList()
        }
    },
    searchItem() {
        
    },
    infiniteLoadList() {
        this.loading = true
        this.$axios.post('getLoseList', qs.stringify({
            filterName: this.filterName,
            order: this.order,
            index: this.loseList.length
        }))
        .then((response) => {
            this.loading = false
            if (response.data.info.length == 0) {
                this.busy = true
                this.$message.warning('到底啦～')
            }
            else {
                this.loseList = this.loseList.concat(response.data.info)
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
