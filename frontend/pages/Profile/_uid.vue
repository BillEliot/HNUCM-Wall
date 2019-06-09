<template>
    <div>
        <!-- drawer - profile -->
        <a-drawer
            title="编辑个人资料"
            :width="360"
            @close="visibleDrawerProfile = false"
            :visible="visibleDrawerProfile"
            :closable = "false"
        >
            <a-form :form="form_profile" layout="vertical">
                <a-form-item label="昵称">
                    <a-input
                        v-decorator="[
                            'nickname',
                            {
                                rules: [{ required: true, message: '请输入你的昵称' }]
                            }
                        ]"
                        placeholder="你的昵称"
                    />
                </a-form-item>
                <a-form-item label="个性签名">
                    <a-input
                        v-decorator="[
                            'bio',
                            {
                                rules: [{ required: true, message: '请输入你的个性签名' }]
                            }
                        ]"
                        placeholder="你的个性签名"
                    />
                </a-form-item>
                <a-form-item label="手机">
                    <a-input
                        v-decorator="[
                            'phone'
                        ]"
                        placeholder="你的手机号"
                    />
                </a-form-item>
                <a-form-item label="qq">
                    <a-input
                        v-decorator="[
                            'qq'
                        ]"
                        placeholder="你的qq"
                    />
                </a-form-item>
                <a-form-item label="微信">
                    <a-input
                        v-decorator="[
                            'wechat'
                        ]"
                        placeholder="你的微信"
                    />
                </a-form-item>
                <a-form-item label="班级">
                    <a-cascader
                        v-decorator="[
                            'class',
                            {
                                initialValue: ['zhongyi', 'wuyi'],
                                rules: [{ type: 'array', required: true, message: '请选择您的班级' }],
                            }
                        ]"
                        :options="classes"
                    />
                </a-form-item>
                <a-form-item class="submit">
                    <a-button @click="visibleDrawerProfile = false" style="margin-right: 10px">取消</a-button>
                    <a-button @click="submitProfile" type="primary" html-type="submit">确定</a-button>
                </a-form-item>
            </a-form>
        </a-drawer>
        <!-- drawer - change password -->
        <a-drawer
            title="修改密码"
            :width="360"
            @close="visibleDrawerPassword = false"
            :visible="visibleDrawerPassword"
            :closable = "false"
        >
            <a-form :form="form_password" layout="vertical">
                <a-form-item label="原密码">
                    <a-input
                        v-decorator="[
                            'originPassword',
                            {
                                rules: [{ 
                                    required: true, message: '请输入原密码' 
                                }]
                            }
                        ]"
                        placeholder="原密码"
                    />
                </a-form-item>
                <a-form-item label="密码">
                    <a-input
                        v-decorator="[
                            'password',
                            {
                                rules: [{ 
                                    required: true, message: '请输入密码' 
                                },
                                {
                                    validator: validatorPassword
                                }]
                            }
                        ]"
                        placeholder="密码"
                    />
                </a-form-item>
                <a-form-item label="重复密码">
                    <a-input
                        v-decorator="[
                            'password2',
                            {
                                rules: [{ 
                                    required: true, message: '请重复输入密码' 
                                },
                                {
                                    validator: validatorPassword2
                                }]
                            }
                        ]"
                        placeholder="重复输入密码"
                        @blur="blurPassword2"
                    />
                </a-form-item>
                <a-form-item class="submit">
                    <a-button @click="visibleDrawerProfile = false" style="margin-right: 10px">取消</a-button>
                    <a-button @click="submitProfile" type="primary" html-type="submit">确定</a-button>
                </a-form-item>
            </a-form>
        </a-drawer>
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
            <a-button class="follow" type="primary"><a-icon type="heart" />关注</a-button>
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
                    <a-input placeholder="硬币" disabled v-model="userProfile.coin + ' 枚硬币'">
                        <a-icon slot="prefix" type="gold" />
                    </a-input>
                    <div style="margin-top: 20px">
                        <!-- actions -->
                        <a-button @click="visibleDrawerProfile = true">编辑资料</a-button>
                        <a-button @click="visibleDrawerPassword = true">修改密码</a-button>
                    </div>
                </div>
            </div>
            <div style="margin-top: 30px"></div>
            <div class="row">
                <div class="col-md-12">
                    <a-tabs defaultActiveKey="1">
                        <!-- comments -->
                        <a-tab-pane key="1">
                            <span slot="tab">
                                <a-icon type="highlight" />留言板
                            </span>
                            <div id="comment">
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
                        <!-- love -->
                        <a-tab-pane key="2">
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
                        <!-- lose -->
                        <a-tab-pane key="3">
                            <span slot="tab">
                                <a-icon type="book" />TA的失物
                            </span>
                            <a-list
                                v-if="userProfile.loses.length"
                                :pagination="losePagination"
                                :dataSource="userProfile.loses"
                                :header="`${userProfile.loses.length} 个丢失物品`"
                                itemLayout="horizontal"
                            >
                                <div slot="footer"><b>这个人也太粗心了叭～</b></div>
                                <a-list-item slot="renderItem" slot-scope="item, index">
                                    <a-comment style="padding-left: 35px">
                                        <p v-if="item.isFound" slot="avatar" class="found">已找到</p>
                                        <p v-else slot="avatar" class="notfound">未找到</p>
                                        <a slot="author" style="font-size: 15px" @click="$router.push({ path: '/lose/detail', query: { id: item.id } })">{{ item.name }}</a>
                                        <p slot="content" class="text-left">{{ item.description }}</p>
                                    </a-comment>
                                </a-list-item>
                            </a-list>
                        </a-tab-pane>
                        <!-- deal -->
                        <a-tab-pane key="4">
                            <span slot="tab">
                                <a-icon type="pay-circle" />TA的二手物品
                            </span>
                            <a-list
                                v-if="userProfile.deals.length"
                                :pagination="losePagination"
                                :dataSource="userProfile.deals"
                                :header="`${userProfile.deals.length} 个交易物品`"
                                itemLayout="horizontal"
                            >
                                <div slot="footer"><b>这个人也太粗心了叭～</b></div>
                                <a-list-item slot="renderItem" slot-scope="item, index">
                                    <a-comment style="padding-left: 35px">
                                        <p v-if="item.isSold" slot="avatar" class="found">已售出</p>
                                        <p v-else slot="avatar" class="notfound">未售出</p>
                                        <a slot="author" style="font-size: 15px" @click="$router.push({ path: '/deal/detail', query: { id: item.id } })">{{ item.name }}</a>
                                        <p slot="content" class="text-left">{{ item.description }}</p>
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
            },
            losePagination: {
                current: 1,
                pageSize: 10,
                onChange (page) {
                    this.current = page
                }
            },
            visibleDrawerProfile: false,
            visibleDrawerPassword: false,
            form_profile: this.$form.createForm(this),
            form_password: this.$form.createForm(this),
            confirmDirty: false
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
        blurPassword2(e) {
            this.confirmDirty = this.confirmDirty || !!e.target.value
        },
        validatorPassword(rule, value, callback) {
            if (value && this.confirmDirty) {
                this.form_password.validateFields(['password2'], { force: true })
            }
            callback()
        },
        validatorPassword2(rule, value, callback) {
            if (value && value !== this.form_password.getFieldValue('password')) {
                callback('两次密码不一致')
            }
            else {
                callback()
            }
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
        },
        submitProfile() {

        }
    },
    computed: mapState({
        baseUrl: state => state.baseUrl,
        classes: state => state.classes,
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

.submit {
    position: 'absolute';
    left: 0;
    bottom: 0;
    width: 100%;
    border-top: 1px solid #e9e9e9;
    padding: 10px 16px;
    background: #fff;
    text-align: right;
}

.follow {
    float: right;
    margin-right: 20px
}

.back {
    float: left;
    margin-left: 20px
}

.found {
    cursor: default;
    color: green;
    font-weight: bold;
}
.notfound {
    cursor: default;
    color: red;
    font-weight: bold;
}
</style>
