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
                            <a-button type="primary" @click="$router.push({ path: '/lose/new' })">发布失物</a-button>
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
                    <!-- List -->
                    <DynamicScroller
                        :items="loseList"
                        :min-item-size="50"
                        v-infinite-scroll="infiniteLoadList"
                        infinite-scroll-disabled="busy"
                        :infinite-scroll-distance="20"
                        style="width: 100%"
                    >
                        <template v-slot="{ item, index, active }">
                            <DynamicScrollerItem
                                :item="item"
                                :active="active"
                                :size-dependencies="[item]"
                                :data-index="index"
                                slot="renderItem"
                            >
                                <a-card hoverable style="width: 100%; margin-bottom: 20px" @click="$router.push({ path: '/lose/detail', query: { id: item.id } })">
                                    <p class="losetime">丢失时间：{{ item.date }}</p>
                                    <h2 v-if="item.isFound" class="found">已找到</h2>
                                    <h2 v-else class="notfound">未找到</h2>
                                    <a-card-meta
                                        :title="item.name"
                                        :description="item.description">
                                        <a-avatar slot="avatar" :src="baseUrl + item.avatar" />
                                    </a-card-meta>
                                    <img :src="baseUrl + item.cover" slot="cover" style="height: 200px" />
                                </a-card>
                            </DynamicScrollerItem>
                        </template>
                    </DynamicScroller>
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

        loseList: []
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
    infiniteLoadList() {
        this.loading = true
        this.$axios.post('getLoseList', qs.stringify({
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
