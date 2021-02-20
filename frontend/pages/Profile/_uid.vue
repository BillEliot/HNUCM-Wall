<template>
    <div>
        <!-- drawer - profile -->
        <a-drawer
            title="编辑个人资料"
            placement="top"
            height=512
            @close="visibleDrawerProfile = false"
            :visible="visibleDrawerProfile"
        >
            <a-form :form="form_profile" layout="vertical">
                <a-form-item label="头像">
                    <a-upload
                        name="avatar"
                        listType="picture-card"
                        :showUploadList="false"
                        :action="baseUrl + '/api/uploadAvatar'"
                        :withCredentials="true"
                        :beforeUpload="beforeAvatarUpload"
                        @change="handleChange_avatarUpload"
                    >
                        <a-icon :type="loading_uploadAvatar ? 'loading' : 'plus'" />
                        <div>修改头像</div>
                    </a-upload>
                </a-form-item>
                <a-form-item label="昵称">
                    <a-input
                        v-decorator="['username', {
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
                <!--
                <a-form-item label="手机">
                    <a-input
                        v-decorator="['phone']"
                        placeholder="你的手机号"
                    />
                </a-form-item>
                -->
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
            placement="top"
            height=512
            @close="visibleDrawerPassword = false"
            :visible="visibleDrawerPassword"
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
                                    required: true, message: '请输入密码',
                                }, {
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
                                    required: true, message: '请重复输入密码',
                                }, {
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
        <!-- drawer - phone auth -->
        <!--
        <a-drawer
            title="手机认证"
            placement="top"
            height=468
            @close="visibleDrawerPhone = false"
            :visible="visibleDrawerPhone"
        >
            <a-form :form="form_phone" layout="vertical">
                <a-form-item label="手机号码">
                    <a-input
                        v-decorator="[
                            'phone',
                            {
                                rules: [{ 
                                    required: true, message: '请输入手机号码',
                                }, {
                                    validator: validator_phone
                                }]
                            }
                        ]"
                        type="number"
                    />
                </a-form-item>
            </a-form>
            <a-form-item label="验证码" extra="验证码会发往您的手机">
                <a-input
                    v-decorator="['captcha', {
                        rules: [{ required: true, message: '请输入验证码' }]
                    }]"
                />
                <a-button :disabled="isDisableSMSCaptcha" @click="getSMSCaptcha">{{ SMSCaptchaButtonText }}</a-button>
            </a-form-item>
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
                <a-button @click="phoneAuth" type="primary" html-type="submit">确定</a-button>
            </div>
        </a-drawer>
        -->
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
                    <div v-for="user in userProfile.followings" :key="user.id">
                        <a-avatar v-if="user.id == -1" :size="64" :src="baseUrl + user.avatar" />
                        <a-avatar v-else :size="64" :src="baseUrl + user.avatar" @click="$router.push({ path: '/profile', query: { id: user.id } })" style="cursor: pointer" />
                        <a v-if="user.id == -1">{{ user.username }}</a>
                        <a v-else @click="$router.push({ path: '/profile', query: { id: user.id } })">{{ user.username }}</a>
                        <p class="bio">{{ user.bio }}</p>
                        <a-tag v-for="tag in user.auth" :color="randomColor()" :key="tag">{{ tag }}</a-tag>
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
                            <h1>个人信息</h1>
                            <p class="subheading">又来偷偷看TA～♪(^∇^*)</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div style="margin-top: 30px">
            <a-button v-if="userBaseInfo.id != -1 && userBaseInfo.id != $route.query.id && !userProfile.isFollowing" @click="follow($route.query.id)" type="primary" class="follow">
                <a-icon type="heart" />关注
            </a-button>
            <a-button v-if="userBaseInfo.id != -1 && userBaseInfo.id != $route.query.id && userProfile.isFollowing" @click="unFollow($route.query.id)" type="dashed" class="follow">
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
                <div class="text-center col-md-12">
                    <a-avatar :size="64" :src="baseUrl + userProfile.avatar" />
                    <h2>{{ userProfile.username }}</h2>
                    <a-tag v-for="tag in userProfile.auth" :color="randomColor()" :key="tag">{{ tag }}</a-tag>
                    <p class="bio">{{ userProfile.bio }}</p>

                    <a-descriptions title="用户信息" bordered>
                        <a-descriptions-item label="EMail">
                            <a-icon type="mail" /> {{ userProfile.email }}
                        </a-descriptions-item>
                        <a-descriptions-item label="手机">
                            <a-icon type="phone" /> {{ userProfile.phone }}
                        </a-descriptions-item>
                        <a-descriptions-item label="qq">
                            <a-icon type="qq" /> {{ userProfile.qq }}
                        </a-descriptions-item>
                        <a-descriptions-item label="微信">
                            <a-icon type="wechat" /> {{ userProfile.wechat }}
                        </a-descriptions-item>
                        <a-descriptions-item label="性别">
                            <a-icon :type="userProfile.gender == '男' ? 'man' : 'woman'" /> {{ userProfile.gender }}
                        </a-descriptions-item>
                        <a-descriptions-item label="班级">
                            <a-icon type="build" /> {{ userProfile.class }}
                        </a-descriptions-item>
                        <a-descriptions-item label="硬币">
                            <a-icon type="gold" /> {{ userProfile.coin }}
                        </a-descriptions-item>
                    </a-descriptions>
                </div>
                <div v-if="userBaseInfo.id != -1 && userBaseInfo.id == $route.query.id" class="text-center col-md-12" style="margin-top: 20px">
                    <!-- actions -->
                    <a-button @click="OnVisibleDrawerProfile()">编辑个人信息</a-button>
                    <a-button @click="visibleDrawerPassword = true">修改密码</a-button>
                    <!--<a-button @click="visibleDrawerPhone = true">手机认证</a-button>-->
                    <a-button @click="applyAuth()">申请身份认证</a-button>
                </div>
            </div>
            <div style="margin-top: 30px"></div>
            <div class="row">
                <div class="col-md-12">
                    <a-tabs defaultActiveKey="love">
                        <!-- love -->
                        <a-tab-pane key="love">
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
                                        <div v-if="item.userTo_id != -1" slot="avatar" class="text-center">
                                            <a-avatar :src="baseUrl + item.userTo_avatar" @click="$router.push({ path: '/profile', query: { id: item.userTo_id } })" />
                                            <br />
                                            <nuxt-link :to="{ path: '/profile', query: { id: item.userTo_id } }">{{ item.userTo_username.split('/')[0] }}</nuxt-link>
                                        </div>
                                        <a-avatar v-else slot="avatar">
                                            <a-icon slot="icon" type="team" />
                                        </a-avatar>
                                        
                                        <a slot="author" style="font-size: 15px" @click="$router.push({ path: '/love/detail', query: { id: item.id } })">To {{ item.userTo_username }}</a>
                                        <p slot="content" class="text-left abbr">{{ item.content }}</p>
                                        <span>{{ item.date }}</span>
                                    </a-comment>
                                </a-list-item>
                            </a-list>
                        </a-tab-pane>
                        <!-- lose -->
                        <a-tab-pane key="lose">
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
                        <a-tab-pane key="deal">
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
                        <a-tab-pane key="help">
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
                        <a-tab-pane key="article">
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
                    </a-tabs>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import qs from "qs"
