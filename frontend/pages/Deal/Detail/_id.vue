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
                            <h1>二手交易</h1>
                            <p class="subheading">愉快的交易呀～</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div style="margin-top: 50px"></div>
        <!-- container -->
        <div class="container">
            <div class="row">
                <div class="text-center col-md-12">
                    <a-row>
                        <a-col :span="8">
                            <p class="price text-left">最低价：¥ {{ dealDetail.price }}</p>
                        </a-col>
                        <a-col :span="8">
                            <span class="new">
                                <a-rate :defaultValue="dealDetail.new" disabled /> {{ dealDetail.new*2 }} 成新
                            </span>
                        </a-col>
                        <a-col :span="8">
                            <p v-if="dealDetail.isFound" class="sold">已售出</p>
                            <p v-else class="notsold">未售出</p>
                        </a-col>
                    </a-row>
                    <a-avatar :size="64" :src="baseUrl + dealDetail.avatar" />
                        <div>
                            <a @click="$router.push({ path: '/profile', query: { uid: dealDetail.uid } })">{{ dealDetail.nickname }}</a>
                            <p class="bio">{{ dealDetail.bio }}</p>
                        </div>
                    <hr />
                    <a-card :title="dealDetail.name">
                        <p>{{ dealDetail.description }}</p>
                    </a-card>
                    <hr />
                    <a-carousel arrows dotsClass="slick-dots slick-thumb">
                        <a slot="customPaging" slot-scope="props">
                            <img :src="baseUrl + dealDetail.images[props.i]" />
                        </a>
                        <div v-for="image in dealDetail.images">
                            <img :src="baseUrl + image" />
                        </div>
                    </a-carousel>
                    <hr style="margin-top: 70px" />
                    <div>
                        <div class="icon-right">
                            <a target='_blank' href="http://connect.qq.com/widget/shareqq/index.html?url=http://127.0.0.1&sharesource=qzone&title=湖南中医药大学失物墙&summary=描述&desc=简述">
                                <icon-font type="icon-qq" />
                            </a>
                            <icon-font type="icon-wechat" />
                            <a target='_blank' href="https://sns.qzone.qq.com/cgi-bin/qzshare/cgi_qzshare_onekey?url=http://127.0.0.1&sharesource=qzone&title=湖南中医药大学失物墙&summary=描述">
                                <icon-font type="icon-qzone" />
                            </a>
                            <icon-font type="icon-pyq" />
                            <icon-font type="icon-weibo" />
                        </div>
                    </div>
                    
                    <div id="comment" style="margin-top: 50px">
                        <a-list
                            v-if="dealDetail.comments.length"
                            :pagination="commentPagination"
                            :dataSource="dealDetail.comments"
                            :header="`${dealDetail.comments.length} 条回复`"
                            itemLayout="horizontal"
                        >
                            <div slot="footer"><b>友善的回复是交流的起点</b></div>
                            <a-list-item slot="renderItem" slot-scope="item, index">
                                <a-comment style="padding-left: 35px">
                                    <a-avatar slot="avatar" :src="baseUrl + item.avatar" @click="$router.push({ path: '/profile', query: { uid: item.uid } })"></a-avatar>
                                    <a slot="author" style="font-size: 15px" @click="$router.push({ path: '/profile', query: { uid: item.uid } })">{{ item.nickname }}</a>
                                    <p slot="content" class="text-left">{{ item.content }}</p>
                                    <span class="date">{{ moment(item.date).format('lll') }}</span>
                                </a-comment>
                            </a-list-item>
                        </a-list>
                        <a-comment :avatar="baseUrl + userBaseInfo.avatar" :author="userBaseInfo.nickname">
                            <div slot="content">
                                <a-form-item>
                                    <a-textarea :rows="4" v-model="commentContent" ></a-textarea>
                                </a-form-item>
                                <a-form-item class="text-left">
                                    <a-button htmlType="submit" :loading="commenting" @click="submitComment" type="primary">评论</a-button>
                                    <a-anchor v-if="showAnchor" :affix="false" class="anchor" @click="commentPagination.current=1">
                                        <a-anchor-link href="#comment" title="查看评论" />
                                    </a-anchor>
                                </a-form-item>
                            </div>
                        </a-comment>
                    </div>
                </div>
            </div>
        </div>

        <Footer />

    </div>
