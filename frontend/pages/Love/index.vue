<template>
    <div>
        <!-- drawer - more userto -->
        <a-drawer
            v-if="loveList.length > 0"
            title="所有被表白人"
            placement="right"
            :width="300"
            :closable="false"
            @close="visibleMoreUserTo = false"
            :visible="visibleMoreUserTo"
        >
            <div class="row">
                <div class="col-md-4 col-md-offset-4 col-xs-4 col-xs-offset-4 c text-center">
                    <div v-for="user in loveList[currentLoveIndex].userTo" :key="user.username">
                        <a-avatar v-if="user.id == -1" :size="64" :src="baseUrl + '/media/' + user.avatar" />
                        <a-avatar v-else :size="64" :src="baseUrl + '/media/' + user.avatar" @click="$router.push({ path: '/profile', query: { id: user.id } })" style="cursor: pointer" />
                        <a v-if="user.id == -1">{{ user.username }}</a>
                        <a v-else @click="$router.push({ path: '/profile', query: { id: user.id } })">{{ user.username }}</a>
                        <p class="bio">{{ user.bio }}</p>
                    </div>
                </div>
            </div>
        </a-drawer>
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
                    <div class="text-center top">
                        <a-row>
                            <a-col :span="8">
                                <a-avatar v-if="top_love.userFrom_id == -1" :size="64" :src="baseUrl + top_love.userFrom_avatar" />
                                <a-avatar v-else :size="64" :src="baseUrl + top_love.userFrom_avatar" @click="$router.push({ path: '/profile', query: { id: top_love.userFrom_id } })" style="cursor: pointer;" />
                                <div>
                                    <a v-if="top_love.userFrom_id == -1">等待上榜</a>
                                    <a v-else @click="$router.push({ path: '/profile', query: { id: top_love.userFrom_id } })">{{ top_love.userFrom_username }}</a>
                                    <p class="bio">{{ top_love.userFrom_bio }}</p>
                                </div>
                            </a-col>
                            <a-col :span="8" :offset="8">
                                <a-avatar v-if="top_love.userTo[0].id == -1" :size="64" :src="baseUrl + '/media/' + top_love.userTo[0].avatar" />
                                <a-avatar v-else :size="64" :src="baseUrl + '/media/' + top_love.userTo[0].avatar" @click="$router.push({ path: '/profile', query: { id: top_love.userTo[0].id } })" style="cursor: pointer;" />
                                <a-avatar v-if="top_love.userTo.length > 1" :size="64" @click="moreUserTo(index)" class="more-avatar">更多</a-avatar>
                                <div>
                                    <a v-if="top_love.userTo[0].id == -1">{{ top_love.userTo[0].username }}</a>
                                    <a v-else @click="$router.push({ path: '/profile', query: { id: top_love.userTo[0].id } })">{{ top_love.userTo[0].username }}</a>
                                    <p class="bio">{{ top_love.userTo[0].bio }}</p>
                                </div>
                            </a-col>
                        </a-row>
                        <!-- content -->
                        <p class="content">{{ top_love.content }}</p>
                        <div class="text-center">
                            <a-carousel arrows style="display: inline-block; width: 400px">
                                <div
                                    slot="prevArrow"
                                    slot-scope="props"
                                    class="custom-slick-arrow"
                                    style="left: 10px; zIndex: 1"
                                >
                                    <a-icon type="left-circle" />
                                </div>
                                <div
                                    slot="nextArrow"
                                    slot-scope="props"
                                    class="custom-slick-arrow"
                                    style="right: 10px"
                                >
                                    <a-icon type="right-circle" />
                                </div>
                                <img v-for="(image, index) in top_love.images" :key="index" :src="baseUrl + '/media/' + image" />
                            </a-carousel>
                        </div>
                        <br />

                        <a-row v-if="top_love.id != -1">
                            <a-col :span="8">
                                <span style="fontSize: 24px">
                                    <a-icon type="like-o" :theme="top_love.isThumbsUp ? 'filled' : 'outlined'" @click="ThumbsUp(top_love)" style="cursor: pointer;" /> {{ top_love.thumbsUp }}
                                </span>
                            </a-col>
                            <a-col :span="8">
                                <a-button style="width: 100%" type="danger" @click="$router.push({ path: '/love/detail', query: { id: top_love.id } })">
                                    <a-icon type="heart" />进去看看<a-icon type="heart" />
                                </a-button>
                            </a-col>
                            <a-col :span="8">
                                <span style="fontSize: 24px">
                                    <a-icon type="message" /> {{ top_love.comments }}
                                </span>
                            </a-col>
                            <span style="color: gray">{{ moment(top_love.date).format('lll') }}</span>
                        </a-row>
                    </div>
                    <hr />
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
                            :items="loveList"
                            :item-size="32"
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
                                        <a-avatar v-if="item.userFrom_id == -1" :size="64" :src="baseUrl + item.userFrom_avatar" />
                                        <a-avatar v-else :size="64" :src="baseUrl + item.userFrom_avatar" @click="$router.push({ path: '/profile', query: { id: item.userFrom_id } })" style="cursor: pointer;" />
                                        <div>
                                            <a v-if="item.userFrom_id == -1">匿名</a>
                                            <a v-else @click="$router.push({ path: '/profile', query: { id: item.userFrom_id } })">{{ item.userFrom_username }}</a>
                                            <p class="bio">{{ item.userFrom_bio }}</p>
                                        </div>
                                    </a-col>
                                    <a-col :span="8" :offset="8">
                                        <a-avatar v-if="item.userTo[0].id == -1" :size="64" :src="baseUrl + '/media/' + item.userTo[0].avatar" />
                                        <a-avatar v-else :size="64" :src="baseUrl + '/media/' + item.userTo[0].avatar" @click="$router.push({ path: '/profile', query: { id: item.userTo[0].id } })" style="cursor: pointer;" />
                                        <a-avatar v-if="item.userTo.length > 1" :size="64" @click="moreUserTo(index)" class="more-avatar">更多</a-avatar>
                                        <div>
                                            <a v-if="item.userTo[0].id == -1">{{ item.userTo[0].username }}</a>
                                            <a v-else @click="$router.push({ path: '/profile', query: { id: item.userTo[0].id } })">{{ item.userTo[0].username }}</a>
                                            <p class="bio">{{ item.userTo[0].bio }}</p>
                                        </div>
                                    </a-col>
                                </a-row>
                                <!-- content -->
                                <p class="content">{{ item.content }}</p>
                                <div class="text-center">
                                    <a-carousel arrows style="display: inline-block; width: 400px">
                                        <div
                                            slot="prevArrow"
                                            slot-scope="props"
                                            class="custom-slick-arrow"
                                            style="left: 10px; zIndex: 1"
                                        >
                                            <a-icon type="left-circle" />
                                        </div>
                                        <div
                                            slot="nextArrow"
                                            slot-scope="props"
                                            class="custom-slick-arrow"
                                            style="right: 10px"
                                        >
                                            <a-icon type="right-circle" />
                                        </div>
                                        <img v-for="(image, index) in item.images" :key="index" :src="baseUrl + '/media/' + image" />
                                    </a-carousel>
                                </div>
                                <br />

                                <a-row>
                                    <a-col :span="8">
                                        <span style="fontSize: 24px">
                                            <a-icon type="like-o" :theme="item.isThumbsUp ? 'filled' : 'outlined'" @click="ThumbsUp(item)" style="cursor: pointer;" /> {{ item.thumbsUp }}
                                        </span>
                                    </a-col>
                                    <a-col :span="8">
                                        <a-button style="width: 100%" type="primary" @click="$router.push({ path: '/love/detail', query: { id: item.id } })">
                                            <a-icon type="heart" />进去看看<a-icon type="heart" />
                                        </a-button>
                                    </a-col>
                                    <a-col :span="8">
                                        <span style="fontSize: 24px">
                                            <a-icon type="message" /> {{ item.comments }}
                                        </span>
                                    </a-col>
                                    <span style="color: gray">{{ moment(item.date).format('lll') }}</span>
                                </a-row>
                                <hr />
                            </div>
                        </RecycleScroller>
                    </a-spin>
                    <a-spin v-if="loading" class="loading" />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import qs from 'qs'