import { mapState } from 'vuex'

export default {
    layout: 'common',
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
            visibleDrawerProfile: false,
            visibleDrawerPassword: false,
            visibleDrawerPhone: false,
            visibleDrawerFollowing: false,
            form_profile: this.$form.createForm(this),
            form_password: this.$form.createForm(this),
            form_phone: this.$form.createForm(this),
            confirmDirty: false,
            loading_uploadAvatar: false,
            isDisableSMSCaptcha: false,
            SMSCaptchaButtonText: '获取'
        }
    },
    async asyncData({ $axios, query }) {
        let userProfile = null

        await $axios.get('getUserProfile', {
            params: {
                id: query.id
            }
        })
        .then((response) => {
            if (response.data.code == 200 && response.data.status == 'success') {
                userProfile = response.data.data
            }
        })

        return {
            userProfile: userProfile
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
        validator_phone (rule, value, callback) {
            var regex_phone = /^1[345789]\d{9}$/
            if (value && !regex_phone.test(value)) {
                callback('请输入合法的手机号')
            }
            callback()
        },
        getSMSCaptcha() {
            var phone = this.form_phone.getFieldValue('phone')
            if (phone) {
                this.$axios.post('getSMSCaptcha', qs.stringify({
                    phone: phone
                }))
                .then((response) => {
                    if (response.data.code == 302) {
                        this.$router.push({ path: '/login' })
                    }
                    else if (response.data.code == 200) {
                        if (response.data.status == 'success') {
                            this.$message.success('验证码已发往您的手机，有效期为3分钟，请查收')
                        }
                        else {
                            this.$message.error('发送失败, 请稍后重试或联系管理员')
                        }
                    }
                })

                this.isDisableSMSCaptcha = true
                let time = 60
                var countDown = setInterval(() => {
                    time --
                    if (time == 0) {
                        this.isDisableSMSCaptcha = false
                        this.SMSCaptchaButtonText = '获取'
                        clearInterval(countDown)
                    }
                    else {
                        this.SMSCaptchaButtonText = time.toString() + '后重新获取'
                    }
                }, 1000)
            }
            else {
                this.$message.error('请输入您的手机号码')
            }
        },
        randomColor() {
            let color = ['pink', 'red', 'orange', 'green', 'cyan', 'blue', 'purple']
            return color[Math.round(Math.random() * (color.length - 1))]
        },
        OnVisibleDrawerProfile() {
            this.visibleDrawerProfile = true
            this.$axios.get('getUserDetail')
            .then((res) => {
                if (res.data == 1) {
                    this.$message.error('未知错误')
                }
                else {
                    this.form_profile.setFieldsValue({
                        username: res.data.username,
                        bio: res.data.bio,
                        //phone: res.data.phone,
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
                        id: userBaseInfo.id,
                        username: values.username,
                        bio: values.bio,
                        gender: values.gender,
                        class: values.class[0] + '/' + values.class[1],
                        qq: values.qq,
                        wechat: values.wechat,
                    }))
                    .then((response) => {
                        if (response.data.code == 200 && response.data.status == 'success') {
                            this.$message.success('修改成功')
                            this.form_profile.resetFields()
                            this.visibleDrawerProfile = false
                            this.$router.go(0)
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
                        originPassword: values.originPassword,
                        password: values.password
                    }))
                    .then((response) => {
                        if (response.data.code == 200 && response.data.status == 'success')
                            this.$message.success('修改成功')
                            this.form_password.resetFields()
                            this.visibleDrawerPassword = false
                        })
                }
            })
        },
        /*
        phoneAuth() {
        },
        */
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
                this.loading_uploadAvatar = false
                if (info.file.response.code == 200 && info.file.response.status == 'success') {
                    this.$message.success('修改头像成功')
                    this.visibleDrawerProfile = false
                    this.$router.go(0)
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

        follow(id) {
            this.$axios.get('follow', {
                params: {
                    id: id
                }
            })
            .then((response) => {
                if (response.data.code == 200 && response.data.status == 'success') {
                    this.$message.success('关注成功')
                    this.userProfile.isFollowing = true
                }
            })
        },
        unFollow(id) {
            this.$axios.get('unFollow', {
                params: {
                    id: id
                }
            })
            .then((response) => {
                if (response.data.code == 200 && response.data.status == 'success') {
                    this.$message.success('取消关注')
                    this.userProfile.isFollowing = false
                }
            })
        }
    },
    watch: {
        // the same path, but different query, force to refresh
        '$route' () {
            this.$axios.get('getUserProfile', {
                params: {
                    id: this.$route.query.id
                }
            })
            .then((response) => {
                if (response.data.code == 200 && response.data.status == 'success') {
                    this.userProfile = response.data.data
                }
            })
        }
    },
    computed: mapState({
        baseUrl: state => state.baseUrl,
        classes: state => state.classes,
        userBaseInfo: state => state.userBaseInfo
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