</template>

<script>
import qs from 'qs'
import moment from 'moment'
import { Icon } from 'ant-design-vue'
import { mapState } from 'vuex'
import navbar from '~/components/navbar'
import Footer from '~/components/footer'

const IconFont = Icon.createFromIconfontCN({
  scriptUrl: '//at.alicdn.com/t/font_1211094_e7pjz6z6y7.js'
})
export default {
  components: {
    IconFont,
    navbar,
    Footer
  },
  data() {
    return {
        commenting: false,
        commentContent: null,
        commentPagination: {
            current: 1,
            pageSize: 10,
            onChange (page) {
                this.current = page
            }
        },
        showAnchor: false
    }
  },
  async asyncData({ $axios, query, redirect }) {
      if (!query.id) {
          redirect('/deal')
      }

      let dealDetail = null
      await $axios.post('getDealDetail', qs.stringify({
          id: query.id
      }))
      .then((response) => {
          if (response.data == 1) {
              redirect('/deal')
          }
          else {
              dealDetail = response.data
          }
      })

      let userBaseInfo = null
      await $axios.get('getUserBaseInfo')
      .then((response) => {
          userBaseInfo = response.data
      })

      return {
          dealDetail: dealDetail,
          userBaseInfo: userBaseInfo
      }
  },
  methods: {
      moment,
      submitComment() {
          if (!this.commentContent) {
              this.$message.warning('说点什么吧～')
          }
          else if (this.userBaseInfo.uid == -1) {
              this.$message.warning('登录之后再评论吧～')
          }
          else {
              this.commenting = true
              this.$axios.post('submitDealComment', qs.stringify({
                  id: this.dealDetail.id,
                  uid: this.userBaseInfo.uid,
                  content: this.commentContent
              }))
              .then((response) => {
                  this.commenting = false
                  if (response.data == 1) {
                      this.$message.error('未知错误')
                  }
                  else {
                      this.dealDetail.comments.unshift({
                          avatar: this.userBaseInfo.avatar,
                          nickname: this.userBaseInfo.nickname,
                          content: this.commentContent
                      })
                      this.commentContent = ''
                      this.showAnchor = true
                      setTimeout(() => {
                          this.showAnchor = false
                      }, 3000)
                      this.$message.success('评论成功')
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
a {
    text-decoration: none;
}
a:hover {
    color: blue;
}

.price {
    color: indigo;
    font-size: 28px;
    font-weight: bold;
}
.sold {
    color: green;
    font-size: 28px;
    font-weight: bold;
}
.notsold {
    color: red;
    font-size: 28px;
    font-weight: bold;
}
.new {
    color: darkgreen;
    font-size: 20px;
    font-weight: bold;
}

.anchor >>> .ant-anchor-link-title {
    text-decoration: none;
}

.icon-right {
    position: absolute;
    right: 10px;
}
.icon-right >>> .anticon {
    font-size: 24px;
    cursor: pointer;
}

.ant-carousel >>> .slick-dots {
    height: auto
}
.ant-carousel >>> .slick-slide img{
    border: 5px solid #FFF;
    display: block;
    margin: auto;
    max-width: 300px;
}
.ant-carousel >>> .slick-thumb {
    bottom: -45px;
}
.ant-carousel >>> .slick-thumb li {
    width: 60px;
    height: 45px;
}
.ant-carousel >>> .slick-thumb li img {
    width: 100%;
    height: 100%;
    filter: grayscale(100%);
}
.ant-carousel >>> .slick-thumb li.slick-active img{
    filter: grayscale(0%);
}

.date {
    font-style: italic;
    color: gray;
}

@media (min-width: 992px) {
    .ant-carousel >>> .slick-slide img{
        max-width: 600px;
    }
}
</style>
