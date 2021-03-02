<template>
    <div>
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
                            <a-button @click="filterDate">时间<a-icon :type="type_date" /></a-button>
                            <a-button @click="filterThumbsUp">赞数<a-icon :type="type_thumbsUp" /></a-button>
                            <a-button @click="filterCoin">硬币数<a-icon :type="type_coin" /></a-button>
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
                            <div class="search-tag">
                                <template v-for="(tag, index) in tags">
                                    <a-tooltip v-if="tag.length > 20" :key="tag" :title="tag">
                                        <a-tag :key="tag" :closable="index !== 0" :afterClose="() => handleCloseTag(tag)">
                                            {{`${tag.slice(0, 20)}...`}}
                                        </a-tag>
                                    </a-tooltip>
                                    <a-tag v-else :key="tag" :closable="true" :afterClose="() => handleCloseTag(tag)">
                                        {{ tag }}
                                    </a-tag>
                                </template>
                                <a-input
                                    v-if="canInputTag"
                                    ref="input"
                                    type="text"
                                    size="small"
                                    :style="{ width: '78px' }"
                                    :value="inputTag"
                                    @change="handleTagChange"
                                    @blur="handleTagConfirm"
                                    @keyup.enter="handleTagConfirm"
                                />
                                <a-tag v-else @click="showInputTag" style="background: #fff; borderStyle: dashed;">
                                    <a-icon type="plus" /> 添加Tag
                                </a-tag>
                                <a-button type="primary" @click="searchArticleByTag">搜索Tag</a-button>
                            </div>
                        </div>
                    </div>
                    <a-list
                        itemLayout="vertical"
                        :dataSource="articleList"
                        :pagination="pagination"
                        size="large"
                        :loading="loading"
                    >
                        <a-list-item slot="renderItem" slot-scope="item, index">
                            <!-- article -->
                            <a-list-item-meta :description="item.content">
                                <a slot="title" @click="openArticleDetail(item.id)">{{ item.title }}</a>
                            </a-list-item-meta>
                            <!-- tags -->
                            <span>
                                <a-tag v-for="tag in item.tags" :color="randomColor()" :key="tag">{{ tag }}</a-tag>
                            </span>
                            <div>
                                <span>发布时间：{{ moment(item.publicDate).format('lll') }}</span>
                                <br />
                                <span>最后编辑：{{ moment(item.editDate).format('lll') }}</span>
                            </div>
                            <!-------------------------------------------------------->
                            <span slot="actions">需要硬币： {{ item.neededCoin }}</span>
                            <span slot="actions">
                                <a-icon type="like-o" /> {{ item.thumbsUp }}
                            </span>
                            <span slot="actions">
                                <a-icon type="message" /> {{ item.comments }}
                            </span>
                            <span slot="actions">
                                <a-icon type="eye" /> {{ item.viewCount }}
                            </span>
                            <!-- avatar -->
                            <div class="avatar-card text-center">
                                <a-avatar
                                    :size="64"
                                    :src="baseUrl + item.user.avatar"
                                    @click="$router.push({ path: '/profile', query: { id: item.user.id } })"
                                    class="avatar"
                                />
                                <br />
                                <a @click="$router.push({ path: '/profile', query: { id: item.user.id } })">{{ item.user.username }}</a>
                                <br />
                                <span>{{ item.user.bio }}</span>
                                <br />
                                <a-tag v-for="tag in item.user.auth" :color="randomColor()" :key="tag">{{ tag }}</a-tag>
                            </div>
                        </a-list-item>
                    </a-list>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import qs from 'qs'
import moment from 'moment'
import { mapState } from 'vuex'
import { max } from 'moment'

