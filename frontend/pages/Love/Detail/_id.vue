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
                            <h1>（づ￣3￣）づ╭❤～</h1>
                            <p class="subheading">说出来了呢～</p>
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
                        <a-col :span="12">
                            <a-avatar :size="64" :src="baseUrl + loveDetail.userFrom_avatar" />
                            <div>
                                <a v-if="loveDetail.userFrom_nickname == 'Anony'">匿名</a>
                                <a v-else @click="$router.push({ path: 'profile', query: { nickname: loveDetail.userFrom_nickname } })">{{ loveDetail.userFrom_nickname }}</a>
                                <p class="bio">{{ loveDetail.userFrom_bio }}</p>
                            </div>
                        </a-col>
                        <a-col :span="12">
                            <a-avatar :size="64" :src="baseUrl + loveDetail.userTo_avatar" />
                            <div>
                                <a v-if="loveDetail.userTo_nickname == 'Anony'">{{ loveDetail.nameTo }}</a>
                                <a v-else @click="$router.push({ path: 'profile', query: { nickname: loveDetail.userTo_nickname } })">{{ loveDetail.userTo_nickname }}</a>
                                <p class="bio">{{ loveDetail.userTo_bio }}</p>
                            </div>
                        </a-col>
                    </a-row>
                    <hr />
                    <a-card title="对Ta的话">
                        <p>{{ loveDetail.content }}</p>
                    </a-card>
                    <hr />
                    <a-carousel arrows dotsClass="slick-dots slick-thumb">
                        <a slot="customPaging" slot-scope="props">
                            <img :src="baseUrl + loveDetail.images[props.i]" />
                        </a>
                        <div v-for="image in loveDetail.images">
                            <img :src="baseUrl + image" />
                        </div>
                    </a-carousel>
                    <hr style="margin-top: 70px" />
                    <div>
                        <div class="icon-left">
                            <a-icon type="like-o" :theme="loveDetail.isThumbsUp ? 'filled' : 'outlined'" @click="ThumbsUp(loveDetail)" /> {{ loveDetail.thumbsUp }}
                        </div>
                        <div class="icon-right">
                            <a target='_blank' href="http://connect.qq.com/widget/shareqq/index.html?url=http://127.0.0.1&sharesource=qzone&title=湖南中医药大学表白墙&summary=描述&desc=简述">
                                <icon-font type="icon-qq" />
                            </a>
                            <icon-font type="icon-wechat" />
                            <a target='_blank' href="https://sns.qzone.qq.com/cgi-bin/qzshare/cgi_qzshare_onekey?url=http://127.0.0.1&sharesource=qzone&title=湖南中医药大学表白墙&summary=描述">
                                <icon-font type="icon-qzone" />
                            </a>
                            <icon-font type="icon-pyq" />
                            <icon-font type="icon-weibo" />
                        </div>
                    </div>
                    
                    <div id="comment" style="margin-top: 50px">
                        <a-list
                            v-if="loveDetail.comments.length"
                            :pagination="commentPagination"
                            :dataSource="loveDetail.comments"
                            :header="`${loveDetail.comments.length} 条回复`"
                            itemLayout="horizontal"
                        >
                            <div slot="footer"><b>友善的回复是交流的起点</b></div>
                            <a-list-item slot="renderItem" slot-scope="item, index">
                                <a-comment style="padding-left: 35px">
                                    <a-avatar slot="avatar" :src="baseUrl + item.avatar" @click="$router.push({ path: '/profile', query: { uid: item.uid } })"></a-avatar>
                                    <a slot="author" style="font-size: 15px" @click="$router.push({ path: '/profile', query: { uid: item.uid } })">{{ item.nickname }}</a>
                                    <p slot="content" class="text-left">{{ item.content }}</p>
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
        numComment: 0,
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
  async asyncData({ $axios, query, redirect, app }) {
      if (!query.id) {
          redirect('/')
      }

      let loveDetail = null
      let numComment = 0
      await $axios.post('getLoveDetail', qs.stringify({
          id: query.id
      }))
      .then((response) => {
          if (response.data == 1) {
              redirect('/')
          }
          else {
              loveDetail = response.data
              numComment = loveDetail.numComment
          }
      })

      let userBaseInfo = null
      await $axios.get('getUserBaseInfo')
      .then((response) => {
          userBaseInfo = response.data
      })

      return {
          loveDetail: loveDetail,
          numComment: numComment,
          userBaseInfo: userBaseInfo
      }
  },
  methods: {
      ThumbsUp (loveDetail) {
        if (this.userBaseInfo.uid == -1) {
            this.$message.warning('先登录吧～')
        }
        else {
            if (loveDetail.isThumbsUp) {
                loveDetail.isThumbsUp = false
                loveDetail.thumbsUp -= 1
                this.$axios.post('thumbsUp', qs.stringify({
                    id: loveDetail.id,
                    isThumbsUp: false
                }))
            }
            else {
                loveDetail.isThumbsUp = true
                loveDetail.thumbsUp += 1
                this.$axios.post('thumbsUp', qs.stringify({
                    id: loveDetail.id,
                    isThumbsUp: true
                }))
            }
        }
      },
      submitComment() {
          if (!this.commentContent) {
              this.$message.warning('说点什么吧～')
          }
          else {
              this.commenting = true
              this.$axios.post('submitComment', qs.stringify({
                  id: this.loveDetail.id,
                  uid: this.userBaseInfo.uid,
                  content: this.commentContent
              }))
              .then((response) => {
                  this.commenting = false
                  if (response.data == 1) {
                      this.$message.error('未知错误')
                  }
                  else {
                      this.loveDetail.comments.unshift({
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
.icon-left {
    position: absolute;
    left: 10px;
    font-size: 18px;
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

@media (min-width: 992px) {
    .ant-carousel >>> .slick-slide img{
        max-width: 600px;
    }
}
</style>
