<template>
  <div class="container">
    <a-row type="flex" justify="center" align="middle">
      <a-col :lg="8" :md="12" :sm="18" :xs="20">
        <a-spin :spinning="spinning">
          <div class="fh5co-form">
            <a-tabs defaultActiveKey="1" :tabBarStyle="{ 'text-align': 'center' }">
              <a-tab-pane tab="账号密码登录" key="1">
                <a-form :form="form_login" @submit="login">
                  <a-form-item label="邮箱" :label-col="{ span: 5 }" :wrapper-col="{ span: 18 }">
                    <a-input v-decorator="[
                        'email',
                        { rules: [{ required: true, message: '请输入邮箱'}] }
                      ]"
                      placeholder="请输入邮箱">
                      <a-icon slot="prefix" type="user" style="color:rgba(0,0,0,.25)" />
                    </a-input>
                  </a-form-item>
                  <a-form-item label="密码" :label-col="{ span: 5 }" :wrapper-col="{ span: 18 }">
                    <a-input v-decorator="[
                        'password',
                        { rules: [{ required: true, message: '请输入密码'}] }
                      ]"
                      type="password" 
                      placeholder="请输入密码">
                      <a-icon slot="prefix" type="lock" style="color:rgba(0,0,0,.25)" />
                    </a-input>
                  </a-form-item>
                  <a-form-item :wrapper-col="{ xs: { span: 24, offset: 0 }, sm: { span: 16, offset: 5 } }">
                    <a-checkbox v-decorator="[
                        'isRemember',
                        { valuePropName: 'checked' }
                      ]"
                    >
                      记住我
                    </a-checkbox>
                  </a-form-item>
                  <a-form-item>
                    <router-link to="/register">
                      没有账号？注册一个
                    </router-link>
                    <a-divider type="vertical" />
                    <router-link to="/login/findpassword">
                      忘记密码
                    </router-link>
                    <a-row type="flex" justify="center" align="middle" :gutter="16">
                      <a-col :span="12">
                        <a-button @click="$router.push({ path: '/' })" style="width: 100%">返回主页</a-button>
                      </a-col>                        
                      <a-col :span="12">
                        <a-button type="primary" html-type="submit" style="width: 100%">登录</a-button>
                      </a-col>
                    </a-row>
                  </a-form-item>
                </a-form>
                <span style="font-weight: bold; color: red">注意：由于服务端升级，之前已注册用户的密码统一为123456，请尽快修改。(此消息将于2021/08/18消失)</span>
              </a-tab-pane>
              <a-tab-pane tab="手机登录" key="2" forceRender>
                <a-form :form="form_SMS" @submit="sendSMS">
                  <a-form-item label="手机号" extra="因短信服务价格高昂，敬请期待！" :label-col="{ span: 5 }" :wrapper-col="{ span: 18 }">
                    <a-input v-decorator="[
                          'phone',
                          { rules: [{ required: true, message: '请输入手机号'}] }
                        ]" 
                        type="number"
                        placeholder="请输入手机号">
                        <a-icon slot="prefix" type="phone" style="color:rgba(0,0,0,.25)" />
                    </a-input>
                  </a-form-item>
                  <a-form-item>
                    <a-button type="primary" html-type="submit" style="width: 100%">发送</a-button>
                  </a-form-item>
                </a-form>
              </a-tab-pane>
            </a-tabs>
          </div>
        </a-spin>
      </a-col>
    </a-row>
  </div>
</template>

<script>
import qs from "qs"
import { mapMutations } from 'vuex'

export default {
  layout: 'common',
  data() {
    return {
      form_login: this.$form.createForm(this),
      form_SMS: this.$form.createForm(this),
      spinning: false
    }
  },
  async asyncData({ store, redirect }) {
    if (store.state.userBaseInfo.id != -1) {
      redirect('/')
    }
  },
  methods: {
    ...mapMutations({
      setUserBaseInfo: 'setUserBaseInfo'
    }),

    login(e) {
      this.spinning = true
      e.preventDefault()
      this.form_login.validateFields((err, values) => {
        if (!err) {
          this.$axios.post('login', qs.stringify({
            email: values.email,
            password: values.password,
            isRemember: values.isRemember
          }))
          .then((response) => {
            this.spinning = false
            if (response.data.code == 200 && response.data.status == 'success') {
              this.$axios.get('getUserBaseInfo')
              .then((response) => {
                this.setUserBaseInfo(response.data.data)
                this.$router.push({ path: '/' })
              })
            }
          })
        }
      })
    },
    sendSMS() {
    }
  }
}
</script>

<style scoped>
a {
  text-decoration: none;
}
</style>
