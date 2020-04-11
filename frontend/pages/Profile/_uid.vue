<template>
    <div>
        <!-- drawer - profile -->
        <a-drawer
            title="编辑个人资料"
            :width="360"
            @close="visibleDrawerProfile = false"
            :visible="visibleDrawerProfile"
            :wrapStyle="{ height: 'calc(100% - 108px)', overflow: 'auto', paddingBottom: '108px' }"
        >
            <a-form :form="form_profile" layout="vertical">
                <a-form-item label="头像">
                    <a-upload
                        name="avatar"
                        listType="picture-card"
                        :showUploadList="false"
                        :action="baseUrl + '/api/uploadAvatar'"
                        :data="{ uid: userBaseInfo.uid, platform: 'web' }"
                        :beforeUpload="beforeAvatarUpload"
                        @change="handleChange_avatarUpload"
                    >
                        <a-icon :type="loading_uploadAvatar ? 'loading' : 'plus'" />
                        <div>修改头像</div>
                    </a-upload>
                </a-form-item>
                <a-form-item label="昵称">
                    <a-input
                        v-decorator="['nickname', {
                                rules: [{ required: true, message: '请输入你的昵称' }]
                            }
                        ]"
                        placeholder="你的昵称"
                    />
                </a-form-item>
                <a-form-item label="个性签名">
                    <a-input
                        v-decorator="['bio', {
                                rules: [{ required: true, message: '请输入你的个性签名' }]
                            }
                        ]"
                        placeholder="你的个性签名"
                    />
                </a-form-item>
                <a-form-item label="手机">
                    <a-input
                        v-decorator="['phone']"
                        placeholder="你的手机号"
                    />
                </a-form-item>
                <a-form-item label="qq">
                    <a-input
                        v-decorator="['qq']"
                        placeholder="你的qq"
                    />
                </a-form-item>
                <a-form-item label="微信">
                    <a-input
                        v-decorator="['wechat']"
                        placeholder="你的微信"
                    />
                </a-form-item>
                <a-form-item label="性别">
                    <a-select
                        v-decorator="['gender', {
                            rules: [{ required: true, message: '请选择您的性别' }],
                            initialValue: '男'
                        }]"
                        placeholder="性别"
                    >
                        <a-select-option value="男">男</a-select-option>
                        <a-select-option value="女">女</a-select-option>
                    </a-select>
                </a-form-item>
                <a-form-item label="班级">
                    <a-cascader
                        v-decorator="['class', {
                            rules: [{ type: 'array', required: true, message: '请选择您的班级' }],
                        }]"
                        :options="classes"
                        placeholder="你的班级"
                    />
                </a-form-item>
            </a-form>
            <div 
                :style="{
                    position: 'absolute',
                    left: 0,
                    bottom: 0,
                    width: '100%',
                    borderTop: '1px solid #e9e9e9',
                    padding: '10px 16px',
                    background: '#fff',
                    textAlign: 'right',
                }">
                <a-button @click="visibleDrawerProfile = false" style="margin-right: 10px">取消</a-button>
                <a-button @click="submitProfile" type="primary" html-type="submit">确定</a-button>
            </div>
        </a-drawer>
        <!-- drawer - change password -->
        <a-drawer
            title="修改密码"
            :width="360"
            @close="visibleDrawerPassword = false"
            :visible="visibleDrawerPassword"
            :wrapStyle="{ height: 'calc(100% - 108px)', overflow: 'auto', paddingBottom: '108px' }"
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
                        type="password"
                        placeholder="原密码"
                    />
                </a-form-item>
                <a-form-item label="密码">
                    <a-input
                        v-decorator="['password', {
                                rules: [{ 
                                    required: true, message: '请输入密码' 
                                },
                                {
                                    validator: validatorPassword
                                }]
                            }
                        ]"
                        type="password"
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
                        type="password"
                        placeholder="重复输入密码"
                        @blur="blurPassword2"
                    />
                </a-form-item>
            </a-form>
            <div 
                :style="{
                    position: 'absolute',
                    left: 0,
                    bottom: 0,
                    width: '100%',
                    borderTop: '1px solid #e9e9e9',
                    padding: '10px 16px',
                    background: '#fff',
                    textAlign: 'right',
            }">
                <a-button @click="visibleDrawerPassword = false" style="margin-right: 10px">取消</a-button>
                <a-button @click="changePassword" type="primary" html-type="submit">确定</a-button>
            </div>
        </a-drawer>
        <!-- drawer - following list -->
        <a-drawer
            title="关注列表"
            placement="right"
            :closable="false"
            :visible="visibleDrawerFollowing"
            @close="visibleDrawerFollowing = false"
        >
            <div class="row">
                <div class="col-md-4 col-md-offset-4 col-xs-4 col-xs-offset-4 text-center">
                    <div v-for="user in userProfile.followings" :key="user.uid">
                        <a-avatar v-if="user.uid == -1" :size="64" :src="baseUrl + user.avatar" />
                        <a-avatar v-else :size="64" :src="baseUrl + user.avatar" @click="$router.push({ path: '/profile', query: { uid: user.uid } })" style="cursor: pointer" />
                        <a v-if="user.uid == -1">{{ user.nickname }}</a>
                        <a v-else @click="$router.push({ path: '/profile', query: { uid: user.uid } })">{{ user.nickname }}</a>
                        <p class="bio">{{ user.bio }}</p>
                        <a-tag v-for="tag in user.auth" :color="randomColor()" :key="tag">{{ tag }}</a-tag>
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
                            <h1>个人信息</h1>
                            <p class="subheading">又来偷偷看TA～♪(^∇^*)</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div style="margin-top: 30px">
            <a-button v-if="userBaseInfo.uid != -1 && userBaseInfo.uid != $route.query.uid && !userProfile.isFollowing" @click="follow($route.query.uid)" type="primary" class="follow">
                <a-icon type="heart" />关注
            </a-button>
            <a-button v-if="userBaseInfo.uid != -1 && userBaseInfo.uid != $route.query.uid && userProfile.isFollowing" @click="unFollow($route.query.uid)" type="dashed" class="follow">
                <a-icon type="heart" />取消关注
            </a-button>
            <a-button @click="visibleDrawerFollowing = true" class="follow" type="primary">
                <a-icon type="heart" />关注列表
            </a-button>
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
                    <a-tag v-for="tag in userProfile.auth" :color="randomColor()" :key="tag">{{ tag }}</a-tag>
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
                    <a-input placeholder="性别" disabled v-model="userProfile.gender">
                        <a-icon v-if="userProfile.gender == '男'" slot="prefix" type="man" />
                        <a-icon v-else slot="prefix" type="woman" />
                    </a-input>
                    <a-cascader :options="classes" placeholder="班级" disabled v-model="userProfile.class.split('/')" style="width: 100%; text-align: left">
                        <a-icon type="table" slot="suffixIcon" />
                    </a-cascader>
                    <a-input placeholder="硬币" disabled v-model="userProfile.coin + ' 枚硬币'">
                        <a-icon slot="prefix" type="gold" />
                    </a-input>
                    <div v-if="userBaseInfo.uid != -1 && userBaseInfo.uid == $route.query.uid" style="margin-top: 20px">
                        <!-- actions -->
                        <a-button @click="OnVisibleDrawerProfile()">编辑资料</a-button>
                        <a-button @click="visibleDrawerPassword = true">修改密码</a-button>
                        <a-button @click="applyAuth()">申请身份认证</a-button>
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
                                            <span>{{ item.date }}</span>
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
                                        <a slot="author" style="font-size: 15px" @click="$router.push({ path: '/love/detail', query: { id: item.id } })">To {{ item.userTo_nickname }}</a>
                                        <p slot="content" class="text-left abbr">{{ item.content }}</p>
                                        <span>{{ item.date }}</span>
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
                                        <p slot="content" class="text-left abbr">{{ item.description }}</p>
                                        <span>{{ item.date }}</span>
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
                                <div slot="footer"><b>TA的二手物品哦～</b></div>
                                <a-list-item slot="renderItem" slot-scope="item, index">
                                    <a-comment style="padding-left: 35px">
                                        <p v-if="item.isSold" slot="avatar" class="found">已售出</p>
                                        <p v-else slot="avatar" class="notfound">未售出</p>
                                        <a slot="author" style="font-size: 15px" @click="$router.push({ path: '/deal/detail', query: { id: item.id } })">{{ item.name }}</a>
                                        <p slot="content" class="text-left abbr">{{ item.description }}</p>
                                        <span>{{ item.date }}</span>
                                    </a-comment>
                                </a-list-item>
                            </a-list>
                        </a-tab-pane>
                        <!-- help -->
                        <a-tab-pane key="5">
                            <span slot="tab">
                                <a-icon type="question-circle" />TA的求助
                            </span>
                            <a-list
                                v-if="userProfile.helps.length"
                                :pagination="helpPagination"
                                :dataSource="userProfile.helps"
                                :header="`${userProfile.helps.length} 个求助`"
                                itemLayout="horizontal"
                            >
                                <div slot="footer"><b>TA的求助哦～</b></div>
                                <a-list-item slot="renderItem" slot-scope="item, index">
                                    <div>
                                        <a style="font-size: 15px" @click="$router.push({ path: '/help/detail', query: { id: item.id } })">{{ item.title }}</a>
                                        <p class="text-left">{{ item.content }}</p>
                                        <span>{{ item.date }}</span>
                                    </div>
                                </a-list-item>
                            </a-list>
                        </a-tab-pane>
                        <!-- article -->
                        <a-tab-pane key="6">
                            <span slot="tab">
                                <a-icon type="question-circle" />TA的文章
                            </span>
                            <a-list
                                v-if="userProfile.articles.length"
                                :pagination="articlePagination"
                                :dataSource="userProfile.articles"
                                :header="`${userProfile.articles.length} 篇文章`"
                                itemLayout="horizontal"
                            >
                                <div slot="footer"><b>TA的文章哦～</b></div>
                                <a-list-item slot="renderItem" slot-scope="item, index">
                                    <div>
                                        <a style="font-size: 15px" @click="$router.push({ path: '/article/detail', query: { id: item.id } })">{{ item.title }}</a>
                                        <p class="text-left abbr">{{ item.content }}</p>
                                        <a-tag v-for="tag in item.tags" :color="randomColor()" :key="tag">{{ tag }}</a-tag>
                                        <br />
                                        <span>所需硬币：{{ item.neededCoin }}</span>
                                        <br />
                                        <span>最后编辑：{{ item.editDate }}</span>
                                        <br />
                                        <span>发布日期：{{ item.publicDate }}</span>
                                    </div>
                                </a-list-item>
                            </a-list>
                        </a-tab-pane>
                        <!-- error book -->
                        <a-tab-pane key="7" v-if="userBaseInfo.uid != -1 && userBaseInfo.uid == $route.query.uid">
                            <span slot="tab">
                                <a-icon type="file-text" />错题本
                            </span>

                            <a-popconfirm
                                title="确定清空错题本吗？"
                                @confirm="confirm_clearErrorBook()"
                                okText="是"
                                cancelText="否"
                            >
                                <a-icon slot="icon" type="question-circle-o" style="color: red" />
                                <a-button type="danger">清空错题本</a-button>
                            </a-popconfirm>
                            <a-list
                                v-if="userProfile.errorBook.length"
                                :pagination="errorBookPagination"
                                :dataSource="userProfile.errorBook"
                                :header="`${userProfile.errorBook.length} 个错题`"
                                itemLayout="horizontal"
                            >
                                <div slot="footer"><b>做错的题目～</b></div>
                                <a-list-item slot="renderItem" slot-scope="item">
                                    <div>
                                        <a-tag color="red">科目：{{ item.subject }}</a-tag>
                                        <a-tag color="green">章节：{{ item.chapter }}</a-tag>
                                        <h4>{{ item.title }}</h4>
                                        <a-tag color="purple" v-if="item.A != ''">A. {{ item.A }}</a-tag>
                                        <a-tag color="purple" v-if="item.A != ''">B. {{ item.B }}</a-tag>
                                        <a-tag color="purple" v-if="item.A != ''">C. {{ item.C }}</a-tag>
                                        <a-tag color="purple" v-if="item.A != ''">D. {{ item.D }}</a-tag>
                                        <a-tag color="purple" v-if="item.A != ''">E. {{ item.E }}</a-tag>
                                        <br />
                                        <a-collapse :bordered="false">
                                            <a-collapse-panel header="正确答案">
                                                <p>{{ item.answer }}</p>
                                            </a-collapse-panel>
                                        </a-collapse>
                                        <a-popconfirm
                                            title="确定从错题本中删除这道题目吗？"
                                            @confirm="confirm_removeErrorBook(item.id)"
                                            okText="是"
                                            cancelText="否"
                                        >
                                            <a-icon slot="icon" type="question-circle-o" style="color: red" />
                                            <a-button type="danger" size="small" style="margin-top: 10px">删除题目</a-button>
                                        </a-popconfirm>
                                    </div>
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
import md5 from 'js-md5'
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
            helpPagination: {
                current: 1,
                pageSize: 10,
                onChange (page) {
                    this.current = page
                }
            },
            articlePagination: {
                current: 1,
                pageSize: 10,
                onChange (page) {
                    this.current = page
                }
            },
            errorBookPagination: {
                current: 1,
                pageSize: 10,
                onChange (page) {
                    this.current = page
                }
            },
            visibleDrawerProfile: false,
            visibleDrawerPassword: false,
            visibleDrawerFollowing: false,
            form_profile: this.$form.createForm(this),
            form_password: this.$form.createForm(this),
            confirmDirty: false,
            loading_uploadAvatar: false
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
        randomColor() {
            let color = ['pink', 'red', 'orange', 'green', 'cyan', 'blue', 'purple']
            return color[Math.round(Math.random() * (color.length - 1))]
        },
        submitUserComment() {
            if (!this.commentContent) {
                this.$message.warning('说点什么吧～')
            }
            else if (this.userBaseInfo.uid == this.$route.query.uid) {
                this.$message.warning('不能自己给自己留言哦～')
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
        OnVisibleDrawerProfile() {
            this.visibleDrawerProfile = true
            this.$axios.post('getUserDetail', qs.stringify({
                uid: this.userBaseInfo.uid
            }))
            .then((res) => {
                if (res.data == 1) {
                    this.$message.error('未知错误')
                }
                else {
                    this.form_profile.setFieldsValue({
                        nickname: res.data.nickname,
                        bio: res.data.bio,
                        phone: res.data.phone,
                        qq: res.data.qq,
                        wechat: res.data.wechat,
                        class: res.data.class
                    })
                }
            })
        },
        submitProfile(e) {
            e.preventDefault()
            this.form_profile.validateFieldsAndScroll((err, values) => {
                if (!err) {
                    this.$axios.post('updateUser', qs.stringify({
                        uid: this.userBaseInfo.uid,
                        nickname: values.nickname,
                        bio: values.bio,
                        gender: values.gender,
                        class: values.class[0] + '/' + values.class[1],
                        phone: values.phone,
                        qq: values.qq,
                        wechat: values.wechat,
                    }))
                    .then((res) => {
                        if (res.data == 0) {
                            this.$message.success('修改成功')
                            this.form_profile.resetFields()
                            this.visibleDrawerProfile = false
                            this.$router.go(0)
                        }
                        else if (res.data == 1) {
                            this.$message.error('未知错误')
                        }
                    })
                }
            })
        },
        changePassword(e) {
            e.preventDefault()
            this.form_password.validateFieldsAndScroll((err, values) => {
                if (!err) {
                    this.$axios.post('changePassword', qs.stringify({
                        uid: this.userBaseInfo.uid,
                        originPassword: md5(values.originPassword),
                        password: md5(values.password)
                    }))
                    .then((res) => {
                        if (res.data == 0) {
                            this.$message.success('修改成功')
                            this.form_password.resetFields()
                            this.visibleDrawerPassword = false
                        }
                        else if (res.data == 1) {
                            this.$message.error('密码错误')
                        }
                        else if (res.data == 2) {
                            this.$message.error('未知错误')
                        }
                    })
                }
            })
        },
        beforeAvatarUpload (avatar) {
            const isSupportFormat = avatar.type === 'image/jpeg' || avatar.type === 'image/png'
            if (!isSupportFormat) {
                this.$message.error('仅支持jpeg或png格式图片')
            }
            const isLt2M = avatar.size / 1024 / 1024 < 2;
            if (!isLt2M) {
                this.$message.error('图片大小必须小于2MB')
            }

            return isSupportFormat && isLt2M
        },
        handleChange_avatarUpload (info) {
            if (info.file.status === 'uploading') {
                this.loading_uploadAvatar = true
                return
            }
            if (info.file.status === 'done') {
                if (info.file.response == 0) {
                    this.$message.success('修改图像成功')
                    this.loading_uploadAvatar = false
                    this.visibleDrawerProfile = false
                    this.$router.go(0)
                }
                else {
                    this.$message.error('未知错误')
                    this.loading_uploadAvatar = false
                }
            }
        },
        applyAuth() {
            this.$notification['success']({
                message: '申请身份认证',
                description: '请联系 qq1161142536 / eliotwjz@gmail.com 申请身份认证！',
                duration: null
            })
        },
        confirm_removeErrorBook(id) {
            this.$axios.post('removeErrorBook', qs.stringify({
                id: id
            }))
            .then((response) => {
                if (response.data == 1) {
                    this.$message.error('未知错误')
                }
                else {
                    this.userProfile.errorBook.forEach((item, index) => {
                        if (item.id == id) {
                            this.userProfile.errorBook.splice(index, 1)
                            this.$message.success('删除成功')
                            return true
                        }
                    })
                }
            })
        },
        confirm_clearErrorBook() {
            if (this.userProfile.errorBook.length == 0) {
                this.$message.warning('错题本已经是空的了～')
            }
            else {
                this.$axios.get('clearErrorBook')
                .then((response) => {
                    if (response.data == 1) {
                        this.$message.error('未知错误')
                    }
                    else {
                        this.userProfile.errorBook = []
                        this.$message.success('清除成功')
                    }
                })
            }
        },
        follow(uid) {
            this.$axios.post('follow', qs.stringify({
                uid: uid
            }))
            .then((response) => {
                if (response.data == 1) {
                    this.$message.error('未知错误')
                }
                else {
                    this.$message.success('关注成功')
                    this.userProfile.isFollowing = true
                }
            })
        },
        unFollow(uid) {
            this.$axios.post('unFollow', qs.stringify({
                uid: uid
            }))
            .then((response) => {
                if (response.data == 1) {
                    this.$message.error('未知错误')
                }
                else {
                    this.$message.success('取消关注成功')
                    this.userProfile.isFollowing = false
                }
            })
        }
    },
    watch: {
        // the same path, but different query, force to refresh
        '$route' () {
            this.$axios.post('getUserProfile', qs.stringify({
                uid: this.$route.query.uid
            }))
            .then((response) => {
                if (response.data == 1) {
                    this.$message.error('未知错误')
                }
                else {
                    this.userProfile = response.data
                }
            })
            this.$axios.get('getUserBaseInfo')
            .then((response) => {
                if (response.data == 1) {
                    this.$message.error('未知错误')
                }
                else {
                    this.userBaseInfo = response.data
                }
            })
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

.abbr {
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
}
</style>
