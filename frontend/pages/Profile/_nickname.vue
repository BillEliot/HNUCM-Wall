<template>
    <div>
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
                            <span slot="tab">
                                <a-icon type="highlight" />留言板
                            </span>
                            <a-comment>
                                <a-avatar
                                    slot="avatar"
                                    src="https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png"
                                    alt="Han Solo"
                                />
                                <div slot="content">
                                    <a-form-item>
                                    <a-textarea :rows="4" @change="handleChange" :value="value" ></a-textarea>
                                    </a-form-item>
                                    <a-form-item>
                                    <a-button
                                        htmlType="submit"
                                        :loading="submitting"
                                        @click="handleSubmit"
                                        type="primary"
                                    >
                                        Add Comment
                                    </a-button>
                                    </a-form-item>
                                </div>
                            </a-comment>
                        </a-tab-pane>
                        <a-tab-pane key="2">
                            <span slot="tab">
                                <a-icon type="heart" />TA的表白
                            </span>
                        </a-tab-pane>
                    </a-tabs>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import qs from "qs";
import { mapState } from 'vuex'

export default {
    data() {
        return {
            userProfile: null
        }
    },
    async asyncData({ $axios, query, redirect }) {
        if (!query.nickname) {
            redirect({ path: '/' })
        }

        let userProfile = null
        await $axios.post('getUserProfile', qs.stringify({
            nickname: query.nickname
        }))
        .then((response) => {
            if (response.data == 1) {
                redirect({ path: '/' })
            }
            else {
                userProfile = response.data
            }
        })

        return {
            userProfile: userProfile
        }
    },
    methods: {
        searchClass() {

        }
    },
    computed: mapState({
        baseUrl: state => state.baseUrl,
        classes: state => state.classes
    })
}
</script>

<style>
.follow {
    float: right;
    margin-right: 20px
}

.back {
    float: left;
    margin-left: 20px
}
</style>
