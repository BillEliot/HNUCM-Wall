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
                            <h1>个人信息</h1>
                            <p class="subheading">又来偷偷看TA～♪(^∇^*)</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div style="margin-top: 30px">
            <a-button class="follow" type="primary">关注TA</a-button>
            <a-button class="follow">偷偷关注TA</a-button>
            <router-link to="/">
                <a-button class="back" type="primary"><a-icon type="left" />返回主页</a-button>
            </router-link>
        </div>
        <!-- container -->
        <div class="container">
            <div class="row">
                <div class="text-center col-md-4 col-md-offset-4">
                    <a-avatar :size="64" :src="baseUrl + userProfile.avatar" />
                    <h2>{{ userProfile.nickname }}</h2>
                    <p class="bio">{{ userProfile.bio }}</p>
                    <a-input placeholder="email" disabled v-model="userProfile.email">
                        <a-icon slot="prefix" type="mail" />
                    </a-input>
                    <a-input placeholder="手机" disabled v-model="userProfile.phone">
                        <a-icon slot="prefix" type="phone" />
                    </a-input>
                    <a-input placeholder="qq" disabled v-model="userProfile.qq">
                        <a-icon slot="prefix" type="qq" />
                    </a-input>
                    <a-input placeholder="微信" disabled v-model="userProfile.wechat">
                        <a-icon slot="prefix" type="wechat" />
                    </a-input>
                    <a-cascader :options="classes" placeholder="班级" disabled v-model="userProfile.class.split('/')" style="width: 100%; text-align: left">
                        <a-icon type="table" slot="suffixIcon" />
                    </a-cascader>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12">
                    <a-tabs defaultActiveKey="1">
                        <a-tab-pane key="1">
                            <!-- comments -->
                            <span slot="tab">
                                <a-icon type="highlight" />留言板
                            </span>
                            <div id="comment" style="margin-top: 50px">
                                <a-list
                                    v-if="userProfile.comments.length"
                                    :pagination="commentPagination"
                                    :dataSource="userProfile.comments"
                                    :header="`${userProfile.comments.length} 条留言`"
                                    itemLayout="horizontal"
                                >
                                    <div slot="footer"><b>朋友们对TA的留言～</b></div>
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
                                        <a-form-item>
                                            <a-button htmlType="submit" :loading="commenting" @click="submitUserComment" type="primary">评论</a-button>
                                            <a-anchor v-if="showAnchor" :affix="false" class="anchor" @click="commentPagination.current=1">
                                                <a-anchor-link href="#comment" title="查看评论" />
                                            </a-anchor>
                                        </a-form-item>
                                    </div>
                                </a-comment>
                            </div>
                        </a-tab-pane>
                        <a-tab-pane key="2">
                            <!-- loves -->
                            <span slot="tab">
                                <a-icon type="heart" />TA的表白
                            </span>
                            <a-list
                                v-if="userProfile.loves.length"
                                :pagination="lovePagination"
                                :dataSource="userProfile.loves"
                                :header="`${userProfile.loves.length} 条表白`"
                                itemLayout="horizontal"
                            >
                                <div slot="footer"><b>匿名表白看不到哦～</b></div>
                                <a-list-item slot="renderItem" slot-scope="item, index">
                                    <a-comment style="padding-left: 35px">
                                        <a-avatar v-if="item.userTo_uid == -1" slot="avatar" :src="baseUrl + item.userTo_avatar" />
                                        <a-avatar v-else slot="avatar" :src="baseUrl + item.userTo_avatar" @click="$router.push({ path: '/profile', query: { uid: item.userTo_uid } })" />
                                        <a slot="author" style="font-size: 15px" @click="$router.push({ path: '/profile', query: { uid: item.userTo_uid } })">To {{ item.userTo_nickname }}</a>
                                        <p slot="content" class="text-left">{{ item.content }}</p>
                                    </a-comment>
                                </a-list-item>
                            </a-list>
                        </a-tab-pane>
                    </a-tabs>
                </div>
            </div>
        </div>

        <Footer />

    </div>
</template>

<script>
import qs from "qs";
import { mapState } from 'vuex'
import Footer from '~/components/footer'
import navbar from '~/components/navbar'

export default {
    components: {
        Footer,
        navbar
    },
    data() {
        return {
            commentContent: null,
            commenting: false,
            showAnchor: false,
            commentPagination: {
                current: 1,
                pageSize: 10,
                onChange (page) {
                    this.current = page
                }
            },
            lovePagination: {
                current: 1,
                pageSize: 10,
                onChange (page) {
                    this.current = page
                }
            }
        }
    },
    async asyncData({ $axios, query, error }) {
        if (!query.uid) {
            error({ statusCode: 400, message: '非法请求' })
        }

        let userProfile = null
        await $axios.post('getUserProfile', qs.stringify({
            uid: query.uid
        }))
        .then((response) => {
            if (response.data == 1) {
                error({ statusCode: 500, message: '未知错误' })
            }
            else {
                userProfile = response.data
            }
        })
        let userBaseInfo = null
        await $axios.get('getUserBaseInfo')
        .then((response) => {
            if (response.data == 1) {
                error({ statusCode: 500, message: '未知错误' })
            }
            else {
                userBaseInfo = response.data
            }
        })

        return {
            userProfile: userProfile,
            userBaseInfo: userBaseInfo
        }
    },
    methods: {
        searchClass() {

        },
        submitUserComment() {
            if (!this.commentContent) {
                this.$message.warning('说点什么吧～')
            }
            else {
                this.commenting = true
                this.$axios.post('submitUserComment', qs.stringify({
                    uidTo: this.userProfile.uid,
                    uidFrom: this.userBaseInfo.uid,
                    content: this.commentContent
                }))
                .then((response) => {
                    this.commenting = false
                    if (response.data == 1) {
                        this.$message.error('未知错误')
                    }
                    else {
                        this.userProfile.comments.unshift({
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
        baseUrl: state => state.baseUrl,
        classes: state => state.classes
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

.follow {
    float: right;
    margin-right: 20px
}

.back {
    float: left;
    margin-left: 20px
}
</style>