import { mapState } from 'vuex'
import moment from 'moment'

export default {
  layout: 'common',
  data() {
    return {
        moment,

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
  async asyncData({ $axios, app }) {
    let loveList = []
    let top_love = null

    await $axios.get('getLoveList', {
        params: {
            page_number: 1
        }
    })
    .then((response) => {
        if (response.data.code == 200 && response.data.status == 'success') {
            top_love = response.data.data.top
            loveList = response.data.data.list
        }
    })

    return {
        loveList: loveList,
        top_love: top_love
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
            this.$axios.get('searchLoveItem', {
                params: {
                    name: value,
                    object: 'from'
                }
            })
            .then((response) => {
                this.spinning = false
                if (response.data.code == 200 && response.data.status == 'success') {
                    this.type_date = 'minus'
                    this.type_thumbsUp = 'minus'
                    // hack reset
                    this.loveList = []
                    this.$nextTick(() => {
                        this.loveList = response.data.data
                    })
                    this.$notification.open({
                        message: '搜索结果',
                        description: `共搜索到 ${response.data.data.length} 条结果`,
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
            this.$axios.get('searchLoveItem', {
                params: {
                    name: value,
                    object: 'to'
                }
            })
            .then((response) => {
                this.spinning = false
                if (response.data.code == 200 && response.data.status == 'success') {
                    this.type_date = 'minus'
                    this.type_thumbsUp = 'minus'
                    this.loveList = []
                    this.$nextTick(() => {
                        this.loveList = response.data.data
                    })
                    this.$notification.open({
                        message: '搜索结果',
                        description: `共搜索到 ${response.data.data.length} 条结果`,
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
        this.$axios.get('getLoveList', {
            params: {
                page_number: Math.ceil(this.loveList.length / 10 + 1),
                filterType: this.filterType,
                order: this.order
            }
        })
        .then((response) => {
            this.loading = false
            this.spinning = false
            if (response.data.code == 200) {
                if (response.data.status == 'success') {
                    this.loveList = this.loveList.concat(response.data.data.list)
                }
                else if (response.data.status == 'none') {
                    this.busy = true
                    this.$message.warning('到底啦～')
                }
            }
        })
    },
    ThumbsUp(item) {
        if (this.userBaseInfo.id == -1) {
            this.$message.warning('先登录吧～')
        }
        else {
            if (item.isThumbsUp) {
                item.isThumbsUp = false
                item.thumbsUp -= 1
                this.$axios.post('thumbsUpLove', qs.stringify({
                    id: item.id,
                    isThumbsUp: false,
                }))
            }
            else {
                item.isThumbsUp = true
                item.thumbsUp += 1
                this.$axios.post('thumbsUpLove', qs.stringify({
                    id: item.id,
                    isThumbsUp: true,
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
      baseUrl: state => state.baseUrl,
      userBaseInfo: state => state.userBaseInfo
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

.top {
    border: 1px dashed;
    border-radius: 10px;
    padding: 20px;
}

.content {
    border: 1px solid;
    border-radius: 15px;
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

.ant-carousel >>> .custom-slick-arrow {
  width: 25px;
  height: 25px;
  font-size: 25px;
  color: #fff;
  background-color: rgba(31, 45, 61, 0.11);
  opacity: 0.3;
}
.ant-carousel >>> .custom-slick-arrow:before {
  display: none;
}
.ant-carousel >>> .custom-slick-arrow:hover {
  opacity: 0.5;
}
</style>
