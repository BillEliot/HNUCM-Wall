<template>
    <div>
        <!-- drawer - more userto -->
        <a-drawer
            title="所有被表白人"
            placement="right"
            :width="300"
            :closable="false"
            @close="visibleMoreUserTo = false"
            :visible="visibleMoreUserTo"
            v-if="loveList.length > 0"
        >
            <div class="row">
                <div class="col-md-4 col-md-offset-4 col-xs-4 col-xs-offset-4 c text-center">
                    <div v-for="user in loveList[currentLoveIndex].userTo" :key="user.nickname">
                        <a-avatar v-if="user.uid == -1" :size="64" :src="baseUrl + user.avatar" />
                        <a-avatar v-else :size="64" :src="baseUrl + user.avatar" @click="$router.push({ path: '/profile', query: { uid: user.uid } })" style="cursor: pointer" />
                        <a v-if="user.uid == -1">{{ user.nickname }}</a>
                        <a v-else @click="$router.push({ path: '/profile', query: { uid: user.uid } })">{{ user.nickname }}</a>
                        <p class="bio">{{ user.bio }}</p>
                    </div>
                </div>
            </div>
        </a-drawer>
        <!-- navbar -->
        <navbar :userBaseInfo="userBaseInfo" />
        <!-- banner -->
        <div class="main-wrapper">
            <div class="page-title">
                <div class="container">
                    <div class="title-holder">
                        <div class="title-text text-center">
                            <h1>表白墙</h1>
                            <p class="subheading">ヾ(≧O≦)〃嗷~</p>
                            <br />
                            <a-button type="primary" @click="$router.push({ path: '/love/new' })" style="margin-top: 20px">我要表白</a-button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div style="margin-top: 50px"></div>
        <!-- container -->
        <div class="container">
            <div class="row">
                <div class="col-md-8 col-md-offset-2 col-xs-12">
                    <!-- Top -->
                    <a-card hoverable style="width: 100%; margin-bottom: 20px">
                        <a-card-meta
                            title="Nickname"
                            description="表白的话">
                        <a-avatar slot="avatar" src="https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png" />
                        </a-card-meta>
                        <img
                            src="https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png"
                            slot="cover"
                            style="height: 300px"
                        />
                    </a-card>
                    <!-- filter -->
                    <div class="filter">
                        <a-button @click="filterDate">时间<a-icon :type="type_date" /></a-button>
                        <a-button @click="filterThumbsUp">赞数<a-icon :type="type_thumbsUp" /></a-button>
                        <a-input-search
                            placeholder="搜索表白人"
                            @search="searchLoveFrom"
                            enterButton
                            style="width: 30%"
                        />
                        <a-input-search
                            placeholder="搜索被表白人"
                            @search="searchLoveTo"
                            enterButton
                            style="width: 30%"
                        />
                    </div>
                    <!-- List -->
                    <a-spin :spinning="spinning">
                        <RecycleScroller
                            v-if="hackReset"
                            :items="loveList"
                            :item-size="1"
                            v-slot="{ item, index }"
                            v-infinite-scroll="infiniteLoadList"
                            infinite-scroll-disabled="busy"
                            :infinite-scroll-distance="20"
                            style="height: 100%"
                            class="text-center"
                        >
                            <div style="margin-bottom: 20px;">
                                <a-row>
                                    <a-col :span="8">
                                        <a-avatar v-if="item.userFrom_uid == -1" :size="64" :src="baseUrl + item.userFrom_avatar" />
                                        <a-avatar v-else :size="64" :src="baseUrl + item.userFrom_avatar" @click="$router.push({ path: 'profile', query: { uid: item.userFrom_uid } })" style="cursor: pointer;" />
                                        <div>
                                            <a v-if="item.userFrom_uid == -1">匿名</a>
                                            <a v-else @click="$router.push({ path: 'profile', query: { uid: item.userFrom_uid } })">{{ item.userFrom_nickname }}</a>
                                            <p class="bio">{{ item.userFrom_bio }}</p>
                                        </div>
                                    </a-col>
                                    <a-col :span="8">
                                        <!-- placeholder -->
                                    </a-col>
                                    <a-col :span="8">
                                        <a-avatar v-if="item.userTo[0].uid == -1" :size="64" :src="baseUrl + item.userTo[0].avatar" />
                                        <a-avatar v-else :size="64" :src="baseUrl + item.userTo[0].avatar" @click="$router.push({ path: 'profile', query: { uid: item.userTo[0].uid } })" style="cursor: pointer;" />
                                        <a-avatar v-if="item.userTo.length > 1" :size="64" @click="moreUserTo(index)" class="more-avatar">更多</a-avatar>
                                        <div>
                                            <a v-if="item.userTo[0].uid == -1">{{ item.userTo[0].nickname }}</a>
                                            <a v-else @click="$router.push({ path: 'profile', query: { uid: item.userTo[0].uid } })">{{ item.userTo[0].nickname }}</a>
                                            <p class="bio">{{ item.userTo[0].bio }}</p>
                                        </div>
                                    </a-col>
                                </a-row>

                                <p class="content">{{ item.content }}</p>
                                <img v-if="item.cover" style="width: 60%; margin-bottom: 10px;" :src="baseUrl + item.cover" @click="previewCover=true" />
                                <a-modal v-model="previewCover" :footer="null">
                                    <img style="width: 100%" :src="baseUrl + item.cover">
                                </a-modal>
                                <br />

                                <a-row>
                                    <a-col :span="8">
                                        <span style="fontSize: 24px">
                                            <a-icon type="like-o" :theme="item.isThumbsUp ? 'filled' : 'outlined'" @click="ThumbsUp(item)" style="cursor: pointer;" /> {{ item.thumbsUp }}
                                        </span>
                                    </a-col>
                                    <a-col :span="8">
                                        <a-button style="width: 100%" @click="$router.push({ path: '/love/detail', query: { id: item.id } })">
                                            <a-icon type="heart" />戳进去<a-icon type="heart" />
                                        </a-button>
                                    </a-col>
                                    <a-col :span="8">
                                        <span style="fontSize: 24px">
                                            <a-icon type="message" /> {{ item.comments }}
                                        </span>
                                    </a-col>
                                </a-row>
                                <hr />
                            </div>
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
        loveList: [],

        isSearched: false,
        filterType: '',
        order: 'normal',
        type_date: 'minus',
        type_thumbsUp: 'minus',

        visibleMoreUserTo: false,
        currentLoveIndex: 0
    }
  },
  async asyncData({ $axios }) {
    let userBaseInfo = null
    let loveList = []

    await $axios.get('getUserBaseInfo')
    .then((response) => {
        userBaseInfo = response.data
    })

    await $axios.post('getLoveList', qs.stringify({
        index: '0',
        uid: userBaseInfo.uid
    }))
    .then((response) => {
        loveList = response.data.info
    })

    return {
        userBaseInfo: userBaseInfo,
        loveList: loveList
    }
  },
  methods: {
    filterDate() {
        this.isSearched = false
        this.spinning = true
        this.filterType = 'date'
        this.type_thumbsUp = 'minus'
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
        this.loveList = []
        this.infiniteLoadList()
    },
    filterThumbsUp() {
        this.isSearched = false
        this.spinning = true
        this.filterType = 'thumbsUp'
        this.type_date = 'minus'
        if (this.type_thumbsUp == 'minus') {
            this.order = 'positive'
            this.type_thumbsUp = 'up'
        }
        else if (this.type_thumbsUp == 'up') {
            this.order = 'reverse'
            this.type_thumbsUp = 'down'
        }
        else if (this.type_thumbsUp == 'down') {
            this.order = 'positive'
            this.type_thumbsUp = 'up'
        }
        this.loveList = []
        this.infiniteLoadList()
    },
    searchLoveFrom(value) {
        if (!!value) {
            this.spinning = true
            this.isSearched = true
            this.$axios.post('searchLoveItem', qs.stringify({
                name: value,
                object: 'from'
            }))
            .then((response) => {
                this.spinning = false
                if (response.data == 1) {
                    this.$message.error('未知错误')
                }
                else {
                    this.type_date = 'minus'
                    this.type_thumbsUp = 'minus'
                    this.loveList = response.data.info
                    // hack reset
                    this.hackReset = false
                    this.$nextTick(() => {
                        this.hackReset = true
                    })
                    this.$notification.open({
                        message: '搜索结果',
                        description: `共搜索到 ${this.loveList.length} 条结果`,
                        icon: <a-icon type="smile" style="color: #108ee9" />,
                        duration: 0
                    })
                }
            })
        }
        else {
            this.$message.warning('输入要搜索的人吧～')
        }
    },
    searchLoveTo(value) {
        if (!!value) {
            this.spinning = true
            this.isSearched = true
            this.$axios.post('searchLoveItem', qs.stringify({
                name: value,
                object: 'to'
            }))
            .then((response) => {
                this.spinning = false
                if (response.data == 1) {
                    this.$message.error('未知错误')
                }
                else {
                    this.type_date = 'minus'
                    this.type_thumbsUp = 'minus'
                    this.loveList = response.data.info
                    // hack reset
                    this.hackReset = false
                    this.$nextTick(() => {
                        this.hackReset = true
                    })
                    this.$notification.open({
                        message: '搜索结果',
                        description: `共搜索到 ${this.loveList.length} 条结果`,
                        icon: <a-icon type="smile" style="color: #108ee9" />,
                        duration: 0
                    })
                }
            })
        }
        else {
            this.$message.warning('输入要搜索的人吧～')
        }
    },
    infiniteLoadList() {
        this.loading = true
        this.$axios.post('getLoveList', qs.stringify({
            filterType: this.filterType,
            order: this.order,
            index: this.loveList.length,
            uid: this.userBaseInfo.uid
        }))
        .then((response) => {
            this.loading = false
            this.spinning = false
            if (response.data.info.length == 0) {
                this.busy = true
                this.$message.warning('到底啦～')
            }
            else {
                this.loveList = this.loveList.concat(response.data.info)
            }
        })
    },
    ThumbsUp(item) {
        if (this.userBaseInfo.uid == -1) {
            this.$message.warning('先登录吧～')
        }
        else {
            if (item.isThumbsUp) {
                item.isThumbsUp = false
                item.thumbsUp -= 1
                this.$axios.post('thumbsUpLove', qs.stringify({
                    id: item.id,
                    isThumbsUp: false,
                    uid: this.userBaseInfo.uid
                }))
            }
            else {
                item.isThumbsUp = true
                item.thumbsUp += 1
                this.$axios.post('thumbsUpLove', qs.stringify({
                    id: item.id,
                    isThumbsUp: true,
                    uid: this.userBaseInfo.uid
                }))
            }
        }
    },
    moreUserTo(index) {
        this.visibleMoreUserTo = true
        this.currentLoveIndex = index
    },
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

.more-avatar {
    cursor: pointer;
    color: white;
}
.more-avatar:hover {
    color: blueviolet;
}

.content {
    border: 1px dashed gray;
    padding: 10px;
    font-size: large
}

.loading {
  position: absolute;
  bottom: 40px;
  width: 100%;
  text-align: center;
}

.filter {
    margin-bottom: 50px;
}
</style>