export default {
  layout: 'common',
  data() {
    return {
        moment,

        tags: [],
        canInputTag: false,
        inputTag: '',

        current_page_number: 1,
        articleTotal: 0,
        loading: false,
        searchValue: '',
        searchType: '',
        filterType: '',
        order: 'normal',
        type_date: 'minus',
        type_thumbsUp: 'minus',
        type_coin: 'minus',
    }
  },
  async asyncData({ $axios, error }) {
    let articleList = []
    let articleTotal = 0

    await $axios.get('getArticleList', {
        params: {
            page_number: 1
        }
    })
    .then((response) => {
        if (response.data.code == 200 && response.data.status == 'success') {
            articleList = response.data.data.list
            articleTotal = response.data.data.total
        }
    })

    return {
        articleList: articleList,
        articleTotal: articleTotal
    }
  },
  methods: {
      randomColor() {
          let color = ['pink', 'red', 'orange', 'green', 'cyan', 'blue', 'purple']
          return color[Math.round(Math.random() * (color.length - 1))]
      },
      openArticleDetail(id) {
          let routeData = this.$router.resolve({ path: '/article/detail', query: { id: id } })
          window.open(routeData.href, '_blank')

          this.articleList.forEach(article => {
              if (article.id == id) {
                  article.viewCount += 1
                  return
              }
          })
      },
      filterDate() {
          this.loading = true
          this.current_page_number = 1
          this.searchType = ''
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
          this.getArticleList(1)
      },
      filterThumbsUp() {
          this.loading = true
          this.current_page_number = 1
          this.searchType = ''
          this.filterType = 'thumbsUp'
          this.type_date = 'minus'
          this.type_coin = 'minus'
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
          this.getArticleList(1)
      },
      filterCoin() {
          this.loading = true
          this.current_page_number = 1
          this.searchType = ''
          this.filterType = 'coin'
          this.type_thumbsUp = 'minus'
          this.type_date = 'minus'
          if (this.type_coin == 'minus') {
              this.order = 'positive'
              this.type_coin = 'up'
          }
          else if (this.type_coin == 'up') {
              this.order = 'reverse'
              this.type_coin = 'down'
          }
          else if (this.type_coin == 'down') {
              this.order = 'positive'
              this.type_coin = 'up'
          }
          this.getArticleList(1)
      },
      ///////////////////////////////////////////////////////////////////
      search(api, value, page_number, bShowNotification) {
          this.loading = true
          this.$axios.get(api, {
              params: {
                  value: value,
                  page_number: page_number
              }
          })
          .then((response) => {
              this.loading = false
              if (response.data.code == 200 && response.data.status == 'success') {
                  this.current_page_number = 1
                  this.type_date = 'minus'
                  this.type_thumbsUp = 'minus'
                  this.type_coin = 'minus'
                  this.articleList = response.data.data.list
                  this.articleTotal = response.data.data.total
                  if (bShowNotification) {
                      this.$notification.open({
                          message: '搜索结果',
                          description: `共搜索到 ${response.data.data.total} 条结果`,
                          icon: <a-icon type="smile" style="color: #108ee9" />,
                          duration: 0
                      })
                  }
              }
          })
      },
      ///////////////////////////////////////////////////////////////////
      searchArticle(value) {
          if (!!value) {
              this.searchValue = value
              this.searchType = 'article'
              this.search('searchArticle', value, 1, true)
          }
          else {
              this.$message.warning('输入要搜索的物品吧～')
          }
      },
      ///////////////////////////////////////////////////////////////////
      searchUser(value) {
          if (!!value) {
              this.searchValue = value
              this.searchType = 'user'
              this.search('searchArticleByUser', value, 1, true)
          }
          else {
              this.$message.warning('输入要搜索的用户吧～')
          }
      },
      ///////////////////////////////////////////////////////////////////
      searchArticleByTag() {
          if (!!this.tags && this.tags.length != 0) {
              this.searchValue = this.tags
              this.searchType = 'tag'
              this.search('searchArticleByTag', this.tags, 1, true)
        }
        else {
            this.$message.warning('输入要搜索的Tag吧～')
        }
      },
      ///////////////////////////////////////////////////////////////////
      getArticleList(page_number) {
          this.$axios.get('getArticleList', {
              params: {
                  page_number: page_number,
                  filterType: this.filterType,
                  order: this.order
              }
          })
          .then((response) => {
              this.loading = false
              if (response.data.code == 200 && response.data.status == 'success') {
                  this.articleList = response.data.data.list
                  this.articleTotal = response.data.data.total
              }
          })
      },
      ///////////////////////////////////////////////////////////////////
      handleCloseTag (removedTag) {
          let tags = this.tags.filter(tag => tag !== removedTag)
          this.tags = tags
      },

      showInputTag () {
          this.canInputTag = true
          this.$nextTick(function () {
              this.$refs.input.focus()
          })
      },
      handleTagChange (e) {
          this.inputTag = e.target.value
      },
      handleTagConfirm () {
          let inputTag = this.inputTag
          let tags = this.tags
          if (inputTag && tags.indexOf(inputTag) === -1) {
              tags = [...tags, inputTag]
          }
          Object.assign(this, {
              tags,
              canInputTag: false,
              inputTag: ''
          })
      }
  },
  computed: {
      ...mapState({
          baseUrl: state => state.baseUrl
      }),

      pagination() {
          const _this = this
          return {
              pageSize: 10,
              total: this.articleTotal,
              current: this.current_page_number,
              onChange(page, pageSize) {
                if (this.current != page) {
                    _this.current_page_number = page
                    _this.loading = true
                    if (_this.searchType == 'article') {
                        _this.search('searchArticle', _this.searchValue, page)
                    }
                    else if (_this.searchType == 'user') {
                        _this.search('searchArticleByUser', _this.searchValue, page)
                    }
                    else if (_this.searchType == 'tag') {
                        _this.search('searchArticleByTag', _this.searchValue, page)
                    }
                    else {
                        _this.getArticleList(page)
                    }

                    scrollTo(0, 600)
                }
              }
          }
      }
  }
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
        width: 200px;
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
