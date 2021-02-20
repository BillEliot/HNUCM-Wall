<template>
    <div>
        <!-- banner -->
        <div class="main-wrapper">
            <div class="page-title">
                <div class="container">
                    <div class="title-holder">
                        <div class="title-text text-center">
                            <h1>二手墙</h1>
                            <p class="subheading">旧东西们都复活吧～</p>
                            <br />
                            <a-button type="primary" @click="$router.push({ path: '/deal/new' })" style="margin-top: 20px">发布物品</a-button>
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
                        <a-button @click="filterDate">时间<a-icon :type="type_date" /></a-button>
                        <a-button @click="filterNew">新度<a-icon :type="type_new" /></a-button>
                        <a-button @click="filterPrice">价格<a-icon :type="type_price" /></a-button>
                        <a-button @click="filterSold">售出<a-icon :type="type_isSold" /></a-button>
                        <a-input-search
                            placeholder="搜索物品"
                            @search="searchItem"
                            enterButton
                            style="width: 30%"
                        />
                    </div>
                    <!-- List -->
                    <a-spin :spinning="spinning">
                        <RecycleScroller
                            :items="dealList"
                            :item-size="1"
                            v-slot="{ item }"
                            v-infinite-scroll="infiniteLoadList"
                            infinite-scroll-disabled="busy"
                            :infinite-scroll-distance="20"
                            style="height: 100%"
                        >
                            <a-card hoverable @click="$router.push({ path: '/deal/detail', query: { id: item.id } })" style="margin-bottom: 20px">
                                <p class="price">最低价：¥ {{ item.price }}</p>
                                <div class="info">
                                    <span class="new">
                                        <a-rate :defaultValue="item.new" allowHalf :tooltips="desc" disabled /> {{ item.new * 2 }} 成新
                                    </span>
                                    <br />
                                    <h2 v-if="item.isFound" class="sold">已售出</h2>
                                    <h2 v-else class="notsold">未售出</h2>
                                </div>
                                <a-card-meta
                                    :title="item.name"
                                    :description="item.description"
                                >
                                    <div slot="avatar" class="text-center">
                                        <a-avatar :src="baseUrl + item.user.avatar" @click="this.$router.push({ path: '/profile', query: { id: item.user.id } })" />
                                        <br />
                                        <nuxt-link :to="{ path: '/profile', query: { id: item.user.id } }">{{ item.user.username }}</nuxt-link>
                                    </div>
                                </a-card-meta>
                                <img :src="baseUrl + item.cover" slot="cover" style="height: 200px" />
                            </a-card>
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

export default {
  layout: 'common',
  data() {
    return {
        desc: ['糟糕', '破损', '一般', '陈旧', '极好'],
        loading: false,
        spinning: false,
        busy: false,
        previewCover: false,
        dealList: [],

        filterType: '',
        order: 'normal',
        type_date: 'minus',
        type_new: 'minus',
        type_price: 'minus',
        type_isSold: 'minus'
    }
  },
  async asyncData({ $axios }) {
    let dealList = []

    await $axios.get('getDealList', {
        params: {
            page_number: 1
        }
    })
    .then((response) => {
        if (response.data.code == 200 && response.data.status == 'success') {
            dealList = response.data.data
        }
    })

    return {
        dealList: dealList
    }
  },
  methods: {
    filterDate() {
        this.spinning = true
        this.filterType = 'date'
        this.type_new = 'minus'
        this.type_price = 'minus'
        this.type_isSold = 'minus'
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
        this.dealList = []
        this.infiniteLoadList()
    },
    filterNew() {
        this.spinning = true
        this.filterType = 'new'
        this.type_price = 'minus'
        this.type_isSold = 'minus'
        this.type_date = 'minus'
        if (this.type_new == 'minus') {
            this.order = 'positive'
            this.type_new = 'up'
        }
        else if (this.type_new == 'up') {
            this.order = 'reverse'
            this.type_new = 'down'
        }
        else if (this.type_new == 'down') {
            this.order = 'positive'
            this.type_new = 'up'
        }
        this.dealList = []
        this.infiniteLoadList()
    },
    filterPrice() {
        this.spinning = true
        this.filterType = 'price'
        this.type_new = 'minus'
        this.type_isSold = 'minus'
        this.type_date = 'minus'
        if (this.type_price == 'minus') {
            this.order = 'positive'
            this.type_price = 'up'
        }
        else if (this.type_price == 'up') {
            this.order = 'reverse'
            this.type_price = 'down'
        }
        else if (this.type_price == 'down') {
            this.order = 'positive'
            this.type_price = 'up'
        }
        this.dealList = []
        this.infiniteLoadList()
    },
    filterSold() {
        this.spinning = true
        this.filterType = 'isSold'
        this.type_new = 'minus'
        this.type_price = 'minus'
        this.type_date = 'minus'
        if (this.type_isSold == 'minus') {
            this.order = 'positive'
            this.type_isSold = 'up'
        }
        else if (this.type_isSold == 'up') {
            this.order = 'reverse'
            this.type_isSold = 'down'
        }
        else if (this.type_isSold == 'down') {
            this.order = 'positive'
            this.type_isSold = 'up'
        }
        this.dealList = []
        this.infiniteLoadList()
    },
    searchItem(value) {
        if (!!value) {
            this.spinning = true
            this.$axios.get('searchDealItem', {
                params: {
                    name: value
                }
            })
            .then((response) => {
                this.spinning = false
                if (response.data.code == 200 && response.data.status == 'success') {
                    this.type_date = 'minus'
                    this.type_new = 'minus'
                    this.type_price = 'minus'
                    this.type_isSold = 'minus'

                    this.dealList = []
                    this.$nextTick(() => {
                        this.dealList = response.data.data
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
            this.$message.warning('输入要搜索的物品吧～')
        }
    },
    infiniteLoadList() {
        this.loading = true
        this.$axios.get('getDealList', {
            params: {
                page_number: Math.ceil(this.dealList.length / 10 + 1),
                filterType: this.filterType,
                order: this.order
            }
        })
        .then((response) => {
            this.loading = false
            this.spinning = false
            if (response.data.code == 200) {
                if (response.data.status == 'success') {
                    this.dealList = this.dealList.concat(response.data.data)
                }
                else if (response.data.status == 'none') {
                    this.busy = true
                    this.$message.warning('到底啦～')
                }
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
